from __future__ import unicode_literals
import base64
import re
import socket
from socket import AF_INET, AF_INET6
import string

# Supported Operations - return value of check_format_function
FMT_CHK = 0     # Format check function exists
FMT_CVT = 1     # Binary conversion functions exist

# Format Operations - return value of get_format_function
FMT_NAME = 0    # Name of format option
FMT_CHECK = 1   # Function to check if value is valid (String, Binary, or Integer/Number types)
FMT_B2S = 2     # Function to convert binary to string (encode / serialize Binary types)
FMT_S2B = 3     # Function to convert string to binary (decode / deserialize Binary types)


# From https://stackoverflow.com/questions/2532053/validate-a-hostname-string
def s_hostname(sval):
    if not isinstance(sval, type('')):
        raise TypeError
    hostname = sval[:]      # Copy since we're modifying input
    if hostname[-1] == ".":
        hostname = hostname[:-1]  # strip exactly one dot from the right, if present
    if len(sval) > 253:
        raise ValueError
    allowed = re.compile("(?!-)[A-Z\d-]{1,63}(?<!-)$", re.IGNORECASE)
    if all(allowed.match(x) for x in hostname.split(".")):
        return sval
    raise ValueError


# Use regex from https://stackoverflow.com/questions/201323/how-to-validate-an-email-address-using-a-regular-expression
#   A more comprehensive email address validator is available at http://isemail.info/about
def s_email(sval):
    if not isinstance(sval, type('')):
        raise TypeError
    rfc5322_re = (
        r"(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|"
        r'"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*")@'
        r"(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:(2(5[0-5]|[0-4][0-9])"
        r"|1[0-9][0-9]|[1-9]?[0-9]))\.){3}(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9])|[a-z0-9-]*[a-z0-9]"
        r":(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])")
    if re.match(rfc5322_re, sval):
        return sval
    raise ValueError


def b_ip_addr(bval):        # Length of IP addr must be 32 or 128 bits
    if not isinstance(bval, bytes):
        raise TypeError
    if len(bval) == 4 or len(bval) == 16:
        return bval
    raise ValueError


def b_ipv4_addr(bval):      # Length of IPv4 addr must be 32 bits
    if not isinstance(bval, bytes):
        raise TypeError
    if len(bval) == 4:
        return bval
    raise ValueError


def b_ipv6_addr(bval):      # Length of IPv6 addr must be 128 bits
    if not isinstance(bval, bytes):
        raise TypeError
    if len(bval) == 16:
        return bval
    raise ValueError


def b_mac_addr(bval):       # Length of MAC addr must be 48 or 64 bits
    if not isinstance(bval, bytes):
        raise TypeError
    if len(bval) == 6 or len(bval) == 8:
        return bval
    raise ValueError


def s_uri(sval):            # Check if valid URI
    if not isinstance(sval, type('')):
        raise TypeError
    if True:                # TODO: write it
        return sval
    raise ValueError


def _format_ok(val):        # No value constraints on this type
    return val


def _err(val):              # Unsupported format type
    raise NameError


FORMAT_CHECK_FUNCTIONS = {
    'hostname':     [s_hostname, _err, _err],       # Domain-Name
    'email':        [s_email, _err, _err],          # Email-Addr
    'ip-addr':      [_err, b_ip_addr, _err],        # IP-Addr (IPv4 or IPv6)
    'ipv4':         [_err, b_ipv4_addr, _err],      # IPv4-Addr
    'mac-addr':     [_err, b_mac_addr, _err],       # MAC-Addr
    'uri':          [s_uri, _err, _err]             # URI
}


def s2b_hex(sval):      # Convert from hex string to binary
    return base64.b16decode(sval)


def b2s_hex(bval):      # Convert from binary to hex string
    return base64.b16encode(bval).decode()


def s2b_base64url(sval):      # Convert from base64url string to binary
    v = sval + ((4 - len(sval) % 4) % 4)*'='          # Pad b64 string out to a multiple of 4 characters
    if set(v) - set(string.ascii_letters + string.digits + '-_='):  # Python 2 doesn't support Validate
        raise TypeError('base64decode: bad character')
    return base64.b64decode(str(v), altchars='-_')


