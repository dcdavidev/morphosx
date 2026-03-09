from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Tuple

from morphosx.app.engine.processor import ProcessingOptions


class BaseProcessor(ABC):
    """
    Abstract base class for all media processing engines.
    """

    @abstractmethod
    def process(
        self,
        source_data: bytes,
        options: ProcessingOptions,
        filename: Optional[str] = None,
    ) -> Tuple[bytes, str]:
        """
        Process the source data and return transformed bytes and MIME type.

        :param source_data: Raw bytes of the original asset.
        :param options: Transformation and formatting options.
        :param filename: Optional filename to help with type detection.
        :return: (processed_bytes, mime_type)
        """
        pass

    def get_metadata(self, source_data: bytes, filename: Optional[str] = None) -> dict:
        """
        Extract metadata from the asset. Default implementation returns basic info.
        """
        return {"size": len(source_data), "filename": filename}


class ProcessorRegistry:
    """
    Registry to map file extensions to specific processors.
    """

    def __init__(self):
        self._processors: Dict[str, BaseProcessor] = {}
        self._default_processor: Optional[BaseProcessor] = None

    def register(self, extensions: List[str], processor: BaseProcessor):
        for ext in extensions:
            self._processors[ext.lower().lstrip(".")] = processor

    def set_default(self, processor: BaseProcessor):
        self._default_processor = processor

    def get_processor(self, filename: str) -> BaseProcessor:
        ext = filename.split(".")[-1].lower() if "." in filename else ""
        return self._processors.get(ext, self._default_processor)


# Global registry instance
registry = ProcessorRegistry()


def initialize_registry():
    """
    Bootstrap the processor registry with all available engines.
    """
    from morphosx.app.engine.archive import ArchiveProcessor
    from morphosx.app.engine.audio import AudioProcessor
    from morphosx.app.engine.bim import BIMProcessor
    from morphosx.app.engine.document import DocumentProcessor
    from morphosx.app.engine.font import FontProcessor
    from morphosx.app.engine.model3d import Model3DProcessor
    from morphosx.app.engine.office import OfficeProcessor
    from morphosx.app.engine.processor import ImageProcessor
    from morphosx.app.engine.raw import RawProcessor
    from morphosx.app.engine.text import TextProcessor
    from morphosx.app.engine.video import VideoProcessor
    from morphosx.app.engine.vips import VipsProcessor
    from morphosx.app.settings import settings

    # 1. Initialize core image engine
    if settings.engine_type == "vips":
        core_processor = VipsProcessor()
    else:
        core_processor = ImageProcessor()

    registry.set_default(core_processor)

    # 2. Initialize and register specialized engines
    video_engine = VideoProcessor(core_processor)
    registry.register(["mp4", "webm", "mov", "avi"], video_engine)

    audio_engine = AudioProcessor(core_processor)
    registry.register(["mp3", "wav", "ogg", "flac"], audio_engine)

    doc_engine = DocumentProcessor(core_processor)
    registry.register(["pdf"], doc_engine)

    raw_engine = RawProcessor(core_processor)
    registry.register(["cr2", "nef", "dng", "arw"], raw_engine)

    text_engine = TextProcessor(core_processor)
    registry.register(["json", "xml", "md", "txt"], text_engine)

    office_engine = OfficeProcessor(core_processor)
    registry.register(["docx", "pptx", "xlsx"], office_engine)

    font_engine = FontProcessor(core_processor)
    registry.register(["ttf", "otf"], font_engine)

    model3d_engine = Model3DProcessor(core_processor)
    registry.register(["stl", "obj", "glb", "gltf"], model3d_engine)

    archive_engine = ArchiveProcessor(core_processor)
    registry.register(["zip", "tar", "gz"], archive_engine)

    bim_engine = BIMProcessor(core_processor)
    registry.register(["ifc"], bim_engine)

    return registry
