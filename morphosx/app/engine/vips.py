import io
from typing import Optional, Tuple
from morphosx.app.engine.processor import ProcessingOptions, ImageFormat


class VipsProcessor:
    """
    High-performance image transformation engine using libvips (via pyvips).
    
    Libvips is significantly faster and uses much less memory than Pillow 
    for large image operations due to its tiled, streaming architecture.
    """

    def process(self, source_data: bytes, options: ProcessingOptions) -> Tuple[bytes, str]:
        """
        Apply transformations using libvips.
        
        :param source_data: Raw image bytes.
        :param options: Transformation parameters.
        :return: A tuple of (processed bytes, mime type).
        """
        try:
            import pyvips
        except ImportError:
            raise RuntimeError("pyvips is not installed. Run 'pip install morphosx[vips]' to enable this feature.")

        try:
            # Load image from memory buffer
            img = pyvips.Image.new_from_buffer(source_data, "")

            # Resize if dimensions are provided
            if options.width or options.height:
                img = self._resize(img, options.width, options.height)

            # Map ImageFormat to libvips format string
            format_map = {
                ImageFormat.JPEG: ".jpg",
                ImageFormat.PNG: ".png",
                ImageFormat.WEBP: ".webp",
            }
            vips_format = format_map.get(options.format, ".webp")

            # Prepare saving parameters
            save_params = self._get_save_params(options)
            
            # Export to buffer
            processed_data = img.write_to_buffer(vips_format, **save_params)
            mime_type = f"image/{options.format.value.lower()}"
            
            return processed_data, mime_type
            
        except Exception as e:
            raise RuntimeError(f"Vips processing failed: {str(e)}")

    def _resize(self, img, width: Optional[int], height: Optional[int]):
        """
        Resize image while maintaining aspect ratio using libvips' thumbnail-style scaling.
        """
        try:
            import pyvips
        except ImportError:
            raise RuntimeError("pyvips is not installed.")
            
        original_width = img.width
        original_height = img.height

        if width and not height:
            scale = width / original_width
        elif height and not width:
            scale = height / original_height
        elif width and height:
            # Fit-style resize: Choose the scale that fits both dimensions
            scale_w = width / original_width
            scale_h = height / original_height
            scale = min(scale_w, scale_h)
        else:
            return img

        # Use libvips' 'thumbnail' approach or direct 'resize'
        # 'resize' is simple for general scaling
        return img.resize(scale)

    def _get_save_params(self, options: ProcessingOptions) -> dict:
        """
        Generate libvips-specific save parameters.
        
        :param options: Processing options.
        :return: Dictionary of parameters for write_to_buffer().
        """
        params = {"Q": options.quality}
        
        if options.format == ImageFormat.WEBP:
            params["lossless"] = False
            params["effort"] = 6  # Equivalent to Pillow's method 6
            
        return params
