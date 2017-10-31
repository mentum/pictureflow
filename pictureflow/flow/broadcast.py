from pictureflow.core import Node, Image


class Broadcast(Node):
    _input_types = [None, int]
    _output_type = None

    def __init__(self, parent, count):
        super().__init__('broadcast', parent, count)
        self.count = count

    def apply(self, itm, count):
        for i in range(count):
            yield itm
