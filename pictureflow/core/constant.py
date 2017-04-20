from pictureflow.core import Node


class Constant(Node):

    def __init__(self, value, id='constant'):
        super().__init__(id=id)

        def iterator():
            while True:
                yield self.value

        self.parent = iterator()
        self.value = value
