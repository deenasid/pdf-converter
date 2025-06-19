from flask import Flask, render_template, request, send_file, jsonify, abort, redirect, url_for
from PyPDF2 import PdfReader, PdfWriter
from pdf2image import convert_from_path
from docx import Document
import os
import tempfile
from werkzeug.utils import secure_filename
from pdf2docx import Converter
import mimetypes
from docx2pdf import convert
import shutil

app = Flask(__name__, static_folder='static', static_url_path='/static')

# Configuration
UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'output'
ALLOWED_EXTENSIONS = {'pdf', 'docx', 'jpg', 'jpeg', 'png'}

# Set Poppler path
POPPLER_PATH = os.path.join(os.getcwd(), 'poppler', 'poppler-24.02.0', 'Library', 'bin')

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Ensure folders exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# Add MIME type mappings
mimetypes.add_type('application/vnd.openxmlformats-officedocument.wordprocessingml.document', '.docx')
mimetypes.add_type('image/jpeg', '.jpg')
mimetypes.add_type('application/pdf', '.pdf')

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def convert_word_to_pdf(input_file, output_file):
    try:
        # Ensure input file exists and is readable
        if not os.path.exists(input_file):
            raise Exception(f"Input file not found: {input_file}")
        
        # Check if input file is readable
        if not os.access(input_file, os.R_OK):
            raise Exception(f"Input file not readable: {input_file}")
        
        # Ensure output directory exists
        output_dir = os.path.dirname(output_file)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir, exist_ok=True)
        
        # Initialize COM for this thread
        try:
            # Convert using docx2pdf with explicit file handling
            convert(input_file, output_file)
            
            # Verify the output file was created and has content
            if os.path.exists(output_file) and os.path.getsize(output_file) > 0:
                print(f"Successfully converted {input_file} to {output_file}")
                return True
            else:
                raise Exception("Conversion failed: Output file is empty or not created")
                
        except Exception as conversion_error:
            print(f"Conversion error: {str(conversion_error)}")
            raise conversion_error
            
    except Exception as e:
        print(f"Error in convert_word_to_pdf: {str(e)}")
        return False

def convert_pdf_to_word(input_file, output_file):
    try:
        # Ensure input file exists and is readable
        if not os.path.exists(input_file):
            raise Exception(f"Input file not found: {input_file}")
        
        # Check if input file is readable
        if not os.access(input_file, os.R_OK):
            raise Exception(f"Input file not readable: {input_file}")
        
        # Ensure output directory exists
        output_dir = os.path.dirname(output_file)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir, exist_ok=True)
        
        # Use pdf2docx for conversion with explicit file handling
        cv = None
        try:
            cv = Converter(input_file)
            cv.convert(output_file)
            
            # Verify the output file exists and has content
            if os.path.exists(output_file) and os.path.getsize(output_file) > 0:
                print(f"Successfully converted {input_file} to {output_file}")
                return True
            else:
                raise Exception("Conversion failed: Output file is empty or not created")
                
        except Exception as conversion_error:
            print(f"Conversion error: {str(conversion_error)}")
            raise conversion_error
        finally:
            # Always close the converter
            if cv:
                try:
                    cv.close()
                except:
                    pass
            
    except Exception as e:
        print(f"Error in PDF to Word conversion: {str(e)}")
        return False

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/select_file')
def select_file():
    conversion_type = request.args.get('type', 'pdf')
    return render_template('select_file.html', type=conversion_type)

