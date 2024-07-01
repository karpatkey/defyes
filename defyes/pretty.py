"""
This module provides utilities for pretty-printing in Python.

It includes a custom print function that uses the `pprint` module to format output,
and a `jprint` function for pretty-printing JSON-style objects.

Functions:
    jprint(obj): Print a JSON-style object with indentation and other formatting.
"""

import json
from pprint import PrettyPrinter

pp = PrettyPrinter(indent=2, width=180, compact=True, underscore_numbers=True)

buildin_print = print
print = pp.pprint


def jprint(obj):
    """
    JSON style pretty printer.
    """
    buildin_print(json.dumps(obj, indent=2, default=lambda o: str(o)))
