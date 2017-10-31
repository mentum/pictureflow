from pictureflow.core import Node, Image


class Combine(Node):

    """
    The oposite of the Broadcast node, allows the combination of multiple branches into a single branch

    Args:
        parents (Node<Any>): Parent nodes
    """

    _input_types = None
    _output_type = None

    def __init__(self, *parents):
        super().__init__('combine', *parents)

    def apply(self, *parents):
        yield from parents
