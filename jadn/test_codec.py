# This Python file uses the following encoding: utf-8
from __future__ import unicode_literals

import json
import os
import binascii
import unittest

from libs.codec.codec import Codec
from libs.jadn import jadn_load, jadn_check, jadn_analyze


# Encode and decode data to verify that numeric object keys work properly when JSON converts them to strings
def _j(data):
    return json.loads(json.dumps(data))


schema_basic = {                # JADN schema for datatypes used in Basic Types tests
    'meta': {'module': 'unittests-BasicTypes'},
    'types': [
        ['t_bool', 'Boolean', [], ''],
        ['t_int', 'Integer', [], ''],
        ['t_num', 'Number', [], ''],
        ['t_str', 'String', [], ''],
        ['t_bin', 'Binary', [], ''],
        ['t_array_of', 'ArrayOf', ['*Integer'], ''],
        ['t_choice', 'Choice', [], '', [
            [1, 'type1', 'String', [], ''],
            [4, 'type2', 'Boolean', [], ''],
            [7, 'type3', 'Integer', [], '']
        ]],
        ['t_choice_c', 'Choice', ['='], '', [       # Choice.ID - API key = tag
            [1, 'type1', 'String', [], ''],
            [4, 'type2', 'Boolean', [], ''],
            [7, 'type3', 'Integer', [], '']
        ]],
        ['t_enum', 'Enumerated', [], '', [
            [1, 'first', ''],
            [15, 'extra', ''],
            [8, 'Chunk', '']
        ]],
        ['t_enum_c', 'Enumerated', ['='], '', [
            [1, 'first', ''],
            [15, 'extra', ''],
            [8, 'Chunk', '']
        ]],
        ['t_array', 'Array', [], '', [
            [1, 'fbool', 'Boolean', ['[0'], ''],
            [2, 'fint', 'Integer', [], ''],
            [3, 'fnum', 'Number', [], ''],
            [4, 'fstr', 'String', ['[0'], ''],
            [5, 'farr', 't_aoa', ['[0'], ''],
            [6, 'fao', 't_aoi', ['[0'], '']
        ]],
        ['t_aoa', 'Array', [], '', [
            [1, '', 'Integer', [], ''],
            [2, '', 'String', [], '']
        ]],
        ['t_aoi', 'ArrayOf', ['*Integer'], ''],
        ['t_map_rgba', 'Map', [], '', [
            [2, 'red', 'Integer', [], ''],
            [4, 'green', 'Integer', ['[0'], ''],
            [6, 'blue', 'Integer', [], ''],
            [9, 'alpha', 'Integer', ['[0'], '']
        ]],
        ['t_arr_rgba', 'Array', [], '', [
            [1, 'red', 'Integer', [], ''],
            [2, 'green', 'Integer', ['[0'], ''],
            [3, 'blue', 'Integer', [], ''],
            [4, 'alpha', 'Integer', ['[0'], '']
        ]],
        ['t_rec_rgba', 'Record', [], '', [
            [1, 'red', 'Integer', [], ''],
            [2, 'green', 'Integer', ['[0'], ''],
            [3, 'blue', 'Integer', [], ''],
            [4, 'alpha', 'Integer', ['[0'], '']
        ]]
    ]}


