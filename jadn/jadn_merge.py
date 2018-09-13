"""
Merge a JSON Abstract Data Notation (JADN) module and its imported modules into a single file.
"""

from __future__ import print_function
import os

from libs.codec.jadn_defs import *
from libs.codec.jadn import jadn_load, jadn_dump, jadn_analyze, jadn_strip


"""
    # Prettyprint JADN, and convert to other formats

    schema = jadn_load(source)
    sa = jadn_analyze(schema)

    patch = ', ' + schema['meta']['patch'] if 'patch' in schema['meta'] else ''
    exports = ', '.join(schema['meta']['exports']) if 'exports' in schema['meta'] else ''
    sa.update({'module': schema['meta']['module'] + patch, 'exports': exports})
    print('\n'.join(['  ' + k + ': ' + str(sa[k]) for k in ('module', 'exports', 'unreferenced', 'undefined', 'cycles')]))

    jadn_dump(jadn_strip(schema), dest + '-strip.jadn')
    jadn_dump(schema, dest + '.jadn')
"""

"""
Merge an imported schema into a base schema
"""

def merge_import(base, imp, nsid):
    types = base['types'][:]
    print(len(types), 'types')
    for t in imp['types']:
        nt = [nsid + ':' + t[TNAME], t[TTYPE], t[TOPTS], t[TDESC]]
        nf = []
        if len(t) > FIELDS:
            nf = t[FIELDS][:]
            if t[TTYPE] != 'Enumerated':

        types.append(nt + nf)
    return {'meta': base['meta'], 'types': types}


def jadn_merge(idir, base=None):
    def _merge_imports(info, dest, files):
        base_schema = jadn_load(info['source'])
        for nsid, module in info['imports']:
            imp = [i for i in files.values() if i['module'] == module]
            patches = [i['patch'] for i in imp]
            print(nsid, module, patches)
            if len(imp) > 1:
                raise ValueError('More than one matching import:', nsid, module, patches)
            elif len(imp) == 1:
                imported_schema = jadn_load(imp[0]['source'])

    def _meta(schema, item):
        return schema['meta'][item] if item in schema['meta'] else ''

    cdir = os.path.dirname(os.path.realpath('__file__'))    # Current directory
    odir = os.path.normpath(os.path.join(cdir, '..', '..', 'schema_out'))     # Put generated schemas outside of the repo
    print('Merging imported schemas from', os.path.realpath(idir), 'to', odir)
    files = {}
    for fn in (f[0] for f in (os.path.splitext(i) for i in os.listdir(idir)) if f[1] == '.jadn'):
        source = os.path.join(idir, fn) + '.jadn'
        dest = os.path.join(odir, fn) + '.jadn'
        schema = jadn_load(source)
        id = _meta(schema, 'module') + '/' + _meta(schema, 'patch')
        if id in files:
            raise ValueError('Duplicate schema IDs:', id, source, files['id']['source'])
        else:
            files.update({id: {
                'source': source,
                'id': id,
                'module': _meta(schema, 'module'),
                'patch': _meta(schema, 'patch'),
                'imports': _meta(schema, 'imports'),
                'exports': _meta(schema, 'exports'),
            }})

    for k, v in files.items():
        if v['imports']:
            print(k, 'imports', v['imports'])
            _merge_imports(v, dest, files)


if __name__ == '__main__':
    jadn_merge('schema', 'oasis-open.org/openc2/v1.0/openc2-lang/wd08-slpf')
