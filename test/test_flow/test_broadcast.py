from test.context import pf

import unittest


class TestBroadcastInitialize(unittest.TestCase):

    def test_broadcast_has_correct_inputs(self):
        expected_inputs = [None, int]

        self.assertEqual(pf.flow.Broadcast._input_types, expected_inputs)

    def test_broadcast_has_wildcard_output(self):
        self.assertIsNone(pf.flow.Broadcast._output_type)

    def test_broadcast_initialize_sets_count(self):
        expected_count = pf.Constant(42)

        broadcast = pf.flow.Broadcast(pf.Placeholder(out_type=int), count=expected_count)

        self.assertEqual(broadcast.count, expected_count)

    def test_broadcast_initialize_defaults_id_to_broadcast(self):
        broadcast = pf.flow.Broadcast(pf.Placeholder(out_type=int), count=pf.Constant(42))

        self.assertEqual(broadcast.id, 'broadcast')


class TestBroadcastApply(unittest.TestCase):

    def test_broadcast_apply_correctly_broadcasts_values(self):
        input_vals = [1, 2, 3, 4]
        count = 2

        expected_out = [1, 1, 2, 2, 3, 3, 4, 4]

        broadcast = pf.flow.Broadcast(pf.Placeholder(out_type=int), count=pf.Constant(42))

        actual_out = []
        for val in input_vals:
            actual_out += [x for x in broadcast.apply(val, count)]

        self.assertEqual(actual_out, expected_out)
