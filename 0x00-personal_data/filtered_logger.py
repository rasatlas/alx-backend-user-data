#!/usr/bin/env python3
"""0. Regex-ing"""
import re
from typing import List


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """A function that returns the log message obfuscated."""
    return re.sub(
        r"({}=)([^{}]+)".format("|".join(fields), separator), r"\1" +
        redaction, message
    )
