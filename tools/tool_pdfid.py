import tempfile
import os
import fitz
from werkzeug.datastructures import FileStorage
from pdfid import pdfid
import json

from .base_tool import BaseTool


class PdfIdTool(BaseTool):
    """
    A class to represent a PDF identifier tool.
    This class is a placeholder for the actual implementation of PDF identification logic.
    """

    def __init__(self):
        """
        Initializes the PdfId instance.
        """
        super().__init__("PdfId")

    def run(self, file_storage: FileStorage):
        import xml.dom.minidom

        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
            file_storage.save(tmp_file.name)
            tmp_path = tmp_file.name

        try:
            doc = pdfid.PDFiD(tmp_path)

            data = {k: getattr(doc, k) for k in dir(doc)
                    if not k.startswith('_') and isinstance(getattr(doc, k), int)}

            return data

        finally:
            os.remove(tmp_path)
