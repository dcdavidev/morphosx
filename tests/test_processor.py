import io
import time
from PIL import Image
from morphosx.app.engine.processor import ImageProcessor, ProcessingOptions, ImageFormat


def create_sample_image(width: int = 1920, height: int = 1080) -> bytes:
    """Generate a dummy RGB image for testing purposes."""
    img = Image.new("RGB", (width, height), color=(255, 0, 0))
    buffer = io.BytesIO()
    img.save(buffer, format="JPEG")
    return buffer.getvalue()


def test_image_processor_resize_and_convert():
    """
    Test 1: Full pipeline validation.
    Check if a 1080p JPEG can be converted to a 300px width WebP.
    """
    processor = ImageProcessor()
    source_data = create_sample_image()
    
    options = ProcessingOptions(width=300, format=ImageFormat.WEBP, quality=80)
    
    start_time = time.perf_counter()
    processed_bytes, mime_type = processor.process(source_data, options)
    execution_time = time.perf_counter() - start_time
    
    # Assertions
    assert mime_type == "image/webp"
    assert len(processed_bytes) > 0
    
    # Validate result image dimensions
    with Image.open(io.BytesIO(processed_bytes)) as result_img:
        assert result_img.width == 300
        # Check aspect ratio preservation (1920/1080 = 1.777, 300/1.777 ~= 168)
        assert result_img.height == 168
        assert result_img.format == "WEBP"

    print(f"\n[PASS] Processing time: {execution_time:.4f}s")


def test_image_processor_no_dimensions():
    """
    Test 2: Format-only conversion.
    Check if format can be changed without resizing.
    """
    processor = ImageProcessor()
    source_data = create_sample_image(500, 500)
    
    options = ProcessingOptions(format=ImageFormat.PNG)
    processed_bytes, mime_type = processor.process(source_data, options)
    
    assert mime_type == "image/png"
    with Image.open(io.BytesIO(processed_bytes)) as result_img:
        assert result_img.size == (500, 500)
        assert result_img.format == "PNG"


def test_image_processor_aspect_ratio_height():
    """
    Test 3: Height-only resize.
    Ensure width is calculated correctly when only height is provided.
    """
    processor = ImageProcessor()
    source_data = create_sample_image(1000, 500) # 2:1 ratio
    
    options = ProcessingOptions(height=250)
    processed_bytes, _ = processor.process(source_data, options)
    
    with Image.open(io.BytesIO(processed_bytes)) as result_img:
        assert result_img.width == 500
        assert result_img.height == 250


if __name__ == "__main__":
    test_image_processor_resize_and_convert()
    test_image_processor_no_dimensions()
    test_image_processor_aspect_ratio_height()
    print("All tests passed!")
