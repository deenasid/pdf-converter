#!/usr/bin/env python3
"""
Test script for small Word to PDF conversion
"""

import os
import sys
from app import convert_word_to_pdf

def test_small_word_conversion():
    """Test conversion of small Word files to PDF"""
    
    # Test with a small Word file from uploads folder
    uploads_dir = 'uploads'
    output_dir = 'output'
    
    # Find Word files in uploads
    word_files = []
    for filename in os.listdir(uploads_dir):
        if filename.lower().endswith(('.docx', '.doc')):
            word_files.append(filename)
    
    if not word_files:
        print("No Word files found in uploads folder")
        return False
    
    print(f"Found {len(word_files)} Word files to test:")
    for file in word_files:
        print(f"  - {file}")
    
    # Test each Word file
    success_count = 0
    total_count = len(word_files)
    
    for word_file in word_files:
        print(f"\n--- Testing conversion of {word_file} ---")
        
        input_path = os.path.join(uploads_dir, word_file)
        output_filename = word_file.rsplit('.', 1)[0] + '_test.pdf'
        output_path = os.path.join(output_dir, output_filename)
        
        try:
            # Get file size
            file_size = os.path.getsize(input_path)
            print(f"File size: {file_size} bytes ({file_size/1024:.1f} KB)")
            
            # Attempt conversion
            print("Starting conversion...")
            result = convert_word_to_pdf(input_path, output_path)
            
            if result:
                print(f"✅ SUCCESS: {word_file} converted to {output_filename}")
                success_count += 1
                
                # Check output file
                if os.path.exists(output_path):
                    output_size = os.path.getsize(output_path)
                    print(f"   Output file size: {output_size} bytes ({output_size/1024:.1f} KB)")
                else:
                    print("   ⚠️  Warning: Output file not found")
            else:
                print(f"❌ FAILED: {word_file} conversion failed")
                
        except Exception as e:
            print(f"❌ ERROR: {word_file} - {str(e)}")
    
    print(f"\n--- Test Results ---")
    print(f"Total files tested: {total_count}")
    print(f"Successful conversions: {success_count}")
    print(f"Failed conversions: {total_count - success_count}")
    print(f"Success rate: {(success_count/total_count)*100:.1f}%")
    
    return success_count > 0

if __name__ == "__main__":
    print("Testing small Word to PDF conversion...")
    success = test_small_word_conversion()
    
    if success:
        print("\n✅ Test completed successfully!")
        sys.exit(0)
    else:
        print("\n❌ Test failed!")
        sys.exit(1) 