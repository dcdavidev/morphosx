
from morphosx.app.engine.processor import ImageFormat, ProcessingOptions
from morphosx.app.engine.text import TextProcessor


def test_text_processor_render_json(core_processor, sample_json, options):
    """Test rendering JSON text to an image."""
    processor = TextProcessor(core_processor)

    # Requesting an image format (WebP from options)
    processed_bytes, mime_type = processor.process(
        sample_json, options, filename="test.json"
    )

    assert mime_type == "image/webp"
    assert len(processed_bytes) > 0


def test_text_processor_render_markdown(core_processor, sample_md, options):
    """Test rendering Markdown text to an image."""
    processor = TextProcessor(core_processor)

    processed_bytes, mime_type = processor.process(
        sample_md, options, filename="test.md"
    )

    assert mime_type == "image/webp"
    assert len(processed_bytes) > 0


def test_text_processor_minification(core_processor, sample_json):
    """Test text-to-text minification logic."""
    processor = TextProcessor(core_processor)

    # Requesting JSON output format explicitly
    options = ProcessingOptions(format=ImageFormat.JSON)
    processed_bytes, mime_type = processor.process(
        sample_json, options, filename="test.json"
    )

    assert mime_type == "application/json"
    # Minified version should have no spaces
    assert b" " not in processed_bytes
    assert b"morphosx" in processed_bytes


def test_text_processor_markdown_to_html(core_processor, sample_md):
    """Test markdown to HTML conversion."""
    processor = TextProcessor(core_processor)

    # Markdown format usually results in text/html or application/x-markdown
    # Based on TextProcessor.process_text, it returns text/html
    options = ProcessingOptions(
        format=ImageFormat.MD
    )  # Assuming MD is in ImageFormat enum
    processed_bytes, mime_type = processor.process(
        sample_md, options, filename="test.md"
    )

    assert mime_type == "text/html"
    assert b"<h1>MorphosX</h1>" in processed_bytes
