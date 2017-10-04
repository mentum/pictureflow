from pictureflow.core import Image, Node

import cv2
import numpy as np


class FitToSize(Node):

    _input_type = Image
    _output_type = Image

    def __init__(self, parent, tgt_size, id='size_fit'):
        super().__init__(parent, id)
        self.tgt_size = tgt_size

    def apply(self, item):
        img_raw = item.img_mat
        tgt_size = next(self.tgt_size)

        item.id += f'-{self.id}{tgt_size}'

        # Sum RGB values to make identification of null pixels easier
        summed = np.sum(img_raw, axis=2)
        nonzero_y, nonzero_x = np.nonzero(summed)

        min_y = nonzero_y.min()
        max_y = nonzero_y.max()

        min_x = nonzero_x.min()
        max_x = nonzero_x.max()

        object_width = max_x - min_x
        object_height = max_y - min_y

        window_width = int(round(max([object_width, object_height]) / tgt_size) * tgt_size)

        x_delta = (window_width - object_width) // 2
        y_delta = (window_width - object_height) // 2

        start_x = int(min_x - x_delta)
        start_y = int(min_y - y_delta)

        new_img = img_raw[start_y:start_y + window_width, start_x:start_x + window_width]

        item.img_mat = cv2.resize(new_img, (tgt_size, tgt_size))
        return item
