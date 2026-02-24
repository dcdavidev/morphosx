import fitz  # PyMuPDF
import io


class DocumentProcessor:
    """
    Core engine for document (PDF) processing.
    """

    def extract_page_as_image(self, document_data: bytes, page_number: int = 1, dpi: int = 150) -> bytes:
        """
        Extract a specific page from a PDF and render it as a PNG image.
        
        :param document_data: Raw PDF bytes.
        :param page_number: The 1-based index of the page to extract.
        :param dpi: Resolution for rendering the page to image.
        :return: PNG image bytes.
        """
        try:
            # Open PDF from memory stream
            doc = fitz.open(stream=document_data, filetype="pdf")
            
            # fitz uses 0-based indexing
            page_index = max(0, page_number - 1)
            
            if page_index >= len(doc):
                raise ValueError(f"Page {page_number} is out of bounds for a {len(doc)}-page document.")
            
            page = doc[page_index]
            
            # Render page to an image (Pixmap)
            # The matrix is used to scale the default 72 DPI to the target DPI
            zoom = dpi / 72.0
            matrix = fitz.Matrix(zoom, zoom)
            pix = page.get_pixmap(matrix=matrix, alpha=False)
            
            # Export as PNG
            png_bytes = pix.tobytes(output="png")
            doc.close()
            
            return png_bytes
            
        except Exception as e:
            raise RuntimeError(f"Document processing failed: {str(e)}")
