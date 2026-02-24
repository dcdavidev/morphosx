import io
import pytest
from PIL import Image
import pillow_heif
from morphosx.app.engine.processor import ImageProcessor, ProcessingOptions, ImageFormat

def test_image_processor_heif_support():
    """
    Verify that ImageProcessor can open and convert a HEIF file.
    Since we don't have a real HEIF file, we'll create a dummy one using pillow_heif.
    """
    processor = ImageProcessor()
    
    # Create a dummy HEIF in memory
    img = Image.new("RGB", (100, 100), color=(0, 255, 0))
    heif_file = pillow_heif.from_pillow(img)
    buffer = io.BytesIO()
    heif_file.save(buffer)
    heif_bytes = buffer.getvalue()
    
    options = ProcessingOptions(width=50, format=ImageFormat.WEBP)
    processed_bytes, mime_type = processor.process(heif_bytes, options)
    
    assert mime_type == "image/webp"
    with Image.open(io.BytesIO(processed_bytes)) as result_img:
        assert result_img.width == 50
        assert result_img.format == "WEBP"

if __name__ == "__main__":
    test_image_processor_heif_support()
    print("HEIF test passed!")
