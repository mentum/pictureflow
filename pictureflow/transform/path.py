from pictureflow.core import Image, Node

import cv2
import numpy as np


class PathMask(Node):

    _input_type = Image
    _output_type = Image

    def __init__(self, parent, path, id='path-mask'):
        super().__init__(path, id)

        self.paths = path

    def apply(self, img):

        pth = next(self.paths)

        mask = np.zeros(img.shape, np.uint8)
        channel_count = img.shape[2]

        ignore_mask_color = (255,) * channel_count
        cv2.fillPoly(mask, [pth], ignore_mask_color)
        return cv2.bitwise_and(img, mask)