class BasicTypes(unittest.TestCase):

    def setUp(self):
        jadn_check(schema_basic)
        self.tc = Codec(schema_basic, verbose_rec=False, verbose_str=False)

    def test_primitive(self):   # Non-composed types (bool, int, num, str)
        self.assertEqual(self.tc.decode('t_bool', True), True)
        self.assertEqual(self.tc.decode('t_bool', False), False)
        self.assertEqual(self.tc.encode('t_bool', True), True)
        self.assertEqual(self.tc.encode('t_bool', False), False)
        with self.assertRaises(TypeError):
            self.tc.decode('t_bool', 'True')
        with self.assertRaises(TypeError):
            self.tc.decode('t_bool', 1)
        with self.assertRaises(TypeError):
            self.tc.encode('t_bool', 'True')
        with self.assertRaises(TypeError):
            self.tc.encode('t_bool', 1)

        self.assertEqual(self.tc.decode('t_int', 35), 35)
        self.assertEqual(self.tc.encode('t_int', 35), 35)
        with self.assertRaises(TypeError):
            self.tc.decode('t_int', 35.4)
        with self.assertRaises(TypeError):
            self.tc.decode('t_int', True)
        with self.assertRaises(TypeError):
            self.tc.decode('t_int', 'hello')
        with self.assertRaises(TypeError):
            self.tc.encode('t_int', 35.4)
        with self.assertRaises(TypeError):
            self.tc.encode('t_int', True)
        with self.assertRaises(TypeError):
            self.tc.encode('t_int', 'hello')

        self.assertEqual(self.tc.decode('t_num', 25.96), 25.96)
        self.assertEqual(self.tc.decode('t_num', 25), 25)
        self.assertEqual(self.tc.encode('t_num', 25.96), 25.96)
        self.assertEqual(self.tc.encode('t_num', 25), 25)
        with self.assertRaises(TypeError):
            self.tc.decode('t_num', True)
        with self.assertRaises(TypeError):
            self.tc.decode('t_num', 'hello')
        with self.assertRaises(TypeError):
            self.tc.encode('t_num', True)
        with self.assertRaises(TypeError):
            self.tc.encode('t_num', 'hello')

        self.assertEqual(self.tc.decode('t_str', 'parrot'), 'parrot')
        self.assertEqual(self.tc.encode('t_str', 'parrot'), 'parrot')
        with self.assertRaises(TypeError):
            self.tc.decode('t_str', True)
        with self.assertRaises(TypeError):
            self.tc.decode('t_str', 1)
        with self.assertRaises(TypeError):
            self.tc.encode('t_str', True)
        with self.assertRaises(TypeError):
            self.tc.encode('t_str', 1)

    def test_array_of(self):
        self.assertEqual(self.tc.decode('t_array_of', [1, 4, 9, 16]), [1, 4, 9, 16])
        self.assertEqual(self.tc.encode('t_array_of', [1, 4, 9, 16]), [1, 4, 9, 16])
        with self.assertRaises(TypeError):
            self.tc.decode('t_array_of', [1, '4', 9, 16])
        with self.assertRaises(TypeError):
            self.tc.decode('t_array_of', 9)
        with self.assertRaises(TypeError):
            self.tc.encode('t_array_of', [1, '4', 9, 16])
        with self.assertRaises(TypeError):
            self.tc.decode('t_array_of', 9)

    B1b = b'data to be encoded'
    B1s = 'ZGF0YSB0byBiZSBlbmNvZGVk'
    B2b = 'data\nto be ëncoded 旅程'.encode(encoding='UTF-8')
    B2s = 'ZGF0YQp0byBiZSDDq25jb2RlZCDml4XnqIs'
    B3b = binascii.a2b_hex('18e0c9987b8f32417ca6744f544b815ad2a6b4adca69d2c310bd033c57d363e3')
    B3s = 'GODJmHuPMkF8pnRPVEuBWtKmtK3KadLDEL0DPFfTY-M'
    B_bad1b = 'string'
    B_bad2b = 394
    B_bad3b = True
    B_bad1s = 'ZgF%&0B++'

    def test_binary(self):
        self.assertEqual(self.tc.decode('t_bin', self.B1s), self.B1b)
        self.assertEqual(self.tc.decode('t_bin', self.B2s), self.B2b)
        self.assertEqual(self.tc.decode('t_bin', self.B3s), self.B3b)
        self.assertEqual(self.tc.encode('t_bin', self.B1b), self.B1s)
        self.assertEqual(self.tc.encode('t_bin', self.B2b), self.B2s)
        self.assertEqual(self.tc.encode('t_bin', self.B3b), self.B3s)
        with self.assertRaises((TypeError, binascii.Error)):
            self.tc.decode('t_bin', self.B_bad1s)
        with self.assertRaises(TypeError):
            self.tc.encode('t_bin', self.B_bad1b)
        with self.assertRaises(TypeError):
            self.tc.encode('t_bin', self.B_bad2b)
        with self.assertRaises(TypeError):
            self.tc.encode('t_bin', self.B_bad3b)

    C1a = {'type1': 'foo'}  # Choice - API keys are names
    C2a = {'type2': False}
    C3a = {'type3': 42}
    C1m = {1: 'foo'}
    C2m = {4: False}
    C3m = {7: 42}
    C1_bad1a = {'type1': 15}
    C1_bad2a = {'type5': 'foo'}
    C1_bad3a = {'type1': 'foo', 'type2': False}
    C1_bad1m = {1: 15}
    C1_bad2m = {3: 'foo'}
    C1_bad3m = {1: 'foo', '4': False}
    C1_bad4m = {'one': 'foo'}

    Cc1a = {1: 'foo'}       # Choice.ID - API keys are IDs
    Cc2a = {4: False}
    Cc3a = {7: 42}
    Cc1m = {1: 'foo'}
    Cc2m = {4: False}
    Cc3m = {7: 42}
    Cc1_bad1a = {1: 15}
    Cc1_bad2a = {8: 'foo'}
    Cc1_bad3a = {1: 'foo', 4: False}
    Cc1_bad1m = {1: 15}
    Cc1_bad2m = {3: 'foo'}
    Cc1_bad3m = {1: 'foo', '4': False}
    Cc1_bad4m = {'one': 'foo'}

    def test_choice_min(self):
        self.assertEqual(self.tc.encode('t_choice', self.C1a), self.C1m)
        self.assertEqual(self.tc.decode('t_choice', self.C1m), self.C1a)
        self.assertEqual(self.tc.decode('t_choice', _j(self.C1m)), self.C1a)
        self.assertEqual(self.tc.encode('t_choice', self.C2a), self.C2m)
        self.assertEqual(self.tc.decode('t_choice', self.C2m), self.C2a)
        self.assertEqual(self.tc.decode('t_choice', _j(self.C2m)), self.C2a)
        self.assertEqual(self.tc.encode('t_choice', self.C3a), self.C3m)
        self.assertEqual(self.tc.decode('t_choice', self.C3m), self.C3a)
        self.assertEqual(self.tc.decode('t_choice', _j(self.C3m)), self.C3a)
        with self.assertRaises(TypeError):
            self.tc.encode('t_choice', self.C1_bad1a)
        with self.assertRaises(ValueError):
            self.tc.encode('t_choice', self.C1_bad2a)
        with self.assertRaises(ValueError):
            self.tc.encode('t_choice', self.C1_bad3a)
        with self.assertRaises(TypeError):
            self.tc.decode('t_choice', self.C1_bad1m)
        with self.assertRaises(ValueError):
            self.tc.decode('t_choice', self.C1_bad2m)
        with self.assertRaises(ValueError):
            self.tc.decode('t_choice', self.C1_bad3m)
        with self.assertRaises(ValueError):
            self.tc.decode('t_choice', self.C1_bad4m)

    def test_choice_verbose(self):
        self.tc.set_mode(True, True)
        self.assertEqual(self.tc.encode('t_choice', self.C1a), self.C1a)
        self.assertEqual(self.tc.decode('t_choice', self.C1a), self.C1a)
        self.assertEqual(self.tc.encode('t_choice', self.C2a), self.C2a)
        self.assertEqual(self.tc.decode('t_choice', self.C2a), self.C2a)
        self.assertEqual(self.tc.encode('t_choice', self.C3a), self.C3a)
        self.assertEqual(self.tc.decode('t_choice', self.C3a), self.C3a)
        with self.assertRaises(TypeError):
            self.tc.encode('t_choice', self.C1_bad1a)
        with self.assertRaises(ValueError):
            self.tc.encode('t_choice', self.C1_bad2a)
        with self.assertRaises(ValueError):
            self.tc.encode('t_choice', self.C1_bad3a)
        with self.assertRaises(TypeError):
            self.tc.decode('t_choice', self.C1_bad1a)
        with self.assertRaises(ValueError):
            self.tc.decode('t_choice', self.C1_bad2a)
        with self.assertRaises(ValueError):
            self.tc.decode('t_choice', self.C1_bad3a)

    def test_choice_id_min(self):
        self.assertEqual(self.tc.encode('t_choice_c', self.Cc1a), self.Cc1m)
        self.assertEqual(self.tc.decode('t_choice_c', self.Cc1m), self.Cc1a)
        self.assertEqual(self.tc.decode('t_choice_c', _j(self.Cc1m)), self.Cc1a)
        self.assertEqual(self.tc.encode('t_choice_c', self.Cc2a), self.Cc2m)
        self.assertEqual(self.tc.decode('t_choice_c', self.Cc2m), self.Cc2a)
        self.assertEqual(self.tc.decode('t_choice_c', _j(self.Cc2m)), self.Cc2a)
        self.assertEqual(self.tc.encode('t_choice_c', self.Cc3a), self.Cc3m)
        self.assertEqual(self.tc.decode('t_choice_c', self.Cc3m), self.Cc3a)
        self.assertEqual(self.tc.decode('t_choice_c', _j(self.Cc3m)), self.Cc3a)
        with self.assertRaises(TypeError):
            self.tc.encode('t_choice_c', self.Cc1_bad1a)
        with self.assertRaises(ValueError):
            self.tc.encode('t_choice_c', self.Cc1_bad2a)
        with self.assertRaises(ValueError):
            self.tc.encode('t_choice_c', self.Cc1_bad3a)
        with self.assertRaises(TypeError):
            self.tc.decode('t_choice_c', self.Cc1_bad1m)
        with self.assertRaises(ValueError):
            self.tc.decode('t_choice_c', self.Cc1_bad2m)
        with self.assertRaises(ValueError):
            self.tc.decode('t_choice_c', self.Cc1_bad3m)
        with self.assertRaises(ValueError):
            self.tc.decode('t_choice_c', self.Cc1_bad4m)

    def test_choice_id_verbose(self):
        self.tc.set_mode(True, True)
        self.assertEqual(self.tc.encode('t_choice_c', self.Cc1a), self.Cc1a)
        self.assertEqual(self.tc.decode('t_choice_c', self.Cc1a), self.Cc1a)
        self.assertEqual(self.tc.encode('t_choice_c', self.Cc2a), self.Cc2a)
        self.assertEqual(self.tc.decode('t_choice_c', self.Cc2a), self.Cc2a)
        self.assertEqual(self.tc.encode('t_choice_c', self.Cc3a), self.Cc3a)
        self.assertEqual(self.tc.decode('t_choice_c', self.Cc3a), self.Cc3a)
        with self.assertRaises(TypeError):
            self.tc.encode('t_choice_c', self.Cc1_bad1a)
        with self.assertRaises(ValueError):
            self.tc.encode('t_choice_c', self.Cc1_bad2a)
        with self.assertRaises(ValueError):
            self.tc.encode('t_choice_c', self.Cc1_bad3a)
        with self.assertRaises(TypeError):
            self.tc.decode('t_choice_c', self.Cc1_bad1a)
        with self.assertRaises(ValueError):
            self.tc.decode('t_choice_c', self.Cc1_bad2a)
        with self.assertRaises(ValueError):
            self.tc.decode('t_choice_c', self.Cc1_bad3a)

    def test_enumerated_min(self):
        self.assertEqual(self.tc.encode('t_enum', 'extra'), 15)
        self.assertEqual(self.tc.decode('t_enum', 15), 'extra')
        with self.assertRaises(ValueError):
            self.tc.encode('t_enum', 'foo')
        with self.assertRaises(TypeError):
            self.tc.encode('t_enum', 15)
        with self.assertRaises(TypeError):
            self.tc.encode('t_enum', [1])
        with self.assertRaises(ValueError):
            self.tc.decode('t_enum', 13)
        with self.assertRaises(TypeError):
            self.tc.decode('t_enum', 'extra')
        with self.assertRaises(TypeError):
            self.tc.decode('t_enum', ['first'])

    def test_enumerated_verbose(self):
        self.tc.set_mode(True, True)
        self.assertEqual(self.tc.encode('t_enum', 'extra'), 'extra')
        self.assertEqual(self.tc.decode('t_enum', 'extra'), 'extra')
        with self.assertRaises(ValueError):
            self.tc.encode('t_enum', 'foo')
        with self.assertRaises(TypeError):
            self.tc.encode('t_enum', 42)
        with self.assertRaises(TypeError):
            self.tc.encode('t_enum', ['first'])
        with self.assertRaises(ValueError):
            self.tc.decode('t_enum', 'foo')
        with self.assertRaises(TypeError):
            self.tc.decode('t_enum', 42)
        with self.assertRaises(TypeError):
            self.tc.decode('t_enum', ['first'])

    def test_enumerated_id_min(self):
        self.assertEqual(self.tc.encode('t_enum_c', 15), 15)
        self.assertEqual(self.tc.decode('t_enum_c', 15), 15)
        with self.assertRaises(TypeError):
            self.tc.encode('t_enum_c', 'extra')
        with self.assertRaises(TypeError):
            self.tc.decode('t_enum_c', 'extra')

    def test_enumerated_id_verbose(self):
        self.tc.set_mode(True, True)
        self.assertEqual(self.tc.encode('t_enum_c', 15), 15)
        self.assertEqual(self.tc.decode('t_enum_c', 15), 15)
        with self.assertRaises(TypeError):
            self.tc.encode('t_enum_c', 'extra')
        with self.assertRaises(TypeError):
            self.tc.decode('t_enum_c', 'extra')

    RGB1 = {'red': 24, 'green': 120, 'blue': 240}    # API (decoded) and verbose values Map and Record
    RGB2 = {'red': 50, 'blue': 100}
    RGB3 = {'red': 9, 'green': 80, 'blue': 96, 'alpha': 128}
    RGB_bad1a = {'red': 24, 'green': 120}
    RGB_bad2a = {'red': 9, 'green': 80, 'blue': 96, 'beta': 128}
    RGB_bad3a = {'red': 9, 'green': 80, 'blue': 96, 'alpha': 128, 'beta': 196}
    RGB_bad4a = {'red': 'four', 'green': 120, 'blue': 240}
    RGB_bad5a = {'red': 24, 'green': '120', 'blue': 240}
    RGB_bad6a = {'red': 24, 'green': 120, 'bleu': 240}
    RGB_bad7a = {'1': 24, 'green': 120, 'blue': 240}
    RGB_bad8a = {1: 24, 'green': 120, 'blue': 240}

    Map1m = {2: 24, 4: 120, 6: 240}                  # Encoded values Map (minimized and dict/tag mode)
    Map2m = {2: 50, 6: 100}
    Map3m = {2: 9, 4: 80, 6: 96, 9: 128}
    Map_bad1m = {2: 24, 4: 120}
    Map_bad2m = {2: 9, 4: 80, 6: 96, 9: 128, 12: 42}
    Map_bad3m = {2: 'four', 4: 120, 6: 240}
    Map_bad4m = {'two': 24, 4: 120, 6: 240}
    Map_bad5m = [24, 120, 240]

    Rec1m = [24, 120, 240]                          # Encoded values Record (minimized) and API+encoded Array values
    Rec2m = [50, None, 100]
    Rec3m = [9, 80, 96, 128]
    Rec_bad1m = [24, 120]
    Rec_bad2m = [9, 80, 96, 128, 42]
    Rec_bad3m = ['four', 120, 240]

    Rec1n = {1: 24, 2: 120, 3: 240}                  # Encoded values Record (unused dict/tag mode)
    Rec2n = {1: 50, 3: 100}
    Rec3n = {1: 9, 2: 80, 3: 96, 4: 128}
    Rec_bad1n = {1: 24, 2: 120}
    Rec_bad2n = {1: 9, 2: 80, 3: 96, 4: 128, 5: 42}
    Rec_bad3n = {1: 'four', 2: 120, 3: 240}
    Rec_bad4n = {'one': 24, 2: 120, 3: 240}

    RGB1c = [24, 120, 240]                           # Encoded values Record (concise)
    RGB2c = [50, None, 100]
    RGB3c = [9, 80, 96, 128]
    RGB_bad1c = [24, 120]
    RGB_bad2c = [9, 80, 96, 128, 42]
    RGB_bad3c = ['four', 120, 240]

    def test_map_min(self):             # dict structure, identifier tag
        self.assertDictEqual(self.tc.encode('t_map_rgba', self.RGB1), self.Map1m)
        self.assertDictEqual(self.tc.decode('t_map_rgba', self.Map1m), self.RGB1)
        self.assertDictEqual(self.tc.decode('t_map_rgba', _j(self.Map1m)), self.RGB1)
        self.assertDictEqual(self.tc.encode('t_map_rgba', self.RGB2), self.Map2m)
        self.assertDictEqual(self.tc.decode('t_map_rgba', self.Map2m), self.RGB2)
        self.assertDictEqual(self.tc.decode('t_map_rgba', _j(self.Map2m)), self.RGB2)
        self.assertDictEqual(self.tc.encode('t_map_rgba', self.RGB3), self.Map3m)
        self.assertDictEqual(self.tc.decode('t_map_rgba', self.Map3m), self.RGB3)
        self.assertDictEqual(self.tc.decode('t_map_rgba', _j(self.Map3m)), self.RGB3)
        with self.assertRaises(ValueError):
            self.tc.encode('t_map_rgba', self.RGB_bad1a)
        with self.assertRaises(ValueError):
            self.tc.encode('t_map_rgba', self.RGB_bad2a)
        with self.assertRaises(ValueError):
            self.tc.encode('t_map_rgba', self.RGB_bad3a)
        with self.assertRaises(TypeError):
            self.tc.encode('t_map_rgba', self.RGB_bad4a)
        with self.assertRaises(TypeError):
            self.tc.encode('t_map_rgba', self.RGB_bad5a)
        with self.assertRaises(ValueError):
            self.tc.encode('t_map_rgba', self.RGB_bad6a)
        with self.assertRaises(ValueError):
            self.tc.encode('t_map_rgba', self.RGB_bad7a)
        with self.assertRaises(ValueError):
            self.tc.decode('t_map_rgba', self.Map_bad1m)
        with self.assertRaises(ValueError):
            self.tc.decode('t_map_rgba', self.Map_bad2m)
        with self.assertRaises(TypeError):
            self.tc.decode('t_map_rgba', self.Map_bad3m)
        with self.assertRaises(ValueError):
            self.tc.decode('t_map_rgba', self.Map_bad4m)
        with self.assertRaises(TypeError):
            self.tc.decode('t_map_rgba', self.Map_bad5m)

    def test_map_unused(self):         # dict structure, identifier tag
        self.tc.set_mode(True, False)
        self.assertDictEqual(self.tc.encode('t_map_rgba', self.RGB1), self.Map1m)
        self.assertDictEqual(self.tc.decode('t_map_rgba', self.Map1m), self.RGB1)
        self.assertDictEqual(self.tc.decode('t_map_rgba', _j(self.Map1m)), self.RGB1)
        self.assertDictEqual(self.tc.encode('t_map_rgba', self.RGB2), self.Map2m)
        self.assertDictEqual(self.tc.decode('t_map_rgba', self.Map2m), self.RGB2)
        self.assertDictEqual(self.tc.decode('t_map_rgba', _j(self.Map2m)), self.RGB2)
        self.assertDictEqual(self.tc.encode('t_map_rgba', self.RGB3), self.Map3m)
        self.assertDictEqual(self.tc.decode('t_map_rgba', self.Map3m), self.RGB3)
        self.assertDictEqual(self.tc.decode('t_map_rgba', _j(self.Map3m)), self.RGB3)
        with self.assertRaises(ValueError):
            self.tc.encode('t_map_rgba', self.RGB_bad1a)
        with self.assertRaises(ValueError):
            self.tc.encode('t_map_rgba', self.RGB_bad2a)
        with self.assertRaises(ValueError):
            self.tc.encode('t_map_rgba', self.RGB_bad3a)
        with self.assertRaises(TypeError):
            self.tc.encode('t_map_rgba', self.RGB_bad4a)
        with self.assertRaises(TypeError):
            self.tc.encode('t_map_rgba', self.RGB_bad5a)
        with self.assertRaises(ValueError):
            self.tc.encode('t_map_rgba', self.RGB_bad6a)
        with self.assertRaises(ValueError):
            self.tc.encode('t_map_rgba', self.RGB_bad7a)
        with self.assertRaises(ValueError):
            self.tc.decode('t_map_rgba', self.Map_bad1m)
        with self.assertRaises(ValueError):
            self.tc.decode('t_map_rgba', self.Map_bad2m)
        with self.assertRaises(TypeError):
            self.tc.decode('t_map_rgba', self.Map_bad3m)
        with self.assertRaises(ValueError):
            self.tc.decode('t_map_rgba', self.Map_bad4m)
        with self.assertRaises(ValueError):
            self.tc.decode('t_map_rgba', _j(self.Map_bad4m))

    def test_map_concise(self):         # dict structure, identifier name
        self.tc.set_mode(False, True)
        self.assertDictEqual(self.tc.encode('t_map_rgba', self.RGB1), self.RGB1)
        self.assertDictEqual(self.tc.decode('t_map_rgba', self.RGB1), self.RGB1)
        self.assertDictEqual(self.tc.encode('t_map_rgba', self.RGB2), self.RGB2)
        self.assertDictEqual(self.tc.decode('t_map_rgba', self.RGB2), self.RGB2)
        self.assertDictEqual(self.tc.encode('t_map_rgba', self.RGB3), self.RGB3)
        self.assertDictEqual(self.tc.decode('t_map_rgba', self.RGB3), self.RGB3)
        with self.assertRaises(ValueError):
            self.tc.decode('t_map_rgba', self.RGB_bad1a)
        with self.assertRaises(ValueError):
            self.tc.decode('t_map_rgba', self.RGB_bad2a)
        with self.assertRaises(ValueError):
            self.tc.decode('t_map_rgba', self.RGB_bad3a)
        with self.assertRaises(TypeError):
            self.tc.decode('t_map_rgba', self.RGB_bad4a)
        with self.assertRaises(TypeError):
            self.tc.decode('t_map_rgba', self.RGB_bad5a)
        with self.assertRaises(ValueError):
            self.tc.decode('t_map_rgba', self.RGB_bad6a)
        with self.assertRaises(ValueError):
            self.tc.decode('t_map_rgba', self.RGB_bad7a)
        with self.assertRaises(ValueError):
            self.tc.encode('t_map_rgba', self.RGB_bad1a)
        with self.assertRaises(ValueError):
            self.tc.encode('t_map_rgba', self.RGB_bad2a)
        with self.assertRaises(ValueError):
            self.tc.encode('t_map_rgba', self.RGB_bad3a)
        with self.assertRaises(TypeError):
            self.tc.encode('t_map_rgba', self.RGB_bad4a)
        with self.assertRaises(TypeError):
            self.tc.encode('t_map_rgba', self.RGB_bad5a)
        with self.assertRaises(ValueError):
            self.tc.encode('t_map_rgba', self.RGB_bad6a)
        with self.assertRaises(ValueError):
            self.tc.encode('t_map_rgba', self.RGB_bad7a)

    def test_map_verbose(self):     # dict structure, identifier name
        self.tc.set_mode(True, True)
        self.assertDictEqual(self.tc.encode('t_map_rgba', self.RGB1), self.RGB1)
        self.assertDictEqual(self.tc.decode('t_map_rgba', self.RGB1), self.RGB1)
        self.assertDictEqual(self.tc.encode('t_map_rgba', self.RGB2), self.RGB2)
        self.assertDictEqual(self.tc.decode('t_map_rgba', self.RGB2), self.RGB2)
        self.assertDictEqual(self.tc.encode('t_map_rgba', self.RGB3), self.RGB3)
        self.assertDictEqual(self.tc.decode('t_map_rgba', self.RGB3), self.RGB3)
        with self.assertRaises(ValueError):
            self.tc.encode('t_map_rgba', self.RGB_bad1a)
        with self.assertRaises(ValueError):
            self.tc.encode('t_map_rgba', self.RGB_bad2a)
        with self.assertRaises(ValueError):
            self.tc.encode('t_map_rgba', self.RGB_bad3a)
        with self.assertRaises(TypeError):
            self.tc.encode('t_map_rgba', self.RGB_bad4a)
        with self.assertRaises(TypeError):
            self.tc.encode('t_map_rgba', self.RGB_bad5a)
        with self.assertRaises(ValueError):
            self.tc.encode('t_map_rgba', self.RGB_bad6a)
        with self.assertRaises(ValueError):
            self.tc.encode('t_map_rgba', self.RGB_bad7a)
        with self.assertRaises(ValueError):
            self.tc.encode('t_map_rgba', self.RGB_bad8a)
        with self.assertRaises(ValueError):
            self.tc.decode('t_map_rgba', self.RGB_bad1a)
        with self.assertRaises(ValueError):
            self.tc.decode('t_map_rgba', self.RGB_bad2a)
        with self.assertRaises(ValueError):
            self.tc.decode('t_map_rgba', self.RGB_bad3a)
        with self.assertRaises(TypeError):
            self.tc.decode('t_map_rgba', self.RGB_bad4a)
        with self.assertRaises(TypeError):
            self.tc.decode('t_map_rgba', self.RGB_bad5a)
        with self.assertRaises(ValueError):
            self.tc.decode('t_map_rgba', self.RGB_bad6a)
        with self.assertRaises(ValueError):
            self.tc.decode('t_map_rgba', self.RGB_bad7a)
        with self.assertRaises(ValueError):
            self.tc.decode('t_map_rgba', self.RGB_bad8a)

    def test_record_min(self):
        self.assertListEqual(self.tc.encode('t_rec_rgba', self.RGB1), self.Rec1m)
        self.assertDictEqual(self.tc.decode('t_rec_rgba', self.Rec1m), self.RGB1)
        self.assertListEqual(self.tc.encode('t_rec_rgba', self.RGB2), self.Rec2m)
        self.assertDictEqual(self.tc.decode('t_rec_rgba', self.Rec2m), self.RGB2)
        self.assertListEqual(self.tc.encode('t_rec_rgba', self.RGB3), self.Rec3m)
        self.assertDictEqual(self.tc.decode('t_rec_rgba', self.Rec3m), self.RGB3)
        with self.assertRaises(ValueError):
            self.tc.encode('t_rec_rgba', self.RGB_bad1a)
        with self.assertRaises(ValueError):
            self.tc.encode('t_rec_rgba', self.RGB_bad2a)
        with self.assertRaises(ValueError):
            self.tc.encode('t_rec_rgba', self.RGB_bad3a)
        with self.assertRaises(TypeError):
            self.tc.encode('t_rec_rgba', self.RGB_bad4a)
        with self.assertRaises(TypeError):
            self.tc.encode('t_rec_rgba', self.RGB_bad5a)
        with self.assertRaises(ValueError):
            self.tc.encode('t_rec_rgba', self.RGB_bad6a)
        with self.assertRaises(ValueError):
            self.tc.encode('t_rec_rgba', self.RGB_bad7a)
        with self.assertRaises(ValueError):
            self.tc.decode('t_rec_rgba', self.Rec_bad1m)
        with self.assertRaises(ValueError):
            self.tc.decode('t_rec_rgba', self.Rec_bad2m)
        with self.assertRaises(TypeError):
            self.tc.decode('t_rec_rgba', self.Rec_bad3m)

    def test_record_unused(self):
        self.tc.set_mode(True, False)
        self.assertDictEqual(self.tc.encode('t_rec_rgba', self.RGB1), self.Rec1n)
        self.assertDictEqual(self.tc.decode('t_rec_rgba', self.Rec1n), self.RGB1)
        self.assertDictEqual(self.tc.decode('t_rec_rgba', _j(self.Rec1n)), self.RGB1)
        self.assertDictEqual(self.tc.encode('t_rec_rgba', self.RGB2), self.Rec2n)
        self.assertDictEqual(self.tc.decode('t_rec_rgba', self.Rec2n), self.RGB2)
        self.assertDictEqual(self.tc.decode('t_rec_rgba', _j(self.Rec2n)), self.RGB2)
        self.assertDictEqual(self.tc.encode('t_rec_rgba', self.RGB3), self.Rec3n)
        self.assertDictEqual(self.tc.decode('t_rec_rgba', self.Rec3n), self.RGB3)
        self.assertDictEqual(self.tc.decode('t_rec_rgba', _j(self.Rec3n)), self.RGB3)
        with self.assertRaises(ValueError):
            self.tc.encode('t_rec_rgba', self.RGB_bad1a)
        with self.assertRaises(ValueError):
            self.tc.encode('t_rec_rgba', self.RGB_bad2a)
        with self.assertRaises(ValueError):
            self.tc.encode('t_rec_rgba', self.RGB_bad3a)
        with self.assertRaises(TypeError):
            self.tc.encode('t_rec_rgba', self.RGB_bad4a)
        with self.assertRaises(TypeError):
            self.tc.encode('t_rec_rgba', self.RGB_bad5a)
        with self.assertRaises(ValueError):
            self.tc.encode('t_rec_rgba', self.RGB_bad6a)
        with self.assertRaises(ValueError):
            self.tc.encode('t_rec_rgba', self.RGB_bad7a)
        with self.assertRaises(ValueError):
            self.tc.decode('t_rec_rgba', self.Rec_bad1n)
        with self.assertRaises(ValueError):
            self.tc.decode('t_rec_rgba', self.Rec_bad2n)
        with self.assertRaises(TypeError):
            self.tc.decode('t_rec_rgba', self.Rec_bad3n)
        with self.assertRaises(ValueError):
            self.tc.decode('t_rec_rgba', self.Rec_bad4n)

    def test_record_concise(self):
        self.tc.set_mode(False, True)
        self.assertListEqual(self.tc.encode('t_rec_rgba', self.RGB1), self.RGB1c)
        self.assertDictEqual(self.tc.decode('t_rec_rgba', self.RGB1c), self.RGB1)
        self.assertListEqual(self.tc.encode('t_rec_rgba', self.RGB2), self.RGB2c)
        self.assertDictEqual(self.tc.decode('t_rec_rgba', self.RGB2c), self.RGB2)
        self.assertListEqual(self.tc.encode('t_rec_rgba', self.RGB3), self.RGB3c)
        self.assertDictEqual(self.tc.decode('t_rec_rgba', self.RGB3c), self.RGB3)
        with self.assertRaises(ValueError):
            self.tc.encode('t_rec_rgba', self.RGB_bad1a)
        with self.assertRaises(ValueError):
            self.tc.encode('t_rec_rgba', self.RGB_bad2a)
        with self.assertRaises(ValueError):
            self.tc.encode('t_rec_rgba', self.RGB_bad3a)
        with self.assertRaises(TypeError):
            self.tc.encode('t_rec_rgba', self.RGB_bad4a)
        with self.assertRaises(TypeError):
            self.tc.encode('t_rec_rgba', self.RGB_bad5a)
        with self.assertRaises(ValueError):
            self.tc.encode('t_rec_rgba', self.RGB_bad6a)
        with self.assertRaises(ValueError):
            self.tc.encode('t_rec_rgba', self.RGB_bad7a)
        with self.assertRaises(ValueError):
            self.tc.decode('t_rec_rgba', self.RGB_bad1c)
        with self.assertRaises(ValueError):
            self.tc.decode('t_rec_rgba', self.RGB_bad2c)
        with self.assertRaises(TypeError):
            self.tc.decode('t_rec_rgba', self.RGB_bad3c)

    def test_record_verbose(self):
        self.tc.set_mode(True, True)
        self.assertDictEqual(self.tc.encode('t_rec_rgba', self.RGB1), self.RGB1)
        self.assertDictEqual(self.tc.decode('t_rec_rgba', self.RGB1), self.RGB1)
        self.assertDictEqual(self.tc.encode('t_rec_rgba', self.RGB2), self.RGB2)
        self.assertDictEqual(self.tc.decode('t_rec_rgba', self.RGB2), self.RGB2)
        self.assertDictEqual(self.tc.encode('t_rec_rgba', self.RGB3), self.RGB3)
        self.assertDictEqual(self.tc.decode('t_rec_rgba', self.RGB3), self.RGB3)
        with self.assertRaises(ValueError):
            self.tc.encode('t_rec_rgba', self.RGB_bad1a)
        with self.assertRaises(ValueError):
            self.tc.encode('t_rec_rgba', self.RGB_bad2a)
        with self.assertRaises(ValueError):
            self.tc.encode('t_rec_rgba', self.RGB_bad3a)
        with self.assertRaises(TypeError):
            self.tc.encode('t_rec_rgba', self.RGB_bad4a)
        with self.assertRaises(TypeError):
            self.tc.encode('t_rec_rgba', self.RGB_bad5a)
        with self.assertRaises(ValueError):
            self.tc.encode('t_rec_rgba', self.RGB_bad6a)
        with self.assertRaises(ValueError):
            self.tc.encode('t_rec_rgba', self.RGB_bad7a)
        with self.assertRaises(ValueError):
            self.tc.encode('t_rec_rgba', self.RGB_bad8a)
        with self.assertRaises(ValueError):
            self.tc.decode('t_rec_rgba', self.RGB_bad1a)
        with self.assertRaises(ValueError):
            self.tc.decode('t_rec_rgba', self.RGB_bad2a)
        with self.assertRaises(ValueError):
            self.tc.decode('t_rec_rgba', self.RGB_bad3a)
        with self.assertRaises(TypeError):
            self.tc.decode('t_rec_rgba', self.RGB_bad4a)
        with self.assertRaises(TypeError):
            self.tc.decode('t_rec_rgba', self.RGB_bad5a)
        with self.assertRaises(ValueError):
            self.tc.decode('t_rec_rgba', self.RGB_bad6a)
        with self.assertRaises(ValueError):
            self.tc.decode('t_rec_rgba', self.RGB_bad7a)
        with self.assertRaises(ValueError):
            self.tc.decode('t_rec_rgba', self.RGB_bad8a)

    Arr1 = [True, 3, 2.71828, 'Red']
    Arr2 = [None, 3, 2]
    Arr3 = [True, 3, 2, 'Red', [1, 'Blue'], [2, 3]]
    Arr4 = [True, 3, 2.71828, None, [1, 'Blue'], [2, 3]]
    Arr_bad1 = [True, 3, None, 'Red']
    Arr_bad2 = [True, 3, False, 'Red']
    Arr_bad3 = [True, 3, 2.71828, 'Red', []]            # Optional arrays are omitted, not empty
    Arr_bad4 = [True, 3, 2.71828, 'Red', None, []]

    def test_array(self):

        def ta():
            self.assertListEqual(self.tc.encode('t_array', self.Arr1), self.Arr1)
            self.assertListEqual(self.tc.decode('t_array', self.Arr1), self.Arr1)
            self.assertListEqual(self.tc.encode('t_array', self.Arr2), self.Arr2)
            self.assertListEqual(self.tc.decode('t_array', self.Arr2), self.Arr2)
            self.assertListEqual(self.tc.encode('t_array', self.Arr3), self.Arr3)
            self.assertListEqual(self.tc.decode('t_array', self.Arr3), self.Arr3)
            self.assertListEqual(self.tc.encode('t_array', self.Arr4), self.Arr4)
            self.assertListEqual(self.tc.decode('t_array', self.Arr4), self.Arr4)
            with self.assertRaises(ValueError):
                self.tc.encode('t_array', self.Arr_bad1)
            with self.assertRaises(ValueError):
                self.tc.decode('t_array', self.Arr_bad1)
            with self.assertRaises(TypeError):
                self.tc.encode('t_array', self.Arr_bad2)
            with self.assertRaises(TypeError):
                self.tc.decode('t_array', self.Arr_bad2)
            with self.assertRaises(ValueError):
                self.tc.encode('t_array', self.Arr_bad3)
            with self.assertRaises(ValueError):
                self.tc.decode('t_array', self.Arr_bad3)
            with self.assertRaises(ValueError):
                self.tc.encode('t_array', self.Arr_bad4)
            with self.assertRaises(ValueError):
                self.tc.decode('t_array', self.Arr_bad4)

            self.assertListEqual(self.tc.encode('t_arr_rgba', self.Rec1m), self.Rec1m)
            self.assertListEqual(self.tc.decode('t_arr_rgba', self.Rec1m), self.Rec1m)
            self.assertListEqual(self.tc.encode('t_arr_rgba', self.Rec2m), self.Rec2m)
            self.assertListEqual(self.tc.decode('t_arr_rgba', self.Rec2m), self.Rec2m)
            self.assertListEqual(self.tc.encode('t_arr_rgba', self.Rec3m), self.Rec3m)
            self.assertListEqual(self.tc.decode('t_arr_rgba', self.Rec3m), self.Rec3m)
            with self.assertRaises(ValueError):
                self.tc.encode('t_arr_rgba', self.Rec_bad1m)
            with self.assertRaises(ValueError):
                self.tc.decode('t_arr_rgba', self.Rec_bad1m)
            with self.assertRaises(ValueError):
                self.tc.encode('t_arr_rgba', self.Rec_bad2m)
            with self.assertRaises(ValueError):
                self.tc.decode('t_arr_rgba', self.Rec_bad2m)
            with self.assertRaises(TypeError):
                self.tc.encode('t_arr_rgba', self.Rec_bad3m)
            with self.assertRaises(TypeError):
                self.tc.decode('t_arr_rgba', self.Rec_bad3m)

        # Ensure that mode has no effect on array serialization

        self.tc.set_mode(False, False)
        ta()
        self.tc.set_mode(False, True)
        ta()
        self.tc.set_mode(True, False)
        ta()
        self.tc.set_mode(True, True)
        ta()


