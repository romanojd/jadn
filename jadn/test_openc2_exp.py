# This Python file uses the following encoding: utf-8
from __future__ import unicode_literals

import os
import unittest

from libs.codec.codec import Codec
from libs.codec.jadn import jadn_load, jadn_analyze

# These unit tests include features that are not currently used in the OpenC2 Language Specification or
# any actuator profile.  They demonstrate that potential features work and show how to use them, to
# provide concrete illustration of alternative proposals.


class Experimental_IP(unittest.TestCase):

    def setUp(self):
        fn = os.path.join('schema', 'oc2ls-exp_merged.jadn')        # Load experimental OpenC2 schema
        schema = jadn_load(fn)
        sa = jadn_analyze(schema)
        if sa['undefined']:
            print('Warning - undefined:', sa['undefined'])
        self.tc = Codec(schema, verbose_rec=True, verbose_str=True)

    ipv4_addr_b64_api = {           # API IPv4 address target.  All API values are identical except for target name.
      'action': 'deny',
      'target': {'exp': {'ipv4_addr_b64': b'\xc0\xa8\x00\xfe'}}}

    ipv4_addr_b64_ser = {           # IPv4 address target serialized in Base64url format
      'action': 'deny',
      'target': {'exp': {'ipv4_addr_b64': 'wKgA_g'}}}

    ipv4_addr_hex_api = {           # API IPv4 address target.  All API values are identical except for target name.
      'action': 'deny',
      'target': {'exp': {'ipv4_addr_x': b'\xc0\xa8\x00\xfe'}}}

    ipv4_addr_hex_ser = {           # IPv4 address target serialized in hex format
      'action': 'deny',
      'target': {'exp': {'ipv4_addr_x': 'C0A800FE'}}}

    ipv4_addr_str_api = {           # API IPv4 address target.  All API values are identical except for target name.
      'action': 'deny',
      'target': {'exp': {'ipv4_addr_s': b'\xc0\xa8\x00\xfe'}}}

    ipv4_addr_str_ser = {           # IPv4 address target serialized in type-specific string (dotted decimal) format
      'action': 'deny',
      'target': {'exp': {'ipv4_addr_s': '192.168.0.254'}}}

    def test_ipv4_b64(self):
        self.assertEqual(self.tc.encode('OpenC2-Command', self.ipv4_addr_b64_api), self.ipv4_addr_b64_ser)
        self.assertEqual(self.tc.decode('OpenC2-Command', self.ipv4_addr_b64_ser), self.ipv4_addr_b64_api)

    def test_ipv4_hex(self):
        self.assertEqual(self.tc.encode('OpenC2-Command', self.ipv4_addr_hex_api), self.ipv4_addr_hex_ser)
        self.assertEqual(self.tc.decode('OpenC2-Command', self.ipv4_addr_hex_ser), self.ipv4_addr_hex_api)

    def test_ipv4_str(self):
        self.assertEqual(self.tc.encode('OpenC2-Command', self.ipv4_addr_str_api), self.ipv4_addr_str_ser)
        self.assertEqual(self.tc.decode('OpenC2-Command', self.ipv4_addr_str_ser), self.ipv4_addr_str_api)

    ipv6_addr_b64_api = {           # API IPv6 address target.  All API values are identical except for target name.
      'action': 'deny',
      'target': {'exp': {'ipv6_addr_b64': b' \x01\r\xb8\x85\xa3\x08\xd3\x13\x19\x8a.\x03psH'}}}

    ipv6_addr_b64_ser = {           # IPv6 address target serialized in Base64url format
      'action': 'deny',
      'target': {'exp': {'ipv6_addr_b64': 'IAENuIWjCNMTGYouA3BzSA'}}}

    ipv6_addr_hex_api = {           # API IPv6 address target.  All API values are identical except for target name.
      'action': 'deny',
      'target': {'exp': {'ipv6_addr_x': b' \x01\r\xb8\x85\xa3\x08\xd3\x13\x19\x8a.\x03psH'}}}

    ipv6_addr_hex_ser = {           # IPv6 address target serialized in hex format
      'action': 'deny',
      'target': {'exp': {'ipv6_addr_x': '20010DB885A308D313198A2E03707348'}}}

    ipv6_addr_str_api = {           # API IPv6 address target.  All API values are identical except for target name.
      'action': 'deny',
      'target': {'exp': {'ipv6_addr_s': b' \x01\r\xb8\x85\xa3\x08\xd3\x13\x19\x8a.\x03psH'}}}

    ipv6_addr_str_ser = {           # IPv6 address target serialized in type-specific string (dotted decimal) format
      'action': 'deny',
      'target': {'exp': {'ipv6_addr_s': '2001:db8:85a3:8d3:1319:8a2e:370:7348'}}}

    def test_ipv6_b64(self):
        self.assertEqual(self.tc.encode('OpenC2-Command', self.ipv6_addr_b64_api), self.ipv6_addr_b64_ser)
        self.assertEqual(self.tc.decode('OpenC2-Command', self.ipv6_addr_b64_ser), self.ipv6_addr_b64_api)

    def test_ipv6_hex(self):
        self.assertEqual(self.tc.encode('OpenC2-Command', self.ipv6_addr_hex_api), self.ipv6_addr_hex_ser)
        self.assertEqual(self.tc.decode('OpenC2-Command', self.ipv6_addr_hex_ser), self.ipv6_addr_hex_api)

    def test_ipv6_str(self):
        self.assertEqual(self.tc.encode('OpenC2-Command', self.ipv6_addr_str_api), self.ipv6_addr_str_ser)
        self.assertEqual(self.tc.decode('OpenC2-Command', self.ipv6_addr_str_ser), self.ipv6_addr_str_api)

if __name__ == '__main__':
    unittest.main()
