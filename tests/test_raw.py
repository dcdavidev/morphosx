import pytest
from unittest.mock import MagicMock, patch
from morphosx.app.engine.raw import RawProcessor

def test_raw_processor_extract_preview_mocked(core_processor, sample_image, options):
    """
    Test RawProcessor with mocked rawpy to avoid actual RAW files.
    """
    processor = RawProcessor(core_processor)
    
    # Since rawpy is imported inside the method, we mock it via sys.modules 
    # or by patching where it is used.
    with patch("rawpy.imread") as mock_imread:
        mock_raw = MagicMock()
        mock_imread.return_value.__enter__.return_value = mock_raw
        
        # mock_raw.postprocess returns a numpy array. 
        # We can just return a simple array that PIL can convert.
        import numpy as np
        mock_raw.postprocess.return_value = np.zeros((100, 100, 3), dtype=np.uint8)
        
        processed_bytes, mime_type = processor.process(b"fake-raw-data", options, filename="test.cr2")
        
        assert mime_type == "image/webp"
        assert len(processed_bytes) > 0
        mock_imread.assert_called_once()

def test_raw_processor_import_error(core_processor, options):
    """Test behavior when rawpy is not installed."""
    processor = RawProcessor(core_processor)
    
    with patch("builtins.__import__", side_effect=ImportError("rawpy")):
        with pytest.raises(RuntimeError) as exc:
            processor.process(b"data", options, filename="test.cr2")
        assert "rawpy or imageio is not installed" in str(exc.value)
