import io
from PIL import Image, ImageDraw


class BIMProcessor:
    """
    Engine for generating technical summaries for BIM (IFC) files.
    """

    def render_summary(self, ifc_data: bytes, filename: str) -> bytes:
        """
        Create a technical data card for an IFC file.
        """
        try:
            import ifcopenshell
            import ifcopenshell.util.element
        except ImportError:
            raise RuntimeError("ifcopenshell is not installed. Run 'pip install morphosx[bim]' to enable this feature.")

        try:
            # Load IFC from memory
            # IfcOpenShell usually expects a file path, but we can use a temp file 
            # or try the direct string loader if the version supports it.
            # For robustness in memory-only environments, we use a temporary named file.
            import tempfile
            import os
            
            with tempfile.NamedTemporaryFile(delete=False, suffix=".ifc") as tmp:
                tmp.write(ifc_data)
                tmp_path = tmp.name
            
            try:
                model = ifcopenshell.open(tmp_path)
                
                # Metadata extraction
                project = model.by_type("IfcProject")[0] if model.by_type("IfcProject") else None
                site = model.by_type("IfcSite")[0] if model.by_type("IfcSite") else None
                
                walls = len(model.by_type("IfcWall"))
                windows = len(model.by_type("IfcWindow"))
                doors = len(model.by_type("IfcDoor"))
                stories = len(model.by_type("IfcBuildingStorey"))
                
                title = f"BIM Project: {project.Name if project else 'Unnamed'}"
                summary = (
                    f"Site: {site.Name if site else 'Unknown'}
"
                    f"Building Stories: {stories}

"
                    f"Element Count:
"
                    f"- Walls: {walls}
"
                    f"- Windows: {windows}
"
                    f"- Doors: {doors}

"
                    f"Schema: {model.schema}"
                )
            finally:
                if os.path.exists(tmp_path):
                    os.remove(tmp_path)

            return self._create_bim_card(title, summary)
            
        except Exception as e:
            return self._create_bim_card("BIM Parsing Error", f"Could not parse IFC: {str(e)}")

    def _create_bim_card(self, title: str, text: str) -> bytes:
        """Render a technical architecture-style card."""
        width, height = 800, 600
        img = Image.new("RGB", (width, height), color=(30, 30, 35)) # Dark gray
        draw = ImageDraw.Draw(img)
        
        # Draw some 'architectural' lines
        draw.line([0, 100, width, 100], fill=(100, 200, 100), width=2)
        draw.line([100, 0, 100, height], fill=(100, 200, 100), width=1)
        
        # Text
        draw.text((120, 40), title, fill=(255, 255, 255))
        draw.text((120, 130), text, fill=(180, 200, 180))
        
        # Simple house icon silhouette
        draw.polygon([(600, 200), (750, 200), (675, 100)], outline=(100, 255, 100), width=2)
        draw.rectangle([620, 200, 730, 300], outline=(100, 255, 100), width=2)

        output = io.BytesIO()
        img.save(output, format="JPEG")
        return output.getvalue()
