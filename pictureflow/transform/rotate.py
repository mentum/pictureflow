from pictureflow import Constant
from pictureflow.core import Image, Node

import cv2


class Rotate(Node):

    """
    Rotate an image.
    
    Args:
        parent (Node<Image>): Parent node
        rot_angle (Node<int>): Angle of rotation (defaults to 90 degrees when left blank)
        id (str): ID of the node
    """

    _input_types = [Image, int]
    _output_type = Image

    def __init__(self, parent, rot_angle=None, id='rotate'):
        if rot_angle is None:
            rot_angle = Constant(value=90)

        super().__init__(id, parent, rot_angle)

    def apply(self, item, rotation):

        item.id += f'-{self.id}({rotation})'
        img = item.img_mat

        rows, cols = img.shape[:2]

        M = cv2.getRotationMatrix2D((cols / 2, rows / 2), rotation, 1)

        dst = cv2.warpAffine(img, M, (cols, rows))

        item.img_mat = dst

        yield item
