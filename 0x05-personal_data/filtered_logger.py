#!/usr/bin/env python3
"""
Function called filter_datum that returns the log message obfuscated
"""
import re
from typing import List
import logging
import os
import mysql.connector


PII_FIELDS = ('name', 'email', 'phone', 'ssn', 'password')


def filter_datum(fields: List[str],
                 redaction: str,
                 message: str,
                 separator: str) -> str:
    """Return - Log message obfuscated"""
    for i in fields:
        message = re.sub(f'{i}=.+?{separator}',
                         f'{i}={redaction}{separator}', message)
    return message


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
    """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """Init
        """
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """Format
        """
        return filter_datum(self.fields, self.REDACTION,
                            super().format(record), self.SEPARATOR)


def get_logger() -> logging.Logger:
    """Return
        - An object
    """
    logger = logging.getLogger("user_data")
    str_handler = logging.StreamHandler()
    str_handler.setLevel(logging.INFO)
    logger.propagate = False
    formatter = logging.formatter(RedactingFormatter(PII_FIELDS))
    str_handler.setFormatter(formatter)
    logger.addHandler(str_handler)
    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """Database connector
    """
    user = os.getenv('PERSONAL_DATA_DB_USERNAME')
    password = os.getenv('PERSONAL_DATA_DB_PASSWORD')
    host = os.getenv('PERSONAL_DATA_DB_HOST')
    database = os.getenv('PERSONAL_DATA_DB_NAME')

    return mysql.connector.connect(user=user,
                                   password=password,
                                   host=host,
                                   database=database)
