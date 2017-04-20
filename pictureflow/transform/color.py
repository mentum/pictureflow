from pictureflow import Constant
from pictureflow.core import Image, Node


class ColorMask(Node):

    _input_type = Image
    _output_type = Image

    def __init__(self, parent, color_mask=None, id='colormask'):
        super().__init__(parent, id)

        if color_mask is None:
            color_mask = Constant(value=[None, None, None])

        self.color_mask = color_mask

    def apply(self, item):
        item.id += '-colormask'

        mask = next(self.color_mask)

        img = item.img_mat

        for i, val in enumerate(mask):
            if val is not None:
                img[:, :, i] = val

        item.img_mat = img

        return item
