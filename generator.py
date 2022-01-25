from __future__ import annotations
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> #
#           < IN THE NAME OF GOD >           #
# ------------------------------------------ #
__AUTHOR__ = "ToorajJahangiri"
__EMAIL__ = "Toorajjahangiri@gmail.com"
# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< #


# IMPORT
import random
import string

from typing import Iterable, Sequence, Literal

# \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\^////////////////////////////// #

# PATTERN TYPE
T_PATTERN = Literal[
    'all',
    'num',
    'upper',
    'lower',
    'number',
    'symbol',
    'uppercase',
    'lowercase',
    'letter',
    'digit',
    'special'
    ]

# CHARACKTER CLASS
class DefaultChars:
    """
    Default Character
    UPPERCASE: Sequence[str] = [Ascii UpperCase - `A-Z`]
    LOWERCASE: Sequence[str] = [Ascii LowerCase - `a-z`]
    LETTER: Sequence[str] = [Ascii Letters `LowerCase + UpperCase` - `a-z-A-Z`]
    DIGIT: Sequence[str] = [Ascii Digit `0-9`]
    SPECIAL: Sequence[str] = [Ascii Punctuation `Symbols`]
    ALL: Sequence[str] = [Ascii `Letter + Digit + Special`]
    """
    UPPERCASE = string.ascii_uppercase
    LOWERCASE = string.ascii_lowercase
    LETTER = string.ascii_letters
    DIGIT = string.digits
    SPECIAL = string.punctuation
    ALL = f'{LETTER}{DIGIT}{SPECIAL}'

    def pattern(self, patterns: Iterable[str] | list[T_PATTERN], remove: str = None) -> str:
        """
        Pattern Make Sequence [String] Character.
        args:
            patterns [Iterable[str] | list[T_PATTERN]] : [Making Sequence Of Character from Pattern].
            remove [str] : [Remove Characters From The Pattern] default is `None`.

        return:
            [str]: [Created Sequence Character].
        """
        res = ''
        translate = {'UPPER': 'UPPERCASE', 'LOWER': 'LOWERCASE', 'NUM': 'DIGIT', 'NUMBER': 'DIGIT', 'SYMBOL': 'SPECIAL'}
        for name in patterns:
            name = translate.get(name.upper(), name.upper())
            if hasattr(self, name):
                res += getattr(self, name)
            continue

        if remove:
            res = (i for i in res if i not in remove)
            res = ''.join(res)
        return res


def gen_key(length: int, chars: Sequence[str] | list[T_PATTERN] = None, remove: str = None) -> str:
    """
    Generate Key
    args:
        length [int] : [Length Of Generate Key].
        chars [Sequence[str] | list[T_PATTERN]] : [Available Character For Choiceing] default is `None` -> [ALL].
        remove [str]: [Remove Characters From The chars] default is `None`.
    """
    defaults = DefaultChars()

    if chars is None:
        chars = defaults.ALL
        if remove is not None:
            chars = ''.join([c for c in chars if c not in remove])

    elif isinstance(chars, (list, tuple)):
        chars = defaults.pattern(chars, remove)

    else:
        if remove is not None:
            chars = ''.join([c for c in chars if c not in remove])

    choices = [*chars]
    random.shuffle(choices)
    random.shuffle(choices)
    return ''.join([random.choice(choices) for _ in range(length)])


__dir__ = ('T_PATTERN', 'DefaultChars', 'gen_key')
