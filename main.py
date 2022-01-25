from __future__ import annotations
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> #
#           < IN THE NAME OF GOD >           #
# ------------------------------------------ #
__AUTHOR__ = "ToorajJahangiri"
__EMAIL__ = "Toorajjahangiri@gmail.com"
# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< #


# IMPORT
import sys
import os
import time
import argparse
import json

from typing import NamedTuple, Sequence

# IMPORT LOCAL
from analyzer import rate_secure_password
from generator import gen_key, T_PATTERN

# \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\^////////////////////////////// #


def make_key(length: int = 16, chars: str | T_PATTERN = None, remove: str = None, gen: int = 500, rate_limit: int = 12, cpl_file: str = None) -> str:
    if remove and remove.lower() == 'default':
        remove = ':\\/"\'()[]{};.,><|=_^~+`'
    elif remove in (' ', ''):
        remove = None

    keys = (gen_key(length, chars, remove) for _ in range(gen))
    keys = (
        (key, rate_secure_password(key, cpl_file))
        for key in keys
        if rate_secure_password(key)['rate'] >= rate_limit
        )

    mk = NamedTuple('MK', (('key', str), ('details', dict)))
    return mk(*max(keys, key=lambda x: x[1]['rate']))

def make_handle(parse: argparse.ArgumentParser) -> None:
    # Get Mode Not Use Any Where
    parse.add_argument('mode')

    parse.add_argument(
        '--length',
        type=int,
        default=16,
        help='Length For Generate Key'
        )

    parse.add_argument(
        '--chars',
        type = str,
        default= ['all'],
        help='Character For Generate Key - default all chars `letter, digit, symbol`',
    )

    parse.add_argument(
        '--pattern',
        type=str,
        default=None,
        help='Make Charackter Pattern Use List - `["upper", "digit", "symbol", "lower", "letter", "all"]`'
    )

    parse.add_argument(
        '--remove',
        type=str,
        default='default',
        help='Remove Chars From Dec Chars if need remove nothing use empty string "" - default ":\\/"\'()[]{};.,><|=_^~+"'
    )

    parse.add_argument(
        '--ratelimit',
        type=int,
        choices=range(1, 23),
        default=12,
        help='Limit Rate For Make Key - [1-23]'
    )

    parse.add_argument(
        '--dec',
        type=int,
        default = 500,
        help='Generate key in Dec For Choice Max Rate From Dec - Bigger Better But Slower'
    )

    parse.add_argument(
        '--listfile',
        type=str,
        default=None,
        help='Password List File Path'
    )

    parse.add_argument(
        '--time', '-t',
        action='store_true',
        default=False,
        help='Time Options'
    )

    parse.add_argument(
        '--details', '-D',
        action='store_true',
        default=False,
        help='Show Key Details Options'
    )

    arguments = vars(parse.parse_args())

    if arguments['pattern']:
        arguments['chars'] = arguments['pattern']
    t0 = time.monotonic()

    mk = make_key(
        arguments['length'],
        arguments['chars'],
        arguments['remove'],
        arguments['dec'],
        arguments['ratelimit'],
        arguments['listfile']
    )

    t1 = time.monotonic()
    print(f"{mk.key}")

    if arguments['details']:
        rate_detail = mk.details
        rate_detail['details'] = {k:v for k,v in zip(['length','upper','lower','digit','special'], rate_detail['details'])}
        rate_detail = json.dumps(rate_detail, indent=4)
        print(f'Details: {rate_detail}')

    if arguments['time']:
        print(f"Time: {t1-t0:.3f}")

def rate_handle(parse: argparse.ArgumentParser) -> None:

    parse.add_argument(
        'key',
        type=str,
        help='Key Or Password Checking Secure'
    )

    parse.add_argument(
        '--listfile',
        type=str,
        default=None,
        help='Password List File Path'
    )

    parse.add_argument(
        '--cplskip',
        action='store_true',
        default=False,
        help='Ignore Cpl File Checking Break'
    )


    parse.add_argument(
        '--time', '-t',
        action='store_true',
        default=False,
        help='Time Options'
    )
    parse.add_argument(
        '--write',
        type=str,
        default=None,
        help='Write Result To This Path'
    )

    arguments = vars(parse.parse_args())

    t0 = time.monotonic()
    check = rate_secure_password(
        arguments['key'],
        arguments['listfile'],
        arguments['cplskip']
    )
    check['details'] = {k:v for k,v in zip(['length','upper','lower','digit','special'], check['details'])}
    details = json.dumps(check, indent=4)
    t1 = time.monotonic()

    print(details)

    if arguments['write']:
        pack = {}
        path = os.path.realpath(arguments['write'])
        pack['key'] = arguments['key']
        pack.update(check)
        with open(path, 'w') as f:
            json.dump(pack, f, indent=4)

    del details, check

    if arguments['time']:
        print(f"Time: {t1-t0:.3f}")


def main(argv: Sequence[str] = None) -> int:
    _key_make_name = ('make', '*k')
    argv = argv if argv is not None else sys.argv[1:]

    names = " or ".join(_key_make_name)
    parse = argparse.ArgumentParser(
        'Password Secure Check',
        description=f'Check "Password" Or "Key" is Secure for Generate New "Key" or "Password" Use [{names}] as first Arguments'
        )

    if len(argv) >= 1:
        if argv[0] in _key_make_name:
            make_handle(parse)
        else:
            rate_handle(parse)
    else:
        print("| PASSWORD SECURE CHECK |")
        print("- Run Without Order - ")
        print("\n-- Hint:")
        print(f"\t-- For Generate New 'Key' or 'Password' Use [{names}] as First Arguments")
        print("\t-- Other Wise Run Password Secure Check As Default App")
        print(f"\t-- View MakeKey Help Run Command -> {_key_make_name[0]} --help")
        print("\t-- View PasswordSecure Help Run Command -> --help")
        # print(f"\n- Author : {__AUTHOR__}\n- Email  : {__EMAIL__}")
        print(f"-- -- --\n")

    return 0

if __name__ == '__main__':
    raise SystemExit(main(sys.argv[1:]))

