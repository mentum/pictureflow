from pictureflow.core import Node


class ConstantIterator(object):

    def __init__(self, val):
        self.val = val
        self._iterator = self._get_iterator()

    def _get_iterator(self):
        while True:
            yield self.val

    def reset(self):
        pass

    def __iter__(self):
        return self._iterator

    def __next__(self):
        return next(self._iterator)


class Constant(Node):

    """
    Simplest implementation of :py:class:`Node`. Its iterator will always yield the value
    specified at instantiation.

    Args:
        value (Any): Value of the constant
        id (str): ID of the constant
    """

    def __init__(self, value, id='constant'):
        super().__init__(id=id)

        self._output_type = type(value)
        self.parents = [ConstantIterator(value)]

    def apply(self, val):
        yield val
