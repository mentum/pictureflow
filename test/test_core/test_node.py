from test.context import pf

from unittest.mock import MagicMock, patch

import types
import unittest


class TypedNode(pf.core.Node):
    _input_types = [str]
    _output_type = int

    def apply(self, in_str):
        yield len(in_str)


class TestNodeInitialization(unittest.TestCase):

    def test_node_sets_id_properly(self):
        node_id = 'hello'

        n = pf.core.Node(id=node_id)
        self.assertEqual(n.id, node_id)

    def test_node_defaults_id_properly(self):
        expected_id = 'node'

        n = pf.core.Node()
        self.assertEqual(n.id, expected_id)

    def test_node_enables_typecheck_when_types_are_defined(self):
        with patch('pictureflow.core.Node._validate_parent_types', MagicMock()):
            n = TypedNode()
            self.assertTrue(n._typecheck_enabled)

    def test_node_disables_typecheck_when_no_types_are_defined(self):
        n = pf.core.Node()

        self.assertFalse(n._typecheck_enabled)

    def test_node_sets_parents(self):
        parents = ['a', 'b', 'c']

        n = pf.core.Node('node', *parents)

        self.assertEqual(n.parents, parents)


class TestNodeValidateParentTypes(unittest.TestCase):

    @staticmethod
    def run_type_validation(inputs, parents_types):
        n = pf.core.Node()

        n._input_types = inputs

        n.parents = []
        for t in parents_types:
            parent = pf.core.Node()
            parent._output_type = t
            n.parents.append(parent)

        n._typecheck_enabled = True

        n._validate_parent_types(n.parents)

    def test_node_validate_parent_does_nothing_if_typecheck_disabled(self):
        n = pf.core.Node()

        # Setup so validation fails
        n._input_types = [1, 2, 3]
        n.parents = [1, 2]

        n._typecheck_enabled = False

        try:
            n._validate_parent_types(n.parents)

        except Exception:
            self.fail(f'Parent typecheck should not run when typecheck is disabled')

    def test_node_validate_parent_raises_typeerror_if_input_type_length_different_from_parent_length(self):
        with self.assertRaises(TypeError):
            self.run_type_validation([int, int, int], [int, int])

    def test_node_validate_parent_doesnt_raise_if_all_types_match(self):
        try:
            self.run_type_validation([int, int, int], [int, int, int])
        except Exception:
            self.fail("Parent typecheck should not fail when all types match")

    def test_node_validate_parent_doesnt_raise_if_input_type_has_wildcard(self):
        try:
            self.run_type_validation([int, None, int], [int, str, int])

        except Exception:
            self.fail('Parent typecheck should not fail when lengths match and wildcard is present')

    def test_node_validate_parent_raises_typeerror_if_parent_type_mismatch(self):
        with self.assertRaises(TypeError):
            self.run_type_validation([int, int, int], [int, str, int])


class TestNodeValidateRuntimeInput(unittest.TestCase):

    @staticmethod
    def run_type_validation(input_types, args):
        n = pf.core.Node()

        n._input_types = input_types
        n._typecheck_enabled = True

        n._validate_runtime_input(args)

    def test_validate_runtime_input_does_nothing_if_typecheck_is_disabled(self):
        n = pf.core.Node()

        n._input_types = [int, int, int]
        n._typecheck_enabled = False

        try:
            n._validate_runtime_input(('test',))

        except Exception:
            self.fail('Runtime input typecheck should not run when typecheck is disabled')

    def test_validate_runtime_input_doesnt_raise_if_types_match(self):

        try:
            self.run_type_validation([int, int, int], [1, 2, 3])

        except Exception:
            self.fail('Runtime input typecheck should not fail when all types match')

    def test_validate_runtime_input_doesnt_raise_if_input_has_wildcard(self):
        try:
            self.run_type_validation([int, None, int], [1, 'test', 3])

        except Exception:
            self.fail('Runtime input typecheck should not fail when a wildcard is used')

    def test_validate_runtime_input_raises_typerror_if_inputs_dont_match(self):
        with self.assertRaises(TypeError):
            self.run_type_validation([str, str], ['test', 1])


