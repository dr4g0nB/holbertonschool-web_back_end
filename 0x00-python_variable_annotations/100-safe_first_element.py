#!/usr/bin/env python3
"""Corrects duck-type annotations"""


from typing import Sequence, Any, Union


def safe_first_element(lst: Sequence[Any]) -> Union[Any, None]:
    """Duck-type"""
    if lst:
        return lst[0]
    else:
        return None