@app.route('/convert', methods=['POST'])
def convert_file():
    print("=== Starting file conversion ===")
    
    if 'file' not in request.files:
        print("No file in request")
        return jsonify({'error': 'No file uploaded'}), 400
    
    file = request.files['file']
    conversion_type = request.form.get('type', 'word')
    
    print(f"File: {file.filename}, Type: {conversion_type}")
    
    if file.filename == '':
        print("No filename")
        return jsonify({'error': 'No file selected'}), 400
    
    # Validate file type
    if conversion_type == 'word' and not file.filename.lower().endswith('.pdf'):
        return jsonify({'error': 'Please upload a PDF file for conversion to Word'}), 400
    elif conversion_type == 'pdf' and not file.filename.lower().endswith(('.docx', '.doc')):
        return jsonify({'error': 'Please upload a Word file for conversion to PDF'}), 400
    
    try:
        # Save uploaded file directly to uploads folder
        filename = secure_filename(file.filename)
        input_path = os.path.join(UPLOAD_FOLDER, filename)
        
        print(f"Saving file to: {input_path}")
        file.save(input_path)
        
        # Check if file was saved
        if not os.path.exists(input_path):
            raise Exception("Failed to save uploaded file")
        
        file_size = os.path.getsize(input_path)
        print(f"File saved: {file_size} bytes")
        
        if file_size == 0:
            raise Exception("Uploaded file is empty")
        
        # Determine output filename
        output_filename = os.path.splitext(filename)[0]
        if conversion_type == 'pdf':
            output_filename += '.pdf'
        else:
            output_filename += '.docx'
        
        output_path = os.path.join(UPLOAD_FOLDER, output_filename)
        print(f"Output path: {output_path}")
        
        # Perform conversion
        success = False
        if conversion_type == 'pdf':
            success = convert_word_to_pdf(input_path, output_path)
        else:
            success = convert_pdf_to_word(input_path, output_path)
        
        print(f"Conversion success: {success}")
        
        if success and os.path.exists(output_path):
            # Get file size
            output_size = os.path.getsize(output_path)
            if output_size < 1024:
                size_str = f"{output_size} B"
            elif output_size < 1024 * 1024:
                size_str = f"{output_size / 1024:.1f} KB"
            else:
                size_str = f"{output_size / (1024 * 1024):.1f} MB"
            
            # Create success message
            if conversion_type == 'pdf':
                success_message = 'Word document converted to PDF successfully!'
            else:
                success_message = 'PDF converted to Word document successfully!'
            
            # Clean up input file
            try:
                os.remove(input_path)
                print(f"Removed input file: {input_path}")
            except:
                pass
            
            # Prepare files info for download page
            files_info = [{'name': output_filename, 'size': size_str}]
            files_param = str(files_info).replace("'", '"')
            
            print(f"Conversion completed: {output_filename}")
            return redirect(url_for('download', success='true', message=success_message, files=files_param))
        else:
            # Clean up input file on failure
            try:
                os.remove(input_path)
            except:
                pass
            
            error_message = 'Conversion failed. Please try again.'
            return redirect(url_for('download', success='false', message=error_message, files='[]'))
            
    except Exception as e:
        print(f"Error: {e}")
        error_message = f'Error: {str(e)}'
        return redirect(url_for('download', success='false', message=error_message, files='[]'))

@app.route('/split', methods=['POST'])
def split_pdf():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if not allowed_file(file.filename):
        return jsonify({'error': 'Invalid file type'}), 400
    
    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)
    
    try:
        # Split PDF logic
        pdf = PdfReader(filepath)
        output_files = []
        
        for i, page in enumerate(pdf.pages):
            writer = PdfWriter()
            writer.add_page(page)
            output_filename = f"page_{i+1}.pdf"
            output_path = os.path.join(app.config['UPLOAD_FOLDER'], output_filename)
            
            with open(output_path, 'wb') as out:
                writer.write(out)
            output_files.append(output_filename)
        
        # Clean up input file
        os.remove(filepath)
        
        # Redirect to download page with success message
        files_info = []
        for filename in output_files:
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            if os.path.exists(file_path):
                file_size = os.path.getsize(file_path)
                # Convert to human readable format
                if file_size < 1024:
                    size_str = f"{file_size} B"
                elif file_size < 1024 * 1024:
                    size_str = f"{file_size / 1024:.1f} KB"
                else:
                    size_str = f"{file_size / (1024 * 1024):.1f} MB"
                files_info.append({'name': filename, 'size': size_str})
            else:
                files_info.append({'name': filename, 'size': 'Ready for download'})
        
        files_param = str(files_info).replace("'", '"')
        return redirect(url_for('download', success='true', message='PDF split successfully', files=files_param))
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/to-images', methods=['POST'])
def to_images():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if not file.filename.lower().endswith('.pdf'):
        return jsonify({'error': 'File must be a PDF'}), 400

    try:
        # Save the uploaded file
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        # Convert PDF to images
        images = convert_from_path(filepath, poppler_path=POPPLER_PATH)
        
        # Save images
        image_files = []
        for i, image in enumerate(images):
            image_filename = f"{os.path.splitext(filename)[0]}_page_{i+1}.jpg"
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], image_filename)
            image.save(image_path, 'JPEG')
            image_files.append(image_filename)

        # Clean up the original PDF
        os.remove(filepath)

        # Get file sizes for download page
        files_info = []
        for image_filename in image_files:
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], image_filename)
            if os.path.exists(image_path):
                file_size = os.path.getsize(image_path)
                if file_size < 1024:
                    size_str = f"{file_size} B"
                elif file_size < 1024 * 1024:
                    size_str = f"{file_size / 1024:.1f} KB"
                else:
                    size_str = f"{file_size / (1024 * 1024):.1f} MB"
                files_info.append({'name': image_filename, 'size': size_str})
            else:
                files_info.append({'name': image_filename, 'size': 'Ready for download'})
        
        files_param = str(files_info).replace("'", '"')
        return redirect(url_for('download', success='true', message=f'Successfully converted PDF to {len(image_files)} images', files=files_param))

    except Exception as e:
        return redirect(url_for('download', success='false', message=f'Conversion failed: {str(e)}', files='[]'))