schema_compound = {
    'meta': {'module': 'unittests-Compound'},
    'types': [
        ['t_choice', 'Choice', [], '', [
            [10, 'rec', 't_crec', [], ''],
            [11, 'map', 't_cmap', [], ''],
            [12, 'array', 't_carray', [], ''],
            [13, 'choice', 't_cchoice', [], '']
        ]],
        ['t_crec', 'Record', [], '', [
            [1, 'a', 'Integer', [], ''],
            [2, 'b', 'String', [], '']
        ]],
        ['t_cmap', 'Map', [], '', [
            [4, 'c', 'Integer', [], ''],
            [6, 'd', 'String', [], '']
        ]],
        ['t_carray', 'Array', [], '', [
            [1, 'e', 'Integer', [], ''],
            [2, 'f', 'String', [], '']
        ]],
        ['t_cchoice', 'Choice', [], '', [
            [7, 'g', 'Integer', [], ''],
            [8, 'h', 'String', [], '']
        ]],
    ]}


class Compound(unittest.TestCase):      # TODO: arrayOf(rec,map,array,arrayof,choice), array(), map(), rec()

    def setUp(self):
        jadn_check(schema_compound)
        self.tc = Codec(schema_compound)

    C4a = {'rec': {'a': 1, 'b': 'c'}}
    C4m = {10: [1, 'c']}

    def test_choice_rec_verbose(self):
        self.tc.set_mode(True, True)
        self.assertEqual(self.tc.decode('t_choice', self.C4a), self.C4a)
        self.assertEqual(self.tc.encode('t_choice', self.C4a), self.C4a)

    def test_choice_rec_min(self):
        self.tc.set_mode(False, False)
        self.assertEqual(self.tc.decode('t_choice', self.C4m), self.C4a)
        self.assertEqual(self.tc.encode('t_choice', self.C4a), self.C4m)


