from streamprocessing.conf.dbconf import collection
from streamprocessing.conf.kafkaconf import Consumer
from exceptionhandling.retry import retry
from kafka.errors import CommitFailedError

from logs.loggers import logger


@retry(CommitFailedError, tries=10, delay=0, backoff=0, logger=logger)
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
re