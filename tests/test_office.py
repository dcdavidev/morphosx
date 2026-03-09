import pytest
import io
from PIL import Image
from morphosx.app.engine.office import OfficeProcessor
from morphosx.app.engine.processor import ProcessingOptions, ImageFormat

def test_office_processor_docx_to_image(core_processor, real_docx, options):
    """Test rendering a real DOCX document to an image."""
    processor = OfficeProcessor(core_processor)
    
    # Requesting an image output (WebP)
    processed_bytes, mime_type = processor.process(real_docx, options, filename="test.docx")
    
    assert mime_type == "image/webp"
    assert len(processed_bytes) > 0
    
    # Verify it's a valid image
    img = Image.open(io.BytesIO(processed_bytes))
    assert img.width == options.width