schema_selectors = {                # JADN schema for selector tests
    'meta': {'module': 'unittests-Selectors'},
    'types': [
        ['t_attr_arr_tag', 'Array', [], '', [
            [1, 'type', 'Enumerated', ['*Menu_tag'], ''],
            [2, 'value', 'Menu_tag', ['&1'], '']
        ]],
        ['t_attr_arr_tags', 'Array', [], '', [
            [1, 'type', 'Enumerated', ['*Menu_tag'], ''],
            [2, 'value', 'Menu_tag', ['&1', ']0'], '']
        ]],
        ['t_attr_arr_name', 'Array', [], '', [
            [1, 'type', 'Enumerated', ['*Menu_name'], ''],
            [2, 'value', 'Menu_name', ['&1'], '']
        ]],
        ['t_attr_arr_names', 'Array', [], '', [
            [1, 'type', 'Enumerated', ['*Menu_name'], ''],
            [2, 'values', 'Menu_name', ['&1', ']0'], '']
        ]],
        ['t_attr_rec_tag', 'Record', [], '', [
            [1, 'type', 'Enumerated', ['*Menu_tag'], ''],
            [2, '*', 'Menu_tag', ['&type'], '']
        ]],
        ['t_attr_rec_name', 'Record', [], '', [
            [1, 'type', 'Enumerated', ['*Menu_name'], ''],
            [2, 'value', 'Menu_name', ['&type'], '']
        ]],
        ['t_property_implicit_primitive', 'Record', [], '', [
            [1, 'foo', 'String', [], ''],
            [2, '<', 'Primitive', [], '']
        ]],
        ['t_property_explicit_primitive', 'Record', [], '', [
            [1, 'foo', 'String', [], ''],
            [2, 'data', 'Primitive', [], '']
        ]],
        ['t_property_implicit_category', 'Record', [], '', [
            [1, 'foo', 'String', [], ''],
            [2, '<', 'Category', [], '']
        ]],
        ['t_property_explicit_category', 'Record', [], '', [
            [1, 'foo', 'String', [], ''],
            [2, 'data', 'Category', [], '']
        ]],
        ['Menu_tag', 'Choice', ['='], '', [
            [9, 'name', 'String', [], ''],
            [4, 'flag', 'Boolean', [], ''],
            [7, 'count', 'Integer', [], ''],
            [6, 'color', 'Colors', [], ''],
            [5, 'animal', 'Animals', [], '']
        ]],
        ['Menu_name', 'Choice', [], '', [
            [9, 'name', 'String', [], ''],
            [4, 'flag', 'Boolean', [], ''],
            [7, 'count', 'Integer', [], ''],
            [6, 'color', 'Colors', [], ''],
            [5, 'animal', 'Animals', [], '']
        ]],
        ['Primitive', 'Choice', [], '', [
            [1, 'name', 'String', [], ''],
            [4, 'flag', 'Boolean', [], ''],
            [7, 'count', 'Integer', [], '']
        ]],
        ['Category', 'Choice', [], '', [
            [2, 'animal', 'Animals', [], ''],
            [6, 'color', 'Colors', [], '']
        ]],
        ['Animals', 'Map', [], '', [
            [3, 'cat', 'String', ['[0'], ''],
            [4, 'dog', 'Integer', ['[0'], ''],
            [5, 'rat', 'Rattrs', ['[0'], '']
        ]],
        ['Colors', 'Enumerated', [], '', [
            [2, 'red', ''],
            [3, 'green', ''],
            [4, 'blue', '']
        ]],
        ['Rattrs', 'Record', [], '', [
            [1, 'length', 'Integer', [], ''],
            [2, 'weight', 'Number', [], '']
        ]]
    ]}


