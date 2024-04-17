# -*- coding: utf-8 -*- 

import logging
from logging.handlers import RotatingFileHandler

class Logger(object):
    def __init__(self, logsrep:str, service:str, level:str) -> None:
        self.__init_logs(logsrep, service, level)
        self.logger = logging.getLogger(service)

    def __init_logs(self, logsrep:str, programme:str, level:str) -> logging.Logger:
        # logs.py by @louxfaure, check file for more comments
        # D'aprés http://sametmax.com/ecrire-des-logs-en-python/
        logsfile = logsrep + "/" + programme + ".log"
        logger = logging.getLogger(programme)
        # Make sure the log level is correct
        level = level.strip().upper()
        if level not in ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]:
            level = "INFO"
        logger.setLevel(getattr(logging, level))
        # Formatter
        formatter = logging.Formatter(u'%(asctime)s :: %(levelname)s :: %(message)s')
        file_handler = RotatingFileHandler(logsfile, 'a', 100000000, 1, encoding="utf-8")
        file_handler.setLevel(getattr(logging, level))
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        # For console
        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(getattr(logging, level))
        stream_handler.setFormatter(formatter)
        logger.addHandler(stream_handler)

        logger.info('Logger initialised')

        return logger

    def critical(self, msg:str):
        """Basic log critical function"""
        self.logger.critical(f"{msg}")

    def debug(self, msg:str):
        """Log a debug statement logging first the service then the message"""
        self.logger.debug(f"{msg}")

    def info(self, msg:str):
        """Basic log info function"""
        self.logger.info(f"{msg}")

    def simple_debug(self, msg:str, data):
        """Log an info statement separating msg and data by :"""
        self.logger.debug(f"{msg} : {data}")

    def simple_info(self, msg:str, data):
        """Log an info statement separating msg and data by :"""
        self.logger.info(f"{msg} : {data}")

    def simple_warning(self, msg:str, data):
        """Log an info statement separating msg and data by :"""
        self.logger.warning(f"{msg} : {data}")

    def big_info(self, msg:str):
        """Logs a info statement encapsuled between ----"""
        self.logger.info(f"--------------- {msg} ---------------")

    def warning(self, msg:str):
        """Log a warning  statement logging first the service then the message"""
        self.logger.warning(f"{msg}")

    def error(self, msg:str):
        """Log a error statement logging first the service then the message"""
        self.logger.error(f"{msg}")

    def error_in_record_loop(self, index:int, record_id:str, err:str):
        """Log an error statement for a loop through records, displayin :
            - the record index
            - the record ID
            - a message"""
        self.logger.error(f"[Index {str(index)}, ID : {record_id}] {err}")