
def s_hostname(sval):
    assert isinstance(sval, type(''))
    return True


def s_email(sval):
    assert isinstance(sval, type(''))
    return True


def b_ip_addr(bval):
    assert isinstance(bval, bytes)
    return len(bval) == 4 or len(bval) == 16


def b_mac_addr(bval):
    assert isinstance(bval, bytes)
    return len(bval) == 6 or len(bval) == 8


def s_uri(sval):
    assert isinstance(sval, type(''))
    return True


def ok(val):
    return True


def get_format_function(name, type):
    try:
        col = {'String': 0, 'Binary': 1}[type]
        return (name, FORMAT_FUNCTIONS[name][col])
    except KeyError:
        return ('', None)


FORMAT_FUNCTIONS = {
    'hostname': [s_hostname, None],       # Domain-Name
    'email': [s_email, None],             # Email-Addr
    'ip-addr': [ok, b_ip_addr],           # IP-Addr
    'mac-addr': [ok, b_mac_addr],         # MAC-Addr
    'uri': [s_uri, None]                  # URI
}

# Date-Time  - Integer - min and max value
# Duration   - Integer - max value?
# Identifier - String - regex pattern
# Port       - Integer - min 1 ?, max 65535
# Request-Id - Binary - len 0 - 8 bytes
# UUID       - Binary - len == 16 bytes

# Semantic validation functions from JSON Schema
#    date-time
#    date
#    time
#    email
#    idn-email
#    hostname
#    idn-hostname
#    ipv4
#    ipv6
#    uri
#    uri-reference
#    iri
#    iri-reference
#    uri-template
#    json-pointer
#    relative-json-pointer
#    regex

