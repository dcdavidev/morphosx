import io
import zipfile
import tarfile
from PIL import Image, ImageDraw


class ArchiveProcessor:
    """
    Engine for generating content-list previews for ZIP and TAR archives.
    """

    def render_thumbnail(self, archive_data: bytes, filename: str) -> bytes:
        """
        Create a preview of the archive contents.
        """
        ext = filename.split(".")[-1].lower()
        file_list = []
        try:
            if ext == "zip":
                with zipfile.ZipFile(io.BytesIO(archive_data)) as z:
                    file_list = [f.filename for f in z.infolist()[:15]]
                    total = len(z.infolist())
            elif ext == "tar" or filename.endswith(".tar.gz"):
                with tarfile.open(fileobj=io.BytesIO(archive_data)) as t:
                    file_list = [f.name for f in t.getmembers()[:15]]
                    total = len(t.getmembers())
            
            summary = "\n".join(file_list)
            if total > 15:
                summary += f"\n... and {total - 15} more files."
            
            title = f"Archive: {filename} ({total} files)"
            return self._create_folder_card(title, summary)
            
        except Exception as e:
            return self._create_folder_card("Archive Error", f"Could not read archive: {str(e)}")

    def _create_folder_card(self, title: str, text: str) -> bytes:
        """Render a folder-style card image."""
        width, height = 800, 600
        img = Image.new("RGB", (width, height), color=(255, 250, 230)) # Manila folder yellow
        draw = ImageDraw.Draw(img)
        
        # Draw a folder 'tab'
        draw.rectangle([20, 10, 200, 40], fill=(210, 180, 100))
        
        # Draw main folder body
        draw.rectangle([20, 40, 780, 580], outline=(180, 150, 80), width=3)
        
        # Draw text
        draw.text((40, 60), title, fill=(100, 80, 20))
        draw.text((40, 110), text, fill=(60, 50, 30))

        output = io.BytesIO()
        img.save(output, format="JPEG")
        return output.getvalue()
