"""
Support functions for JADN codec
  Convert dict between nested and flat
  Convert typedef options between dict and strings
"""

from functools import reduce
from libs.jadn_defs import *

# Dict conversion utilities

def _dmerge(x, y):
    k, v = next(iter(y.items()))
    if k in x:
        _dmerge(x[k], v)
    else:
        x[k] = v
    return x


def hdict(keys, value, sep="."):
    """
    Convert a hierarchical-key value pair to a nested dict
    """
    return reduce(lambda v, k: {k: v}, reversed(keys.split(sep)), value)


def fluff(src, sep="."):
    """
    Convert a flat dict with hierarchical keys to a nested dict

    :param src: flat dict - e.g., {"a.b.c": 1, "a.b.d": 2}
    :param sep: separator character for keys
    :return: nested dict - e.g., {"a": {"b": {"c": 1, "d": 2}}}
    """
    return reduce(lambda x, y: _dmerge(x, y), [hdict(k, v, sep) for k, v in src.items()], {})


def flatten(cmd, path="", fc=None, sep="."):
    """
    Convert a nested dict to a flat dict with hierarchical keys
    """
    if fc is None:
        fc = {}
    fcmd = fc.copy()
    if isinstance(cmd, dict):
        for k, v in cmd.items():
            k = k.split(":")[1] if ":" in k else k
            fcmd = flatten(v, sep.join((path, k)) if path else k, fcmd)
    elif isinstance(cmd, list):
        for n, v in enumerate(cmd):
            fcmd.update(flatten(v, sep.join([path, str(n)])))
    else:
        fcmd[path] = cmd
    return fcmd


def dlist(src):
    """
    Convert dicts with numeric keys to lists

    :param src: {"a": {"b": {"0":"red", "1":"blue"}, "c": "foo"}}
    :return: {"a": {"b": ["red", "blue"], "c": "foo"}}
    """
    if isinstance(src, dict):
        for k in src:
            src[k] = dlist(src[k])
        if set(src) == set([str(k) for k in range(len(src))]):
            src = [src[str(k)] for k in range(len(src))]
    return src


# Option conversions

def topts_s2d(ostr):
    """
    Convert list of type definition option strings to options dictionary
    """

    tval = {
        "compact": lambda x: True,
        "cvt": lambda x: x,
        "format": lambda x: x,
        "min": lambda x: int(x),
        "max": lambda x: int(x),
        'ktype': lambda x: x,
        "rtype": lambda x: x,
        "pattern": lambda x: x,
    }

    assert set(tval) == {k for k in TYPE_OPTIONS.values()}
    assert isinstance(ostr, (list, tuple)), "%r is not a list" % ostr
    opts = {}
    for o in ostr:
        try:
            k = TYPE_OPTIONS[ord(o[0])]
            opts[k] = tval[k](o[1:])
        except KeyError:
            raise ValueError('Unknown type option: %s' % o)
    return opts

def fopts_s2d(ostr):
    """
    Convert list of field definition option strings to options dictionary
    """

    fval = {
        "min": lambda x: int(x),
        "max": lambda x: int(x),
        "atfield": lambda x: x,
        "rtype": lambda x: x,
        "etype": lambda x: x,
        'enum': lambda x: True,
        "default": lambda x: x
    }

    assert set(fval) == {k for k in FIELD_OPTIONS.values()}
    assert isinstance(ostr, (list, tuple)), "%r is not a list" % ostr
    opts = {}
    for o in ostr:
        try:
            k = FIELD_OPTIONS[ord(o[0])]
            opts[k] = fval[k](o[1:])
        except KeyError:
            raise ValueError('Unknown field option: %s' % o)
    return opts


def basetype(tt):                   # Return base type of derived subtypes
    return tt.rsplit('.')[0]        # Strip off subtype (e.g., .ID)


def multiplicity(min, max):
    if min == 1 and max == 1:
        return '1'
    return str(min) + '..' + ('*' if max == 0 else str(max))
