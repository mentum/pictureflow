from pictureflow.core import Node


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

        def iterator():
            while True:
                yield self.value

        self.parents = [iterator()]
        self.value = value

    def apply(self, val):
        yield val
