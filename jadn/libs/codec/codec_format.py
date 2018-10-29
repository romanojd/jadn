import re
import socket
from socket import AF_INET, AF_INET6

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


def s2b_ip_addr(sval):      # Convert IP addr from string to binary
    try:
        return socket.inet_pton(AF_INET, sval)
    except OSError:
        raise ValueError


def b2s_ip_addr(bval):      # Convert IP addr from binary to string
    try:
        return socket.inet_ntop(AF_INET, bval)
    except OSError:
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
    if True:    # TODO
        return sval
    raise ValueError


def get_format_function(name, type):
    try:
        col = {'String': 0, 'Binary': 1, 'Number': 2}[type]
        return name, FORMAT_FUNCTIONS[name][col]
    except KeyError:
        return '', None


FORMAT_FUNCTIONS = {
    'hostname': [s_hostname, None, None],       # Domain-Name
    'email':    [s_email, None, None],          # Email-Addr
    'ip-addr':  [None, b_ip_addr, None],        # IP-Addr
    'mac-addr': [None, b_mac_addr, None],       # MAC-Addr
    'uri':      [s_uri, None, None]             # URI
}

SERIALIZE_FUNCTIONS = {
    'ip-addr':  (b2s_ip_addr, s2b_ip_addr)      # IP Address
}

# May not need functions for:
#   Date-Time  - Integer - min and max value
#   Duration   - Integer - max value?
#   Identifier - String - regex pattern
#   Port       - Integer - min 1 ?, max 65535
#   Request-Id - Binary - len 0 - 8 bytes
#   UUID       - Binary - len == 16 bytes + RFC 4122 checks?

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

