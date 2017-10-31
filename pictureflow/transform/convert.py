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

    _input_types = [Image, str]
    _output_type = None

    def __init__(self, parents, dest=None, id='convert'):
        if dest is None:
            dest = Constant('rgb')

        super().__init__(id, parents, dest)

        self.flags = [i for i in dir(cv2) if i.startswith('COLOR_')]

    def apply(self, item, tgt):

        frm = item.color_space.upper()
        tgt = tgt.upper()

        item.id += f'-{self.id}({tgt})'
        item.color_space = tgt

        try:
            cvt = getattr(cv2, f'COLOR_{frm}2{tgt}')

        except AttributeError:
            raise

        item.img_mat = cv2.cvtColor(item.img_mat, cvt)

        yield item
