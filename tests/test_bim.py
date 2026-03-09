import pytest
import io
import json
from PIL import Image
from morphosx.app.engine.bim import BIMProcessor
from morphosx.app.engine.processor import ProcessingOptions, ImageFormat

def test_bim_processor_ifc_to_image(core_processor, real_ifc, options):
    """Test rendering an IFC file to a technical data card image."""
    processor = BIMProcessor(core_processor)
    
    # Process as image (WebP)
    processed_bytes, mime_type = processor.process(real_ifc, options, filename="house.ifc")
    
    assert mime_type == "image/webp"
    assert len(processed_bytes) > 0
    
    # Verify it's a valid image
    img = Image.open(io.BytesIO(processed_bytes))
    assert img.width == options.width

def test_bim_processor_metadata_json(core_processor, real_ifc):
    """Test extracting structural metadata from a real IFC file as JSON."""
    processor = BIMProcessor(core_processor)
    
    # Explicitly request JSON output
    options = ProcessingOptions(format=ImageFormat.JSON)
    processed_bytes, mime_type = processor.process(real_ifc, options, filename="house.ifc")
    
    assert mime_type == "application/json"
    metadata = json.loads(processed_bytes.decode("utf-8"))
    
    assert "type" in metadata
    assert metadata["type"] == "BIM"
    assert "element_count" in metadata
    # Even if empty, the keys should exist
    assert "walls" in metadata["element_count"]
