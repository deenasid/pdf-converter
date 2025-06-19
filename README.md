# PDF Converter Application

A modern web application for converting and manipulating PDF files. Built with Python Flask and Bootstrap.

## Features

- Split PDF into individual pages
- Convert PDF to JPG images
- Modern and responsive user interface
- Real-time file processing
- Secure file handling

## Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- Poppler (for PDF to image conversion)

### Installing Poppler

#### Windows
1. Download Poppler for Windows from: https://github.com/oschwartz10612/poppler-windows/releases/
2. Extract the downloaded file
3. Add the `bin` directory to your system's PATH environment variable

#### macOS
```bash
brew install poppler
```

#### Linux
```bash
sudo apt-get install poppler-utils
```

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd pdf-converter
```

2. Create and activate a virtual environment:
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

3. Install the required packages:
```bash
pip install -r requirements.txt
```

## Running the Application

1. Start the Flask development server:
```bash
python app.py
```

2. Open your web browser and navigate to:
```
http://localhost:5000
```

## Usage

### Split PDF
1. Click on the "Split PDF" card
2. Select a PDF file
3. Wait for the processing to complete
4. Download individual PDF pages

### PDF to Images
1. Click on the "PDF to Images" card
2. Select a PDF file
3. Wait for the processing to complete
4. Download individual JPG images

## Security Features

- File type validation
- Secure filename handling
- Maximum file size limit (16MB)
- Temporary file cleanup

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details. 