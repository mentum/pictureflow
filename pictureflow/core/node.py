from copy import copy


class Node(object):

    _input_type = None
    _output_type = None

    def __init__(self, parent=None, id='node'):
        self.id = id

        # Check if parent output is compatible with current input
        if self._input_type is not None and parent is not None and parent._output_type != self._input_type:
            parent_name = parent.__class__.__name__
            parent_type = parent._output_type.__name__ if parent._output_type else str(parent._output_type)
            input_type = self._input_type.__name__ if self._input_type else str(self._input_type)
            raise TypeError(f'"{parent_name}" output "{parent_type}" is not compatible with input "{input_type}"')

        self.parent = parent

    def __iter__(self):
        return self

    def __next__(self):
        return self._apply_typecheck(copy(next(self.parent)))

    def _apply_typecheck(self, item):

        # TODO: Improve error message generation

        if self._input_type is not None and not isinstance(item, self._input_type):
            raise TypeError(f'Node {self.id} expected an object of type {self._input_type} but got {type(item)}')

        out = self.apply(item)

        if self._output_type is not None and not isinstance(out, self._output_type):
            raise TypeError(f'Node {self.id} should return an object of type {self._output_type} but returned a {type(item)}')

        return out

    def apply(self, item):
        # Base node does nothing
        return item
