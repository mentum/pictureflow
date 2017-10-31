class Image(object):

    """
    Base model representing an image. Most stock pictureflow nodes operate on it.
    
    Args:
        id (str): ID of the image
        ext (str): Extension of the image
        img_mat (cv2.Mat): Image matrix, as loaded by OpenCV
        color_space (str): Color space of the image, defaults to BGR (which is the default colorspace used by OpenCV)
    """

    def __init__(self, id, ext, img_mat, color_space='bgr'):
        self.id = id
        self.ext = ext

        self.color_space = color_space

        self.img_mat = img_mat

    def __str__(self):
        return "{0}.{1}".format(self.id, self.ext)

    def __repr__(self):
        return self.__str__()
