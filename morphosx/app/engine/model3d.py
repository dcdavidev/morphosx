import io
import json
import xml.etree.ElementTree as ET
from typing import Optional, Tuple

import trimesh
import yaml
from PIL import Image, ImageDraw

from morphosx.app.engine.base import BaseProcessor
from morphosx.app.engine.processor import ImageFormat, ProcessingOptions


class Model3DProcessor(BaseProcessor):
    """
    Engine for generating 2D previews and metadata for 3D Models (STL, OBJ, GLB).
    """

    def __init__(self, image_processor: BaseProcessor):
        self.image_processor = image_processor

    def process(
        self,
        source_data: bytes,
        options: ProcessingOptions,
        filename: Optional[str] = None,
    ) -> Tuple[bytes, str]:
        """
        Generate blueprint or return metadata.
        """
        if options.format in (ImageFormat.JSON, ImageFormat.YAML, ImageFormat.XML):
            metadata = self.get_metadata(source_data, filename or "model.obj")
            if options.format == ImageFormat.JSON:
                return (
                    json.dumps(metadata, indent=2).encode("utf-8"),
                    "application/json",
                )
            elif options.format == ImageFormat.YAML:
                return (
                    yaml.dump(metadata, sort_keys=False).encode("utf-8"),
                    "application/x-yaml",
                )
            elif options.format == ImageFormat.XML:
                root = ET.Element("metadata")

                def build_xml(parent, data):
                    if isinstance(data, dict):
                        for k, v in data.items():
                            child = ET.SubElement(parent, k)
                            build_xml(child, v)
                    else:
                        parent.text = str(data)

                build_xml(root, metadata)
                return ET.tostring(root, encoding="utf-8"), "application/xml"

        blueprint_bytes = self.render_thumbnail(source_data, filename or "model.obj")
        return self.image_processor.process(blueprint_bytes, options)

    def get_metadata(self, model_data: bytes, filename: str) -> dict:
        """
        Extract structural metadata from a 3D model.
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
                faces = len(mesh.graph.nodes)  # approximation
                is_scene = True
            else:
                vertices = mesh.vertices.shape[0]
                faces = mesh.faces.shape[0]
                is_scene = False

            bounds = mesh.bounds
            size = bounds[1] - bounds[0]

            return {
                "type": "3D_Model",
                "format": ext.upper(),
                "is_scene": is_scene,
                "vertices": vertices,
                "faces_or_nodes": faces,
                "bounding_box": {
                    "x": float(size[0]),
                    "y": float(size[1]),
                    "z": float(size[2]),
                },
                "volume": float(getattr(mesh, "volume", 0)),
            }
        except Exception as e:
            return {"error": f"Could not parse 3D file: {str(e)}"}

    def render_thumbnail(self, model_data: bytes, filename: str) -> bytes:
        """
        Create a preview of the 3D model.
        """
        metadata = self.get_metadata(model_data, filename)

        if "error" in metadata:
            return self._create_blueprint_card("3D Model Error", metadata["error"])

        title = f"{'3D Scene' if metadata['is_scene'] else '3D Model'} ({metadata['format']})"
        summary = (
            f"Vertices: {metadata['vertices']}\n"
            f"Faces/Nodes: {metadata['faces_or_nodes']}\n\n"
            f"Bounding Box Dimensions:\n"
            f"X: {metadata['bounding_box']['x']:.2f}\n"
            f"Y: {metadata['bounding_box']['y']:.2f}\n"
            f"Z: {metadata['bounding_box']['z']:.2f}\n\n"
            f"Volume: {metadata['volume']:.2f}"
        )

        return self._create_blueprint_card(title, summary)

    def _create_blueprint_card(self, title: str, text: str) -> bytes:
        """Render a technical blueprint-style card."""
        width, height = 800, 600
        img = Image.new("RGB", (width, height), color=(10, 50, 100))  # Blueprint blue
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