class Selectors(unittest.TestCase):         # TODO: bad schema - verify * field has only Choice type
                                            # TODO: add test cases to decode multiple values for Choice (bad)
    def setUp(self):
        jadn_check(schema_selectors)
        self.tc = Codec(schema_selectors)

    arr_name1_api = ['count', 17]
    arr_name2_api = ['color', 'green']
    arr_name3_api = ['animal', {'cat': 'Fluffy'}]
    arr_name4_bad_api = ['name', 17]        # name is type String, not Integer
    arr_name5_bad_api = ['universe', 17]    # universe is not a defined type
    arr_names1_api = ['count', [13, 17]]    # array of values of the specified type

    arr_tag1_api = [7, 17]                  # enumerated tag values are integers
    arr_tag2_api = [6, 'green']
    arr_tag3_api = [5, {'cat': 'Fluffy'}]
    arr_tag4_bad_api = [9, 17]              # name is type String, not Integer
    arr_tag5_bad_api = [2, 17]              # 2 is not a defined type
    arr_tags1_api = [7, [13, 17]]           # array of values of the specified type

    arr_name1_min = [7, 17]                 # Enumerated type with 'compact' option always uses min encoding (tag)
    arr_name2_min = [6, 3]
    arr_name3_min = [5, {3: 'Fluffy'}]      # min encoding of map (serialized keys are strings)
    arr_name4_bad_min = [9, 17]
    arr_name5_bad_min = [2, 17]

    arr_tag1_min = arr_name1_min
    arr_tag2_min = arr_name2_min
    arr_tag3_min = arr_name3_min
    arr_tag4_bad_min = arr_name4_bad_min
    arr_tag5_bad_min = arr_name5_bad_min

    def test_attr_arr_name_verbose(self):
        self.tc.set_mode(True, True)
        self.assertListEqual(self.tc.encode('t_attr_arr_name', self.arr_name1_api), self.arr_name1_api)
        self.assertListEqual(self.tc.decode('t_attr_arr_name', self.arr_name1_api), self.arr_name1_api)
        self.assertListEqual(self.tc.encode('t_attr_arr_name', self.arr_name2_api), self.arr_name2_api)
        self.assertListEqual(self.tc.decode('t_attr_arr_name', self.arr_name2_api), self.arr_name2_api)
        self.assertListEqual(self.tc.encode('t_attr_arr_name', self.arr_name3_api), self.arr_name3_api)
        self.assertListEqual(self.tc.decode('t_attr_arr_name', self.arr_name3_api), self.arr_name3_api)
        with self.assertRaises(TypeError):
            self.tc.encode('t_attr_arr_name', self.arr_name4_bad_api)
        with self.assertRaises(TypeError):
            self.tc.decode('t_attr_arr_name', self.arr_name4_bad_api)
        with self.assertRaises(ValueError):
            self.tc.encode('t_attr_arr_name', self.arr_name5_bad_api)
        with self.assertRaises(ValueError):
            self.tc.decode('t_attr_arr_name', self.arr_name5_bad_api)

    def test_attr_arrays_verbose(self):
        self.tc.set_mode(True, True)
        self.assertListEqual(self.tc.encode('t_attr_arr_names', self.arr_names1_api), self.arr_names1_api)
        self.assertListEqual(self.tc.decode('t_attr_arr_names', self.arr_names1_api), self.arr_names1_api)
        self.assertListEqual(self.tc.encode('t_attr_arr_tags', self.arr_tags1_api), self.arr_tags1_api)
        self.assertListEqual(self.tc.decode('t_attr_arr_tags', self.arr_tags1_api), self.arr_tags1_api)

    def test_attr_arr_tag_verbose(self):
        self.tc.set_mode(True, True)
        self.assertListEqual(self.tc.encode('t_attr_arr_tag', self.arr_tag1_api), self.arr_tag1_api)
        self.assertListEqual(self.tc.decode('t_attr_arr_tag', self.arr_tag1_api), self.arr_tag1_api)
        self.assertListEqual(self.tc.encode('t_attr_arr_tag', self.arr_tag2_api), self.arr_tag2_api)
        self.assertListEqual(self.tc.decode('t_attr_arr_tag', self.arr_tag2_api), self.arr_tag2_api)
        self.assertListEqual(self.tc.encode('t_attr_arr_tag', self.arr_tag3_api), self.arr_tag3_api)
        self.assertListEqual(self.tc.decode('t_attr_arr_tag', self.arr_tag3_api), self.arr_tag3_api)
        with self.assertRaises(TypeError):
            self.tc.encode('t_attr_arr_tag', self.arr_tag4_bad_api)
        with self.assertRaises(TypeError):
            self.tc.decode('t_attr_arr_tag', self.arr_tag4_bad_api)
        with self.assertRaises(ValueError):
            self.tc.encode('t_attr_arr_tag', self.arr_tag5_bad_api)
        with self.assertRaises(ValueError):
            self.tc.decode('t_attr_arr_tag', self.arr_tag5_bad_api)

    def test_attr_arr_name_min(self):
        self.tc.set_mode(False, False)
        self.assertListEqual(self.tc.encode('t_attr_arr_name', self.arr_name1_api), self.arr_name1_min)
        self.assertListEqual(self.tc.decode('t_attr_arr_name', self.arr_name1_min), self.arr_name1_api)
        self.assertListEqual(self.tc.encode('t_attr_arr_name', self.arr_name2_api), self.arr_name2_min)
        self.assertListEqual(self.tc.decode('t_attr_arr_name', self.arr_name2_min), self.arr_name2_api)
        self.assertListEqual(self.tc.encode('t_attr_arr_name', self.arr_name3_api), self.arr_name3_min)
        self.assertListEqual(self.tc.decode('t_attr_arr_name', self.arr_name3_min), self.arr_name3_api)
        with self.assertRaises(TypeError):
            self.tc.encode('t_attr_arr_name', self.arr_name4_bad_api)
        with self.assertRaises(TypeError):
            self.tc.decode('t_attr_arr_name', self.arr_name4_bad_min)
        with self.assertRaises(ValueError):
            self.tc.encode('t_attr_arr_name', self.arr_name5_bad_api)
        with self.assertRaises(ValueError):
            self.tc.decode('t_attr_arr_name', self.arr_name5_bad_min)

    def test_attr_arr_tag_min(self):
        self.tc.set_mode(False, False)
        self.assertListEqual(self.tc.encode('t_attr_arr_tag', self.arr_tag1_api), self.arr_tag1_min)
        self.assertListEqual(self.tc.decode('t_attr_arr_tag', self.arr_tag1_min), self.arr_tag1_api)
        self.assertListEqual(self.tc.encode('t_attr_arr_tag', self.arr_tag2_api), self.arr_tag2_min)
        self.assertListEqual(self.tc.decode('t_attr_arr_tag', self.arr_tag2_min), self.arr_tag2_api)
        self.assertListEqual(self.tc.encode('t_attr_arr_tag', self.arr_tag3_api), self.arr_tag3_min)
        self.assertListEqual(self.tc.decode('t_attr_arr_tag', self.arr_tag3_min), self.arr_tag3_api)
        with self.assertRaises(TypeError):
            self.tc.encode('t_attr_arr_tag', self.arr_tag4_bad_api)
        with self.assertRaises(TypeError):
            self.tc.decode('t_attr_arr_tag', self.arr_tag4_bad_min)
        with self.assertRaises(ValueError):
            self.tc.encode('t_attr_arr_tag', self.arr_tag5_bad_api)
        with self.assertRaises(ValueError):
            self.tc.decode('t_attr_arr_tag', self.arr_tag5_bad_min)

    rec_name1_api = {'type': 'count', 'value': 17}
    rec_name2_api = {'type': 'color', 'value': 'green'}
    rec_name3_api = {'type': 'animal', 'value': {'cat': 'Fluffy'}}
    rec_name4_bad_api = {'type': 'name', 'value': 17}
    rec_name5_bad_api = {'type': 'universe', 'value': 'Fred'}

    rec_name1_min = arr_name1_min
    rec_name2_min = arr_name2_min
    rec_name3_min = arr_name3_min
    rec_name4_bad_min = arr_name4_bad_min
    rec_name5_bad_min = arr_name5_bad_min

    """
    rec_name1_min = ['Integer', 17]
    rec_name2_min = ['Primitive', {'7': 17}]
    rec_name3_min = ['Category', {'2': {'5': [21, 0.342]}}]
    rec_name4_bad_min = ['Vegetable', {'7': 17}]
    rec_name5_bad_min = ['Category', {'2': {'9': 10}}]
    """

    def test_attr_rec_name_verbose(self):
        self.tc.set_mode(True, True)
        self.assertDictEqual(self.tc.encode('t_attr_rec_name', self.rec_name1_api), self.rec_name1_api)
        self.assertDictEqual(self.tc.decode('t_attr_rec_name', self.rec_name1_api), self.rec_name1_api)
        self.assertDictEqual(self.tc.encode('t_attr_rec_name', self.rec_name2_api), self.rec_name2_api)
        self.assertDictEqual(self.tc.decode('t_attr_rec_name', self.rec_name2_api), self.rec_name2_api)
        self.assertDictEqual(self.tc.encode('t_attr_rec_name', self.rec_name3_api), self.rec_name3_api)
        self.assertDictEqual(self.tc.decode('t_attr_rec_name', self.rec_name3_api), self.rec_name3_api)
        with self.assertRaises(TypeError):
            self.tc.encode('t_attr_rec_name', self.rec_name4_bad_api)
        with self.assertRaises(TypeError):
            self.tc.decode('t_attr_rec_name', self.rec_name4_bad_api)
        with self.assertRaises(ValueError):
            self.tc.encode('t_attr_rec_name', self.rec_name5_bad_api)
        with self.assertRaises(ValueError):
            self.tc.decode('t_attr_rec_name', self.rec_name5_bad_api)

    def test_attr_rec_name_min(self):
        self.tc.set_mode(False, False)
        self.assertListEqual(self.tc.encode('t_attr_rec_name', self.rec_name1_api), self.rec_name1_min)
        self.assertDictEqual(self.tc.decode('t_attr_rec_name', self.rec_name1_min), self.rec_name1_api)
        self.assertListEqual(self.tc.encode('t_attr_rec_name', self.rec_name2_api), self.rec_name2_min)
        self.assertDictEqual(self.tc.decode('t_attr_rec_name', self.rec_name2_min), self.rec_name2_api)
        self.assertListEqual(self.tc.encode('t_attr_rec_name', self.rec_name3_api), self.rec_name3_min)
        self.assertDictEqual(self.tc.decode('t_attr_rec_name', self.rec_name3_min), self.rec_name3_api)
        with self.assertRaises(TypeError):
            self.tc.encode('t_attr_rec_name', self.rec_name4_bad_api)
        with self.assertRaises(TypeError):
            self.tc.decode('t_attr_rec_name', self.rec_name4_bad_min)
        with self.assertRaises(ValueError):
            self.tc.encode('t_attr_rec_name', self.rec_name5_bad_api)
        with self.assertRaises(ValueError):
            self.tc.decode('t_attr_rec_name', self.rec_name5_bad_min)

    attr1i_api = {'type': 'Integer', 'value': 17}
    attr2i_api = {'type': 'Primitive', 'value': {'count': 17}}
    attr3i_api = {'type': 'Category', 'value': {'animal': {'rat': {'length': 21, 'weight': .342}}}}
    attr4i_bad_api = {'type': 'Vegetable', 'value': 'turnip'}
    attr5i_bad_api = {'type': 'Category', 'value': {'animal': {'fish': 10}}}

    def test_attr_rec_implicit_verbose(self):
        self.tc.set_mode(True, True)
        self.assertDictEqual(self.tc.encode('t_attr_rec_implicit', self.attr1i_api), self.attr1i_api)
        self.assertDictEqual(self.tc.decode('t_attr_rec_implicit', self.attr1i_api), self.attr1i_api)
        self.assertDictEqual(self.tc.encode('t_attr_rec_implicit', self.attr2i_api), self.attr2i_api)
        self.assertDictEqual(self.tc.decode('t_attr_rec_implicit', self.attr2i_api), self.attr2i_api)
        self.assertDictEqual(self.tc.encode('t_attr_rec_implicit', self.attr3i_api), self.attr3i_api)
        self.assertDictEqual(self.tc.decode('t_attr_rec_implicit', self.attr3i_api), self.attr3i_api)
        with self.assertRaises(ValueError):
            self.tc.encode('t_attr_rec_implicit', self.attr4i_bad_api)
        with self.assertRaises(ValueError):
            self.tc.decode('t_attr_rec_implicit', self.attr4i_bad_api)
        with self.assertRaises(ValueError):
            self.tc.encode('t_attr_rec_implicit', self.attr5i_bad_api)
        with self.assertRaises(ValueError):
            self.tc.decode('t_attr_rec_implicit', self.attr5i_bad_api)

    attr1i_min = ['Integer', 17]
    attr2i_min = ['Primitive', {7: 17}]
    attr3i_min = ['Category', {2: {5: [21, 0.342]}}]
    attr4i_bad_min = ['Vegetable', {7: 17}]
    attr5i_bad_min = ['Category', {2: {9: 10}}]

    def test_attr_rec_implicit_min(self):
        self.tc.set_mode(False, False)
        self.assertListEqual(self.tc.encode('t_attr_rec_implicit', self.attr1i_api), self.attr1i_min)
        self.assertDictEqual(self.tc.decode('t_attr_rec_implicit', self.attr1i_min), self.attr1i_api)
        self.assertListEqual(self.tc.encode('t_attr_rec_implicit', self.attr2i_api), self.attr2i_min)
        self.assertDictEqual(self.tc.decode('t_attr_rec_implicit', self.attr2i_min), self.attr2i_api)
        self.assertListEqual(self.tc.encode('t_attr_rec_implicit', self.attr3i_api), self.attr3i_min)
        self.assertDictEqual(self.tc.decode('t_attr_rec_implicit', self.attr3i_min), self.attr3i_api)
        with self.assertRaises(ValueError):
            self.tc.encode('t_attr_rec_implicit', self.attr4i_bad_api)
        with self.assertRaises(ValueError):
            self.tc.decode('t_attr_rec_implicit', self.attr4i_bad_min)
        with self.assertRaises(ValueError):
            self.tc.encode('t_attr_rec_implicit', self.attr5i_bad_api)
        with self.assertRaises(ValueError):
            self.tc.decode('t_attr_rec_implicit', self.attr5i_bad_min)

    pep_api = {'foo': 'bar', 'data': {'count': 17}}
    pec_api = {'foo': 'bar', 'data': {'animal': {'rat': {'length': 21, 'weight': .342}}}}
    pep_bad_api = {'foo': 'bar', 'data': {'turnip': ''}}

    def test_property_explicit_verbose(self):
        self.tc.set_mode(True, True)
        self.assertDictEqual(self.tc.encode('t_property_explicit_primitive', self.pep_api), self.pep_api)
        self.assertDictEqual(self.tc.decode('t_property_explicit_primitive', self.pep_api), self.pep_api)
        self.assertDictEqual(self.tc.encode('t_property_explicit_category', self.pec_api), self.pec_api)
        self.assertDictEqual(self.tc.decode('t_property_explicit_category', self.pec_api), self.pec_api)
        with self.assertRaises(ValueError):
            self.tc.encode('t_property_explicit_primitive', self.pep_bad_api)
        with self.assertRaises(ValueError):
            self.tc.decode('t_property_explicit_primitive', self.pep_bad_api)

    pep_min = ['bar', {7: 17}]
    pec_min = ['bar', {2: {5: [21, 0.342]}}]
    pep_bad_min = ['bar', {'6': 17}]

    def test_property_explicit_min(self):
        self.tc.set_mode(False, False)
        self.assertListEqual(self.tc.encode('t_property_explicit_primitive', self.pep_api), self.pep_min)
        self.assertDictEqual(self.tc.decode('t_property_explicit_primitive', self.pep_min), self.pep_api)
        self.assertListEqual(self.tc.encode('t_property_explicit_category', self.pec_api), self.pec_min)
        self.assertDictEqual(self.tc.decode('t_property_explicit_category', self.pec_min), self.pec_api)
        with self.assertRaises(ValueError):
            self.tc.encode('t_property_explicit_primitive', self.pep_bad_api)
        with self.assertRaises(ValueError):
            self.tc.decode('t_property_explicit_primitive', self.pep_bad_min)

    pip_api = {'foo': 'bar', 'count': 17}
    pic_api = {'foo': 'bar', 'animal': {'rat': {'length': 21, 'weight': .342}}}
    pip_bad1_api = {'foo': 'bar', 'value': 'turnip'}
    pip_bad2_api = {'foo': 'bar', 'value': {'turnip': ''}}

    def test_property_implicit_verbose(self):
        self.tc.set_mode(True, True)
        self.assertDictEqual(self.tc.encode('t_property_implicit_primitive', self.pip_api), self.pip_api)
        self.assertDictEqual(self.tc.decode('t_property_implicit_primitive', self.pip_api), self.pip_api)
        self.assertDictEqual(self.tc.encode('t_property_implicit_category', self.pic_api), self.pic_api)
        self.assertDictEqual(self.tc.decode('t_property_implicit_category', self.pic_api), self.pic_api)
        with self.assertRaises(ValueError):
            self.tc.encode('t_property_implicit_primitive', self.pip_bad1_api)
        with self.assertRaises(ValueError):
            self.tc.decode('t_property_implicit_primitive', self.pip_bad1_api)
        with self.assertRaises(ValueError):
            self.tc.encode('t_property_implicit_primitive', self.pip_bad2_api)
        with self.assertRaises(ValueError):
            self.tc.decode('t_property_implicit_primitive', self.pip_bad2_api)

    pip_min = ['bar', {7: 17}]
    pic_min = ['bar', {2: {'5': [21, .342]}}]
    pip_bad1_min = []
    pip_bad2_min = []

    def test_property_implicit_min(self):
        self.tc.set_mode(False, False)
        self.assertListEqual(self.tc.encode('t_property_implicit_primitive', self.pip_api), self.pip_min)
        self.assertDictEqual(self.tc.decode('t_property_implicit_primitive', self.pip_min), self.pip_api)
        self.assertListEqual(self.tc.encode('t_property_implicit_category', self.pic_api), self.pic_min)
        self.assertDictEqual(self.tc.decode('t_property_implicit_category', self.pic_min), self.pic_api)
        with self.assertRaises(ValueError):
            self.tc.encode('t_property_implicit_primitive', self.pip_bad1_api)
        with self.assertRaises(ValueError):
            self.tc.decode('t_property_implicit_primitive', self.pip_bad1_min)
        with self.assertRaises(ValueError):
            self.tc.encode('t_property_implicit_primitive', self.pip_bad2_api)
        with self.assertRaises(ValueError):
            self.tc.decode('t_property_implicit_primitive', self.pip_bad2_min)


