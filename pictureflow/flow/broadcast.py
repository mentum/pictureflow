from copy import deepcopy
from pictureflow.core import Node


class Broadcast(Node):

    """
    Essentially a repeater, allows to broadcast a single item to multiple branches

    Args:
        parent (Node): Parent node
        count (int): Number of branches to which the broadcast node is connected

    Attributes:
        Input Types: None
        Output Type: None
    """

    _input_types = [None, int]
    _output_type = None

    def __init__(self, parent, count):
        super().__init__('broadcast', parent, count)
        self.count = count

    def apply(self, itm, count):
        for i in range(count):
            yield deepcopy(itm)
