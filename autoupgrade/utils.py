# -*- coding: utf-8 -*-

from re import compile as r


RE_DIGIT = r("(\d+)")
RE_NONDIGIT = r(r'\D+')


def normalize_version(version):
    """
    Helper function to normalize version.
    Returns a comparable object.
    Args:
        version (str) version, e.g. "0.1.0"
    """
    rv = []
    for x in version.split("."):
        try:
            rv.append(int(x))
        except ValueError:
            for y in RE_DIGIT.split(x):
                if y == '':
                    continue
                try:
                    rv.append(int(y))
                except ValueError:
                    rv.append(y)
    return rv


def ver_to_tuple(value):
    """
    Convert version like string to a tuple of integers.
    """
    return tuple(int(_f) for _f in RE_NONDIGIT.split(value) if _f)
