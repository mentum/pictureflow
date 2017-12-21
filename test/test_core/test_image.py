from test.context import pf

import unittest


class TestImageInitialize(unittest.TestCase):

    def test_image_init_sets_id(self):
        img_id = 'hello'

        img = pf.Image(img_id, 'jpg', [[]])

        self.assertEqual(img.id, img_id)

    def test_image_init_sets_extension(self):
        img_ext = 'jpg'

        img = pf.Image('id', img_ext, [[]])

        self.assertEqual(img.ext, img_ext)

    def test_image_init_sets_img_mat(self):
        img_mat = [[]]

        img = pf.Image('id', 'jpg', img_mat)

        self.assertIs(img.img_mat, img_mat)

    def test_image_init_sets_color_space(self):
        color_space = 'rgb'

        img = pf.Image('id', 'jpg', [[]], color_space)

        self.assertEqual(img.color_space, color_space)

    def test_image_init_defaults_colorspace_to_bgr(self):
        img = pf.Image('id', 'jpb', [[]])

        self.assertEqual(img.color_space, 'bgr')


class TestImageRepresentations(unittest.TestCase):

    def setUp(self):
        self.img_id = 'some_id'
        self.ext = 'jpg'

        self.img = pf.Image(self.img_id, self.ext, [[]])

    def test_image_str_returns_formatted_filename(self):
        expected_filename = f'{self.img_id}.{self.ext}'

        self.assertEqual(str(self.img), expected_filename)

    def test_image_repr_returns_formatted_filename(self):
        expected_filename = f'{self.img_id}.{self.ext}'

        self.assertEqual(self.img.__repr__(), expected_filename)
