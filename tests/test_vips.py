import io
import pytest
from PIL import Image
from morphosx.app.engine.vips import VipsProcessor
from morphosx.app.engine.processor import ProcessingOptions, ImageFormat


def create_sample_image(width: int = 100, height: int = 100) -> bytes:
    """Generate a dummy RGB image for testing purposes."""
    img = Image.new("RGB", (width, height), color=(255, 0, 0))
    buffer = io.BytesIO()
    img.save(buffer, format="JPEG")
    return buffer.getvalue()


def test_vips_processor_resize():
    """
    Validate the VipsProcessor resizing functionality.
    """
    processor = VipsProcessor()
    source_data = create_sample_image(1000, 500)
    
    # Resize to 500px width
    options = ProcessingOptions(width=500, format=ImageFormat.WEBP)
    processed_bytes, mime_type = processor.process(source_data, options)
    
    assert mime_type == "image/webp"
    
    with Image.open(io.BytesIO(processed_bytes)) as result_img:
        assert result_img.width == 500
        assert result_img.height == 250


def test_vips_processor_format_conversion():
    """
    Test format conversion using PyVips.
    """
    processor = VipsProcessor()
    source_data = create_sample_image(100, 100)
    
    options = ProcessingOptions(format=ImageFormat.PNG)
    processed_bytes, mime_type = processor.process(source_data, options)
    
    assert mime_type == "image/png"
    
    with Image.open(io.BytesIO(processed_bytes)) as result_img:
        assert result_img.format == "PNG"

if __name__ == "__main__":
    test_vips_processor_resize()
    test_vips_processor_format_conversion()
    print("Vips tests passed!")
