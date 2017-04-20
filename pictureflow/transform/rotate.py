from pictureflow import Constant
from pictureflow.core import Image, Node

import cv2


class Rotate(Node):

    _input_type = Image
    _output_type = Image

    def __init__(self, parent, rot_angle=None, id='rotate'):
        super().__init__(parent, id)

        if rot_angle is None:
            rot_angle = Constant(value=90)

        self.rot_angle = rot_angle

    def apply(self, item):
        rotation = next(self.rot_angle)

        item.id += '-rotate' + str(rotation)
        img = item.img_mat

        rows, cols = img.shape[:2]

        M = cv2.getRotationMatrix2D((cols / 2, rows / 2), rotation, 1)

        dst = cv2.warpAffine(img, M, (cols, rows))

        item.img_mat = dst

        return item
