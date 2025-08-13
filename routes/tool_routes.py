from flask import Blueprint, request, jsonify
from tools.tool_pdfid import PdfIdTool

TOOLS = {
    "pdfid": PdfIdTool(),
}

tool_bp = Blueprint('tools', __name__)

@tool_bp.route('/tools/<tool_name>', methods=['POST'])
def run_tool(tool_name):
    tool = TOOLS.get(tool_name.lower())
    if not tool:
        return jsonify({"error": "Tool not found"}), 404

    try:
        if "file" not in request.files:
            return jsonify({"error": "No file uploaded"}), 400

        file_storage = request.files["file"]
        result = tool.run(file_storage)

        return jsonify({"tool": tool.name, "result": result})

    except Exception as e:
        return jsonify({"error": str(e)}), 500
