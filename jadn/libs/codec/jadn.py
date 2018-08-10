"""
Load, validate, prettyprint, and dump JSON Abstract Encoding Notation (JADN) schemas
"""

from __future__ import print_function, unicode_literals

import json
import jsonschema
import numbers
import os
from datetime import datetime
from .codec import is_builtin, is_primitive, Codec
from .codec_utils import topts_s2d, fopts_s2d
from .jadn_defs import *

# TODO: convert prints to ValidationError exception

jadn_schema = {
    "type": "object",
    "required": ["meta", "types"],
    "additionalProperties": False,
    "properties": {
        "meta": {
            "type": "object",
            "required": ["module"],
            "additionalProperties": False,
            "properties": {
                "module": {"type": "string"},
                "patch": {"type": "string"},
                "title": {"type": "string"},
                "description": {"type": "string"},
                "imports": {
                    "type": "array",
                    "items": {
                        "type": "array",
                        "minItems": 2,
                        "maxItems": 2,
                        "items": [
                            {"type": "string"},
                            {"type": "string"}
                        ]
                    }
                },
                "exports": {
                    "type": "array",
                    "items": {"type": "string"}
                }
            }
        },
        "types": {
            "type": "array",
            "items": {
                "type": "array",
                "minItems": 4,
                "maxItems": 5,
                "items": [
                    {"type": "string"},
                    {"type": "string"},
                    {"type": "array",
                        "items": {"type": "string"}
                    },
                    {"type": "string"},
                    {"type": "array",
                        "items": {
                            "type": "array",
                            "minItems": 3,
                            "maxItems": 5,
                            "items": [
                                {"type": "integer"},
                                {"type": "string"},
                                {"type": "string"},
                                {"type": "array",
                                 "items": {"type": "string"}
                                },
                                {"type": "string"}
                            ]
                        }
                    }
                ]
            }
        }
    }
}


def jadn_check(schema):
    """
    Validate JADN structure against JSON schema,
    Validate JADN structure against JADN schema, then
    Perform additional checks on type definitions
    """

    jsonschema.Draft4Validator(jadn_schema).validate(schema)
#    with open(os.path.join('schema', 'jadn.jadn')) as f:        # TODO: more robust method for locating JADN definition file
#        jc = Codec(json.load(f), verbose_rec=True, verbose_str=True)
#        assert jc.encode("Schema", schema) == schema

    valid_topts = {
        'Binary': ['min', 'max'],
        'Boolean': [],
        'Integer': ['min', 'max'],
        'Number': ['min', 'max'],
        'Null': [],
        'String': ['min', 'max', 'pattern', 'format'],
        'Array': ['min'],
        'ArrayOf': ['min', 'max', 'rtype'],
        'Choice': ['compact'],
        'Enumerated': ['compact'],
        'Map': ['min'],
        'Record': ['min'],
    }
    valid_fopts = {
        'Binary': ['min', 'max'],
        'Boolean': ['min', 'max'],
        'Integer': ['min', 'max'],
        'Number': ['min', 'max'],
        'Null': [],
        'String': ['min', 'max', 'pattern', 'format'],
        "Array": ['min', 'max', 'etype', 'atfield'],
        'ArrayOf': ['min', 'max', 'rtype'],
        "Choice": ['min', 'max', 'etype'],
        "Enumerated": ['rtype'],
        "Map": ['min', 'max', 'etype'],
        "Record": ['min', 'max', 'etype', 'atfield'],
    }

    # TODO: raise exception instead of print
    # TODO: field type Null can't have options

    assert set(valid_topts) == set(STRUCTURE_TYPES + PRIMITIVE_TYPES)       # Ensure valid options list is in sync with jadn_defs
    assert set(valid_fopts) == set(STRUCTURE_TYPES + PRIMITIVE_TYPES)

    for t in schema["types"]:     # datatype definition: TNAME, TTYPE, TOPTS, TDESC, FIELDS
        tt = t[TTYPE]
        if not is_builtin(tt):
            print("Type error: Unknown type", tt, "(" + t[TNAME] + ")")       # TODO: handle if t[TNAME] doesn't exist

        topts = topts_s2d(t[TOPTS])
        vop = {k for k in topts} - {k for k in valid_topts[tt]}
        if vop:
            print("Error:", t[TNAME], "type", tt, "invalid type option", str(vop))
        if tt == 'ArrayOf' and 'rtype' not in topts:
            print("Error:", t[TNAME], "- Missing array element type")
        if is_primitive(tt) or tt == 'ArrayOf':
            if len(t) != 4:    # TODO: trace back to base type
                print("Type format error:", t[TNAME], "- type", tt, "cannot have items")
        else:
            if len(t) == 5:
                tags = set()
                n = 3 if tt == "Enumerated" else 5
                for k, i in enumerate(t[FIELDS]):       # item definition: 0-tag, 1-name, 2-type, 3-options, 4-description
                    tags.update({i[FTAG]})              # or (enumerated): 0-tag, 1-name, 2-description
                    ordinal = tt in ('Array', 'Record') or (tt == 'Choice' and 'compact' in topts)
                    if ordinal and i[FTAG] != k + 1:
                        print("Item tag error:", t[TNAME] + '(' + tt + '):' + i[FNAME], '--', i[FTAG], "should be", k + 1)
                    if len(i) != n:
                        print("Item format error:", t[TNAME], tt, i[FNAME], "-", len(i), "!=", n)
                    if len(i) > 3 and is_builtin(i[FTYPE]):     # TODO: trace back to builtin types
                        fop = {k for k in fopts_s2d(i[FOPTS])} - {k for k in valid_fopts[i[FTYPE]]}
                        if fop:
                            print("Error:", t[TNAME], ":", i[FNAME], i[FTYPE], "invalid field option", str(fop))
                    # TODO: check that wildcard name has Choice type, and that there is only one wildcard.
                if len(t[FIELDS]) != len(tags):
                    print("Tag collision", t[TNAME], len(t[FIELDS]), "items,", len(tags), "unique tags")
            else:
                print("Type format error:", t[TNAME], "- missing items from compound type", tt)
    return schema

