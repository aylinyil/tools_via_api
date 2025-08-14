import tempfile
from flask import send_file

from werkzeug.datastructures import FileStorage
from .base_tool import BaseTool
from pdf2image import convert_from_bytes
import pyzipper
import io, os

class Pdf2ImageTool(BaseTool):
    """
    A class to represent a PDF to Image conversion tool.
    This class converts PDF files into images and saves them to a (optional) password secured archive.
    """

    def __init__(self):
        """
        Initializes the Pdf2Image instance.
        """
        super().__init__("Pdf2Image")


    def run(self, file_storage: FileStorage, password: str = None):
        """
        Convert a PDF file to images and return a ZIP file (optionally password-protected).

        Args:
            file_storage: FileStorage object from Flask
            password: Optional password for ZIP encryption

        Returns:
            Flask send_file response containing the ZIP
        """
        pdf_bytes = file_storage.read()
        pages = convert_from_bytes(pdf_bytes, dpi=300)

        # Create ZIP in memory
        zip_buffer = io.BytesIO()
        with pyzipper.AESZipFile(zip_buffer, "w", compression=pyzipper.ZIP_DEFLATED,
                                 encryption=pyzipper.WZ_AES) as zipf:
            if password:
                zipf.setpassword(password.encode())

            for i, page in enumerate(pages, start=1):
                img_bytes = io.BytesIO()
                page.save(img_bytes, format="PNG")
                img_bytes.seek(0)
                zipf.writestr(f"page_{i}.png", img_bytes.read())

        zip_buffer.seek(0)

        # Optionally save to subfolder
        output_dir = "zipped_images_from_pdf"
        os.makedirs(output_dir, exist_ok=True)
        zip_path = os.path.join(output_dir, f"{file_storage.filename}_images.zip")
        with open(zip_path, "wb") as f:
            f.write(zip_buffer.getvalue())

        print(f"Saved ZIP file to {zip_path}")

        # Return ZIP to client
        return send_file(
            zip_buffer,
            mimetype="application/zip",
            as_attachment=True,
            download_name=f"{file_storage.filename}_images.zip"
        )

