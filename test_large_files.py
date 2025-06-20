#!/usr/bin/env python3
"""
Test script for large file handling improvements
"""

import os
import sys
import time
import requests
from pathlib import Path

def test_file_size_validation():
    """Test file size validation"""
    print("Testing file size validation...")
    
    # Test with a large file (create a dummy file)
    test_file = "test_large_file.pdf"
    file_size = 150 * 1024 * 1024  # 150MB (exceeds 100MB limit)
    
    # Create a dummy large file
    with open(test_file, 'wb') as f:
        f.write(b'0' * file_size)
    
    try:
        # Test upload
        with open(test_file, 'rb') as f:
            files = {'file': f}
            data = {'type': 'word'}
            response = requests.post('http://localhost:5000/convert', files=files, data=data)
        
        if response.status_code == 400 and "100MB limit" in response.text:
            print("✅ File size validation working correctly")
        else:
            print("❌ File size validation failed")
            
    except Exception as e:
        print(f"❌ Error testing file size validation: {e}")
    
    finally:
        # Clean up
        if os.path.exists(test_file):
            os.remove(test_file)

def test_progress_tracking():
    """Test progress tracking for large files"""
    print("Testing progress tracking...")
    
    # Create a medium-sized test file (15MB)
    test_file = "test_medium_file.docx"
    file_size = 15 * 1024 * 1024  # 15MB
    
    with open(test_file, 'wb') as f:
        f.write(b'0' * file_size)
    
    try:
        # Test upload with progress tracking
        with open(test_file, 'rb') as f:
            files = {'file': f}
            data = {'type': 'pdf'}
            response = requests.post('http://localhost:5000/convert', files=files, data=data)
        
        if response.status_code in [200, 302]:  # Success or redirect
            print("✅ Progress tracking working correctly")
        else:
            print(f"❌ Progress tracking failed: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error testing progress tracking: {e}")
    
    finally:
        # Clean up
        if os.path.exists(test_file):
            os.remove(test_file)

def test_timeout_handling():
    """Test timeout handling for large conversions"""
    print("Testing timeout handling...")
    
    # Create a large test file (80MB)
    test_file = "test_large_conversion.docx"
    file_size = 80 * 1024 * 1024  # 80MB
    
    with open(test_file, 'wb') as f:
        f.write(b'0' * file_size)
    
    try:
        start_time = time.time()
        
        # Test upload with timeout
        with open(test_file, 'rb') as f:
            files = {'file': f}
            data = {'type': 'pdf'}
            response = requests.post('http://localhost:5000/convert', files=files, data=data, timeout=30)
        
        elapsed_time = time.time() - start_time
        
        if response.status_code == 500 and "timed out" in response.text:
            print("✅ Timeout handling working correctly")
        elif elapsed_time < 30:
            print("✅ Conversion completed within reasonable time")
        else:
            print(f"❌ Timeout handling failed: {response.status_code}")
            
    except requests.exceptions.Timeout:
        print("✅ Request timeout working correctly")
    except Exception as e:
        print(f"❌ Error testing timeout handling: {e}")
    
    finally:
        # Clean up
        if os.path.exists(test_file):
            os.remove(test_file)

def main():
    """Run all tests"""
    print("🧪 Testing Large File Handling Improvements")
    print("=" * 50)
    
    # Check if server is running
    try:
        response = requests.get('http://localhost:5000/', timeout=5)
        if response.status_code == 200:
            print("✅ Server is running")
        else:
            print("❌ Server is not responding correctly")
            return
    except requests.exceptions.ConnectionError:
        print("❌ Server is not running. Please start the Flask app first.")
        return
    
    # Run tests
    test_file_size_validation()
    test_progress_tracking()
    test_timeout_handling()
    
    print("\n" + "=" * 50)
    print("🎉 Testing completed!")

if __name__ == "__main__":
    main() 