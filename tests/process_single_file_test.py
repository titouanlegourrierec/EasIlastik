import unittest
from unittest.mock import patch, MagicMock
import os
import numpy as np
import h5py
import sys
import cv2

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from EasIlastik.run_ilastik import process_single_file

class TestProcessSingleFile(unittest.TestCase):
    def setUp(self):
        # Create a mock .h5 file for testing
        self.file_path = "test_file.h5"
        self.threshold = 0.5
        self.below_threshold_color = [0, 0, 0]
        self.channel_colors = [[255, 0, 0], [0, 255, 0], [0, 0, 255]]

        with h5py.File(self.file_path, "w") as f:
            data_shape = (10, 10, len(self.channel_colors))
            max_shape = (10, 10, None)  # Allow unlimited resizing in the third dimension
            data = np.random.rand(*data_shape)
            f.create_dataset("exported_data", data=data, chunks=True, maxshape=max_shape)

    def tearDown(self):
        # Remove the mock .h5 file and any generated .png files
        if os.path.exists(self.file_path):
            os.remove(self.file_path)
        png_file = self.file_path.replace(".h5", ".png")
        if os.path.exists(png_file):
            os.remove(png_file)

    @patch("cv2.imwrite")
    def test_process_single_file_success(self, mock_imwrite):
        mock_imwrite.return_value = True

        try:
            process_single_file(
                file_path=self.file_path,
                threshold=self.threshold,
                below_threshold_color=self.below_threshold_color,
                channel_colors=self.channel_colors,
                deletion=False,
            )
        except Exception as e:
            self.fail(f"process_single_file raised an exception unexpectedly: {e}")

        # Verify that cv2.imwrite was called
        mock_imwrite.assert_called_once()
        args, kwargs = mock_imwrite.call_args
        self.assertTrue(args[0].endswith(".png"))

    def test_file_not_found(self):
        with self.assertRaises(FileNotFoundError):
            process_single_file(
                file_path="non_existent_file.h5",
                threshold=self.threshold,
                below_threshold_color=self.below_threshold_color,
                channel_colors=self.channel_colors,
            )

    def test_invalid_below_threshold_color(self):
        with self.assertRaises(ValueError):
            process_single_file(
                file_path=self.file_path,
                threshold=self.threshold,
                below_threshold_color=[0, 0],  # Invalid length
                channel_colors=self.channel_colors,
            )

    def test_invalid_channel_colors(self):
        with self.assertRaises(ValueError):
            process_single_file(
                file_path=self.file_path,
                threshold=self.threshold,
                below_threshold_color=self.below_threshold_color,
                channel_colors=[[255, 0]],  # Invalid color format
            )

    def test_missing_exported_data(self):
        # Create a mock .h5 file without "exported_data"
        file_path = "invalid_file.h5"
        with h5py.File(file_path, "w") as f:
            f.create_dataset("other_data", data=np.random.rand(10, 10, 3))

        with self.assertRaises(ValueError):
            process_single_file(
                file_path=file_path,
                threshold=self.threshold,
                below_threshold_color=self.below_threshold_color,
                channel_colors=self.channel_colors,
            )

        os.remove(file_path)

    def test_channel_colors_mismatch(self):
        with h5py.File(self.file_path, "r+") as f:
            f["exported_data"].resize((10, 10, 5))  # Change number of channels

        with self.assertRaises(ValueError):
            process_single_file(
                file_path=self.file_path,
                threshold=self.threshold,
                below_threshold_color=self.below_threshold_color,
                channel_colors=self.channel_colors,
            )

if __name__ == "__main__":
    unittest.main()
