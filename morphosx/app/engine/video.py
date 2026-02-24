import io
import os
import tempfile
from typing import Tuple, Optional


class VideoProcessor:
    """
    Core engine for video metadata and thumbnail extraction.
    
    Uses FFmpeg for high-performance frame manipulation.
    """

    def extract_thumbnail(self, video_data: bytes, timestamp: float = 0.0) -> bytes:
        """
        Extract a single frame from video at a given timestamp.
        
        :param video_data: Raw video bytes.
        :param timestamp: Time in seconds to extract the frame from.
        :return: JPEG bytes of the extracted frame.
        """
        try:
            import ffmpeg
        except ImportError:
            raise RuntimeError("ffmpeg-python is not installed. Run 'pip install morphosx[video]' to enable this feature.")

        # FFmpeg works with file paths, so we need a temporary file
        # unless we pipe, but piping video bytes can be complex.
        # For simplicity and performance, we use a temporary file in /tmp (RAM-backed in many Linux distros)
        with tempfile.NamedTemporaryFile(delete=False, suffix=".video") as tmp:
            tmp.write(video_data)
            tmp_path = tmp.name

        try:
            # Command: ffmpeg -ss {timestamp} -i {input} -vframes 1 -f image2 pipe:1
            out, _ = (
                ffmpeg
                .input(tmp_path, ss=timestamp)
                .output('pipe:', vframes=1, format='image2', vcodec='mjpeg')
                .run(capture_stdout=True, quiet=True)
            )
            return out
        except ffmpeg.Error as e:
            raise RuntimeError(f"FFmpeg thumbnail extraction failed: {e.stderr.decode()}")
        finally:
            # Cleanup temp file
            if os.path.exists(tmp_path):
                os.remove(tmp_path)

    def get_metadata(self, video_data: bytes) -> dict:
        """
        Probe video for metadata (resolution, duration, etc).
        """
        try:
            import ffmpeg
        except ImportError:
            raise RuntimeError("ffmpeg-python is not installed. Run 'pip install morphosx[video]' to enable this feature.")

        with tempfile.NamedTemporaryFile(delete=False, suffix=".video") as tmp:
            tmp.write(video_data)
            tmp_path = tmp.name

        try:
            probe = ffmpeg.probe(tmp_path)
            video_stream = next((stream for stream in probe['streams'] if stream['codec_type'] == 'video'), None)
            
            return {
                "duration": float(probe['format'].get('duration', 0)),
                "width": int(video_stream['width']) if video_stream else None,
                "height": int(video_stream['height']) if video_stream else None,
                "codec": video_stream['codec_name'] if video_stream else None,
                "bitrate": int(probe['format'].get('bit_rate', 0))
            }
        except ffmpeg.Error as e:
            raise RuntimeError(f"FFmpeg probe failed: {e.stderr.decode()}")
        finally:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)
