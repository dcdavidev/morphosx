import io
from PIL import Image


class RawProcessor:
    """
    Core engine for processing RAW image formats (e.g., CR2, NEF, DNG, ARW).
    """

    def extract_preview(self, raw_data: bytes) -> bytes:
        """
        Extract the best available preview or render the RAW image to a standard RGB format.
        
        :param raw_data: Raw bytes of the image file.
        :return: Standard image bytes (e.g., JPEG or PNG) ready for ImageProcessor.
        """
        try:
            import rawpy
            import imageio.v3 as iio
        except ImportError:
            raise RuntimeError("rawpy or imageio is not installed. Run 'pip install morphosx[raw]' to enable this feature.")

        try:
            # Load raw data from memory buffer
            with rawpy.imread(io.BytesIO(raw_data)) as raw:
                # Post-process the raw image to an RGB numpy array
                # use_camera_wb=True ensures colors match the camera settings
                # half_size=True speeds up processing by reducing resolution,
                # which is usually fine since the ImageProcessor will likely downscale anyway.
                # However, for highest quality we might want half_size=False. 
                # Let's use half_size=False for best quality, but it might be slower.
                rgb = raw.postprocess(use_camera_wb=True, half_size=False)
                
                # Convert the numpy array to a Pillow Image
                img = Image.fromarray(rgb)
                
                # Save to a memory buffer as JPEG
                output_buffer = io.BytesIO()
                img.save(output_buffer, format="JPEG", quality=95)
                
                return output_buffer.getvalue()
                
        except Exception as e:
            raise RuntimeError(f"RAW image processing failed: {str(e)}")