schema_list_cardinality = {                # JADN schema for fields with cardinality > 1 (e.g., list of x)
    'meta': {'module': 'unittests-ListField'},
    'types': [
        ['t_array0', 'ArrayOf', ['*String', '[0', ']2'], ''],   # Min array length = 0, Max = 2
        ['t_array1', 'ArrayOf', ['*String', ']2'], ''],         # Min array length = 1 (default), Max = 2
        ['t_opt_list0', 'Record', [], '', [
            [1, 'string', 'String', [], ''],
            [2, 'list', 't_array0', ['[0'], '']        # Min = 0, Max default = 1 (Array is optional)
        ]],
        ['t_opt_list1', 'Record', [], '', [
            [1, 'string', 'String', [], ''],
            [2, 'list', 't_array1', ['[0'], '']        # Min = 0, Max default = 1  (Array is optional)
        ]],
        ['t_list_1_2', 'Record', [], '', [
            [1, 'string', 'String', [], ''],
            [2, 'list', 'String', [']2'], '']          # Min default = 1, Max = 2
        ]],
        ['t_list_0_2', 'Record', [], '', [
            [1, 'string', 'String', [], ''],
            [2, 'list', 'String', ['[0', ']2'], '']    # Min = 0, Max = 2
        ]],
        ['t_list_2_3', 'Record', [], '', [
            [1, 'string', 'String', [], ''],
            [2, 'list', 'String', ['[2',']3'], '']     # Min = 2, Max = 3
        ]],
        ['t_list_1_n', 'Record', [], '', [
            [1, 'string', 'String', [], ''],
            [2, 'list', 'String', [']0'], '']  # Min default = 1, Max = 0 -> n
        ]]
    ]}