@app.route('/to-pdf', methods=['POST'])
def to_pdf():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if not file.filename.lower().endswith(('.docx', '.doc')):
        return jsonify({'error': 'File must be a Word document (.docx or .doc)'}), 400

    try:
        # Save the uploaded file
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        # Generate output filename
        output_filename = f"{os.path.splitext(filename)[0]}.pdf"
        output_path = os.path.join(app.config['UPLOAD_FOLDER'], output_filename)

        # Convert Word to PDF
        convert(filepath, output_path)

        # Clean up the original Word file
        os.remove(filepath)

        # Get file size for download page
        file_size = os.path.getsize(output_path)
        if file_size < 1024:
            size_str = f"{file_size} B"
        elif file_size < 1024 * 1024:
            size_str = f"{file_size / 1024:.1f} KB"
        else:
            size_str = f"{file_size / (1024 * 1024):.1f} MB"
        
        files_info = [{'name': output_filename, 'size': size_str}]
        files_param = str(files_info).replace("'", '"')
        
        return redirect(url_for('download', success='true', message='Word document converted to PDF successfully!', files=files_param))

    except Exception as e:
        return redirect(url_for('download', success='false', message=f'Conversion failed: {str(e)}', files='[]'))

@app.route('/to-word', methods=['POST'])
def to_word():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if not file.filename.lower().endswith('.pdf'):
        return jsonify({'error': 'File must be a PDF'}), 400

    try:
        # Save the uploaded file
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        # Generate output filename
        output_filename = f"{os.path.splitext(filename)[0]}.docx"
        output_path = os.path.join(app.config['UPLOAD_FOLDER'], output_filename)

        # Convert PDF to Word
        cv = Converter(filepath)
        cv.convert(output_path)
        cv.close()

        # Clean up the original PDF
        os.remove(filepath)

        # Get file size for download page
        file_size = os.path.getsize(output_path)
        if file_size < 1024:
            size_str = f"{file_size} B"
        elif file_size < 1024 * 1024:
            size_str = f"{file_size / 1024:.1f} KB"
        else:
            size_str = f"{file_size / (1024 * 1024):.1f} MB"
        
        files_info = [{'name': output_filename, 'size': size_str}]
        files_param = str(files_info).replace("'", '"')
        
        return redirect(url_for('download', success='true', message='PDF converted to Word document successfully!', files=files_param))

    except Exception as e:
        return redirect(url_for('download', success='false', message=f'Conversion failed: {str(e)}', files='[]'))

@app.route('/download')
def download():
    success = request.args.get('success', 'false') == 'true'
    message = request.args.get('message', '')
    files = request.args.get('files', '[]')
    
    try:
        files = eval(files)  # Convert string representation of list to actual list
    except:
        files = []
    
    return render_template('download.html', success=success, message=message, files=files)

