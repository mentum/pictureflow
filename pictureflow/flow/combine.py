from pictureflow.core import Node, Image


class Combine(Node):

    _input_type = None
    _output_type = Image

    def __init__(self, *parents):
        super().__init__('combine', *parents)

    def apply(self, *parents):
        yield from parents
