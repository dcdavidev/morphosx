import io
import trimesh
from PIL import Image, ImageDraw


class Model3DProcessor:
    """
    Engine for generating 2D previews for 3D Models (STL, OBJ, GLB).
    
    Generates a 'Blueprint' card with model metadata and a bounding box summary.
    """

    def render_thumbnail(self, model_data: bytes, filename: str) -> bytes:
        """
        Create a preview of the 3D model.
        """
        ext = filename.split(".")[-1].lower()
        try:
            # Load the mesh
            file_obj = io.BytesIO(model_data)
            mesh = trimesh.load(file_obj, file_type=ext)

            # Metadata extraction
            if isinstance(mesh, trimesh.Scene):
                # It's a scene (common for GLB)
                vertices = mesh.vertices.shape[0]
                faces = len(mesh.graph.nodes) # approximation
                title = f"3D Scene ({ext.upper()})"
            else:
                vertices = mesh.vertices.shape[0]
                faces = mesh.faces.shape[0]
                title = f"3D Model ({ext.upper()})"

            bounds = mesh.bounds
            size = bounds[1] - bounds[0]
            
            summary = (
                f"Vertices: {vertices}\n"
                f"Faces/Nodes: {faces}\n\n"
                f"Bounding Box Dimensions:\n"
                f"X: {size[0]:.2f}\n"
                f"Y: {size[1]:.2f}\n"
                f"Z: {size[2]:.2f}\n\n"
                f"Volume: {getattr(mesh, 'volume', 0):.2f}"
            )

            return self._create_blueprint_card(title, summary)
            
        except Exception as e:
            return self._create_blueprint_card("3D Model Error", f"Could not parse 3D file: {str(e)}")

    def _create_blueprint_card(self, title: str, text: str) -> bytes:
        """Render a technical blueprint-style card."""
        width, height = 800, 600
        img = Image.new("RGB", (width, height), color=(10, 50, 100)) # Blueprint blue
        draw = ImageDraw.Draw(img)
        
        # Draw a grid
        for i in range(0, width, 50):
            draw.line([(i, 0), (i, height)], fill=(30, 80, 150), width=1)
        for i in range(0, height, 50):
            draw.line([(0, i), (width, i)], fill=(30, 80, 150), width=1)
            
        # Draw header
        draw.text((20, 20), title, fill=(255, 255, 255))
        draw.text((20, 80), text, fill=(200, 230, 255))
        
        # Decoration (a simple wireframe box)
        draw.rectangle([500, 300, 750, 550], outline=(255, 255, 255), width=2)
        draw.line([500, 300, 550, 250], fill=(255, 255, 255), width=2)
        draw.line([750, 300, 800, 250], fill=(255, 255, 255), width=2)
        draw.line([550, 250, 800, 250], fill=(255, 255, 255), width=2)

        output = io.BytesIO()
        img.save(output, format="JPEG")
        return output.getvalue()
