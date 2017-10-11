from pictureflow.core import Image, Node

import cv2


class ObjectDetector(Node):

    _input_type = Image
    _output_type = Image

    def __init__(self, parent, path_drop_threshold, tgt_size, id='detect_obj'):
        super().__init__(parent, id)

        self.drop_threshold = path_drop_threshold
        self.tgt_size = tgt_size

    def apply(self, item):
        item.id = f'{item.id}-{self.id}'
        img_raw = item.img_mat

        gray = cv2.cvtColor(img_raw, cv2.COLOR_BGR2GRAY)

        gray[gray > 0] = 255
        _, contours, _ = cv2.findContours(gray, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

        drop_thresh = next(self.drop_threshold)
        tgt_size = next(self.tgt_size)

        # Crop around each object
        dropped = 0
        for i, obj_contour in enumerate(contours):
            max_x = obj_contour[:, :, 0].max()
            min_x = obj_contour[:, :, 0].min()

            max_y = obj_contour[:, :, 1].max()
            min_y = obj_contour[:, :, 1].min()

            if (max_x - min_x) * (max_y - min_y) <= drop_thresh:
                dropped += 1
                continue

            object_width = max_x - min_x
            object_height = max_y - min_y

            window_width = int(round(max([object_width, object_height]) / tgt_size) * tgt_size)

            x_delta = (window_width - object_width) // 2
            y_delta = (window_width - object_height) // 2

            start_x = int(min_x - x_delta)
            start_y = int(min_y - y_delta)

            new_img = img_raw[start_y:start_y + window_width, start_x:start_x + window_width]

            new_item = Image(f'{item.id}-seq_{i - dropped}', item.ext, cv2.resize(new_img, (tgt_size, tgt_size)))
            yield new_item
