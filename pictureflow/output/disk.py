from pictureflow.core import Image, Node

import cv2
import os


class DiskOutput(Node):

    """
    Output an image to disk
    
    Args:
        parent (Node<Image>): Parent node
        base_path (Node<string>): Output directory (will be created if nonexistent
        id (str): ID of the node
    """

    _input_types = [Image, str]
    _output_type = Image

    def __init__(self, parent, base_path, id='disk'):
        super().__init__(id, parent, base_path)

    def apply(self, img, pth):

        if not os.path.isdir(pth):
            os.mkdir(pth)

        cv2.imwrite(os.path.join(pth, str(img)), img.img_mat)

        yield img
