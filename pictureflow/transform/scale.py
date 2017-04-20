from pictureflow.core import Image, Node

import cv2


class Scale(Node):

    _input_type = Image
    _output_type = Image

    def __init__(self, parent, scale_factor, id='scale'):
        super().__init__(parent, id)
        self.scale_factor = scale_factor

    def apply(self, image):
        scaling = next(self.scale_factor)
        image.id += '-scale' + str(scaling)

        height, width = image.img_mat.shape[:2]
        image.img_mat = cv2.resize(image.img_mat, (int(scaling * width), int(scaling * height)))

        return image
