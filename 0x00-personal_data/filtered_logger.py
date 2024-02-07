#!/usr/bin/env python3
"""Filter file"""
from typing import List
import re
import logging
import os
import mysql.connector


def filter_datum(
        fields: List[str],
        redaction: str,
        message: str,
        separator: str
        ) -> str:
    """Function that returns the log message obfuscated

    Args:
        fields (List[str]): List of strings representing all fields
                            to obfuscate
        redaction (str): String representing by what the field will
                         be obfuscated
        message (str): String representing the log line
        separator (str): String representing by which character is
                        separating all fields in the log line (message)

    return:
    str: The log message obfuscated
    """
    for field in fields:
        message = re.sub(
            r'{}=[^{}]+'.format(field, separator),
            '{}={}'.format(field, redaction),
            message)
    return message


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
    """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """Initialize the class

        Args:
            fields (List[str]):List of strings representing all fields
                            to obfuscate
        """
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """ filter values in incoming log records using filter_datum

        Args:
            record (logging.LogRecord): values in incoming log records
        """
        record.msg = filter_datum(self.fields,
                                  self.REDACTION, record.msg,
                                  self.SEPARATOR)
        return super().format(record)


PII_FIELDS = ("email", "ssn", "password", "phone", "name")


def get_logger() -> logging.Logger:
    """The logger should be named "user_data" and only log up to logging.INFO
    level. It should not propagate messages to other loggers.
    It should have a StreamHandler with RedactingFormatter as formatter

    Returns:
        logging.Logger:
    """
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.INFO)

    formatter = RedactingFormatter(fields=list(PII_FIELDS))
    stream_handler.setFormatter(formatter)

    logger.addHandler(stream_handler)

    return logger


def get_db():
    """Returns a connector to the database"""
    username = os.getenv("PERSONAL_DATA_DB_USERNAME", "root")
    password = os.getenv("PERSONAL_DATA_DB_PASSWORD", "")
    host = os.getenv("PERSONAL_DATA_DB_HOST", "localhost")
    name = os.getenv("PERSONAL_DATA_DB_NAME")

    connection = mysql.connector.connection.MySQLConnection(
        user=username, password=password, host=host, database=name)

    return connection
