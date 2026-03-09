import io
from typing import Optional, Tuple

from PIL import Image

from .base import BaseProcessor
from .types import ImageFormat, ProcessingOptions

try:
    import pillow_heif

    pillow_heif.register_heif_opener()
except ImportError:
    pass

try:
    import pillow_avif  # noqa: F401
except ImportError:
    pass


class ImageProcessor(BaseProcessor):
    """
    Core engine for on-the-fly image transformations.

    Handles resizing, format conversion, and optimization using memory buffers.
    """

    def process(
        self,
        source_data: bytes,
        options: ProcessingOptions,
        filename: Optional[str] = None,
    ) -> Tuple[bytes, str]:
        """
        Apply transformations to the source image data.
        """
        with Image.open(io.BytesIO(source_data)) as img:
            # Handle orientation from EXIF if present
            img = self._handle_exif_orientation(img)

            # Resize if dimensions are provided
            if options.width or options.height:
                img = self._resize(img, options.width, options.height)

            # Prepare for export
            output_buffer = io.BytesIO()
            save_params = self._get_save_params(options)

            # Convert to RGB if necessary (e.g., saving PNG with alpha to JPEG)
            if options.format == ImageFormat.JPEG and img.mode in ("RGBA", "P"):
                img = img.convert("RGB")

            img.save(output_buffer, format=options.format.value, **save_params)

            processed_data = output_buffer.getvalue()
            mime_type = f"image/{options.format.value.lower()}"

            return processed_data, mime_type

    def _resize(self, img: Image.Image, width: Optional[int], height: Optional[int]) -> Image.Image:
        """
        Resize image while maintaining aspect ratio if only one dimension is provided.

        :param img: PIL Image object.
        :param width: Target width.
        :param height: Target height.
        :return: Resized PIL Image object.
        """
        original_width, original_height = img.size

        if width and not height:
            height = int((width / original_width) * original_height)
        elif height and not width:
            width = int((height / original_height) * original_width)
        elif not width and not height:
            return img

        # Use LANCZOS for high-quality downsampling
        return img.resize((width, height), resample=Image.Resampling.LANCZOS)

    def _handle_exif_orientation(self, img: Image.Image) -> Image.Image:
        """
        Fix image orientation based on EXIF metadata.

        :param img: PIL Image object.
        :return: Oriented PIL Image object.
        """
        try:
            # This is a built-in helper in Pillow to handle EXIF orientation
            from PIL import ImageOps

            return ImageOps.exif_transpose(img)
        except Exception:
            # Fallback to original image if EXIF parsing fails
            return img

    def _get_save_params(self, options: ProcessingOptions) -> dict:
        """
        Generate format-specific save parameters.

        :param options: Processing options.
        :return: Dictionary of parameters for Image.save().
        """
        params = {"quality": options.quality}

        if options.format == ImageFormat.WEBP:
            params["method"] = 6  # Best compression/speed trade-off

        return params
