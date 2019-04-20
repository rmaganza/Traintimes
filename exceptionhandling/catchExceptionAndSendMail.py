import sys
from logs.logger import logger

def cath_exception_and_send_mail(e):
    logger.critical("*CRITICAL ERROR* Program stopped working for exception " + repr(e), exc_info=True)
    sys.exit()

