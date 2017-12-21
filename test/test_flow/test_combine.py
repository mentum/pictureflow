from test.context import pf

import unittest


class TestCombineInitialize(unittest.TestCase):

    def test_combine_defaults_id_to_combine(self):
        combine = pf.flow.Combine()

        self.assertEqual(combine.id, 'combine')


class TestCombineApply(unittest.TestCase):

    def test_combine_apply_yields_arguments_individually(self):
        combine = pf.flow.Combine()

        input_data = [(1, 2, 3), (4, 5, 6), (7, 8, 9)]

        expected_output = [1, 2, 3, 4, 5, 6, 7, 8, 9]

        actual_output = []
        for input_args in input_data:
            actual_output += [x for x in combine.apply(*input_args)]

        self.assertEqual(expected_output, actual_output)
