from pictureflow.core import Image, Node

import cv2


class Scale(Node):

    """
    Scale an image
    
    Args:
        parent (Node): Parent image node
        scale_factor (Node): Scale factor
        id (str): ID of the node

    Attributes:
        Input Types: [ :py:class:`Image`, :py:class:`int` ]
        Output Type: :py:class:`Image`
    """

    _input_types = [Image, float]
    _output_type = Image

    def __init__(self, parent, scale_factor, id='scale'):
        super().__init__(id, parent, scale_factor)

    def apply(self, image, scaling):
        image.id += f'-{self.id}({scaling})'

        height, width = image.img_mat.shape[:2]
        image.img_mat = cv2.resize(image.img_mat, (int(scaling * width), int(scaling * height)))

        yield image
