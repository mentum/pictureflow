from test.context import pf

from unittest.mock import MagicMock, patch

import types
import unittest


class TestConstantInitialize(unittest.TestCase):

    def test_constant_initialize_sets_output_type(self):
        value = 1

        c = pf.Constant(value)

        self.assertEqual(c._output_type, type(value))

    def test_constant_initialize_creates_constant_iterator(self):
        value = 1

        c = pf.Constant(value)

        self.assertEqual(len(c.parents), 1)
        self.assertIsInstance(c.parents[0], pf.core.constant._ConstantIterator)


class TestConstantApply(unittest.TestCase):

    def test_constant_apply_returns_value(self):

        c = pf.Constant('asdf')

        value = 3
        x = [val for val in c.apply(value)]

        self.assertEqual(len(x), 1)
        self.assertEqual(x[0], value)


class TestConstantIteratorInitialize(unittest.TestCase):

    def test_constant_iterator_initialize_sets_value(self):
        value = 42
        iterator = pf.core.constant._ConstantIterator(value)
        self.assertEqual(iterator.val, value)

    def test_constant_iterator_initialize_starts_iterator(self):
        value = 42
        mock_get_iter = MagicMock(return_value=value)

        with patch('pictureflow.core.constant._ConstantIterator._get_iterator', mock_get_iter):
            iterator = pf.core.constant._ConstantIterator('hello')

            self.assertTrue(mock_get_iter.called)
            self.assertEqual(iterator._iterator, value)


class TestConstantIteratorGetIterator(unittest.TestCase):

    def test_constant_iterator_get_iterator_returns_iterator(self):

        c = pf.core.constant._ConstantIterator(13)

        iterator = c._get_iterator()

        self.assertIsInstance(iterator, types.GeneratorType)

    def test_constant_iterator_get_iterator_yield_correct_value(self):
        value = 42

        c = pf.core.constant._ConstantIterator(value)

        iterator = c._get_iterator()

        for i in range(10):
            out_val = next(iterator)
            self.assertEqual(out_val, value)


class TestConstantIteratorReset(unittest.TestCase):

    def test_constant_iterator_reset_doesnt_fail(self):
        c = pf.core.constant._ConstantIterator(1)

        try:
            c.reset()

        except Exception:
            self.fail('ConstantIterator.reset() must not raise any exception')


class TestConstantIteratorIter(unittest.TestCase):

    def test_constant_iter_returns_class_iterator(self):
        c = pf.core.constant._ConstantIterator(1)

        self.assertIs(c.__iter__(), c._iterator)


class TestNextReturnsIteratorNext(unittest.TestCase):

    def test_next_returns_next_iterator_item(self):

        value = 42

        def mock_iterator():
            while True:
                yield value

        c = pf.core.constant._ConstantIterator(value)
        c._iterator = mock_iterator()

        itm = c.__next__()

        self.assertEqual(itm, value)
