import io
import json
import xml.dom.minidom
from typing import Tuple, Optional

import markdown
from pygments import highlight
from pygments.lexers import get_lexer_by_name, get_lexer_for_filename, ClassNotFound
from pygments.formatters import ImageFormatter
from PIL import Image

from morphosx.app.engine.processor import ProcessingOptions, ImageFormat


class TextProcessor:
    """
    Core engine for processing and rendering text-based files (Markdown, JSON, XML).
    
    Can minify/prettify data or render it as a syntax-highlighted image.
    """

    def render_to_image(self, text_data: bytes, filename: str, options: ProcessingOptions) -> bytes:
        """
        Render text content as a syntax-highlighted image.
        
        :param text_data: Raw bytes of the text file.
        :param filename: Original filename to determine the lexer.
        :param options: Transformation parameters.
        :return: Processed image bytes.
        """
        try:
            content = text_data.decode("utf-8")
            
            # Determine lexer
            try:
                if filename.endswith(".json"):
                    lexer = get_lexer_by_name("json")
                    # Minify/reformat if it's JSON to ensure it's clean before rendering
                    data = json.loads(content)
                    content = json.dumps(data, indent=2)
                elif filename.endswith(".xml"):
                    lexer = get_lexer_by_name("xml")
                    dom = xml.dom.minidom.parseString(content)
                    content = dom.toprettyxml()
                elif filename.endswith(".md"):
                    lexer = get_lexer_by_name("markdown")
                else:
                    lexer = get_lexer_for_filename(filename)
            except (ClassNotFound, json.JSONDecodeError, Exception):
                lexer = get_lexer_by_name("text")

            # Configure high-quality formatter
            formatter = ImageFormatter(
                font_name="DejaVu Sans Mono", # Generic mono font
                font_size=16,
                line_number_chars=3,
                line_numbers=True,
                style="monokai"
            )

            # Highlight to image
            image_bytes = highlight(content, lexer, formatter)
            
            # If width/height options are provided, we'll let the main ImageProcessor handle final scaling
            # But we return these bytes as the "source image" for the pipeline
            return image_bytes
            
        except Exception as e:
            raise RuntimeError(f"Text rendering failed: {str(e)}")

    def process_text(self, text_data: bytes, filename: str) -> Tuple[bytes, str]:
        """
        Apply text-specific processing like minification.
        
        :param text_data: Raw bytes.
        :param filename: Filename for extension.
        :return: (Processed bytes, mime-type).
        """
        ext = filename.split(".")[-1].lower()
        content = text_data.decode("utf-8")
        
        try:
            if ext == "json":
                # Minify JSON for delivery
                data = json.loads(content)
                minified = json.dumps(data, separators=(',', ':'))
                return minified.encode("utf-8"), "application/json"
            
            elif ext == "xml":
                # Basic XML whitespace cleanup
                import re
                minified = re.sub(r'>\s+<', '><', content).strip()
                return minified.encode("utf-8"), "application/xml"
                
            elif ext == "md":
                # We could convert MD to HTML here if needed
                html = markdown.markdown(content)
                return html.encode("utf-8"), "text/html"
            
            return text_data, "text/plain"
            
        except Exception:
            return text_data, f"text/{ext}"
