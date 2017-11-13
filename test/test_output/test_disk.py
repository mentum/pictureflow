from test.context import pf

from unittest.mock import MagicMock, patch

import unittest


class TestDiskInitialize(unittest.TestCase):

    def test_diskoutput_has_correct_input_types(self):
        expected_input_types = [pf.Image, str]

        self.assertEqual(pf.output.DiskOutput._input_types, expected_input_types)

    def test_diskoutput_has_correct_output_type(self):
        expected_output_type = pf.Image

        self.assertEqual(pf.output.DiskOutput._output_type, expected_output_type)

    def test_diskoutput_defaults_id_to_disk(self):
        disk = pf.output.DiskOutput(pf.Placeholder(out_type=pf.Image), pf.Placeholder(out_type=str))

        self.assertEqual(disk.id, 'disk')


class TestDiskOutputApply(unittest.TestCase):

    def setUp(self):
        self.disk = pf.output.DiskOutput(pf.Placeholder(out_type=pf.Image), pf.Placeholder(out_type=str))


    @patch('pictureflow.output.disk.cv2.imwrite', MagicMock())
    @patch('pictureflow.output.disk.os.path.isdir', MagicMock(return_value=False))
    @patch('pictureflow.output.disk.os.mkdir')
    def test_disk_output_apply_creates_folder_if_doesnt_exist(self, mock_mkdir):
        [x for x in self.disk.apply(pf.Image('hello', 'jpg', [[]]), 'some/path')]

        self.assertTrue(mock_mkdir.called)

    @patch('pictureflow.output.disk.cv2.imwrite', MagicMock())
    @patch('pictureflow.output.disk.os.path.isdir', MagicMock(return_value=True))
    @patch('pictureflow.output.disk.os.mkdir')
    def test_disk_output_apply_doesnt_create_folder_if_it_exists(self, mock_mkdir):
        [x for x in self.disk.apply(pf.Image('hello', 'jpg', [[]]), 'some/path')]

        self.assertFalse(mock_mkdir.called)

    @patch('pictureflow.output.disk.cv2.imwrite')
    @patch('pictureflow.output.disk.os.path.isdir', MagicMock(return_value=True))
    @patch('pictureflow.output.disk.os.mkdir', MagicMock())
    def test_disk_output_calls_cv_imwrite(self, mock_imwrite):
        [x for x in self.disk.apply(pf.Image('hello', 'jpg', [[]]), 'some/path')]

        self.assertTrue(mock_imwrite.called)

    @patch('pictureflow.output.disk.cv2.imwrite', MagicMock())
    @patch('pictureflow.output.disk.os.path.isdir', MagicMock(return_value=True))
    @patch('pictureflow.output.disk.os.mkdir', MagicMock())
    def test_disk_output_yields_image(self):
        img = pf.Image('hello', 'jpg', [[]])
        output = [x for x in self.disk.apply(img, 'some/path')]

        self.assertEqual(len(output), 1)
        self.assertIs(img, output[0])
