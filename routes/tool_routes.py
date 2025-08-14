from flask import Blueprint, request, jsonify
from tools.tool_pdfid import PdfIdTool
from tools.tool_pdf2image import Pdf2ImageTool

TOOLS = {
    "pdfid": PdfIdTool(),
    "pdf2image": Pdf2ImageTool(),
}

tool_bp = Blueprint('tools', __name__)

@tool_bp.route('/tools/<tool_name>', methods=['POST'])
def run_tool(tool_name):
    tool_name = tool_name.lower()
    tool = TOOLS.get(tool_name)
    if not tool:
        return jsonify({"error": "Tool not found"}), 404

    try:
        if "file" not in request.files:
            return jsonify({"error": "No file uploaded"}), 400

        file_storage = request.files["file"]
        password = request.form.get("password")

        if tool_name == "pdfid":
            result = tool.run(file_storage)
            return jsonify({"tool": tool.name, "result": result})

        elif tool_name == "pdf2image":
            return tool.run(file_storage, password=password)

        else:
            return jsonify({"error": "Tool not supported"}), 400

    except Exception as e:
        return jsonify({"error": str(e)}), 500

