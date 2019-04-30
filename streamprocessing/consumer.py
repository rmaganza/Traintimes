from streamprocessing.conf.dbconf import collection
from streamprocessing.conf.kafkaconf import Consumer

from logs.loggers import logger


def consumer():
    for item in Consumer:
        logger.info("Saving to DB...")
        message = item.value
        collection.update_one({'departureDay': message.get('departureDay'),
                               'trainNumber': message.get('trainNumber')},
                              {'$set': message},
                              upsert=True)
        logger.info("Saved to DB.")


if __name__ == "__main__":
    consumer()
