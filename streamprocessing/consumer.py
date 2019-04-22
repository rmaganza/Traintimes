from streamprocessing.conf.dbconf import collection
from streamprocessing.conf.kafkaconf import Consumer

from logs.loggers import logConsumer, logger


@logConsumer(logger)
def consumer():
    for item in Consumer:
        message = item.value
        collection.update_one({'departureDay': message.get('departureDay'),
                               'trainNumber': message.get('trainNumber')},
                              message,
                              upsert=True)


if __name__ == "__main__":
    consumer()