def b2s_base64url(bval):      # Convert from binary to base64url string
    return base64.urlsafe_b64encode(bval).decode().rstrip('=')


def s2b_ip_addr(sval):
    return s2b_ipv6_addr(sval) if ':' in sval else s2b_ipv4_addr(sval)


def s2b_ipv4_addr(sval):    # Convert IPv4 addr from string to binary
    try:
        return socket.inet_pton(AF_INET, sval)
    except AttributeError:       # Python 2 doesn't support inet_pton on Windows
        return socket.inet_aton(sval)
    except OSError:
        raise ValueError


def s2b_ipv6_addr(sval):    # Convert IPv6 address from string to binary
    return socket.inet_pton(AF_INET6, sval)


def b2s_ip_addr(bval):
    return b2s_ipv6_addr(bval) if len(bval) > 4 else b2s_ipv4_addr(bval)


def b2s_ipv4_addr(bval):      # Convert IPv4 address from binary to string
    try:
        return socket.inet_ntop(AF_INET, bval)
    except AttributeError:
        return socket.inet_ntoa(bval)       # Python 2 doesn't support inet_ntop on Windows
    except OSError:
        raise ValueError


def b2s_ipv6_addr(bval):        # Convert ipv6 address from binary to string
        return socket.inet_ntop(AF_INET6, bval)     # Python 2 doesn't support inet_ntop on Windows


def s2a_ip_net(sval):
    raise ValueError        # TODO: write it


def a2s_ip_net(bval):
    raise ValueError


def s2a_ipv4_net(sval):
    s_ip, s_prefix = sval.split('/', 1)
    ip = s2b_ipv4_addr(s_ip)
    prefix = int(s_prefix)
    return ip, prefix


def a2s_ipv4_net(bval):
    raise ValueError


FORMAT_CONVERT_FUNCTIONS = {
    'b64u': (b2s_base64url, s2b_base64url),         # Base64url
    'x': (b2s_hex, s2b_hex),                        # Hex
    'ip-addr':  (b2s_ip_addr, s2b_ip_addr),         # IP (v4 or v6) Address, version autodetect
    'ipv4': (b2s_ipv4_addr, s2b_ipv4_addr),         # IPv4 Address
    'ipv6': (b2s_ipv6_addr, s2b_ipv6_addr),         # IPv6 Address
    'ip-net': (a2s_ip_net, s2a_ip_net),             # IP (v4 or v6) Net Address with CIDR prefix length
    'ipv4-net': (a2s_ipv4_net, s2a_ipv4_net)        # IPv4 Net Address with CIDR prefix length
}


def check_format_function(name, basetype, convert=None):
    ff = get_format_function(name, basetype, convert)
    return ff[FMT_CHECK] != _err, ff[FMT_B2S] != _err


def get_format_function(name, basetype, convert=None):
    if basetype == 'Binary':
        convert = convert if convert else 'b64u'
        try:
            cvt = FORMAT_CONVERT_FUNCTIONS[convert]
        except KeyError:
            cvt = (_err, _err)    # Binary conversion function not found, return Err
    else:
        cvt = (_err, _err)    # Binary conversion function not applicable, return Err
    try:
        col = {'String': 0, 'Binary': 1, 'Number': 2}[basetype]
        return (name, FORMAT_CHECK_FUNCTIONS[name][col]) + cvt
    except KeyError:
        return (name, _err if name else _format_ok) + cvt


# May not need functions for:
#   Date-Time       - Integer - min and max value for plausible date range
#   Duration        - Integer - max value for plausible durations?
#   Identifier      - String - regex pattern
#   Port            - Integer - min 0, max 65535
#   Request-Id      - Binary - len 0 - 8 bytes
#   UUID            - Binary - len == 16 bytes + RFC 4122 checks?

# Semantic validation functions from JSON Schema Draft 6
#    date-time      - String, RFC 3339, section 5.6
#    email          - String, RFC 5322, section 3.4.1
#    hostname       - String, RFC 1034, section 3.1
#    ipv4           - String, dotted-quad
#    ipv6           - String, RFC 2373, section 2.2
#    uri            - RFC 3986
#    uri-reference  - RFC 3986, section 4.1
#    json-pointer   - RFC 6901
#    uri-template   - RFC 6570
