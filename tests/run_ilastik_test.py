import unittest
from unittest.mock import patch, MagicMock
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from EasIlastik.run_ilastik import run_ilastik

class TestRunIlastik(unittest.TestCase):
    def setUp(self):
        # Define sample inputs for the test
        self.input_path = "test_images"
        self.model_path = "test_model.ilp"
        self.result_base_path = "test_results/"
        self.ilastik_script_path = "ilastik_script"
        
        # Mock file and directory existence
        os.makedirs(self.input_path, exist_ok=True)
        os.makedirs(self.result_base_path, exist_ok=True)
        with open(self.model_path, "w") as f:
            f.write("")

    def tearDown(self):
        # Clean up the files and directories created during setup
        if os.path.exists(self.input_path):
            os.rmdir(self.input_path)
        if os.path.exists(self.result_base_path):
            os.rmdir(self.result_base_path)
        if os.path.exists(self.model_path):
            os.remove(self.model_path)

    @patch("subprocess.run")
    @patch("os.path.isfile")
    @patch("os.path.isdir")
    def test_run_ilastik_success(self, mock_isdir, mock_isfile, mock_subprocess_run):
        mock_isfile.side_effect = lambda path: path == self.model_path
        mock_isdir.side_effect = lambda path: path == self.input_path
        mock_subprocess_run.return_value = MagicMock()

        try:
            run_ilastik(
                input_path=self.input_path,
                model_path=self.model_path,
                result_base_path=self.result_base_path,
                ilastik_script_path=self.ilastik_script_path,
                export_source="Simple Segmentation",
                output_format="png",
            )
        except Exception as e:
            self.fail(f"run_ilastik raised an exception unexpectedly: {e}")

        # Assert subprocess.run was called with the correct arguments
        mock_subprocess_run.assert_called_once()
        args, kwargs = mock_subprocess_run.call_args
        self.assertIn(self.ilastik_script_path, args[0])
        self.assertIn("--headless", args[0])
        self.assertIn(f"--project={self.model_path}", args[0])

    @patch("os.path.isfile")
    @patch("os.path.isdir")
    def test_invalid_input_path(self, mock_isdir, mock_isfile):
        mock_isfile.return_value = False
        mock_isdir.return_value = False

        with self.assertRaises(FileNotFoundError):
            run_ilastik(
                input_path="invalid_path",
                model_path=self.model_path,
                result_base_path=self.result_base_path,
                ilastik_script_path=self.ilastik_script_path,
            )

    def test_invalid_export_source(self):
        with self.assertRaises(ValueError):
            run_ilastik(
                input_path=self.input_path,
                model_path=self.model_path,
                result_base_path=self.result_base_path,
                ilastik_script_path=self.ilastik_script_path,
                export_source="Invalid Source",
            )

    def test_invalid_output_format(self):
        with self.assertRaises(ValueError):
            run_ilastik(
                input_path=self.input_path,
                model_path=self.model_path,
                result_base_path=self.result_base_path,
                ilastik_script_path=self.ilastik_script_path,
                output_format="invalid_format",
            )

if __name__ == "__main__":
    unittest.main()
