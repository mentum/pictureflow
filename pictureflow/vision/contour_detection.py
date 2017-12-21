from pictureflow.core import Image, Node

import cv2


class ContourDetector(Node):

    """
    Performs contour detection steps on an already masked binary image.

    Args:
        parent (Node): Parent image nodes
        drop_threshold (Node): Minimum allowed contour area

    Attributes:
        Input Types: [ :py:class:`Image`, :py:class:`int` ]
        Output Type: :py:class:`list`
    """

    _input_types = [Image, int]
    _output_type = list

    def __init__(self, parent, drop_threshold, id='contour_detect'):
        super().__init__(id, parent, drop_threshold)

    def apply(self, item, threshold):

        img = item.img_mat

        img[img > 0] = 255
        _, contours, _ = cv2.findContours(img, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

        valid_contours = []

        for contour in contours:
            max_x = contour[:, :, 0].max()
            min_x = contour[:, :, 0].min()

            max_y = contour[:, :, 1].max()
            min_y = contour[:, :, 1].min()

            if (max_x - min_x) * (max_y - min_y) > threshold:
                valid_contours.append(contour)

        yield valid_contours
