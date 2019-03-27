"""
Load, validate, prettyprint, and dump JSON Abstract Encoding Notation (JADN) schemas
"""

from __future__ import print_function, unicode_literals

import copy
import json
import jsonschema
import numbers
from datetime import datetime
from libs.jadn_defs import *
from libs.jadn_utils import topts_s2d, fopts_s2d, basetype

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
#        assert jc.encode('Schema', schema) == schema

    # TODO: raise exception instead of print

    for t in schema['types']:     # datatype definition: TypeName, BaseType, TypeOptions, TypeDesc, Fields
        tt = basetype(t[BaseType])
        if is_builtin(tt):
            topts = topts_s2d(t[TypeOptions])
            vop = {k for k in topts} - {k for k in SUPPORTED_TYPE_OPTIONS[tt]}
            if vop:
                print('Error:', t[TypeName], 'type', tt, 'invalid type option', str(vop))
        else:
            print('Error: Unknown Base Type:', tt, '(' + t[TypeName] + ')')       # TODO: handle if t[TypeName] doesn't exist
            topts = {}
        if tt == 'ArrayOf' and 'rtype' not in topts:
            print('Error:', t[TypeName], '- Missing array element type')
        if 'format' in topts:
            f = topts['format']
            if f not in FORMAT_CHECK or tt != FORMAT_CHECK[f]:
                print('Unsupported value constraint', '"' + topts['format'] + '" on', tt + ':',  t[TypeName])
        if 'cvt' in topts:
            f = topts['cvt']
            if f not in FORMAT_CONVERT or tt != FORMAT_CONVERT[f]:
                print('Unsupported String conversion', '"' + topts['cvt'] + '" on', tt + ':',  t[TypeName])
        if is_primitive(tt) or tt == 'ArrayOf':
            if len(t) != 4:    # TODO: trace back to base type
                print('Type format error:', t[TypeName], '- type', tt, 'cannot have items')
        elif is_builtin(tt):
            if len(t) == 5:
                tags = set()                            # TODO: check for name and tag collisions
                n = 3 if tt == 'Enumerated' else 5      # TODO: check Choice min cardinality != 0
                for k, i in enumerate(t[Fields]):       # item definition: 0-tag, 1-name, 2-type, 3-options, 4-description
                    tags.update({i[FieldID]})              # or (enumerated): 0-tag, 1-name, 2-description
                    ordinal = tt in ('Array', 'Record')
                    if ordinal and i[FieldID] != k + 1:
                        print('Item tag error:', t[TypeName] + '(' + tt + '):' + i[FieldName], '--', i[FieldID], 'should be', k + 1)
                    if len(i) != n:
                        print('Item format error:', t[TypeName], tt, i[FieldName], '-', len(i), '!=', n)
                    if len(i) > 3 and is_builtin(i[FieldType]):     # TODO: trace back to builtin types
                        fop = {k for k in fopts_s2d(i[FieldOptions])} - {k for k in SUPPORTED_FIELD_OPTIONS[i[FieldType]]}
                        if fop:
                            print('Error:', t[TypeName], ':', i[FieldName], i[FieldType], 'invalid field option', str(fop))
                    # TODO: check that wildcard name has Choice type, and that there is only one wildcard.
                if len(t[Fields]) != len(tags):
                    print('Tag collision', t[TypeName], len(t[Fields]), 'items,', len(tags), 'unique tags')
            else:
                print('Type format error:', t[TypeName], '- missing items from compound type', tt)
    return schema


def jadn_strip(schema):             # Strip comments from schema
    sc = copy.deepcopy(schema)
    for tdef in sc['types']:
        tdef[TypeDesc] = ''
        if len(tdef) > Fields:
            fd = EnumDesc if tdef[BaseType] == 'Enumerated' else FieldDesc
            for fdef in tdef[Fields]:
                fdef[fd] = ''
    return sc


def jadn_merge(base, imp, nsid):      # Merge an imported schema into a base schema
    def update_opts(opts):
        return [(x[0] + nsid + ':' + x[1:] if x[0] == '*' and x[1:] in imported_names else x) for x in opts]

    types = base['types'][:]        # Make a copy to avoid modifying base
    imported_names = {t[TypeName] for t in imp['types']}
    for t in imp['types']:
        new_types = [nsid + ':' + t[TypeName], t[BaseType], t[TypeOptions], t[TypeDesc]]
        new_types[TypeOptions] = update_opts(new_types[TypeOptions])
        if len(t) > Fields:
            new_fields = t[Fields][:]
            if t[BaseType] != 'Enumerated':
                for f in new_fields:
                    f[FieldOptions] = update_opts(f[FieldOptions])
                    if f[FieldType] in imported_names:
                        f[FieldType] = nsid + ':' + f[FieldType]
            new_types.append(new_fields)
        types.append(new_types)
    return {'meta': base['meta'], 'types': types}


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
    def ns(name, nsids):   # Return namespace if name has a known namespace, otherwise return full name
        nsp = name.split(':')[0]
        return nsp if nsp in nsids else name

    imps = schema['meta']['imports'] if 'imports' in schema['meta'] else []
    items = [(n[0], []) for n in imps]
    nsids = [n[0] for n in imps]
    for tdef in schema['types']:
        deps = []
        if tdef[BaseType] == 'ArrayOf':
            rtype = topts_s2d(tdef[TypeOptions])['rtype']
            if not is_builtin(rtype):
                deps.append(ns(rtype, nsids))
        if len(tdef) > Fields and tdef[BaseType] != 'Enumerated':
            for f in tdef[Fields]:
                if not is_builtin(f[FieldType]):
                    deps.append(ns(f[FieldType], nsids))
        items.append((tdef[TypeName], deps))
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


def jadn_dumps(schema, level=0, indent=1, strip=False, nlevel=None):
    sp = level * indent * ' '
    sp2 = (level + 1) * indent * ' '
    sep2 = ',\n' if strip else ',\n\n'
    if isinstance(schema, dict):
        sep = ',\n' if level > 0 else sep2
        lines = []
        for k in schema:
            lines.append(sp2 + '"' + k + '": ' + jadn_dumps(schema[k], level + 1, indent, strip))
        return '{\n' + sep.join(lines) + '\n' + sp + '}'
    elif isinstance(schema, list):
        sep = ',\n' if level > 1 else sep2
        vals = []
        nest = schema and isinstance(schema[0], list)       # Not an empty list
        for v in schema:
            sp3 = sp2 if nest else ''
            vals.append(sp3 + jadn_dumps(v, level + 1, indent, strip, level))
        if nest:
            spn = (nlevel if nlevel else level) * indent * ' '
            return '[\n' + sep.join(vals) + '\n' + spn + ']'
        return '[' + ', '.join(vals) + ']'
    elif isinstance(schema, (numbers.Number, type(''))):
        return json.dumps(schema)
    return '???'


def jadn_dump(schema, fname, source='', strip=False):
    with open(fname, 'w') as f:
        if source:
            f.write('"Generated from ' + source + ', ' + datetime.ctime(datetime.now()) + '"\n\n')
        f.write(jadn_dumps(schema, strip=strip) + '\n')
