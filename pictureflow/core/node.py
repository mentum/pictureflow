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

        self._iterator = self._get_iterator()

        self.parent = parent

    def _get_iterator(self):
        for child in self.parent:
            cp = copy(child)
            yield from self._apply_typecheck(cp)

    def __iter__(self):
        return self._iterator

    def __next__(self):
        return next(self._iterator)

    def _apply_typecheck(self, item):

        # TODO: Improve error message generation

        if self._input_type is not None and not isinstance(item, self._input_type):
            raise TypeError(f'Node {self.id} expected an object of type {self._input_type} but got {type(item)}')

        for output_item in self.apply(item):
            if self._output_type is not None and not isinstance(output_item, self._output_type):
                raise TypeError(f'Node {self.id} should return an object of type {self._output_type} but returned a {type(item)}')
            yield output_item

    def apply(self, item):
        """
        Base apply method, does nothing.
        
        Args:
            item (Any): Input item

        Returns:
            typeof(item): Input item

        """
        # Base node does nothing
        yield item
