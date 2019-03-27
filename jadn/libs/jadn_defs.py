"""
 JADN Definitions

A JSON Abstract Data Notation (JADN) file contains a list of datatype definitions.  Each type definition
has a specified format - a list of four or five columns depending on whether the type is primitive or
structure: (name, base type, type options, type description [, fields]).

For the enumerated type each field definition is a list of three items: (tag, name, description).

For other structure types (array, choice, map, record) each field definition is a list of five items:
(tag, name, type, field options, field description).
"""

from __future__ import unicode_literals

# JADN Datatype Definition columns
TypeName = 0        # Datatype name
BaseType = 1        # Base type - built-in or defined
TypeOptions = 2     # Type options
TypeDesc = 3        # Type description
Fields = 4          # List of fields

# JADN Field Definition columns
FieldID = 0         # Element ID
FIeldName = 1       # Element name
EnumDesc = 2        # Enumerated value description
FieldType = 2       # Datatype of field
FieldOptions = 3    # Field options
FieldDesc = 4       # Field Description

# JADN built-in datatypes

PRIMITIVE_TYPES = (
    'Binary',
    'Boolean',
    'Integer',
    'Number',
    'Null',
    'String',
)

STRUCTURE_TYPES = (
    'Enumerated',
    'Choice',
    'Array',
    'ArrayOf',          # (value type) Special case: instance is a structure but type definition has no fields
    'Map',
    'MapOf',            # (key type, value type)
    'Record',
)


def is_primitive(vtype):
    return vtype in PRIMITIVE_TYPES


def is_builtin(vtype):
    return vtype in PRIMITIVE_TYPES + STRUCTURE_TYPES


# Option Tags/Keys
#   JADN Type Options (TypeOptions) and Field Options (FieldOptions) contain a list of strings, each of which is an option.
#   The first character of an option string is the type ID; the remaining characters are the value.
#   The option string is converted into a Name: Value pair before use.
#   The tables list the unicode codepoint of the ID and the corresponding Name.

TYPE_OPTIONS = {        # ID, value type, description
    0x3d: 'id',         # '=', boolean, Enumerated type and Choice/Map/Record keys are ID not Name
    0x25: 'enum',       # '%', boolean, enumeration derived from field type
    0x2a: 'vtype',      # '*', string, Value type for ArrayOf and MapOf
    0x2b: 'ktype',      # '+', string, Key type for MapOf
    0x40: 'format',     # '@', string, semantic validation keyword
    0x2e: 'sopt',       # '.', string, serialization and validation keyword
    0x24: 'pattern',    # '$', string, regular expression that a string type must match
    0x7b: 'minv',       # '[', integer, minimum byte or text string length, numeric value, element count
    0x7d: 'maxv',       # ']', integer, maximum byte or text string length, numeric value, element count
    0x21: 'default',    # '!', string, default value for this field (coerced to field type)
}

FIELD_OPTIONS = {
    0x5b: 'minc',       # '[', integer, minimum cardinality, default = 1, 0 = field is optional
    0x5d: 'maxc',       # ']', integer, maximum cardinality, default = 1, 0 = inherited max, not 1 = array
    0x26: 'tfield',     # '&', string, field that specifies the type of this field
    0x3c: 'flatten',    # '<', integer, use FieldName as namespace prefix for FieldType, depending on serialization
}

ALLOWED_TYPE_OPTIONS = {
    'Binary': ['minv', 'maxv', 'format', 'sopt'],
    'Boolean': [],
    'Integer': ['min', 'max', 'format', 'sopt'],
    'Number': ['min', 'max', 'format', 'sopt'],
    'Null': [],
    'String': ['min', 'max', 'format', 'sopt', 'pattern'],
    'Enumerated': ['id'],
    'Choice': ['id'],
    'Array': ['format', 'sopt'],
    'ArrayOf': ['vtype', 'minv', 'maxv'],
    'Map': ['id', 'minv', 'maxv'],
    'MapOf': ['ktype', 'vtype', 'minv', 'maxv'],
    'Record': [],
}

FORMAT_CHECK = {            # Semantic validation functions
    'email': 'String',      # email address, RFC 5322 Section 3.4.1
    'hostname': 'String',   # host name, RFC 1123 Section 2.1
    'ip-addr': 'Binary',    # length must be 4 octets (IPv4) or 16 octets (IPv6)
    'mac-addr': 'Binary',   # length must be 6 octets (EUI-48) or 8 octets (EUI-64)
    'uri': 'String',        # RFC 3986 Appendix A
}

FORMAT_CONVERT = {          # Binary-String and Array-String conversion functions
    'b': 'Binary',          # Base64url - RFC 4648 Section 5 (default)
    'x': 'Binary',          # Hex - RFC 4648 Section 8
    'ipv4-addr': 'Binary',  # IPv4 text representation - draft-main-ipaddr-text-rep-02 Section 3
    'ipv6-addr': 'Binary',  # IPv6 text representation - RFC 5952 Section 4
    'ipv4-net': 'Array',    # IPv4 Network Address CIDR string - RFC 4632 Section 3.1
    'ipv6-net': 'Array',    # IPv6 Network Address CIDR string - RFC 4291 Section 2.3
}
