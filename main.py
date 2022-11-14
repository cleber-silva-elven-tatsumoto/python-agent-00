from bin.consumer import *
from bin.helper import *
import threading
from fastapi import FastAPI

os.environ['CLOUDKARAFKA_USERNAME'] = 'qqihoccr'
os.environ['CLOUDKARAFKA_PASSWORD'] = 'uzAikC-dREN7d-KCGQ4iqEQNpQ3cuYLB'
os.environ['CLOUDKARAFKA_BROKERS']='dory-01.srvs.cloudkafka.com:9094,dory-02.srvs.cloudkafka.com:9094,dory-03.srvs.cloudkafka.com:9094'
os.environ['AGENT'] = '0001'

app = FastAPI()
set_free()

c = threading.Thread(target=consume)
c.start()

@app.get("/")
def read_root():
    return {"Hello": "World"}
