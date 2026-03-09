import io

import pytest
from PIL import Image

from morphosx.app.engine.types import ImageFormat, ProcessingOptions
from morphosx.app.engine.vips import VipsProcessor


def is_vips_installed():
    try:
        import pyvips

        # Test if we can actually call a vips function (might fail if .so is missing)
        pyvips.Image.new_from_memory(b"\0" * 10, 1, 1, 3, "uchar")
        return True
    except (ImportError, Exception):
        return False


@pytest.mark.skipif(not is_vips_installed(), reason="libvips or pyvips not installed")
def test_vips_processor_resize(sample_image, options):
    """
    Validate the VipsProcessor resizing functionality.
    """
    processor = VipsProcessor()

    # Resize to 50px width
    options = ProcessingOptions(width=50, format=ImageFormat.WEBP)
    processed_bytes, mime_type = processor.process(sample_image, options)

    assert mime_type == "image/webp"

    # Check dimensions
    img = Image.open(io.BytesIO(processed_bytes))
    assert img.width == 50


@pytest.mark.skipif(not is_vips_installed(), reason="libvips or pyvips not installed")
def test_vips_processor_format_conversion(sample_image):
    """
    Test format conversion using PyVips.
    """
    processor = VipsProcessor()

    options = ProcessingOptions(format=ImageFormat.PNG)
    processed_bytes, mime_type = processor.process(sample_image, options)

    assert mime_type == "image/png"
    img = Image.open(io.BytesIO(processed_bytes))
    assert img.format == "PNG"
