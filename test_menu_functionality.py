#!/usr/bin/env python3
"""
Test script to verify menu functionality across all pages
"""

import requests
import time
from urllib.parse import urljoin

BASE_URL = "http://127.0.0.1:5000"

def test_page_accessibility():
    """Test that all pages are accessible"""
    pages = [
        "/",  # Home page
        "/select_file?type=pdf",  # Word to PDF
        "/select_file?type=word",  # PDF to Word
    ]
    
    print("Testing page accessibility...")
    for page in pages:
        try:
            response = requests.get(urljoin(BASE_URL, page), timeout=5)
            if response.status_code == 200:
                print(f"✅ {page} - Accessible (Status: {response.status_code})")
            else:
                print(f"❌ {page} - Error (Status: {response.status_code})")
        except requests.exceptions.RequestException as e:
            print(f"❌ {page} - Connection error: {e}")
    
    print("\n" + "="*50 + "\n")

def test_menu_elements():
    """Test that menu elements are present in HTML"""
    print("Testing menu elements in HTML...")
    
    try:
        # Test home page
        response = requests.get(BASE_URL, timeout=5)
        if response.status_code == 200:
            html = response.text
            
            # Check for menu elements
            menu_elements = [
                'menu-toggle',
                'sidebar',
                'overlay',
                'hamburger-line',
                'sidebar-close'
            ]
            
            missing_elements = []
            for element in menu_elements:
                if element not in html:
                    missing_elements.append(element)
            
            if missing_elements:
                print(f"❌ Missing menu elements: {missing_elements}")
            else:
                print("✅ All menu elements found in home page")
            
            # Check for JavaScript functions
            js_functions = [
                'toggleMenu()',
                'openMenu()',
                'closeMenu()'
            ]
            
            missing_functions = []
            for func in js_functions:
                if func not in html:
                    missing_functions.append(func)
            
            if missing_functions:
                print(f"❌ Missing JavaScript functions: {missing_functions}")
            else:
                print("✅ All JavaScript functions found in home page")
        
        # Test select_file page
        response = requests.get(urljoin(BASE_URL, "/select_file?type=pdf"), timeout=5)
        if response.status_code == 200:
            html = response.text
            
            if all(element in html for element in menu_elements):
                print("✅ All menu elements found in select_file page")
            else:
                print("❌ Missing menu elements in select_file page")
            
            if all(func in html for func in js_functions):
                print("✅ All JavaScript functions found in select_file page")
            else:
                print("❌ Missing JavaScript functions in select_file page")
                
    except requests.exceptions.RequestException as e:
        print(f"❌ Connection error: {e}")
    
    print("\n" + "="*50 + "\n")

def test_theme_toggle():
    """Test that theme toggle functionality is present"""
    print("Testing theme toggle functionality...")
    
    try:
        response = requests.get(BASE_URL, timeout=5)
        if response.status_code == 200:
            html = response.text
            
            theme_elements = [
                'theme-toggle',
                'toggleTheme()',
                'light-icon',
                'dark-icon'
            ]
            
            missing_elements = []
            for element in theme_elements:
                if element not in html:
                    missing_elements.append(element)
            
            if missing_elements:
                print(f"❌ Missing theme elements: {missing_elements}")
            else:
                print("✅ All theme toggle elements found")
                
    except requests.exceptions.RequestException as e:
        print(f"❌ Connection error: {e}")
    
    print("\n" + "="*50 + "\n")

def main():
    """Run all tests"""
    print("🧪 Testing Menu Functionality Across All Pages")
    print("="*50)
    
    # Wait a moment for the server to be ready
    time.sleep(2)
    
    test_page_accessibility()
    test_menu_elements()
    test_theme_toggle()
    
    print("🎉 Testing complete!")
    print("\n📋 Manual Testing Instructions:")
    print("1. Open http://127.0.0.1:5000 in your browser")
    print("2. Click the hamburger menu button (☰) in the top-left")
    print("3. Verify the menu slides in from the left")
    print("4. Test clicking the overlay to close the menu")
    print("5. Test pressing ESC key to close the menu")
    print("6. Test the theme toggle button (🌙/☀️)")
    print("7. Navigate to other pages and test menu functionality")
    print("8. Check browser console for any JavaScript errors")

if __name__ == "__main__":
    main() 