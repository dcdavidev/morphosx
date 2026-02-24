import ffmpeg
import os
import tempfile


class AudioProcessor:
    """
    Core engine for audio manipulation and waveform generation.
    """

    def generate_waveform(self, audio_data: bytes, width: int = 800, height: int = 200, color: str = 'cyan') -> bytes:
        """
        Generate a waveform image (PNG) from an audio file.
        
        :param audio_data: Raw audio bytes.
        :param width: Target width of the waveform image.
        :param height: Target height of the waveform image.
        :param color: The color of the waveform.
        :return: PNG image bytes.
        """
        with tempfile.NamedTemporaryFile(delete=False, suffix=".audio") as tmp:
            tmp.write(audio_data)
            tmp_path = tmp.name

        try:
            # Command: ffmpeg -i input -filter_complex "showwavespic=s=800x200:colors=cyan" -frames:v 1 output.png
            # This generates a visual representation of the audio amplitudes.
            out, _ = (
                ffmpeg
                .input(tmp_path)
                .filter('showwavespic', s=f"{width}x{height}", colors=color)
                .output('pipe:', vframes=1, format='image2', vcodec='png')
                .run(capture_stdout=True, quiet=True)
            )
            return out
        except ffmpeg.Error as e:
            raise RuntimeError(f"FFmpeg waveform generation failed: {e.stderr.decode()}")
        finally:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)
