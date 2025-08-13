# Tools via API

A Flask-based REST API that provides access to various analysis tools, currently featuring a PDF identification tool that analyzes PDF files for metadata and security information.

## 🚀 Features

- **PDF Analysis Tool**: Analyze PDF files for metadata, embedded objects, and potential security risks
- **RESTful API**: Clean, simple HTTP endpoints for tool execution
- **File Upload Support**: Accept PDF files via multipart form data
- **Extensible Architecture**: Easy to add new tools following the base tool pattern
- **JSON Response**: Structured JSON responses for easy integration
- **Docker Support**: Containerized deployment with GitHub Container Registry

## 🛠️ Technology Stack

- **Backend**: Flask 3.1.1
- **PDF Processing**: PyMuPDF (fitz) + pdfid
- **Python Version**: 3.13+
- **Virtual Environment**: Python venv
- **Containerization**: Docker + Docker Compose
- **CI/CD**: GitHub Actions

## 📋 Prerequisites

- Python 3.13 or higher
- pip (Python package installer)
- Git (for cloning the repository)
- Docker (for containerized deployment)
- Docker Compose (for local development)

## 🚀 Installation & Setup

### Option 1: Local Development

#### 1. Clone the Repository
```bash
git clone <your-repository-url>
cd tools_via_api
```

#### 2. Create Virtual Environment
```bash
python3 -m venv .venv
```

#### 3. Activate Virtual Environment

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

#### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

#### 5. Start the Flask Server
```bash
python app.py
```

The server will start on `http://127.0.0.1:5001`.

### Option 2: Docker Development

#### 1. Build and Run with Docker Compose
```bash
# Build and start the services
docker-compose up --build

# Run in background
docker-compose up -d --build

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

#### 2. Build and Run with Docker
```bash
# Build the image
docker build -t tools-via-api .

# Run the container
docker run -p 5001:5001 tools-via-api

# Run in background
docker run -d -p 5001:5001 --name tools-api tools-via-api
```

## 🐳 Docker Deployment

### Building the Image
```bash
# Build locally
docker build -t tools-via-api .

# Build with specific tag
docker build -t tools-via-api:v1.0.0 .
```

### Running the Container
```bash
# Basic run
docker run -p 5001:5001 tools-via-api

# With environment variables
docker run -p 5001:5001 \
  -e FLASK_ENV=production \
  -e FLASK_DEBUG=0 \
  tools-via-api

# With volume mounts
docker run -p 5001:5001 \
  -v $(pwd)/logs:/app/logs \
  tools-via-api
```

### Production Deployment
```bash
# Run with nginx reverse proxy
docker-compose --profile production up -d

# Scale the API service
docker-compose up -d --scale tools-api=3
```

## 📦 GitHub Container Registry

This project is configured to automatically publish Docker images to GitHub Container Registry (GHCR) via GitHub Actions.

### Automatic Publishing
- **Branches**: Images are built and published for `main` and `develop` branches
- **Tags**: Versioned releases (e.g., `v1.0.0`) are automatically published
- **Pull Requests**: Images are built but not published for PRs

### Manual Publishing
```bash
# Login to GHCR
echo $GITHUB_TOKEN | docker login ghcr.io -u USERNAME --password-stdin

# Tag your image
docker tag tools-via-api ghcr.io/USERNAME/tools_via_api:latest

# Push to registry
docker push ghcr.io/USERNAME/tools_via_api:latest
```

### Using Published Images
```bash
# Pull from GHCR
docker pull ghcr.io/USERNAME/tools_via_api:latest

# Run from GHCR
docker run -p 5001:5001 ghcr.io/USERNAME/tools_via_api:latest
```

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
    "filename": "document.pdf",
    "filesize": 2853,
    "header": "%PDF-1.4",
    "version": "0.2.7",
    "isPdf": "True",
    "obj": 15,
    "endobj": 15,
    "stream": 2,
    "endstream": 2,
    "xref": 1,
    "trailer": 1,
    "startxref": 1,
    "/Page": 1,
    "/Encrypt": 0,
    "/ObjStm": 0,
    "/JS": 0,
    "/JavaScript": 0,
    "/AA": 0,
    "/OpenAction": 0,
    "/AcroForm": 0,
    "/JBIG2Decode": 0,
    "/RichMedia": 0,
    "/Launch": 0,
    "/EmbeddedFile": 0,
    "/XFA": 0,
    "/Colors > 2^24": 0
  }
}
```

## 🏗️ Project Structure

```
tools_via_api/
├── app.py                 # Main Flask application entry point
├── requirements.txt       # Python dependencies
├── Dockerfile            # Docker container definition
├── docker-compose.yml    # Docker Compose configuration
├── nginx.conf            # Nginx reverse proxy configuration
├── .dockerignore         # Docker build exclusions
├── .gitignore            # Git ignore rules
├── README.md             # This file
├── .github/workflows/    # GitHub Actions workflows
│   └── docker-publish.yml # Docker build and publish workflow
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
1. Start the Flask server: `python app.py` or `docker-compose up`
2. Use curl or any HTTP client to test endpoints
3. Check server logs for debugging information

### Testing with Sample Files
Create test PDF files or use existing ones to verify tool functionality.

### Docker Testing
```bash
# Test the containerized version
docker-compose up --build
curl -X POST -F "file=@test.pdf" http://localhost:5001/tools/pdfid
```

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

#### Docker Issues
**Problem**: Container won't start or build fails
**Solution**: Check Docker logs and ensure all dependencies are properly specified:
```bash
docker-compose logs
docker build --no-cache .
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
- `PORT`: Port to run the application on (default: 5001)

### Port Configuration
The default port is 5001. To change it, modify `app.py`:

```python
if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=YOUR_PORT)
```

### Docker Configuration
Modify `docker-compose.yml` to change ports, environment variables, or add additional services.

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
- [ ] CI/CD pipeline setup (✅ Docker publishing)
- [ ] Kubernetes deployment manifests
- [ ] Monitoring and logging integration
- [ ] API versioning support

---

**Note**: This is a development server. For production use, deploy with a proper WSGI server like Gunicorn or uWSGI, or use the provided Docker containers with a reverse proxy like Nginx.