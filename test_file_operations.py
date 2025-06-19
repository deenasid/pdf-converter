import os
import shutil

def test_file_operations():
    print("=== Testing File Operations ===")
    
    # Test 1: Check if folders exist
    uploads_folder = 'uploads'
    output_folder = 'output'
    
    print(f"1. Checking folders...")
    print(f"   Uploads folder exists: {os.path.exists(uploads_folder)}")
    print(f"   Output folder exists: {os.path.exists(output_folder)}")
    
    # Test 2: Create folders if they don't exist
    print(f"\n2. Creating folders if needed...")
    os.makedirs(uploads_folder, exist_ok=True)
    os.makedirs(output_folder, exist_ok=True)
    print(f"   Folders created/verified")
    
    # Test 3: Check files in uploads folder
    print(f"\n3. Checking files in uploads folder...")
    if os.path.exists(uploads_folder):
        files = os.listdir(uploads_folder)
        print(f"   Files found: {files}")
        for file in files:
            file_path = os.path.join(uploads_folder, file)
            if os.path.isfile(file_path):
                size = os.path.getsize(file_path)
                print(f"   - {file}: {size} bytes")
    
    # Test 4: Test file read/write
    print(f"\n4. Testing file read/write...")
    test_file = os.path.join(uploads_folder, 'test.txt')
    try:
        # Write test file
        with open(test_file, 'w') as f:
            f.write('Test content')
        print(f"   Test file created: {test_file}")
        
        # Read test file
        with open(test_file, 'r') as f:
            content = f.read()
        print(f"   Test file read: '{content}'")
        
        # Check file size
        size = os.path.getsize(test_file)
        print(f"   Test file size: {size} bytes")
        
        # Clean up
        os.remove(test_file)
        print(f"   Test file cleaned up")
        
    except Exception as e:
        print(f"   Error: {e}")
    
    # Test 5: Test file copy
    print(f"\n5. Testing file copy...")
    if os.path.exists(uploads_folder) and os.listdir(uploads_folder):
        source_file = os.path.join(uploads_folder, os.listdir(uploads_folder)[0])
        dest_file = os.path.join(output_folder, 'copy_test.txt')
        
        try:
            shutil.copy2(source_file, dest_file)
            print(f"   File copied: {source_file} -> {dest_file}")
            
            if os.path.exists(dest_file):
                size = os.path.getsize(dest_file)
                print(f"   Copy successful: {size} bytes")
                os.remove(dest_file)
                print(f"   Copy cleaned up")
            else:
                print(f"   Copy failed")
                
        except Exception as e:
            print(f"   Copy error: {e}")
    
    print(f"\n=== Test Complete ===")

if __name__ == "__main__":
    test_file_operations() 