class ListCardinality(unittest.TestCase):      # TODO: arrayOf(rec,map,array,arrayof,choice), array(), map(), rec()

    def setUp(self):
        jadn_check(schema_list_cardinality)
        self.tc = Codec(schema_list_cardinality)

    Lna = {'string': 'cat'}                     # Cardinality 0..n field omits empty list.  Use ArrayOf type to send empty list.
    Lsa = {'string': 'cat', 'list': 'red'}      # Always invalid, value is a string, not a list of one string.
    L0a = {'string': 'cat', 'list': []}         # Arrays SHOULD have minimum cardinality 1 to prevent ambiguity.
    L1a = {'string': 'cat', 'list': ['red']}
    L2a = {'string': 'cat', 'list': ['red', 'green']}
    L3a = {'string': 'cat', 'list': ['red', 'green', 'blue']}

    def test_opt_list0_verbose(self):        # n-P, s-F, 0-F, 1-P, 2-P, 3-F
        self.tc.set_mode(True, True)
        self.assertDictEqual(self.tc.encode('t_opt_list0', self.Lna), self.Lna)
        self.assertDictEqual(self.tc.decode('t_opt_list0', self.Lna), self.Lna)
        with self.assertRaises(TypeError):
            self.tc.encode('t_opt_list0', self.Lsa)
        with self.assertRaises(TypeError):
            self.tc.decode('t_opt_list0', self.Lsa)
        self.assertDictEqual(self.tc.encode('t_opt_list0', self.L0a), self.L0a)
        self.assertDictEqual(self.tc.decode('t_opt_list0', self.L0a), self.L0a)
        self.assertDictEqual(self.tc.encode('t_opt_list0', self.L1a), self.L1a)
        self.assertDictEqual(self.tc.decode('t_opt_list0', self.L1a), self.L1a)
        self.assertDictEqual(self.tc.encode('t_opt_list0', self.L2a), self.L2a)
        self.assertDictEqual(self.tc.decode('t_opt_list0', self.L2a), self.L2a)
        with self.assertRaises(ValueError):
            self.tc.encode('t_opt_list0', self.L3a)
        with self.assertRaises(ValueError):
            self.tc.decode('t_opt_list0', self.L3a)

    def test_opt_list1_verbose(self):        # n-P, s-F, 0-F, 1-P, 2-P, 3-F
        self.tc.set_mode(True, True)
        self.assertDictEqual(self.tc.encode('t_opt_list1', self.Lna), self.Lna)
        self.assertDictEqual(self.tc.decode('t_opt_list1', self.Lna), self.Lna)
        with self.assertRaises(TypeError):
            self.tc.encode('t_opt_list1', self.Lsa)
        with self.assertRaises(TypeError):
            self.tc.decode('t_opt_list1', self.Lsa)
        with self.assertRaises(ValueError):
            self.tc.encode('t_opt_list1', self.L0a)
        with self.assertRaises(ValueError):
            self.tc.decode('t_opt_list1', self.L0a)
        self.assertDictEqual(self.tc.encode('t_opt_list1', self.L1a), self.L1a)
        self.assertDictEqual(self.tc.decode('t_opt_list1', self.L1a), self.L1a)
        self.assertDictEqual(self.tc.encode('t_opt_list1', self.L2a), self.L2a)
        self.assertDictEqual(self.tc.decode('t_opt_list1', self.L2a), self.L2a)
        with self.assertRaises(ValueError):
            self.tc.encode('t_opt_list1', self.L3a)
        with self.assertRaises(ValueError):
            self.tc.decode('t_opt_list1', self.L3a)

    def test_list_1_2_verbose(self):        # n-F, s-F, 0-F, 1-P, 2-P, 3-F
        self.tc.set_mode(True, True)
        with self.assertRaises(ValueError):
            self.tc.encode('t_list_1_2', self.Lna)
        with self.assertRaises(ValueError):
            self.tc.decode('t_list_1_2', self.Lna)
        with self.assertRaises(TypeError):
            self.tc.encode('t_list_1_2', self.Lsa)
        with self.assertRaises(TypeError):
            self.tc.decode('t_list_1_2', self.Lsa)
        with self.assertRaises(ValueError):
            self.tc.encode('t_list_1_2', self.L0a)
        with self.assertRaises(ValueError):
            self.tc.decode('t_list_1_2', self.L0a)
        self.assertDictEqual(self.tc.encode('t_list_1_2', self.L1a), self.L1a)
        self.assertDictEqual(self.tc.decode('t_list_1_2', self.L1a), self.L1a)
        self.assertDictEqual(self.tc.encode('t_list_1_2', self.L2a), self.L2a)
        self.assertDictEqual(self.tc.decode('t_list_1_2', self.L2a), self.L2a)
        with self.assertRaises(ValueError):
            self.tc.encode('t_list_1_2', self.L3a)
        with self.assertRaises(ValueError):
            self.tc.decode('t_list_1_2', self.L3a)

    def test_list_0_2_verbose(self):        # n-P, s-F, 0-F, 1-P, 2-P, 3-F
        self.tc.set_mode(True, True)
        self.assertDictEqual(self.tc.encode('t_list_0_2', self.Lna), self.Lna)
        self.assertDictEqual(self.tc.decode('t_list_0_2', self.Lna), self.Lna)
        with self.assertRaises(TypeError):
            self.tc.encode('t_list_0_2', self.Lsa)
        with self.assertRaises(TypeError):
            self.tc.decode('t_list_0_2', self.Lsa)
        with self.assertRaises(ValueError):
            self.tc.encode('t_list_0_2', self.L0a)
        with self.assertRaises(ValueError):
            self.tc.decode('t_list_0_2', self.L0a)
        self.assertDictEqual(self.tc.encode('t_list_0_2', self.L1a), self.L1a)
        self.assertDictEqual(self.tc.decode('t_list_0_2', self.L1a), self.L1a)
        self.assertDictEqual(self.tc.encode('t_list_0_2', self.L2a), self.L2a)
        self.assertDictEqual(self.tc.decode('t_list_0_2', self.L2a), self.L2a)
        with self.assertRaises(ValueError):
            self.tc.encode('t_list_0_2', self.L3a)
        with self.assertRaises(ValueError):
            self.tc.decode('t_list_0_2', self.L3a)

    def test_list_2_3_verbose(self):        # n-F, 0-F, 1-F, 2-P, 3-P
        self.tc.set_mode(True, True)
        with self.assertRaises(ValueError):
            self.tc.encode('t_list_2_3', self.Lna)
        with self.assertRaises(ValueError):
            self.tc.decode('t_list_2_3', self.Lna)
        with self.assertRaises(ValueError):
            self.tc.encode('t_list_2_3', self.L0a)
        with self.assertRaises(ValueError):
            self.tc.decode('t_list_2_3', self.L0a)
        with self.assertRaises(ValueError):
            self.tc.encode('t_list_2_3', self.L1a)
        with self.assertRaises(ValueError):
            self.tc.decode('t_list_2_3', self.L1a)
        self.assertDictEqual(self.tc.encode('t_list_2_3', self.L2a), self.L2a)
        self.assertDictEqual(self.tc.decode('t_list_2_3', self.L2a), self.L2a)
        self.assertDictEqual(self.tc.encode('t_list_2_3', self.L3a), self.L3a)
        self.assertDictEqual(self.tc.decode('t_list_2_3', self.L3a), self.L3a)

    def test_list_1_n_verbose(self):        # n-F, 0-F, 1-P, 2-P, 3-P
        self.tc.set_mode(True, True)
        with self.assertRaises(ValueError):
            self.tc.encode('t_list_1_n', self.Lna)
        with self.assertRaises(ValueError):
            self.tc.decode('t_list_1_n', self.Lna)
        with self.assertRaises(ValueError):
            self.tc.encode('t_list_1_n', self.L0a)
        with self.assertRaises(ValueError):
            self.tc.decode('t_list_1_n', self.L0a)
        self.assertDictEqual(self.tc.encode('t_list_1_n', self.L1a), self.L1a)
        self.assertDictEqual(self.tc.decode('t_list_1_n', self.L1a), self.L1a)
        self.assertDictEqual(self.tc.encode('t_list_1_n', self.L2a), self.L2a)
        self.assertDictEqual(self.tc.decode('t_list_1_n', self.L2a), self.L2a)
        self.assertDictEqual(self.tc.encode('t_list_1_n', self.L3a), self.L3a)
        self.assertDictEqual(self.tc.decode('t_list_1_n', self.L3a), self.L3a)


schema_list_types = {
    'meta': {'module': 'unittests-ListType'},
    'types': [
        ['t_list', 'ArrayOf', ['*t_list_types'], ''],
        ['t_list_types', 'Record', [], '', [
            [1, 'bins', 'Binary', ['[0', ']2'], ''],
            [2, 'bools', 'Boolean', ['[0', ']2'], ''],
            [3, 'ints', 'Integer', ['[0', ']2'], ''],
            [4, 'strs', 'String', ['[0', ']2'], ''],
            [5, 'arrs', 't_arr', ['[0', ']2'], ''],
            [6, 'aro_s', 't_aro_s', ['[0', ']2'], ''],
            [7, 'aro_ch', 't_aro_ch', ['[0', ']2'], ''],
            [8, 'choices', 't_ch', ['[0', ']2'], ''],
            [9, 'enums', 't_enum', ['[0', ']2'], ''],
            [10, 'maps', 't_map', ['[0', ']2'], ''],
            [11, 'recs', 't_rec', ['[0', ']2'], '']
        ]],
        ['t_arr', 'Array', [], '', [
            [1, 'x', 'Integer', [], ''],
            [2, 'y', 'Number', [], '']
        ]],
        ['t_aro_s', 'ArrayOf', ['*String'], ''],
        ['t_aro_ch', 'ArrayOf', ['*t_ch'], ''],
        ['t_ch', 'Choice', [], '', [
            [1, 'red', 'Integer', [], ''],
            [2, 'blue', 'Integer', [], '']
        ]],
        ['t_enum', 'Enumerated', [], '', [
            [1, 'heads', ''],
            [2, 'tails', '']
        ]],
        ['t_map', 'Map', [], '', [
            [1, 'red', 'Integer', [], ''],
            [2, 'blue', 'Integer', [], '']
        ]],
        ['t_rec', 'Record', [], '', [
            [1, 'red', 'Integer', [], ''],
            [2, 'blue', 'Integer', [], '']
        ]]
    ]}


class List_Types(unittest.TestCase):

    def setUp(self):
        jadn_check(schema_list_types)
        self.tc = Codec(schema_list_types)

    prims = [{
            'bools': [True],
            'ints': [1, 2]
        },
        {'strs': ['cat', 'dog']}
    ]
    enums = [
        {'enums': ['heads', 'tails']},
        {'enums': ['heads']},
        {'enums': ['heads']},
        {'enums': ['tails']},
        {'enums': ['heads']},
        {'enums': ['tails']}
    ]

    def test_list_primitives(self):
        self.tc.set_mode(True, True)
        self.assertListEqual(self.tc.encode('t_list', self.prims), self.prims)
        self.assertListEqual(self.tc.decode('t_list', self.prims), self.prims)
        self.assertListEqual(self.tc.encode('t_list', self.enums), self.enums)
        self.assertListEqual(self.tc.decode('t_list', self.enums), self.enums)


