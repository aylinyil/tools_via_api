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
    This class analyzes PDF files for metadata and security information.
    """

    def __init__(self):
        """
        Initializes the PdfId instance.
        """
        super().__init__("PdfId")

    def run(self, file_storage: FileStorage):
        """
        Analyze a PDF file and return analysis results.
        
        Args:
            file_storage: The uploaded PDF file
            
        Returns:
            dict: PDF analysis results
        """
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
            file_storage.save(tmp_file.name)
            tmp_path = tmp_file.name

        try:
            # Use pdfid to analyze the PDF and get XML output
            xml_doc = pdfid.PDFiD(tmp_path)
            
            # Convert XML to JSON using the built-in function
            json_string = pdfid.PDFiD2JSON(xml_doc, force=False)
            
            # Parse the JSON string to get the actual data
            if isinstance(json_string, str):
                json_data = json.loads(json_string)
            else:
                json_data = json_string
            
            # If json_data is a list, take the first item (usually the main PDF info)
            if isinstance(json_data, list) and len(json_data) > 0:
                pdf_info = json_data[0]
            elif isinstance(json_data, dict):
                pdf_info = json_data
            else:
                pdf_info = {"raw_data": str(json_data)}
            
            # Extract the actual PDF analysis data
            if isinstance(pdf_info, dict) and "pdfid" in pdf_info:
                pdf_analysis = pdf_info["pdfid"]
                
                # Create a clean result structure
                result = {
                    "filename": file_storage.filename,
                    "filesize": os.path.getsize(tmp_path),
                    "header": pdf_analysis.get("header", ""),
                    "version": pdf_analysis.get("version", ""),
                    "isPdf": pdf_analysis.get("isPdf", ""),
                    "errorOccured": pdf_analysis.get("errorOccured", ""),
                    "errorMessage": pdf_analysis.get("errorMessage", "")
                }
                
                # Extract keywords (PDF structure information)
                if "keywords" in pdf_analysis and "keyword" in pdf_analysis["keywords"]:
                    keywords = pdf_analysis["keywords"]["keyword"]
                    for keyword in keywords:
                        name = keyword.get("name", "")
                        count = keyword.get("count", 0)
                        result[name] = count
                
                # Extract dates if available
                if "dates" in pdf_analysis and "date" in pdf_analysis["dates"]:
                    dates = pdf_analysis["dates"]["date"]
                    if dates:
                        result["dates"] = dates
                
                return result
            else:
                # Fallback if structure is unexpected
                return {
                    "filename": file_storage.filename,
                    "filesize": os.path.getsize(tmp_path),
                    "raw_data": pdf_info
                }

        except Exception as e:
            # Return error information if something goes wrong
            return {
                "error": str(e),
                "filename": file_storage.filename,
                "filesize": os.path.getsize(tmp_path) if os.path.exists(tmp_path) else 0
            }
        finally:
            # Clean up temporary file
            if os.path.exists(tmp_path):
                os.remove(tmp_path)
