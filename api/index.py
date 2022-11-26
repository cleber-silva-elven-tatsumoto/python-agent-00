from fastapi import FastAPI
import requests, json, os

SELF_IP = None

def self_ip():
    global SELF_IP
    if SELF_IP:
        return SELF_IP
    print('Buscando IP')
    r = requests.get('https://api.ipify.org?format=json')
    SELF_IP = json.loads(r.text)['ip']
    return SELF_IP

def media_consumo(historico):
    try:
        consumo = [g.get('Dados') 
            for g in historico.get('Graficos') 
                if g.get('TipoGrafico') == 'HistoricoConsumo'][0]
        if len(consumo) > 0:
            total = 0
            for dado in consumo:
                total = total + float(dado.get('MediaConsumo'))
            return (total / len(consumo))
        return 0.0
    except:
        return 0.0

def get_details(arr_chaves, pgp_api):
    chaves =  {
        "chaves": [arr_chaves]
    }
    r = requests.post(pgp_api, json=chaves)
    secrets = json.loads(r.text)

    chave = secrets[0]
    
    chave['tokens'] = get_media_token(secrets[0])
    return get_media_participacao(chave)


def get_media_token(chave):
    try:
        url_token = 'https://servicosonline.cpfl.com.br/agencia-webapi/api/token'
        headers = {
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 10_3 like Mac OS X) AppleWebKit/603.1.30 (KHTML, like Gecko) Version/10.0 Mobile/14E269 Safari/602.1'
        }
        cookies = {"rxvts" : chave['chave'] }
        dados = {
            'client_id' : 'agencia-virtual-cpfl-app',
            'grant_type': 'instalacao_app',
            'identificacao_encriptada' : chave['crypted']
        }
        instalacao_chave = chave.get('chave').split('|')[0]
        r = requests.post(url_token, data=dados, cookies=cookies, headers=headers)
      
        if 'You are being rate limited' in r.text:
            print('BLOQUEADO PELO SITE')
            return data_save({
                'chave': chave.get('chave'),
                'media': 'BLOCK', 
                'participacao': 'BLOCK'
            })
            return None
        else:
            tokens = json.loads(r.text)
            return tokens
    except Exception as e:
        print(e)
        return None

def get_participacao(xml):
    if 'Participacao na ger' in xml:
        return 'Sim'
    return 'Não'

def data_save(data):
    data['agent']=os.getenv('AGENT_NAME') 
    data['ip'] = self_ip()
    return data
    # produce(data, 'qqihoccr-info')
    # print(' --- ESCRITO ---')

def get_media_participacao(chave):
    try:
        tokens = chave["tokens"]
        token = tokens['access_token']
        cookies = {"rxvt" : chave['chave'] }
        instalacao = json.loads(tokens['Instalacao'])
        dados = {
            "Instalacao": instalacao['Instalacao'],
            "CodigoClasse": instalacao['CodClasse'],
            "CodEmpresaSAP": instalacao['CodEmpresaSAP'],
            "NumeroContrato": instalacao['Contrato'],
            "TipoGrafico":"Todos",
            "ParceiroNegocio": instalacao['ParceiroNegocio'],
        }

        print(dados)

        headers = {
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 10_3 like Mac OS X) AppleWebKit/603.1.30 (KHTML, like Gecko) Version/10.0 Mobile/14E269 Safari/602.1',
            'Authorization': f'Bearer {token}',
        }

        url = 'https://servicosonline.cpfl.com.br/agencia-webapi/api/historico-consumo/busca-graficos'
        r = requests.post(url, data=dados, cookies=cookies, headers=headers)
        historico = json.loads(r.text)
        if 'You are being rate limited' in r.text:
            print('BLOQUEADO PELO SITE')
            return data_save({
                'chave': chave.get('chave'),
                'media': 'BLOCK', 
                'participacao': 'BLOCK'
            })
            return
        media = media_consumo(historico)
        print(historico)
        print(media)

        dados = {
            "RetornarDetalhes" : "true", 
            "CodigoFase": instalacao['CodigoFase'],
            "IndGrupoA": instalacao['IndGrupoA'],
            "Situacao": instalacao['Situacao'],
            "ContaContrato": instalacao['ContaContrato'],
            "GerarProtocolo": "true",
            "Instalacao": instalacao['Instalacao'],
            "CodigoClasse": instalacao['CodClasse'],
            "CodEmpresaSAP": instalacao['CodEmpresaSAP'],
            "NumeroContrato": instalacao['Contrato'],
            "ParceiroNegocio": instalacao['ParceiroNegocio'],
        }

        url = 'https://servicosonline.cpfl.com.br/agencia-webapi/api/historico-contas/contas-quitadas'
        r = requests.post(url, data=dados, cookies=cookies, headers=headers)
        if 'You are being rate limited' in r.text:
            print('BLOQUEADO PELO SITE')
            return data_save({
                'chave': chave.get('chave'),
                'media': 'BLOCK', 
                'participacao': 'BLOCK'
            })
            return
            
        quitadas = json.loads(r.text)

        url = 'https://servicosonline.cpfl.com.br/agencia-webapi/api/historico-contas/download-xml-nf3e'
        r = requests.post(url, data={"NumeroDocumento": quitadas['ContasPagas'][0]['NumeroContaEnergia']}, cookies=cookies, headers=headers)
        if 'You are being rate limited' in r.text:
            print('BLOQUEADO PELO SITE')
            return data_save({
                'chave': chave.get('chave'),
                'media': 'BLOCK', 
                'participacao': 'BLOCK'
            })
            return
        participacao = get_participacao(r.text)
        return data_save({
            'chave': chave.get('chave'),
            'media': "%.2f" %  media, 
            'participacao': participacao
        })
        return
    except Exception as e:
        print(e)
        return data_save({
            'chave': chave.get('chave'),
            'media': 'None', 
            'participacao': 'None'
        })
        return



app = FastAPI()
pgp_api = "https://pgp-five.vercel.app/api/pgp"


@app.get("/api/{chave}/{document}")
def read_root(chave: str, document: str):
    data = get_details(f'{chave}|{document}', pgp_api)
    return data


@app.get("/api/health")
def health():
    return {'agent': os.getenv('AGENT_NAME'), 'ip':self_ip()}