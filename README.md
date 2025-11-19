# PTSD OCR Service

A Python OCR service designed to extract text from PDF files and images, with special support for Hebrew text extraction. This service uses multiple OCR engines and techniques to ensure accurate text extraction from various document types.

## Features

- **Multi-format support**: Handles PDF files and various image formats (JPG, PNG, BMP, TIFF, etc.)
- **Hebrew text recognition**: Optimized for Hebrew text extraction with Tesseract OCR Hebrew language support
- **Intelligent PDF processing**: Attempts direct text extraction first, falls back to OCR when needed
- **Image preprocessing**: Uses FFmpeg for converting non-standard image formats
- **File type detection**: Automatic file type detection using python-magic

## Prerequisites

### System Dependencies

Before installing the Python dependencies, you need to install the following system packages:

#### 1. FFmpeg (Required)

FFmpeg is essential for converting non-standard image formats and preprocessing.

**macOS (using Homebrew):**

```bash
brew install ffmpeg
```

**Ubuntu/Debian:**

```bash
sudo apt update
sudo apt install ffmpeg
```

**CentOS/RHEL/Fedora:**

```bash
# For CentOS/RHEL
sudo yum install epel-release
sudo yum install ffmpeg

# For Fedora
sudo dnf install ffmpeg
```

**Windows:**
Download from [FFmpeg official website](https://ffmpeg.org/download.html) and add to PATH, or use package managers like Chocolatey:

```powershell
choco install ffmpeg
```

#### 2. Tesseract OCR Engine

Tesseract is used for optical character recognition.

**macOS:**

```bash
brew install tesseract
brew install tesseract-lang  # Includes Hebrew language pack
```

**Ubuntu/Debian:**

```bash
sudo apt install tesseract-ocr
sudo apt install tesseract-ocr-heb  # Hebrew language pack
```

**CentOS/RHEL/Fedora:**

```bash
# For CentOS/RHEL
sudo yum install tesseract
sudo yum install tesseract-langpack-heb

# For Fedora
sudo dnf install tesseract
sudo dnf install tesseract-langpack-heb
```

**Windows:**
Download from [Tesseract at UB Mannheim](https://github.com/UB-Mannheim/tesseract/wiki) and install, making sure to include the Hebrew language pack.

#### 3. libmagic (for file type detection)

**macOS:**

```bash
brew install libmagic
```

**Ubuntu/Debian:**

```bash
sudo apt install libmagic1
```

**CentOS/RHEL/Fedora:**

```bash
sudo yum install file-devel
# or
sudo dnf install file-devel
```

## Installation

1. **Clone the repository:**

```bash
git clone <repository-url>
cd ptsd-ocr
```

2. **Create and activate virtual environment:**

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install Python dependencies:**

```bash
pip install -r requirements.txt
```

## Usage

### Command Line Interface

Run the main script and provide the path to your file when prompted:

```bash
python main.py
```

Example:

```
Enter the path to your image or PDF file: /path/to/your/document.pdf
```

The extracted text will be printed to the console and saved to `extracted_text.txt`.

### Programmatic Usage

```python
from ocr_service import OCRService

# Initialize the OCR service
ocr_service = OCRService()

# Extract text from a file
text = ocr_service.extract_text("/path/to/your/document.pdf")

if text:
    print("Extracted text:", text)
else:
    print("Failed to extract text")
```

## Supported File Formats

### PDF Files

- Direct text extraction using pdfplumber
- Fallback to OCR using PyMuPDF and Tesseract for scanned PDFs

### Image Files

- **Direct support**: JPG, JPEG, PNG, BMP, TIFF, TIF
- **Via FFmpeg conversion**: Any image format that FFmpeg can handle

## Docker Usage

For easy deployment without local installation, use Docker:

1. **Build the Docker image:**

```bash
docker build -t ptsd-ocr .
```

2. **Run the container:**

```bash
# Interactive mode
docker run -it -v /path/to/your/files:/app/files ptsd-ocr

# Or process a specific file
docker run -v /path/to/your/files:/app/files ptsd-ocr python main.py
```

The Docker image includes all necessary dependencies including FFmpeg, Tesseract with Hebrew language support, and all Python packages.

## Project Structure

```
ptsd-ocr/
├── main.py              # Command line interface
├── ocr_service.py       # Core OCR service class
├── requirements.txt     # Python dependencies
├── Dockerfile          # Docker configuration
└── README.md           # This file
```

## Dependencies

### Python Packages

- `pytesseract`: Python wrapper for Tesseract OCR
- `PyMuPDF`: PDF processing and rendering
- `pdfplumber`: PDF text extraction
- `Pillow`: Image processing
- `python-magic`: File type detection

### System Dependencies

- `FFmpeg`: Image/video conversion
- `Tesseract OCR`: Text recognition with Hebrew language support
- `libmagic`: File type detection library

## Error Handling

The service includes comprehensive error handling:

- File not found detection
- Unsupported file format warnings
- FFmpeg conversion failure handling
- OCR processing error recovery

## Performance Notes

- PDF pages are rendered at 2x resolution for better OCR accuracy
- Hebrew text detection uses a 10% threshold for Hebrew characters
- Temporary files are automatically cleaned up after processing

## Troubleshooting

### Common Issues

1. **"FFmpeg not found" error**

   - Ensure FFmpeg is installed and in your system PATH
   - Test with: `ffmpeg -version`

2. **"Tesseract not found" error**

   - Install Tesseract OCR engine
   - Test with: `tesseract --version`

3. **Poor Hebrew text recognition**

   - Ensure Hebrew language pack is installed for Tesseract
   - Test with: `tesseract --list-langs` (should show 'heb')

4. **libmagic errors**
   - Install libmagic system library
   - On some systems, you may need to set `MAGIC_MIME` environment variable

### Docker Issues

1. **Build fails with dependency errors**

   - Ensure Docker has sufficient memory allocation
   - Try building with `--no-cache` flag

2. **OCR performance in Docker**
   - Mount files using volumes for better I/O performance
   - Consider increasing Docker memory allocation for large documents
