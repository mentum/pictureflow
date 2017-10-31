from pictureflow.core import Image, Node

import cv2
import numpy as np


class PathMask(Node):

    """
    Build a mask from a path and apply it to the image. All pixels inside the polygon defined by the path will be left
    intact, and all those outside will be converted to black.
    
    Args:
        parent (Node<Image>): Parent node
        path (Node<np.array>): List of points forming the path
    """

    _input_types = [Image, np.ndarray]
    _output_type = Image

    def __init__(self, parent, path, id='path_mask'):
        super().__init__(id, parent, path)

    def apply(self, item, pth):

        item.id += f'-{self.id}'
        img = item.img_mat

        mask = np.zeros(img.shape, np.uint8)
        channel_count = img.shape[2]

        ignore_mask_color = (255,) * channel_count
        cv2.fillPoly(mask, [pth], ignore_mask_color)

        item.img_mat = cv2.bitwise_and(img, mask)
        yield item
