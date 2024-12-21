import unittest
import os
import sys
from unittest.mock import patch, mock_open

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from EasIlastik.find_ilastik import get_os, find_file, find_ilastik

class TestFindIlastik(unittest.TestCase):
    def test_get_os(self):
        # Check if the function returns the correct OS name
        self.assertIn(get_os(), ["Linux", "Darwin", "Windows"])

    @patch("os.walk")
    def test_find_file(self, mock_walk):
        # Mock the os.walk function to simulate the file system
        mock_walk.return_value = [
            ("test_dir", [], ["test_file.txt"])
        ]

        # Call the function and check the result
        result = find_file("test_file.txt", "test_dir")
        self.assertEqual(result, os.path.join("test_dir", "test_file.txt"))

    @patch("EasIlastik.find_ilastik.get_os")
    @patch("EasIlastik.find_ilastik.find_file")
    def test_find_ilastik(self, mock_find_file, mock_get_os):
        # Mock the get_os function to return a specific OS
        mock_get_os.return_value = "Darwin"
        mock_find_file.return_value = "/Applications/run_ilastik.sh"
        self.assertEqual(find_ilastik(), "/Applications/run_ilastik.sh")

        mock_get_os.return_value = "Linux"
        mock_find_file.return_value = "/run_ilastik.sh"
        self.assertEqual(find_ilastik(), "/run_ilastik.sh")

        mock_get_os.return_value = "Windows"
        mock_find_file.return_value = "C:\\ilastik.exe"
        self.assertEqual(find_ilastik(), "C:\\ilastik.exe")

if __name__ == '__main__':
    unittest.main()