@app.route('/download_file/<filename>')
def download_file(filename):
    """Download a file with improved error handling"""
    try:
        print(f"=== Download request for: {filename} ===")
        
        # Secure the filename
        safe_filename = secure_filename(filename)
        print(f"Safe filename: {safe_filename}")
        
        # Look for file in uploads folder first, then output folder
        file_path = None
        for folder in [UPLOAD_FOLDER, OUTPUT_FOLDER]:
            test_path = os.path.join(folder, safe_filename)
            if os.path.exists(test_path):
                file_path = test_path
                print(f"File found in {folder}: {file_path}")
                break
        
        if not file_path:
            print(f"File not found in any folder: {safe_filename}")
            return jsonify({'error': f'File "{safe_filename}" not found'}), 404
        
        # Check if file is readable
        if not os.access(file_path, os.R_OK):
            print(f"File not readable: {file_path}")
            return jsonify({'error': f'File "{safe_filename}" is not accessible'}), 403
        
        # Get file size
        try:
            file_size = os.path.getsize(file_path)
            print(f"File size: {file_size} bytes")
            if file_size == 0:
                print("File is empty")
                return jsonify({'error': f'File "{safe_filename}" is empty'}), 400
        except OSError as e:
            print(f"Error getting file size: {e}")
            return jsonify({'error': f'Cannot access file "{safe_filename}"'}), 500
        
        # Determine MIME type
        file_ext = os.path.splitext(safe_filename)[1].lower()
        if file_ext == '.pdf':
            mimetype = 'application/pdf'
        elif file_ext in ['.docx', '.doc']:
            mimetype = 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
        elif file_ext in ['.jpg', '.jpeg']:
            mimetype = 'image/jpeg'
        elif file_ext == '.png':
            mimetype = 'image/png'
        else:
            mimetype = 'application/octet-stream'
        
        print(f"MIME type: {mimetype}")
        
        # Send file with proper headers
        response = send_file(
            file_path,
            as_attachment=True,
            download_name=safe_filename,
            mimetype=mimetype
        )
        
        # Add headers to prevent caching issues
        response.headers['Content-Disposition'] = f'attachment; filename="{safe_filename}"'
        response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '0'
        response.headers['Content-Length'] = str(file_size)
        
        print(f"Download response prepared successfully")
        return response
        
    except Exception as e:
        print(f"Download error: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': f'Download failed: {str(e)}'}), 500

@app.route('/check_file/<filename>')
def check_file(filename):
    """Check if a file exists and is accessible"""
    try:
        safe_filename = secure_filename(filename)
        
        # Check in both folders
        upload_path = os.path.join(UPLOAD_FOLDER, safe_filename)
        output_path = os.path.join(OUTPUT_FOLDER, safe_filename)
        
        file_info = {
            'exists': False,
            'readable': False,
            'size': 0,
            'path': None,
            'error': None
        }
        
        # Check uploads folder first
        if os.path.exists(upload_path):
            file_info['exists'] = True
            file_info['path'] = upload_path
        elif os.path.exists(output_path):
            file_info['exists'] = True
            file_info['path'] = output_path
        
        if file_info['exists']:
            try:
                # Check if file is readable
                if os.access(file_info['path'], os.R_OK):
                    file_info['readable'] = True
                    file_info['size'] = os.path.getsize(file_info['path'])
                else:
                    file_info['error'] = 'File not readable'
            except Exception as e:
                file_info['error'] = str(e)
        else:
            file_info['error'] = 'File not found'
        
        return jsonify(file_info)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def cleanup_old_files():
    """Clean up old files from upload and output folders"""
    try:
        import time
        current_time = time.time()
        max_age = 3600  # 1 hour
        
        for folder in [UPLOAD_FOLDER, OUTPUT_FOLDER]:
            if os.path.exists(folder):
                for filename in os.listdir(folder):
                    file_path = os.path.join(folder, filename)
                    try:
                        # Check file age
                        file_age = current_time - os.path.getmtime(file_path)
                        if file_age > max_age:
                            os.remove(file_path)
                            print(f"Cleaned up old file: {file_path}")
                    except Exception as e:
                        print(f"Error cleaning up {file_path}: {e}")
    except Exception as e:
        print(f"Error in cleanup: {e}")

# Clean up old files on startup
cleanup_old_files()

@app.route('/list_files')
def list_files():
    """List all files in uploads and output folders for debugging"""
    try:
        files_info = {
            'uploads': [],
            'output': []
        }
        
        # List files in uploads folder
        if os.path.exists(UPLOAD_FOLDER):
            for filename in os.listdir(UPLOAD_FOLDER):
                file_path = os.path.join(UPLOAD_FOLDER, filename)
                if os.path.isfile(file_path):
                    size = os.path.getsize(file_path)
                    files_info['uploads'].append({
                        'name': filename,
                        'size': size,
                        'readable': os.access(file_path, os.R_OK)
                    })
        
        # List files in output folder
        if os.path.exists(OUTPUT_FOLDER):
            for filename in os.listdir(OUTPUT_FOLDER):
                file_path = os.path.join(OUTPUT_FOLDER, filename)
                if os.path.isfile(file_path):
                    size = os.path.getsize(file_path)
                    files_info['output'].append({
                        'name': filename,
                        'size': size,
                        'readable': os.access(file_path, os.R_OK)
                    })
        
        return jsonify(files_info)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True) 