import io
from PIL import Image, ImageDraw, ImageFont


class FontProcessor:
    """
    Engine for generating font specimen images from TTF/OTF files.
    """

    def render_specimen(self, font_data: bytes, options: dict) -> bytes:
        """
        Create a preview of the font.
        """
        try:
            width, height = 1200, 800
            img = Image.new("RGB", (width, height), color=(255, 255, 255))
            draw = ImageDraw.Draw(img)
            
            # Load the font from bytes
            font_size = 48
            font = ImageFont.truetype(io.BytesIO(font_data), font_size)
            
            # Specimen text
            lines = [
                "ABCDEFGHIJKLMNOPQRSTUVWXYZ",
                "abcdefghijklmnopqrstuvwxyz",
                "0123456789 !@#$%^&*()",
                "",
                "The quick brown fox jumps over the lazy dog.",
                "Sphinx of black quartz, judge my vow.",
                "",
                "Large size (72pt):",
            ]
            
            y = 40
            for line in lines:
                draw.text((40, y), line, font=font, fill=(0, 0, 0))
                y += font_size + 10
            
            # Draw a larger sample
            large_font = ImageFont.truetype(io.BytesIO(font_data), 72)
            draw.text((40, y), "MorphosX Media Engine", font=large_font, fill=(43, 108, 176))

            output = io.BytesIO()
            img.save(output, format="JPEG")
            return output.getvalue()
            
        except Exception as e:
            # Fallback image if font is corrupted
            img = Image.new("RGB", (400, 200), color=(255, 0, 0))
            draw = ImageDraw.Draw(img)
            draw.text((20, 80), f"Font Error: {str(e)}", fill=(255, 255, 255))
            output = io.BytesIO()
            img.save(output, format="JPEG")
            return output.getvalue()
