import sys
import os
from confluent_kafka import Producer

def produce(message, topic):
    conf = {
        'bootstrap.servers': os.environ['CLOUDKARAFKA_BROKERS'],
        'security.protocol': 'SASL_SSL',
	    'sasl.mechanisms': 'SCRAM-SHA-256',
        'sasl.username': os.environ['CLOUDKARAFKA_USERNAME'],
        'sasl.password': os.environ['CLOUDKARAFKA_PASSWORD']
    }

    p = Producer(**conf)
    p.produce(topic, str(message))
    p.poll(0)
    p.flush()

   