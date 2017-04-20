from pictureflow.core import Node


class Placeholder(Node):

    def __init__(self, id='placeholder', out_type=None):
        super().__init__(id=id)
        self._output_type = out_type
