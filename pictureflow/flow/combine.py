from pictureflow.core import Node


class Combine(Node):

    """
    The opposite of the Broadcast node, allows the combination of multiple branches into a single branch

    Args:
        *parents (Node): Parent nodes

    Attributes:
        Input Types: None
        Output Type: None
    """

    _input_types = None
    _output_type = None

    def __init__(self, *parents):
        super().__init__('combine', *parents)

    def apply(self, *parents):
        yield from parents
