import os
from kafka import KafkaConsumer
from bin.from_app import *
from bin.helper import *

def consume():

    # Consumer configuration
    # See https://github.com/edenhill/librdkafka/blob/master/CONFIGURATION.md
    conf = {
        'bootstrap.servers': os.environ['CLOUDKARAFKA_BROKERS'],
        'group.id': "%s-consumer" % os.environ['CLOUDKARAFKA_USERNAME'],
        'session.timeout.ms': 6000,
        'default.topic.config': {'auto.offset.reset': 'earliest'},
        'security.protocol': 'SASL_SSL',
	    'sasl.mechanisms': 'SCRAM-SHA-256',
        'sasl.username': os.environ['CLOUDKARAFKA_USERNAME'],
        'sasl.password': os.environ['CLOUDKARAFKA_PASSWORD']
    }

    # To consume latest messages and auto-commit offsets
    consumer = KafkaConsumer('qqihoccr-default', 
                            group_id="%s-consumer" % os.environ['CLOUDKARAFKA_USERNAME'],
                            bootstrap_servers=os.environ['CLOUDKARAFKA_BROKERS'],
                            sasl_plain_password=os.environ['CLOUDKARAFKA_PASSWORD'],
                            sasl_plain_username = os.environ['CLOUDKARAFKA_USERNAME'],
                            security_protocol = 'SASL_SSL',
                            sasl_mechanism = 'SCRAM-SHA-256',
                            #max_poll_records = 1,
                            #session_timeout_ms = 6000,
    )
    

    config_data = get_config()
    for message in consumer:
        chave = message.value.decode("utf-8")
        if is_busy():
            produce(chave,'qqihoccr-default')
        else:
            set_busy()
            pgp_api = "https://pgp-five.vercel.app/api/pgp"
            get_details([chave], pgp_api)
            set_free()
