from pictureflow.core import Image, Node, Constant

from pictureflow.flow import Broadcast
from pictureflow.transform import Convert
from pictureflow.vision import ContourDetector


import cv2


class ObjectDetector(Node):

    _input_types = [Image, list, int]
    _output_type = Image

    def __init__(self, parent, path_drop_threshold, tgt_size, id='detect_obj'):

        # Broadcast to send the raw image to the object detector & to the contour detector
        broadcast = Broadcast(parent, Constant(2))

        # Contour detection branch
        grayscale = Convert(broadcast, Constant('gray'))
        contours = ContourDetector(grayscale, path_drop_threshold)

        super().__init__(id, broadcast, contours, tgt_size)

    def apply(self, item, contours, tgt_size):
        item.id += f'-{self.id}'
        img_raw = item.img_mat

        # Crop around each object
        dropped = 0
        for i, obj_contour in enumerate(contours):
            max_x = obj_contour[:, :, 0].max()
            min_x = obj_contour[:, :, 0].min()

            max_y = obj_contour[:, :, 1].max()
            min_y = obj_contour[:, :, 1].min()

            object_width = max_x - min_x
            object_height = max_y - min_y

            window_width = int(round(max([object_width, object_height]) / tgt_size) * tgt_size)

            x_delta = (window_width - object_width) // 2
            y_delta = (window_width - object_height) // 2

            start_x = int(min_x - x_delta)
            start_y = int(min_y - y_delta)

            new_img = img_raw[start_y:start_y + window_width, start_x:start_x + window_width]

            new_item = Image(f'{item.id}({i - dropped})', item.ext, cv2.resize(new_img, (tgt_size, tgt_size)))
            yield new_item
