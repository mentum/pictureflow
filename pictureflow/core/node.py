from copy import copy


class Node(object):

    """
    Base unit of the PictureFlow architecture. All structures capable of manipulating items should inherit from this
    one. The :py:func:`apply()` method tasked with actually applying the manipulations, override it as necessary.

    :py:class:`Node` is also an iterator, meaning that iterating on a node will yield the transformed output of this
    node's parent.

    Args:
        parent (Node<Image>): Parent node of this node
        id (str): ID of the node
    """

    _input_type = None  # Typecheck disabled by default
    _output_type = None

    def __init__(self, id='node', *parents):

        self.id = id

        self._typecheck_enabled = isinstance(self._input_type, list)

        if self._typecheck_enabled:
            if len(self._input_type) != len(parents):
                raise TypeError(f'Node is expecting {len(self._input_type)} inputs, got {len(parents)}')

            for i, parent in enumerate(parents):
                if parent._output_type != self._input_type[i]:
                    parent_name = parent.__class__.__name__
                    parent_type = parent._output_type.__name__ if parent._output_type else str(parent._output_type)
                    input_type = self._input_type[i].__name__ if self._input_type[i] else str(self._input_type[i])
                    raise TypeError(f'"{parent_name}" output "{parent_type}" is not compatible with input "{input_type}"')

        self._iterator = self._get_iterator()

        self.parents = parents

    def _get_iterator(self):
        try:
            while True:
                args = [copy(next(parent)) for parent in self.parents]
                yield from self._apply_typecheck(*args)
        except StopIteration:
            return

    def __iter__(self):
        return self._iterator

    def __next__(self):
        return next(self._iterator)

    def _apply_typecheck(self, *args):

        # TODO: Improve error message generation

        if self._typecheck_enabled:
            for i, arg in enumerate(args):
                if type(arg) != self._input_type[i]:
                    raise TypeError(f'Node {self.id} expected an object of type {self._input_type[i]} but got {type(arg)}')

        for output_item in self.apply(*args):
            if self._output_type is not None and not isinstance(output_item, self._output_type):
                raise TypeError(f'Node {self.id} should return an object of type {self._output_type} but returned a {type(output_item)}')
            yield output_item

    def reset(self):
        self._iterator = self._get_iterator()

        for p in self.parents:
            p.reset()

    def apply(self, *args):
        """
        Base apply method, does nothing.

        Args:
            item (Any): Input item

        Returns:
            typeof(item): Input item

        """
        # Base node does nothing
        yield args
