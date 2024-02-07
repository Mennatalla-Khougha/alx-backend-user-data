#!/usr/bin/env python3
"""Filter file"""
from typing import List
import re
import logging


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
    """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        NotImplementedError


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
