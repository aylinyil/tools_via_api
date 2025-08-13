from flask import Blueprint, request, jsonify
from tools.tool_pdfid import PdfIdTool

TOOLS = {
    "pdfid": PdfIdTool(),
}

tool_bp = Blueprint('tools', __name__)

@tool_bp.route('/tools/<tool_name>', methods=['POST'])
def run_tool(tool_name):
    """
    Endpoint to run a specific tool by name.

    :param tool_name: The name of the tool to run.
    :return: JSON response with the result of the tool execution.
    """
    tool = TOOLS.get(tool_name.lower())
    if not tool:
        return jsonify({"error": "Tool not found"}), 404

    try:
        data = request.get_json() or {}
        result = tool.run(data)
        # Hier dann die Outputs des Tools zurückgeben
        return jsonify({"tool": tool_name, "result": result}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500