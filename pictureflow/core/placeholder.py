from pictureflow.core import Node


class Placeholder(Node):

    """
    Along with :py:class:`Constant`, :py:class:`Placeholder` is the only parent-less node included with PictureFlow. 
    It is most often used as an entry point for the transformation graph, as its value will be substituted at runtime 
    by :py:class:`Session`.
    
    Args:
        id (str): ID of the placeholder
        out_type (type): Type of the placeholder (used to validate compatibility while building the graph)
    """

    def __init__(self, id='placeholder', out_type=None):
        super().__init__(id=id)
        self._output_type = out_type

    def apply(self, parent):
        yield parent
