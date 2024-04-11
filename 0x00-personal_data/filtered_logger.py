#!/usr/bin/env python3
"""0. Regex-ing"""
import re


def filter_datum(
    fields,
    redaction,
    message,
    separator,
):
    """A function that returns the log message obfuscated."""
    return re.sub(
        r"({}=)([^{}]+)".format("|".join(fields), separator), r"\1" +
        redaction, message
    )
