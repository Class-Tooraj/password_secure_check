from __future__ import annotations
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> #
#           < IN THE NAME OF GOD >           #
# ------------------------------------------ #
__AUTHOR__ = "ToorajJahangiri"
__EMAIL__ = "Toorajjahangiri@gmail.com"
# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< #


# IMPORT
import os
import string

# IMPORT TYPING
from typing import NamedTuple

# \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\^////////////////////////////// #

# CHECK IN COMMAN PASSWORD LIST
def comman_password_list(inp: str, file: str) -> NamedTuple[bool, int | None]:
    cpl = NamedTuple('CPL', (('exists', bool), ('line', int | None)))
    with open(file, 'r') as f:
        lst = f.read().splitlines()
        if inp in lst:
            return cpl(True, lst.index(inp))
        return cpl(False, None)

# CHECK CHARACKTER UPPER CASE EXISTS IN INPUT
def upper_case(inp: str) -> list[bool]:
    return [True if c.isupper() else False for c in inp]

# CHECK CHARACKTER LOWER CASE EXISTS IN INPUT
def lower_case(inp: str) -> list[bool]:
    return [True if c.islower() else False for c in inp]

# CHECK DIGIT CHARACKTER EXISTS IN INPUT
def digit(inp: str) -> list[bool]:
    return [True if c.isdigit() else False for c in inp]

# CHECK CHARACKTER SPECIAL EXISTS IN INPUT
def special(inp: str) -> list[bool]:
    _sp = string.punctuation
    return [True if c in _sp else False for c in inp]

# GRAB CHAR FROM LIST
def grab_chars(inp: str, pattern: list[bool]) -> str:
    grab = [c for c, p in zip(inp, pattern) if p is True]
    return ''.join(grab)

# LENGTH RATE
def length_rate(length: int) -> int:
    if length > 6:
        return 1
    elif length > 8:
        return 2
    elif length > 10:
        return 3
    elif length > 12:
        return 4
    elif length > 16:
        return 5

    return 0

# PERCENT
def percent(num: int, size: int) -> float:
    return (num / size) * 100

# MANY TRUE IN LIST
def many_true(lst:list[bool]) -> int:
    many = 0
    for i in lst:
        if i is True:
            many += 1
    return many

# UPPER CASE RATE
def upper_rate(lst:list[bool]) -> int:
    many = many_true(lst)
    length = len(lst)
    per = percent(many, length)

    if 1.0 < per <= 10.0:
        return 2
    elif per <= 20.0:
        return 3
    elif per <= 30.0:
        return 4
    elif per <= 40.0:
        return 5
    elif 50.0 <= per <= 70.0:
        return 6

    return 0

# LOWER CASE RATE
def lower_rate(lst:list[bool]) -> int:
    many = many_true(lst)
    length = len(lst)
    per = percent(many, length)

    if 1.0 < per <= 40.0:
        return 1
    elif 40.0 < per <= 70.0:
        return 2

    return 0

# DIGIT RATE
def digit_rate(lst:list[bool]) -> int:
    many = many_true(lst)
    length = len(lst)
    per = percent(many, length)

    if 1.0 < per <= 30.0:
        return 3
    elif 30.0 < per <= 70.0:
        return 4

    return 0

# SPECIAL RATE
def special_rate(lst:list[bool]) -> int:
    many = many_true(lst)
    length = len(lst)
    per = percent(many, length)

    if 1.0 < per <= 30.0:
        return 4
    elif 30.0 < per <= 70.0:
        return 6

    return 0

# RATE SECURE PASSWORD
def rate_secure_password(inp: str, file: str = None, ignore_cpl: bool = False) -> dict[str, str|int|NamedTuple]:
    file = os.path.realpath("./data/ps-list-01-10000.txt") if file is None else os.path.realpath(file)

    dt = NamedTuple('DETAIL', (('length', int), ('upper', int), ('lower', int), ('digit', int), ('special', int)))

    IN_LIST = comman_password_list(inp, file)
    LENGTH: int = len(inp)
    UPPER: list[bool] = upper_case(inp)
    LOWER: list[bool] = lower_case(inp)
    DIGIT: list[bool] = digit(inp)
    SPECIAL: list[bool] = special(inp)

    rsp_map = {
        'rate': 0,
        'rate_percent': '0 %',
        'length': LENGTH,
        'upper': grab_chars(inp, UPPER) or None,
        'lower': grab_chars(inp, LOWER) or None,
        'digit': grab_chars(inp, DIGIT) or None,
        'special': grab_chars(inp, SPECIAL) or None,
        'cpl_line': IN_LIST.line,
        'details': ()
        }

    rate = 0

    if IN_LIST.exists and not ignore_cpl:
        return rsp_map

    details = dt(length_rate(LENGTH), upper_rate(UPPER), lower_rate(LOWER), digit_rate(DIGIT), special_rate(SPECIAL))

    rate += sum(details)

    rsp_map['details'] = details
    rsp_map['rate'] = rate
    rsp_map['rate_percent'] = f"{round(percent(rate, 23), 1)} %"
    return rsp_map


__dir__ = (
    'comman_password_list',
    'upper_case',
    'lower_case',
    'special',
    'digit',
    'grab_chars',
    'length_rate',
    'percent',
    'many_true',
    'upper_rate',
    'lower_rate',
    'digit_rate',
    'special_rate',
    'rate_secure_password'
    )
