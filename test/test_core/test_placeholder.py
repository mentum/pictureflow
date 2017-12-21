from test.context import pf

import unittest


class TestPlaceholderInitialize(unittest.TestCase):

    def test_placeholder_initialize_sets_output_type(self):
        out_type = str

        p = pf.Placeholder(out_type=out_type)

        self.assertEqual(p._output_type, out_type)

    def test_placeholder_initialize_defaults_output_type_to_none(self):
        p = pf.Placeholder()

        self.assertEqual(p._output_type, None)


class TestPlaceholderApply(unittest.TestCase):

    def test_placeholder_apply_returns_same_value(self):
        p = pf.Placeholder()

        value = 42

        output = [x for x in p.apply(42)]

        self.assertEqual(len(output), 1)
        self.assertEqual(output[0], value)
