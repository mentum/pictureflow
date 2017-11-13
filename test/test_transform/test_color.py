from copy import deepcopy

from test.context import pf

import numpy as np
import unittest


class ColorMaskInitialize(unittest.TestCase):

    def test_colormask_has_correct_input_types(self):
        expected_input_types = [pf.Image, list]

        self.assertEqual(pf.transform.ColorMask._input_types, expected_input_types)

    def test_colormask_has_correct_output_type(self):
        expected_output_type = pf.Image

        self.assertEqual(pf.transform.ColorMask._output_type, expected_output_type)

    def test_colormask_initialize_defaults_id_to_colormask(self):
        mask = pf.transform.ColorMask(pf.Placeholder(out_type=pf.Image))

        self.assertEqual(mask.id, 'colormask')

    def test_colormask_initialize_defaults_colormask_to_empty_mask(self):
        empty_mask = [None, None, None]

        mask = pf.transform.ColorMask(pf.Placeholder(out_type=pf.Image))

        self.assertEqual(len(mask.parents), 2)
        self.assertIsInstance(mask.parents[1], pf.Constant)

        self.assertEqual(next(mask.parents[1]), empty_mask)

    def test_colormask_initialize_accepts_masks(self):
        target_mask = [138, 222, 156]

        mask = pf.transform.ColorMask(pf.Placeholder(out_type=pf.Image), pf.Constant(target_mask))

        self.assertEqual(len(mask.parents), 2)
        self.assertIsInstance(mask.parents[1], pf.Constant)

        self.assertEqual(next(mask.parents[1]), target_mask)


class TestColormaskApply(unittest.TestCase):

    def setUp(self):

        self.img_id = 'someID'

        self.img_data = np.random.randn(10, 10, 3)

        self.image = pf.Image(self.img_id, 'jpg', self.img_data)

        self.mask = pf.transform.ColorMask(pf.Placeholder(out_type=pf.Image), pf.Constant([None, None, None]))

    def test_colormask_apply_appends_to_img_id(self):
        data = [x for x in self.mask.apply(deepcopy(self.image), [None, None, None])]

        self.assertEqual(len(data), 1)
        self.assertEqual(data[0].id, f'{self.img_id}-{self.mask.id}')

    def test_colormask_apply_returns_different_image(self):
        data = [x for x in self.mask.apply(deepcopy(self.image), [120, 0, None])]

        self.assertEqual(len(data), 1)
        self.assertFalse(np.array_equal(data[0].img_mat, self.img_data))
