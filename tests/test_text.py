import io
import pytest
from PIL import Image
from morphosx.app.engine.text import TextProcessor
from morphosx.app.engine.processor import ProcessingOptions, ImageFormat


def test_text_processor_render_json():
    """Test rendering JSON text to an image."""
    processor = TextProcessor()
    json_data = b'{"status": "ok", "code": 200, "message": "MorphosX rules"}'
    options = ProcessingOptions(format=ImageFormat.PNG)
    
    image_bytes = processor.render_to_image(json_data, "test.json", options)
    
    # Verify the output is a valid image
    with Image.open(io.BytesIO(image_bytes)) as img:
        assert img.format == "PNG"
        assert img.width > 0
        assert img.height > 0


def test_text_processor_render_markdown():
    """Test rendering Markdown text to an image."""
    processor = TextProcessor()
    md_data = b"# MorphosX\n\nThis is a **bold** test."
    options = ProcessingOptions(format=ImageFormat.WEBP)
    
    image_bytes = processor.render_to_image(md_data, "test.md", options)
    
    with Image.open(io.BytesIO(image_bytes)) as img:
        assert img.width > 0


def test_text_processor_minification():
    """Test text-to-text minification logic."""
    processor = TextProcessor()
    
    # JSON minification
    json_data = b'{\n  "a": 1,\n  "b": 2\n}'
    processed, mime = processor.process_text(json_data, "test.json")
    assert processed == b'{"a":1,"b":2}'
    assert mime == "application/json"
    
    # XML minification
    xml_data = b'<root>\n  <child>data</child>\n</root>'
    processed, mime = processor.process_text(xml_data, "test.xml")
    assert processed == b'<root><child>data</child></root>'
    assert mime == "application/xml"
