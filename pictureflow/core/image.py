class Image(object):

    def __init__(self, id, ext, img_mat, color_space='bgr'):
        self.id = id
        self.ext = ext

        self.color_space = color_space

        self.img_mat = img_mat

    def __str__(self):
        return "{0}.{1}".format(self.id, self.ext)

    def __repr__(self):
        return self.__str__()
