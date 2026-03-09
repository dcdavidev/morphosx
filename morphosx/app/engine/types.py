from dataclasses import dataclass
from enum import Enum
from typing import Optional


class ImageFormat(str, Enum):
    """Supported output formats."""

    JPEG = "JPEG"
    PNG = "PNG"
    WEBP = "WEBP"
    JSON = "JSON"
    YAML = "YAML"
    XML = "XML"
    MD = "MD"
    HTML = "HTML"


@dataclass(frozen=True)
class ProcessingOptions:
    """
    Configuration options for image transformations.

    :param width: Target width in pixels.
    :param height: Target height in pixels.
    :param format: Output image format (e.g., JPEG, PNG, WEBP).
    :param quality: Compression quality from 1 to 100.
    :param time: For media with a temporal dimension (video/audio), the timestamp in seconds.
    :param page: For multi-page documents (PDF), the 1-based page index.
    """

    width: Optional[int] = None
    height: Optional[int] = None
    format: ImageFormat = ImageFormat.WEBP
    quality: int = 80
    time: float = 0.0
    page: int = 1

    def get_cache_key(self) -> str:
        """
        Generate a unique, readable filename for the processed variant.
        Example: w300_hauto_q80_t1.2_p1.webp
        """
        w_part = f"w{self.width}" if self.width else "wauto"
        h_part = f"h{self.height}" if self.height else "hauto"
        q_part = f"q{self.quality}"
        t_part = f"t{self.time}" if self.time > 0 else "t0"
        p_part = f"p{self.page}" if self.page > 1 else "p1"
        ext = self.format.value.lower()

        return f"{w_part}_{h_part}_{q_part}_{t_part}_{p_part}.{ext}"
