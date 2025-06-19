import os
from pdf2docx import Converter
import pythoncom
from docx2pdf import convert

def test_pdf_to_word():
    print("=== Testing PDF to Word Conversion ===")
    
    # Find a PDF file in uploads
    uploads_folder = 'uploads'
    pdf_files = [f for f in os.listdir(uploads_folder) if f.lower().endswith('.pdf')]
    
    if not pdf_files:
        print("No PDF files found in uploads folder")
        return False
    
    pdf_file = os.path.join(uploads_folder, pdf_files[0])
    output_file = os.path.join(uploads_folder, 'test_output.docx')
    
    print(f"Input PDF: {pdf_file}")
    print(f"Output DOCX: {output_file}")
    
    try:
        # Convert PDF to Word
        cv = Converter(pdf_file)
        cv.convert(output_file)
        cv.close()
        
        if os.path.exists(output_file):
            size = os.path.getsize(output_file)
            print(f"Conversion successful: {size} bytes")
            
            # Clean up
            os.remove(output_file)
            print("Test file cleaned up")
            return True
        else:
            print("Conversion failed: Output file not created")
            return False
            
    except Exception as e:
        print(f"Conversion error: {e}")
        return False

def test_word_to_pdf():
    print("\n=== Testing Word to PDF Conversion ===")
    
    # Find a Word file in uploads
    uploads_folder = 'uploads'
    word_files = [f for f in os.listdir(uploads_folder) if f.lower().endswith(('.docx', '.doc'))]
    
    if not word_files:
        print("No Word files found in uploads folder")
        return False
    
    word_file = os.path.join(uploads_folder, word_files[0])
    output_file = os.path.join(uploads_folder, 'test_output.pdf')
    
    print(f"Input Word: {word_file}")
    print(f"Output PDF: {output_file}")
    
    try:
        # Initialize COM
        pythoncom.CoInitialize()
        
        # Convert Word to PDF
        convert(word_file, output_file)
        
        if os.path.exists(output_file):
            size = os.path.getsize(output_file)
            print(f"Conversion successful: {size} bytes")
            
            # Clean up
            os.remove(output_file)
            print("Test file cleaned up")
            return True
        else:
            print("Conversion failed: Output file not created")
            return False
            
    except Exception as e:
        print(f"Conversion error: {e}")
        return False
    finally:
        try:
            pythoncom.CoUninitialize()
        except:
            pass

if __name__ == "__main__":
    print("Testing conversion libraries...")
    
    # Test PDF to Word
    pdf_success = test_pdf_to_word()
    
    # Test Word to PDF
    word_success = test_word_to_pdf()
    
    print(f"\n=== Results ===")
    print(f"PDF to Word: {'✓' if pdf_success else '✗'}")
    print(f"Word to PDF: {'✓' if word_success else '✗'}") 