class TestValidateRuntimeOutput(unittest.TestCase):

    @staticmethod
    def run_type_validation(output_type, item):
        n = pf.core.Node()
        n._output_type = output_type
        n._typecheck_enabled = True

        n._validate_runtime_output(item)

    def test_validate_runtime_output_does_nothing_if_typecheck_is_disabled(self):
        n = pf.core.Node()

        n._output_type = int
        n._typecheck_enabled = False

        try:
            n._validate_runtime_output('test')

        except Exception:
            self.fail('Runtime output typecheck should not run when typecheck is disabled')

    def test_validate_runtime_output_doesnt_raise_if_types_match(self):
        try:
            self.run_type_validation(int, 3)

        except Exception:
            self.fail('Runtime output typecheck should not fail when types match')

    def test_validate_runtime_output_doesnt_raise_if_output_type_is_wildcard(self):
        try:
            self.run_type_validation(None, 3)

        except Exception:
            self.fail('Runtime output typecheck should not fail when output type is a wildcard')

    def test_validate_runtime_output_raises_typeerror_if_types_dont_match(self):
        with self.assertRaises(TypeError):
            self.run_type_validation(str, 3)


class TestGetIterator(unittest.TestCase):

    def test_get_iterator_returns_generator(self):
        n = pf.core.Node()

        self.assertIsInstance(n._get_iterator(), types.GeneratorType)

    def test_get_iterator_iterator_calls_apply_typecheck(self):

        mock_apply = MagicMock(side_effect=StopIteration)

        with patch('pictureflow.core.Node._apply_typecheck', mock_apply):
            n = pf.core.Node()

            gen = n._get_iterator()

            for _ in gen:
                pass

        self.assertTrue(mock_apply.called)


class TestIterReturnsClassIterator(unittest.TestCase):

    def test_iter_returns_class_iterator(self):
        n = pf.core.Node()

        self.assertIs(n.__iter__(), n._iterator)


class TestNextReturnsIteratorNext(unittest.TestCase):

    def test_next_returns_next_iterator_item(self):

        values = [1, 2, 3, 4, 5]

        def mock_iterator():
            yield from values

        n = pf.core.Node()
        n._iterator = mock_iterator()

        itm = n.__next__()

        self.assertEqual(itm, values[0])


class TestNodeApplyTypecheck(unittest.TestCase):

    @staticmethod
    def mock_apply(*args, **kwargs):
        for i in range(10):
            yield i

    def setUp(self):

        self.node = pf.core.Node()
        self.node.apply = TestNodeApplyTypecheck.mock_apply
        self.node._validate_runtime_input = MagicMock()
        self.node._validate_runtime_output = MagicMock()

    def test_node_apply_typecheck_calls_validate_runtime_input(self):
        for _ in self.node._apply_typecheck():
            pass

        self.assertTrue(self.node._validate_runtime_input.called)

    def test_node_apply_typecheck_calls_validate_runtime_output(self):
        for _ in self.node._apply_typecheck():
            pass

        self.assertTrue(self.node._validate_runtime_output.called)


class TestNodeReset(unittest.TestCase):

    def test_node_reset_resets_node_iterator(self):
        n = pf.core.Node()

        old_iterator = n._iterator

        n.reset()

        self.assertIsNot(n._iterator, old_iterator)

    def test_node_reset_calls_parent_reset(self):

        parents = []

        for i in range(10):
            parent = pf.core.Node()
            parent.reset = MagicMock()
            parents.append(parent)

        n = pf.core.Node('test', *parents)
        n.reset()

        self.assertTrue(all([p.reset.called for p in parents]))


class TestNodeDefaultApply(unittest.TestCase):

    def test_node_apply_yields_args(self):
        n = pf.core.Node()

        vals = (1, 2, 3)

        items = []
        for i in n.apply(*vals):
            items.append(i)

        self.assertEqual(len(items), 1)

        self.assertEqual(items[0], vals)
