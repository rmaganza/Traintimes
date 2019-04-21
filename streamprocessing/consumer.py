from dbconf import collection
from kafkaconf import Consumer

from logs.logger import logConsumer, logger


@logConsumer(logger)
def consumer():
    for item in Consumer:
        message = item.value
        collection.update_one({'departureDay': message.get('departureDay'),
                               'trainNumber': message.get('trainNumber'),
                               'lastCheckedTime': message.get('lastCheckedTime')},
                              message,
                              upsert=True)


if __name__ == "__main__":
    producer()
