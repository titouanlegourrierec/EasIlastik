import unittest
from unittest.mock import patch, MagicMock
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from EasIlastik.run_ilastik import run_ilastik_probabilities

class TestRunIlastikProbabilities(unittest.TestCase):
    def setUp(self):
        # Mock setup
        self.input_path = "test_input"
        self.model_path = "test_model.ilp"
        self.result_base_path = "test_results"
        self.threshold = 128
        self.below_threshold_color = [0, 0, 0]
        self.channel_colors = [[255, 0, 0], [0, 255, 0], [0, 0, 255]]
        self.ilastik_script_path = "ilastik_script"

        # Create directories for testing
        os.makedirs(self.input_path, exist_ok=True)
        os.makedirs(self.result_base_path, exist_ok=True)

    def tearDown(self):
        # Remove directories after testing
        if os.path.exists(self.input_path):
            os.rmdir(self.input_path)
        if os.path.exists(self.result_base_path):
            os.rmdir(self.result_base_path)

    @patch("EasIlastik.run_ilastik.run_ilastik")
    @patch("EasIlastik.run_ilastik.treshold_probabilities")
    def test_run_ilastik_probabilities_success(self, mock_treshold_probabilities, mock_run_ilastik):
        mock_run_ilastik.return_value = None
        mock_treshold_probabilities.return_value = None

        try:
            run_ilastik_probabilities(
                input_path=self.input_path,
                model_path=self.model_path,
                result_base_path=self.result_base_path,
                threshold=self.threshold,
                below_threshold_color=self.below_threshold_color,
                channel_colors=self.channel_colors,
                deletion=False,
                ilastik_script_path=self.ilastik_script_path,
            )
        except Exception as e:
            self.fail(f"run_ilastik_probabilities raised an exception unexpectedly: {e}")

        # Verify that run_ilastik was called with the correct arguments
        mock_run_ilastik.assert_called_once_with(
            self.input_path,
            self.model_path,
            self.result_base_path,
            self.ilastik_script_path,
            export_source="Probabilities",
            output_format="hdf5",
        )

        # Verify that treshold_probabilities was called with the correct arguments
        mock_treshold_probabilities.assert_called_once_with(
            self.result_base_path,
            self.threshold,
            self.below_threshold_color,
            self.channel_colors,
            False,
        )

if __name__ == "__main__":
    unittest.main()
