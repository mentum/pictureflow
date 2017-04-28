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

    _input_type = Image

    def __init__(self, parent, base_path, id='disk-output'):
        super().__init__(parent, id)
        self.base_path = base_path

    def apply(self, img):
        pth = next(self.base_path)

        if not os.path.isdir(pth):
            os.mkdir(pth)

        cv2.imwrite(os.path.join(pth, str(img)), img.img_mat)

        return img
