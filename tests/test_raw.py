import io
import unittest
from unittest.mock import patch, MagicMock
from PIL import Image
import numpy as np

from morphosx.app.engine.raw import RawProcessor


class TestRawProcessor(unittest.TestCase):

    @patch("morphosx.app.engine.raw.rawpy")
    def test_extract_preview(self, mock_rawpy):
        # Create a dummy 10x10 RGB numpy array
        dummy_rgb = np.zeros((10, 10, 3), dtype=np.uint8)
        dummy_rgb[:, :, 0] = 255  # Solid red

        # Mock the rawpy imread object and its postprocess method
        mock_raw_instance = MagicMock()
        mock_raw_instance.postprocess.return_value = dummy_rgb
        
        # mock_rawpy.imread returns a context manager that yields mock_raw_instance
        mock_imread_cm = MagicMock()
        mock_imread_cm.__enter__.return_value = mock_raw_instance
        mock_rawpy.imread.return_value = mock_imread_cm

        processor = RawProcessor()
        dummy_raw_bytes = b"dummy_raw_data"
        
        result_bytes = processor.extract_preview(dummy_raw_bytes)
        
        # Assertions
        mock_rawpy.imread.assert_called_once()
        mock_raw_instance.postprocess.assert_called_once_with(use_camera_wb=True, half_size=False)
        
        # Verify the returned bytes form a valid JPEG image
        with Image.open(io.BytesIO(result_bytes)) as result_img:
            self.assertEqual(result_img.format, "JPEG")
            self.assertEqual(result_img.size, (10, 10))

    @patch("morphosx.app.engine.raw.rawpy")
    def test_extract_preview_failure(self, mock_rawpy):
        mock_rawpy.imread.side_effect = Exception("Mocked parsing error")
        
        processor = RawProcessor()
        
        with self.assertRaises(RuntimeError) as context:
            processor.extract_preview(b"invalid_data")
            
        self.assertIn("RAW image processing failed", str(context.exception))
        self.assertIn("Mocked parsing error", str(context.exception))

if __name__ == "__main__":
    unittest.main()