class Bounds(unittest.TestCase):        # TODO: check max and min string length, integer values, array sizes
                                        # TODO: Schema default and options
    def setUp(self):
        jadn_check(schema_bounds)
        self.tc = Codec(schema_bounds)


schema_format = {  # JADN schema for value constraint tests
    'meta': {'module': 'unittests-Format'},
    'types': [
        ['IPv4-Bin', 'Binary', ['[4', ']4'], ''],                   # Check length = 32 bits with format function
        ['IPv4-Hex', 'Binary', ['[4', ']4', '.x'], ''],             # Check length = 32 bits with min/max size
        ['IPv4-String', 'Binary', ['[4', ']4', '.ipv4-addr'], ''],
        ['IPv6-Base64url', 'Binary', ['[16', ']16'], ''],
        ['IPv6-Hex', 'Binary', ['[16', ']16', '.x'], ''],
        ['IPv6-String', 'Binary', ['[16', ']16', '.ipv6-addr'], ''],
        ['IPv5-error-expected', 'Binary', ['.ipv5'], ''],           # Generate error: unsupported (nonexistent) format
        ['IPv4-Net', 'Array', ['.ipv4-net'], '', [
            [1, 'addr', 'Binary', [], ''],
            [2, 'prefix', 'Integer', [], '']
        ]],
        ['IPv6-Net', 'Array', ['.ipv6-net'], '', [
            [1, 'addr', 'Binary', [], ''],
            [2, 'prefix', 'Integer', [], '']
        ]],
        ['t_ipaddrs', 'ArrayOf', ['*IPv4-Bin'], ''],
        ['MAC-Base64url', 'Binary', ['@mac-addr'], ''],
        ['Email-Addr', 'String', ['@email'], ''],
        ['Hostname', 'String', ['@hostname'], '']
    ]
}


class Format(unittest.TestCase):

    def setUp(self):
        jadn_check(schema_format)
        self.tc = Codec(schema_format, verbose_rec=True, verbose_str=True)

    ipv4_b = binascii.a2b_hex('c6020304')           # IPv4 address
    ipv4_s64 = 'xgIDBA'                             # Base64url encoded
    ipv4_sx = 'C6020304'                            # Hex encoded
    ipv4_str = '198.2.3.4'                          # IPv4-string encoded
    ipv4_b1_bad = binascii.a2b_hex('c60203')        # Too short
    ipv4_b2_bad = binascii.a2b_hex('c602030456')    # Too long
    ipv4_s64_bad = 'xgIDBFY'                        # Too long
    ipv4_sx_bad = 'C602030456'                      # Too long
    ipv4_str_bad = '198.2.3.4.56'                   # Too long

    def test_ipv4_addr(self):
        self.assertEqual(self.tc.encode('IPv4-Bin', self.ipv4_b), self.ipv4_s64)
        self.assertEqual(self.tc.decode('IPv4-Bin', self.ipv4_s64), self.ipv4_b)
        self.assertEqual(self.tc.encode('IPv4-Hex', self.ipv4_b), self.ipv4_sx)
        self.assertEqual(self.tc.decode('IPv4-Hex', self.ipv4_sx), self.ipv4_b)
        self.assertEqual(self.tc.encode('IPv4-String', self.ipv4_b), self.ipv4_str)
        self.assertEqual(self.tc.decode('IPv4-String', self.ipv4_str), self.ipv4_b)
        with self.assertRaises(ValueError):
            self.tc.encode('IPv4-Hex', self.ipv4_b1_bad)
        with self.assertRaises(ValueError):
            self.tc.encode('IPv4-Hex', self.ipv4_b1_bad)
        with self.assertRaises(ValueError):
            self.tc.decode('IPv4-Bin', self.ipv4_s64_bad)
        with self.assertRaises(ValueError):
            self.tc.decode('IPv4-Hex', self.ipv4_sx_bad)
        with self.assertRaises(ValueError):
            self.tc.decode('IPv4-String', self.ipv4_str_bad)
        with self.assertRaises(ValueError):
            self.tc.encode('IPv4-Bin', b'')
        with self.assertRaises(ValueError):
            self.tc.decode('IPv4-Bin', '')
        with self.assertRaises(ValueError):
            self.tc.encode('IPv4-Hex', b'')
        with self.assertRaises(ValueError):
            self.tc.decode('IPv4-Hex', '')
        with self.assertRaises(ValueError):
            self.tc.encode('IPv4-String', b'')
        with self.assertRaises(ValueError):
            self.tc.decode('IPv4-String', '')

    ipv4_net_str = '192.168.0.0/20'                     # IPv4 CIDR network address (not class C /24)
    ipv4_net_a = [binascii.a2b_hex('c0a80000'), 20]

    def test_ipv4_net(self):
        self.assertEqual(self.tc.encode('IPv4-Net', self.ipv4_net_a), self.ipv4_net_str)
        self.assertEqual(self.tc.decode('IPv4-Net', self.ipv4_net_str), self.ipv4_net_a)
        # with self.assertRaises(ValueError):
        #    self.tc.encode('IPv4-Net', self.ipv4_net_bad1)

    ipv6_b = binascii.a2b_hex('20010db885a3000000008a2e03707334')   # IPv6 address
    ipv6_s64 = 'IAENuIWjAAAAAIouA3BzNA'                             # Base64 encoded
    ipv6_sx = '20010DB885A3000000008A2E03707334'                    # Hex encoded
    ipv6_str1 = '2001:db8:85a3::8a2e:370:7334'                      # IPv6-string encoded
    ipv6_str2 = '2001:db8:85a3::8a2e:0370:7334'                     # IPv6-string encoded - leading 0
    ipv6_str3 = '2001:db8:85A3::8a2e:370:7334'                      # IPv6-string encoded - uppercase
    ipv6_str4 = '2001:db8:85a3:0::8a2e:370:7334'                    # IPv6-string encoded - zero not compressed

    def test_ipv6_addr(self):
        self.assertEqual(self.tc.encode('IPv6-Base64url', self.ipv6_b), self.ipv6_s64)
        self.assertEqual(self.tc.decode('IPv6-Base64url', self.ipv6_s64), self.ipv6_b)
        self.assertEqual(self.tc.encode('IPv6-Hex', self.ipv6_b), self.ipv6_sx)
        self.assertEqual(self.tc.decode('IPv6-Hex', self.ipv6_sx), self.ipv6_b)
        self.assertEqual(self.tc.encode('IPv6-String', self.ipv6_b), self.ipv6_str1)
        self.assertEqual(self.tc.decode('IPv6-String', self.ipv6_str1), self.ipv6_b)

    ipv6_net_str = '2001:db8:85a3::8a2e:370:7334/64'                # IPv6 network address
    ipv6_net_a = [binascii.a2b_hex('20010db885a3000000008a2e03707334'), 64]

    def test_ipv6_net(self):
        self.assertEqual(self.tc.encode('IPv6-Net', self.ipv6_net_a), self.ipv6_net_str)
        self.assertEqual(self.tc.decode('IPv6-Net', self.ipv6_net_str), self.ipv6_net_a)

    eui48b = binascii.a2b_hex('002186b56e10')
    eui48s = 'ACGGtW4Q'
    eui64b = binascii.a2b_hex('022186fffeb56e10')
    eui64s = 'AiGG__61bhA'
    eui48b_bad = binascii.a2b_hex('0226fffeb56e10')
    eui48s_bad = 'Aib__rVuEA'

    def test_mac_addr(self):
        self.assertEqual(self.tc.encode('MAC-Base64url', self.eui48b), self.eui48s)
        self.assertEqual(self.tc.decode('MAC-Base64url', self.eui48s), self.eui48b)
        self.assertEqual(self.tc.encode('MAC-Base64url', self.eui64b), self.eui64s)
        self.assertEqual(self.tc.decode('MAC-Base64url', self.eui64s), self.eui64b)
        with self.assertRaises(ValueError):
            self.tc.encode('MAC-Base64url', self.eui48b_bad)
        with self.assertRaises(ValueError):
            self.tc.decode('MAC-Base64url', self.eui48s_bad)

    email1s = 'fred@foo.com'
    email2s_bad = 'https://www.foo.com/index.html'
    email3s_bad = 'Nancy'
    email4s_bad = 'John@'

    def test_email(self):
        self.assertEqual(self.tc.encode('Email-Addr', self.email1s), self.email1s)
        self.assertEqual(self.tc.decode('Email-Addr', self.email1s), self.email1s)
        with self.assertRaises(ValueError):
            self.tc.encode('Email-Addr', self.email2s_bad)
        with self.assertRaises(ValueError):
            self.tc.decode('Email-Addr', self.email2s_bad)
        with self.assertRaises(ValueError):
            self.tc.encode('Email-Addr', self.email3s_bad)
        with self.assertRaises(ValueError):
            self.tc.decode('Email-Addr', self.email3s_bad)
        with self.assertRaises(ValueError):
            self.tc.encode('Email-Addr', self.email4s_bad)
        with self.assertRaises(ValueError):
            self.tc.decode('Email-Addr', self.email4s_bad)

    hostname1s = 'eewww.example.com'
    hostname2s = 'top-gun.2600.xyz'                     # No TLD registry, no requirement to be FQDN
    hostname3s = 'dynamo'                               # No requirement to have more than one label
    hostname1s_bad = '_http._sctp.www.example.com'      # Underscores are allowed in DNS service names but not hostnames
    hostname2s_bad = 'tag-.example.com'                 # Label cannot begin or end with hyphen

    def test_hostname(self):
        self.assertEqual(self.tc.encode('Hostname', self.hostname1s), self.hostname1s)
        self.assertEqual(self.tc.decode('Hostname', self.hostname1s), self.hostname1s)
        self.assertEqual(self.tc.encode('Hostname', self.hostname2s), self.hostname2s)
        self.assertEqual(self.tc.decode('Hostname', self.hostname2s), self.hostname2s)
        self.assertEqual(self.tc.encode('Hostname', self.hostname3s), self.hostname3s)
        self.assertEqual(self.tc.decode('Hostname', self.hostname3s), self.hostname3s)
        with self.assertRaises(ValueError):
            self.tc.encode('Hostname', self.hostname1s_bad)
        with self.assertRaises(ValueError):
            self.tc.decode('Hostname', self.hostname1s_bad)
        with self.assertRaises(ValueError):
            self.tc.encode('Hostname', self.hostname2s_bad)
        with self.assertRaises(ValueError):
            self.tc.decode('Hostname', self.hostname2s_bad)
        with self.assertRaises(ValueError):
            self.tc.encode('Hostname', self.email1s)
        with self.assertRaises(ValueError):
            self.tc.decode('Hostname', self.email1s)


class JADN(unittest.TestCase):

    def setUp(self):
        fn = os.path.join('schema', 'jadn-csdpr02.jadn')
        schema = jadn_load(fn)
        self.schema = schema
        sa = jadn_analyze(schema)
        if sa['undefined']:
            print('Warning - undefined:', sa['undefined'])
        self.tc = Codec(schema, verbose_rec=True, verbose_str=True)

    def test_jadn_self(self):

        self.assertDictEqual(self.tc.encode('Schema', self.schema), self.schema)
        self.assertDictEqual(self.tc.decode('Schema', self.schema), self.schema)


if __name__ == '__main__':
    unittest.main()
