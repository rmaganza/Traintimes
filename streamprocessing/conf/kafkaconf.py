import json

from kafka import KafkaProducer, KafkaConsumer

KAFKA_PORT = '6667'
BASE_SERVER = 'sandbox-hdp.hortonworks.com:'
GROUP_NAME = 'traingroup'
Producer = KafkaProducer(bootstrap_servers=BASE_SERVER + KAFKA_PORT)

TOPIC_NAME = 'trains'

Consumer = KafkaConsumer(TOPIC_NAME,
                         bootstrap_servers=BASE_SERVER + KAFKA_PORT,
                         auto_offset_reset='earliest',
                         consumer_timeout_ms=10 * 60 * 1000,
                         enable_auto_commit=True,
                         auto_commit_interval_ms=45000,
                         value_deserializer=lambda x: json.loads(x.decode('utf-8')),
                         group_id=GROUP_NAME
                         )
