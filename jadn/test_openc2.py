# This Python file uses the following encoding: utf-8
from __future__ import unicode_literals

import os
import unittest

from libs.codec.codec import Codec
from libs.codec.jadn import jadn_load, jadn_analyze


class Language(unittest.TestCase):

    def setUp(self):
        fn = os.path.join('schema', 'openc2-wd07.jadn')
        ls = jadn_load(fn)
        sa = jadn_analyze(ls)
        if sa['undefined']:
            print('Error: undefined:', sa['undefined'])
        self.tc = Codec(ls, verbose_rec=True, verbose_str=True)

    mq1 = {"action": "query", "target": {"openc2": ["versions"]}}
    mq2 = {"action": "query", "target": {"openc2": ["profiles"]}}

    def test_query_oc2(self):
        self.assertEqual(self.tc.encode("OpenC2-Command", self.mq1), self.mq1)
        self.assertEqual(self.tc.decode("OpenC2-Command", self.mq1), self.mq1)
        self.assertEqual(self.tc.encode("OpenC2-Command", self.mq2), self.mq2)
        self.assertEqual(self.tc.decode("OpenC2-Command", self.mq2), self.mq2)
        with self.assertRaises(TypeError):
            self.tc.encode("OpenC2-Command", "mq_bad1")
        with self.assertRaises(TypeError):
            self.tc.decode("OpenC2-Command", "mq_bad1")


if __name__ == "__main__":
    unittest.main()
