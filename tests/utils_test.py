import unittest
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from EasIlastik.utils import get_image_paths

class TestUtils(unittest.TestCase):
    def setUp(self):
        # Create a temporary directory and some dummy files for testing
        self.test_dir = "test_images"
        os.makedirs(self.test_dir, exist_ok=True)
        self.test_files = ["image1.jpg", "image2.png", "image3.bmp"]
        for file in self.test_files:
            open(os.path.join(self.test_dir, file), 'a').close()

    def tearDown(self):
        # Remove the temporary directory and its contents after the test
        for file in self.test_files:
            os.remove(os.path.join(self.test_dir, file))
        os.rmdir(self.test_dir)

    def test_get_image_paths(self):
        # Call the function and check the result
        result = get_image_paths(self.test_dir)
        expected = [os.path.join(self.test_dir, file) for file in self.test_files]
        self.assertCountEqual(result, expected)

if __name__ == '__main__':
    unittest.main()