def topo_sort(items):
    """
    Topological sort with locality
    Sorts a list of (item: (dependencies)) pairs so that 1) all dependency items are listed before the parent item,
    and 2) dependencies are listed in the given order and as close to the parent as possible.
    Returns the sorted list of items and a list of root items.  A single root indicates a fully-connected hierarchy;
    multiple roots indicate disconnected items or hierarchies, and no roots indicate a dependency cycle.
    """
    def walk_tree(item):
        for i in deps[item]:
            if i not in out:
                walk_tree(i)
                out.append(i)

    out = []
    deps = {i[0]:i[1] for i in items}
    roots = {i[0] for i in items} - set().union(*[i[1] for i in items])
    for item in roots:
        walk_tree(item)
        out.append(item)
    out = out if out else [i[0] for i in items]     # if cycle detected, don't sort
    return out, roots


def build_jadn_deps(schema):
    def ns(name):   # Return namespace if present
        return name.split(':')[0]

    imps = schema['meta']['imports'] if 'imports' in schema['meta'] else []
    items = [(n[0], []) for n in imps]
    for tdef in schema["types"]:
        deps = []
        if tdef[TTYPE] == "ArrayOf":
            rtype = topts_s2d(tdef[TOPTS])["rtype"]
            if not is_builtin(rtype):
                deps.append(ns(rtype))
        if len(tdef) > FIELDS and tdef[TTYPE] != "Enumerated":
            for f in tdef[FIELDS]:
                if not is_builtin(f[FTYPE]):
                    deps.append(ns(f[FTYPE]))
        items.append((tdef[TNAME], deps))
    return items


def jadn_analyze(schema):
    items = build_jadn_deps(schema)
#    out, roots = topo_sort(items)
    exports = schema['meta']['exports'] if 'exports' in schema['meta'] else []
    refs = set().union(*[i[1] for i in items]) | set(exports)
    types = {i[0] for i in items}
    return {
        'unreferenced': [str(k) for k in types - refs],
        'undefined': [str(k) for k in refs - types],
        'cycles': [],
    }


def jadn_loads(jadn_str):
    schema = json.loads(jadn_str)
    jadn_check(schema)
    return schema


def jadn_load(fname):
    with open(fname) as f:
        schema = json.load(f)
    jadn_check(schema)
    return schema


def jadn_dumps(schema, level=0, indent=1):
    sp = level * indent * " "
    sp2 = (level + 1) * indent * " "
    if isinstance(schema, dict):
        sep = ",\n" if level > 0 else ",\n\n"
        lines = []
        for k in sorted(schema):
            lines.append(sp2 + "\"" + k + "\": " + jadn_dumps(schema[k], level + 1, indent))
        return "{\n" + sep.join(lines) + "\n" + sp + "}"
    elif isinstance(schema, list):
        sep = ",\n" if level > 1 else ",\n\n"
        vals = []
        nest = schema and isinstance(schema[0], list)
        sp4 = ""
        for v in schema:
            sp3 = sp2 if nest else ""
            sp4 = sp if v and isinstance(v, list) else ""
            vals.append(sp3 + jadn_dumps(v, level + 1, indent))
        if nest:
            return "[\n" + sep.join(vals) + "]\n"
        return "[" + ", ".join(vals) + sp4 + "]"
    elif isinstance(schema, (numbers.Number, type(""))):
        return json.dumps(schema)
    return "???"


def jadn_dump(schema, fname, source=""):
    with open(fname, "w") as f:
        if source:
            f.write("\"Generated from " + source + ", " + datetime.ctime(datetime.now()) + "\"\n\n")
        f.write(jadn_dumps(schema) + "\n")
