import io
from PIL import Image, ImageDraw


class BIMProcessor:
    """
    Engine for generating technical summaries and metadata for BIM (IFC) files.
    """

    def get_metadata(self, ifc_data: bytes) -> dict:
        """
        Extract structural metadata from an IFC file.
        """
        try:
            import ifcopenshell
        except ImportError:
            raise RuntimeError("ifcopenshell is not installed. Run 'pip install morphosx[bim]' to enable this feature.")

        try:
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
                
                return {
                    "type": "BIM",
                    "project_name": project.Name if project else "Unnamed",
                    "site_name": site.Name if site else "Unknown",
                    "building_stories": stories,
                    "element_count": {
                        "walls": walls,
                        "windows": windows,
                        "doors": doors
                    },
                    "schema": model.schema
                }
            finally:
                if os.path.exists(tmp_path):
                    os.remove(tmp_path)
        except Exception as e:
            return {"error": f"Could not parse IFC: {str(e)}"}

    def render_summary(self, ifc_data: bytes, filename: str) -> bytes:
        """
        Create a technical data card for an IFC file.
        """
        metadata = self.get_metadata(ifc_data)
        
        if "error" in metadata:
            return self._create_bim_card("BIM Parsing Error", metadata["error"])

        title = f"BIM Project: {metadata['project_name']}"
        summary = (
            f"Site: {metadata['site_name']}\n"
            f"Building Stories: {metadata['building_stories']}\n\n"
            f"Element Count:\n"
            f"- Walls: {metadata['element_count']['walls']}\n"
            f"- Windows: {metadata['element_count']['windows']}\n"
            f"- Doors: {metadata['element_count']['doors']}\n\n"
            f"Schema: {metadata['schema']}"
        )

        return self._create_bim_card(title, summary)

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
