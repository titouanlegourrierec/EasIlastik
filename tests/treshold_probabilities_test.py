import unittest
from unittest.mock import patch, MagicMock
import os
import numpy as np
import h5py
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from EasIlastik.run_ilastik import treshold_probabilities

class TestTresholdProbabilities(unittest.TestCase):
    def setUp(self):
        # Create a mock .h5 file and directory for testing
        self.file_path = "test_file.h5"
        self.dir_path = "test_dir"
        self.threshold = 0.5
        self.below_threshold_color = [0, 0, 0]
        self.channel_colors = [[255, 0, 0], [0, 255, 0], [0, 0, 255]]

        os.makedirs(self.dir_path, exist_ok=True)
        with h5py.File(self.file_path, "w") as f:
            data_shape = (10, 10, len(self.channel_colors))
            data = np.random.rand(*data_shape)
            f.create_dataset("exported_data", data=data)

        with h5py.File(os.path.join(self.dir_path, "test_file_1.h5"), "w") as f:
            f.create_dataset("exported_data", data=np.random.rand(*data_shape))

        with h5py.File(os.path.join(self.dir_path, "test_file_2.h5"), "w") as f:
            f.create_dataset("exported_data", data=np.random.rand(*data_shape))

    def tearDown(self):
        # Remove the mock .h5 file and directory created for testing
        if os.path.exists(self.file_path):
            os.remove(self.file_path)

        if os.path.exists(self.dir_path):
            for filename in os.listdir(self.dir_path):
                os.remove(os.path.join(self.dir_path, filename))
            os.rmdir(self.dir_path)

    @patch("EasIlastik.run_ilastik.process_single_file")
    def test_treshold_probabilities_file(self, mock_process_single_file):
        mock_process_single_file.return_value = None

        try:
            treshold_probabilities(
                file_or_dir_path=self.file_path,
                threshold=self.threshold,
                below_threshold_color=self.below_threshold_color,
                channel_colors=self.channel_colors,
                deletion=False,
            )
        except Exception as e:
            self.fail(f"treshold_probabilities raised an exception unexpectedly: {e}")

        # Verify process_single_file was called once
        mock_process_single_file.assert_called_once_with(
            self.file_path,
            self.threshold,
            self.below_threshold_color,
            self.channel_colors,
            False,
        )

    @patch("EasIlastik.run_ilastik.process_single_file")
    def test_treshold_probabilities_directory(self, mock_process_single_file):
        mock_process_single_file.return_value = None

        try:
            treshold_probabilities(
                file_or_dir_path=self.dir_path,
                threshold=self.threshold,
                below_threshold_color=self.below_threshold_color,
                channel_colors=self.channel_colors,
                deletion=False,
            )
        except Exception as e:
            self.fail(f"treshold_probabilities raised an exception unexpectedly: {e}")

        # Verify process_single_file was called for each .h5 file in the directory
        expected_calls = [
            ((os.path.join(self.dir_path, "test_file_1.h5"), self.threshold, self.below_threshold_color, self.channel_colors, False),),
            ((os.path.join(self.dir_path, "test_file_2.h5"), self.threshold, self.below_threshold_color, self.channel_colors, False),),
        ]
        mock_process_single_file.assert_has_calls(expected_calls, any_order=True)

if __name__ == "__main__":
    unittest.main()
