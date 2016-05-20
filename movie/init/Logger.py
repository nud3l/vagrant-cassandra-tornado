import logging
import logging.handlers
from datetime import datetime


class Logger:
    def __init__(self, loglocation):
        # File handler
        fileHandler = logging.FileHandler(filename=loglocation + "banking.log")
        fileFormatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        fileHandler.formatter = fileFormatter

        # Syslog handler
        syslogHandler = logging.handlers.SysLogHandler(address='/dev/log')
        syslogFormatter = logging.Formatter(
            'Python: { "loggerName":"%(name)s", "asciTime":"%(asctime)s", "pathName":"%(pathname)s", "logRecordCreationTime":"%(created)f", "functionName":"%(funcName)s", "levelNo":"%(levelno)s", "lineNo":"%(lineno)d", "time":"%(msecs)d", "levelName":"%(levelname)s", "message":"%(message)s"}')
        syslogHandler.formatter = syslogFormatter

        # logging.basicConfig(filename=loglocation, level=logging.DEBUG, )
        requestsLog = logging.getLogger("requests").setLevel(logging.DEBUG)  # suppress info-messages of Python Requests
        socketLog = logging.getLogger("websocket").setLevel(
            logging.CRITICAL)  # suppress info-messages of Python websocket

        #pikaLog = logging.getLogger("pika")
        #pikaLog.setLevel(logging.CRITICAL)
        #pikaLog.addHandler(fileHandler)
        #pikaLog.addHandler(syslogHandler)

        accessLog = logging.getLogger("tornado.access")
        accessHandler = logging.FileHandler(filename=loglocation + "access.log")
        accessFormatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        accessHandler.formatter = accessFormatter
        accessLog.addHandler(accessHandler)

        appLog = logging.getLogger("tornado.application")
        appLog.addHandler(fileHandler)
        appLog.addHandler(syslogHandler)

        genLog = logging.getLogger("tornado.general")
        genLog.addHandler(fileHandler)
        genLog.addHandler(syslogHandler)

        self.logger = logging.getLogger('bank')
        self.logger.setLevel(logging.DEBUG)

        self.logger.addHandler(fileHandler)
        self.logger.addHandler(syslogHandler)

    # Interesting events
    def info(self, messagetext):
        self.logger.info(messagetext)

    # Normal but significant events
    def warning(self, messagetext):
        self.logger.warning(messagetext)

    # Exceptional occurrences that are not errors.
    # Example: Use of deprecated APIs, poor use of an API, undesirable things
    # that are not necessarily wrong.
    def error(self, messagetext):
        self.logger.error(messagetext)

    # Runtime errors that do not require immediate action but should typically
    # be logged and monitored.
    def critical(self, messagetext):
        self.logger.critical(messagetext)

    # Exceptions
    def exception(self, messagetext):
        self.logger.exception(messagetext)
