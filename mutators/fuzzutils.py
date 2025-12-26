#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#-:-:-:-:-:-:-::-:-:#
#     SIP Torch     #
#-:-:-:-:-:-:-::-:-:#

# Author: Refactored by GPT-5-Codex
# Utility helpers for fuzzing RFC 4475 payloads

import os
import random
import string
from typing import Iterable, List, Optional, Tuple

_ASCII_WORDS: List[str] = [
    'fuzz', 'vector', 'entropy', 'packet', 'torment', 'malformed', 'branch',
    'payload', 'variant', 'cursor', 'traverse', 'quantum', 'glyph', 'tangle',
    
]
_UNICODE_PHRASES: List[str] = [
    '\u09b6\u0995\u09cd\u09a4\u09bf \u09aa\u09cd\u09b0\u09ac\u09be\u09b9',
    '\u52d5\u7684\u89e3\u6790', '\u062a\u062d\u0644\u064a\u0644 \u0627\u0644\u0628\u0631\u0648\u062a\u0648\u0643\u0648\u0644',
    '\u03b4\u03b9\u03ac\u03c7\u03c5\u03c3\u03b7 \u03c3\u03ae\u03bc\u03b1\u03c4\u03bf\u03c2',
    '\u0905\u092a\u094d\u0930\u0924\u094d\u092f\u093e\u0936\u093f\u0924 \u0935\u0947\u0915\u094d\u091f\u0930',
    '\u89e3\u6790\u6ce2\u5f62'
]
_ATYPICAL_SCHEMES: List[str] = [
    'ftp', 'ldap', 'gopher', 'modem', 'nntp', 'imap', 'news', 'tn3270', 'fax'
]
_PUNCTUATION_OPTIONS: List[str] = ["'", '-', '&', '.', '~']
_RNG = random.Random()


def seed_rng(seed: Optional[int]) -> int:
    """Seed the internal RNG and python's global RNG for reproducibility."""
    if seed is None:
        seed_bytes = os.urandom(16)
        seed = int.from_bytes(seed_bytes, byteorder='big')
    _RNG.seed(seed)
    random.seed(seed)
    return seed


def random_token(min_len: int = 4, max_len: int = 12, alphabet: str | None = None) -> str:
    alphabet = alphabet or string.ascii_lowercase
    length = _RNG.randint(min_len, max_len)
    return ''.join(_RNG.choice(alphabet) for _ in range(length))


def random_digits(min_digits: int = 2, max_digits: int = 6) -> str:
    length = _RNG.randint(min_digits, max_digits)
    return ''.join(_RNG.choice(string.digits) for _ in range(length))


def random_int_str(min_value: int, max_value: int) -> str:
    return str(_RNG.randint(min_value, max_value))


def random_huge_numeric_string(min_digits: int = 11, max_digits: int = 32) -> str:
    length = _RNG.randint(min_digits, max_digits)
    digits = ''.join(_RNG.choice(string.digits) for _ in range(length))
    if digits.startswith('0'):
        digits = '9' + digits[1:]
    return digits


def random_unknown_param(prefix: str = 'unknown', min_suffix: int = 3, max_suffix: int = 8) -> str:
    suffix = random_token(min_suffix, max_suffix)
    return f'{prefix}{suffix}'


def random_separator_pattern(min_len: int = 4, max_len: int = 8, chars: str = ';,') -> str:
    length = _RNG.randint(min_len, max_len)
    pattern = ''.join(_RNG.choice(chars) for _ in range(length))
    return pattern


def random_display_token(include_punct: bool = True) -> str:
    token = random_token(4, 9, alphabet=string.ascii_lowercase)
    if include_punct and len(token) > 2 and _RNG.random() < 0.7:
        punct = _RNG.choice(_PUNCTUATION_OPTIONS)
        pos = _RNG.randint(1, len(token) - 1)
        token = token[:pos] + punct + token[pos:]
    if _RNG.random() < 0.5:
        token = token.capitalize()
    return token


def random_display_tokens(count: int, include_punct: bool = True) -> List[str]:
    return [random_display_token(include_punct=include_punct) for _ in range(count)]


def random_domain(depth_range: Tuple[int, int] = (1, 2), suffixes: Optional[Iterable[str]] = None) -> str:
    suffixes = list(suffixes) if suffixes is not None else ['example.com', 'invalid.io', 'tst', 'fuzz', 'lab', 'local', 'corp.', 'internal.cc', 'net', 'org', 'dev', 'io']
    depth = _RNG.randint(depth_range[0], depth_range[1])
    labels = [random_token(3, 8, alphabet=string.ascii_lowercase + string.digits) for _ in range(depth)]
    suffix = _RNG.choice(suffixes)
    labels.append(suffix)
    return '.'.join(labels)


def random_known_scheme() -> str:
    return _RNG.choice(_ATYPICAL_SCHEMES)


def random_unknown_scheme(prefix: str = 'x') -> str:
    base = random_token(4, 10)
    return f'{prefix}-{base}'


def random_reason_phrase(include_unicode: bool = True) -> str:
    words = [
        _RNG.choice(_ASCII_WORDS) for _ in range(_RNG.randint(2, 4))
    ]
    if include_unicode:
        words.append(_RNG.choice(_UNICODE_PHRASES))
    return ' '.join(words)


def random_sentence(word_range: Tuple[int, int] = (4, 8)) -> str:
    count = _RNG.randint(*word_range)
    words = [_RNG.choice(_ASCII_WORDS) for _ in range(count)]
    return ' '.join(words)


def repeat_char(charset: str = string.ascii_lowercase, min_repeat: int = 20, max_repeat: int = 80) -> str:
    char = _RNG.choice(charset)
    repeat = _RNG.randint(min_repeat, max_repeat)
    return char * repeat


def repeat_token(token_len_range: Tuple[int, int] = (4, 8), repeat_range: Tuple[int, int] = (5, 12), alphabet: Optional[str] = None) -> str:
    token = random_token(token_len_range[0], token_len_range[1], alphabet)
    return token * _RNG.randint(repeat_range[0], repeat_range[1])


def random_warning_agent() -> str:
    return f"{random_token(4, 8)}-{random_token(4, 6)}"


def random_warning_text() -> str:
    return random_sentence(word_range=(2, 5)).capitalize()


def random_http_uri(scheme: str = 'http') -> str:
    host = random_domain(depth_range=(1, 2))
    path = '/'.join(random_token(3, 7) for _ in range(_RNG.randint(1, 3)))
    return f'{scheme}://{host}/{path}'


def random_contact_name() -> str:
    return f"name:{random_token(6, 12)}"
