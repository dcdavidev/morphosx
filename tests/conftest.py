import pytest
import io
import os
from PIL import Image
from morphosx.app.engine.processor import ImageProcessor, ImageFormat, ProcessingOptions

@pytest.fixture
def core_processor():
    """Returns the default ImageProcessor used by other engines."""
    return ImageProcessor()

@pytest.fixture
def sample_image():
    """Generates a real 100x100 JPEG image in memory."""
    img = Image.new("RGB", (100, 100), color=(255, 0, 0))
    buf = io.BytesIO()
    img.save(buf, format="JPEG")
    return buf.getvalue()

@pytest.fixture
def sample_text():
    """Sample text data."""
    return b"Hello MorphosX\nThis is a test document."

@pytest.fixture
def sample_json():
    """Sample JSON data."""
    return b'{"project": "morphosx", "status": "active"}'

@pytest.fixture
def sample_md():
    """Sample Markdown data."""
    return b"# MorphosX\n\n- High performance\n- Media processing"

@pytest.fixture
def options():
    """Default processing options."""
    return ProcessingOptions(width=200, height=200, format=ImageFormat.WEBP)
