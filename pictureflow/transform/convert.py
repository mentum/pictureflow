from pictureflow import Constant
from pictureflow.core import Image, Node

import cv2


class Convert(Node):

    """
    Converts an :py:class:`Image` from its original color space to another.
    
    Args:
        parent (Node<Image>): Parent node
        dest (Node<str>): Desired colorspace
        id (str): ID of the node
    """

    _input_type = Image
    _output_type = Image

    def __init__(self, parent, dest=None, id='torgb'):
        super().__init__(parent, id)

        self.flags = [i for i in dir(cv2) if i.startswith('COLOR_')]

        if dest is None:
            dest = Constant('rgb')

        self.dest = dest

    def apply(self, item):

        frm = item.color_space.upper()
        tgt = next(self.dest).upper()

        item.id += '-cvt2{}'.format(tgt)
        item.color_space = tgt

        try:
            cvt = getattr(cv2, 'COLOR_{0}2{1}'.format(frm, tgt))

        except AttributeError:
            raise

        item.img_mat = cv2.cvtColor(item.img_mat, cvt)

        yield item
