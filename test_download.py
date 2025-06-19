import requests
import os
import json

def test_download_functionality():
    """Test the download functionality"""
    base_url = "http://127.0.0.1:5000"
    
    print("=== Testing Download Functionality ===")
    
    # Test 1: List files
    print("\n1. Testing /list_files endpoint...")
    try:
        response = requests.get(f"{base_url}/list_files")
        if response.status_code == 200:
            files = response.json()
            print("Files in uploads folder:")
            for file in files['uploads']:
                print(f"  - {file['name']} ({file['size']} bytes, readable: {file['readable']})")
            print("Files in output folder:")
            for file in files['output']:
                print(f"  - {file['name']} ({file['size']} bytes, readable: {file['readable']})")
        else:
            print(f"Error: {response.status_code}")
    except Exception as e:
        print(f"Error: {e}")
    
    # Test 2: Check specific file
    print("\n2. Testing /check_file endpoint...")
    try:
        # Check if there are any files to test with
        response = requests.get(f"{base_url}/list_files")
        if response.status_code == 200:
            files = response.json()
            if files['uploads']:
                test_file = files['uploads'][0]['name']
                print(f"Testing with file: {test_file}")
                
                check_response = requests.get(f"{base_url}/check_file/{test_file}")
                if check_response.status_code == 200:
                    file_info = check_response.json()
                    print(f"File info: {file_info}")
                else:
                    print(f"Check error: {check_response.status_code}")
            else:
                print("No files available for testing")
        else:
            print(f"Error listing files: {response.status_code}")
    except Exception as e:
        print(f"Error: {e}")
    
    # Test 3: Test download endpoint
    print("\n3. Testing /download_file endpoint...")
    try:
        response = requests.get(f"{base_url}/list_files")
        if response.status_code == 200:
            files = response.json()
            if files['uploads']:
                test_file = files['uploads'][0]['name']
                print(f"Testing download with file: {test_file}")
                
                download_response = requests.get(f"{base_url}/download_file/{test_file}")
                print(f"Download response status: {download_response.status_code}")
                print(f"Download response headers: {dict(download_response.headers)}")
                
                if download_response.status_code == 200:
                    print(f"Download successful! File size: {len(download_response.content)} bytes")
                    
                    # Save test download
                    with open(f"test_download_{test_file}", "wb") as f:
                        f.write(download_response.content)
                    print(f"Test file saved as: test_download_{test_file}")
                else:
                    print(f"Download failed: {download_response.text}")
            else:
                print("No files available for download testing")
        else:
            print(f"Error listing files: {response.status_code}")
    except Exception as e:
        print(f"Error: {e}")
    
    print("\n=== Test Complete ===")

if __name__ == "__main__":
    test_download_functionality() 