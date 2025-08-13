# Tools via API

A Flask-based REST API that provides access to various analysis tools, currently featuring a PDF identification tool that analyzes PDF files for metadata and security information.

## 🚀 Features

- **PDF Analysis Tool**: Analyze PDF files for metadata, embedded objects, and potential security risks
- **RESTful API**: Clean, simple HTTP endpoints for tool execution
- **File Upload Support**: Accept PDF files via multipart form data
- **Extensible Architecture**: Easy to add new tools following the base tool pattern
- **JSON Response**: Structured JSON responses for easy integration

## 🛠️ Technology Stack

- **Backend**: Flask 3.1.1
- **PDF Processing**: PyMuPDF (fitz) + pdfid
- **Python Version**: 3.13+
- **Virtual Environment**: Python venv

## 📋 Prerequisites

- Python 3.13 or higher
- pip (Python package installer)
- Git (for cloning the repository)

## 🚀 Installation & Setup

### 1. Clone the Repository
```bash
git clone <your-repository-url>
cd tools_via_api
```

### 2. Create Virtual Environment
```bash
python3 -m venv .venv
```

### 3. Activate Virtual Environment

**On macOS/Linux:**
```bash
source .venv/bin/activate
```

**On Windows:**
```bash
.venv\Scripts\activate
```

**On macOS with Fish shell:**
```bash
source .venv/bin/activate.fish
```

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

## 🏃‍♂️ Running the Application

### Start the Flask Server
```bash
python app.py
```

The server will start on `http://127.0.0.1:5001` (note: port 5001 to avoid conflicts with macOS AirTunes service).

### Development Mode
The application runs in debug mode by default, which provides:
- Auto-reload on code changes
- Detailed error messages
- Debugger interface

## 📚 API Documentation

### Base URL
```
http://localhost:5001
```

### Endpoints

#### POST /tools/{tool_name}
Execute a specific tool with uploaded file data.

**Parameters:**
- `tool_name` (path): Name of the tool to execute (e.g., `pdfid`)
- `file` (form-data): The file to analyze

**Supported Tools:**
- `pdfid`: PDF identification and analysis tool

### Example Usage

#### Using curl
```bash
# Basic PDF analysis
curl -X POST \
  -F "file=@/path/to/your/file.pdf" \
  http://localhost:5001/tools/pdfid

# With verbose output
curl -v -X POST \
  -F "file=@/path/to/your/file.pdf" \
  http://localhost:5001/tools/pdfid

# Save response to file
curl -X POST \
  -F "file=@/path/to/your/file.pdf" \
  http://localhost:5001/tools/pdfid \
  -o analysis_result.json
```

#### Using Python requests
```python
import requests

url = "http://localhost:5001/tools/pdfid"
files = {"file": open("document.pdf", "rb")}

response = requests.post(url, files=files)
result = response.json()
print(result)
```

#### Using JavaScript/Fetch
```javascript
const formData = new FormData();
formData.append('file', fileInput.files[0]);

fetch('http://localhost:5001/tools/pdfid', {
  method: 'POST',
  body: formData
})
.then(response => response.json())
.then(data => console.log(data));
```

## 🔧 Available Tools

### PDF ID Tool (`pdfid`)
Analyzes PDF files for metadata and security information.

**What it analyzes:**
- PDF version and structure
- Embedded objects and scripts
- JavaScript code presence
- Form fields and annotations
- Security settings and encryption
- File size and page count

**Response Format:**
```json
{
  "tool": "PdfId",
  "result": {
    "header": "PDF",
    "version": "1.4",
    "obj": 15,
    "endobj": 15,
    "stream": 2,
    "endstream": 2,
    "xref": 1,
    "trailer": 1,
    "startxref": 1,
    "page": 1,
    "encrypt": 0,
    "objstm": 0,
    "js": 0,
    "javascript": 0,
    "aa": 0,
    "openaction": 0,
    "acroform": 0,
    "jbig2dec": 0,
    "richmedia": 0,
    "launch": 0,
    "embeddedfile": 0,
    "xfa": 0,
    "colors": 0
  }
}
```

## 🏗️ Project Structure

```
tools_via_api/
├── app.py                 # Main Flask application entry point
├── requirements.txt       # Python dependencies
├── .gitignore            # Git ignore rules
├── README.md             # This file
├── routes/               # API route definitions
│   ├── __init__.py
│   └── tool_routes.py    # Tool execution endpoints
└── tools/                # Tool implementations
    ├── __init__.py
    ├── base_tool.py      # Base tool class
    └── tool_pdfid.py     # PDF analysis tool
```

## 🔌 Adding New Tools

To add a new tool, follow these steps:

### 1. Create Tool Class
Create a new file in the `tools/` directory:

```python
from .base_tool import BaseTool

class MyNewTool(BaseTool):
    def __init__(self):
        super().__init__("MyNewTool")
    
    def run(self, file_storage):
        # Your tool logic here
        return {"result": "analysis complete"}
```

### 2. Register Tool
Add the tool to the `TOOLS` dictionary in `routes/tool_routes.py`:

```python
from tools.my_new_tool import MyNewTool

TOOLS = {
    "pdfid": PdfIdTool(),
    "mynewtool": MyNewTool(),  # Add your new tool
}
```

### 3. Test the Tool
```bash
curl -X POST \
  -F "file=@/path/to/file" \
  http://localhost:5001/tools/mynewtool
```

## 🧪 Testing

### Manual Testing
1. Start the Flask server: `python app.py`
2. Use curl or any HTTP client to test endpoints
3. Check server logs for debugging information

### Testing with Sample Files
Create test PDF files or use existing ones to verify tool functionality.

## 🐛 Troubleshooting

### Common Issues

#### Port 5000 Already in Use
**Problem**: `Address already in use` error on port 5000
**Solution**: The app is configured to use port 5001 by default to avoid conflicts with macOS AirTunes service.

#### Import Errors
**Problem**: `ModuleNotFoundError: No module named 'frontend'`
**Solution**: This was caused by conflicting `fitz` packages. The issue has been resolved by using only PyMuPDF.

#### Virtual Environment Issues
**Problem**: Package installation or import errors
**Solution**: Ensure you're using the correct Python interpreter and virtual environment:
```bash
which python
source .venv/bin/activate
pip list
```

### Debug Mode
The application runs in debug mode by default. Check the terminal output for:
- Request logs
- Error messages
- Debug information

## 📝 Configuration

### Environment Variables
- `FLASK_ENV`: Set to `development` for debug mode (default)
- `FLASK_DEBUG`: Set to `1` to enable debug mode (default)

### Port Configuration
The default port is 5001. To change it, modify `app.py`:

```python
if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=YOUR_PORT)
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Commit your changes: `git commit -am 'Add feature'`
4. Push to the branch: `git push origin feature-name`
5. Submit a pull request

## 📄 License

[Add your license information here]

## 🆘 Support

For issues and questions:
1. Check the troubleshooting section
2. Review server logs
3. Create an issue in the repository

## 🔮 Future Enhancements

- [ ] Add more analysis tools (image analysis, text extraction, etc.)
- [ ] Implement authentication and rate limiting
- [ ] Add support for batch file processing
- [ ] Create a web-based frontend
- [ ] Add tool result caching
- [ ] Implement async processing for large files
- [ ] Add comprehensive test suite
- [ ] Docker containerization
- [ ] CI/CD pipeline setup

---

**Note**: This is a development server. For production use, deploy with a proper WSGI server like Gunicorn or uWSGI.