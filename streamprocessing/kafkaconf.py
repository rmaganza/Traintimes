from kafka import KafkaProducer

KAFKA_PORT = '6667'
Producer = KafkaProducer(bootstap_servers='sandbox-hdp.hortonworks.com:' + KAFKA_PORT,)

TOPIC_NAME = 'trains'
