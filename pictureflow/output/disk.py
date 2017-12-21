from pictureflow.core import Image, Node

import cv2
import os


class DiskOutput(Node):

    """
    Output an image to disk
    
    Args:
        parent (Node): Parent node
        base_path (Node): Output directory (will be created if nonexistent)
        id (str): ID of the node

    Attributes:
        Input Types: [ :py:class:`Image`, :py:class:`str` ]
        Output Type: :py:class:`Image`
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
