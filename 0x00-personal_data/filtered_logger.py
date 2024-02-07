#!/usr/bin/env python3
"""Filter file"""
from typing import List
import re


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

    regex = '|'.join(fields)
    print(f'({regex})=[^{separator}]*')
    return re.sub(f'({regex})=[^{separator}]*', f'\\1={redaction}', message)
