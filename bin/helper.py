from os.path import exists
import os, csv
import pandas as pd
import json, os, platform


_BAR = '/' if platform.system() == 'Darwin' else '\\'
_ROOT = os.path.dirname(__file__).replace(f'{_BAR}bin','')
_RESULTS_FOLDER = f'{_ROOT}{_BAR}resultados{_BAR}'

_DRIVER_FOLDERa = f'{_ROOT}{_BAR}bin{_BAR}drivers{_BAR}a{_BAR}chromedriver'
_DRIVERa = _DRIVER_FOLDERa + ('' if platform.system() == 'Darwin' else '.exe')

_DRIVER_FOLDERb = f'{_ROOT}{_BAR}bin{_BAR}drivers{_BAR}b{_BAR}chromedriver'
_DRIVERb = _DRIVER_FOLDERb + ('' if platform.system() == 'Darwin' else '.exe')

_TMP = 'arquivo_tmp.tmp'
_LAST = f'{_RESULTS_FOLDER}last.dat'
_LASTe = f'{_RESULTS_FOLDER}last_e.dat'
_LOG = f'{_RESULTS_FOLDER}error.dat'
_LOGs = f'{_RESULTS_FOLDER}log.dat'
_RELOGIN = f'{_RESULTS_FOLDER}relog'

if(exists(_RESULTS_FOLDER) == False):
    os.mkdir(_RESULTS_FOLDER) 

def get_files():
    files = os.listdir(_RESULTS_FOLDER)
    csv = [f'{_RESULTS_FOLDER}{f}' for f in files if '.csv' in f and not 'completo' in f ]
    return csv

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

def get_participacao(xml):
    if 'Participacao na ger' in xml:
        return 'Sim'
    return 'Não'

def save_temp(data):
    save_data(_TMP, data)

def get_temp_path():
    return f'{_RESULTS_FOLDER}{_TMP}'

def save_data(path, data):
    path_to_file  = f'{_RESULTS_FOLDER}{path}'
    dt = pd.DataFrame([data])
    if(exists(path_to_file)):
        dt.to_csv(path_to_file, mode='a', index=False, header=False, encoding='utf-8')
    else:
        dt.to_csv(path_to_file, mode='a', index=False, header=True, encoding='utf-8')

def is_busy():
    print('Checando busy')
    path='busy'
    path_to_file  = f'{_RESULTS_FOLDER}{path}'
    if(exists(path_to_file)):
        return True
    return False

def set_busy():
    print('Escrevendo busy')
    path='busy'
    path_to_file  = f'{_RESULTS_FOLDER}{path}'
    save_data(path, [])

def set_free():
    path='busy'
    print('Removendo busy')
    path_to_file  = f'{_RESULTS_FOLDER}{path}'
    if(exists(path_to_file)):
        os.remove(path_to_file)

def get_config():
    if exists("config.json") == False:
        return 
    f = open('config.json')
    return json.load(f)

def get_driver_path_a():
    return _DRIVERa

def get_driver_path_b():
    return _DRIVERb

def error_log(instalacao):
    dt = pd.DataFrame([{
        'instalacao' : str(instalacao)
    }])
    dt.to_csv(_LOG, mode='a', index=False, header=False, line_terminator='\n',encoding='utf-8')

def log(content):
    dt = pd.DataFrame([{
        'erro' : str(content)
    }])
    dt.to_csv(_LOGs, mode='a', index=False, header=False, line_terminator='\n',encoding='utf-8')


def save_last_e(instalacao):
    dt = pd.DataFrame([{
        'instalacao' : str(instalacao)
    }])
    dt.to_csv(_LASTe, mode='w', index=False, line_terminator='\n',encoding='utf-8')

def remove_last_e():
    try:
        os.remove(_LOG)
    except:
        pass
    try:
        os.remove(_LASTe)
    except:
        pass

def get_error():
    try:
        with open(_LOG) as f:
            lines = [int(l) for l in f.readlines()]
        return lines
    except:
        return None

def get_last_e():
    try:
        with open(_LASTe) as f:
            input_file = csv.DictReader(f)
            instalacao = [f"{c.get('instalacao')}" for c in input_file]
            return instalacao[0]
    except:
        return None

def save_last(instalacao):
    dt = pd.DataFrame([{
        'instalacao' : str(instalacao)
    }])
    dt.to_csv(_LAST, mode='w', index=False, line_terminator='\n',encoding='utf-8')

def remove_last():
    try:
        os.remove(_LAST)
    except:
        pass

def get_last():
    try:
        with open(_LAST) as f:
            input_file = csv.DictReader(f)
            instalacao = [f"{c.get('instalacao')}" for c in input_file]
            return instalacao[0]
    except:
        return None

def call_relogin():
    dt = pd.DataFrame([{
    }])
    dt.to_csv(_RELOGIN, mode='w', index=False, line_terminator='\n',encoding='utf-8')

def need_reloging():
    if exists(_RELOGIN):
        os.remove(_RELOGIN)
        return True
    return False

