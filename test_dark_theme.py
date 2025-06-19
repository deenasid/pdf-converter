#!/usr/bin/env python3
"""
Test script to verify dark theme functionality across all pages
"""

import requests
import time
from urllib.parse import urljoin

BASE_URL = "http://127.0.0.1:5000"

def test_dark_theme_elements():
    """Test that dark theme elements are present in HTML"""
    pages = [
        "/",  # Home page
        "/select_file?type=pdf",  # Word to PDF
        "/select_file?type=word",  # PDF to Word
    ]
    
    print("Testing dark theme elements...")
    
    for page in pages:
        try:
            response = requests.get(urljoin(BASE_URL, page), timeout=5)
            if response.status_code == 200:
                html = response.text
                
                # Check for dark theme CSS classes
                dark_theme_elements = [
                    '.dark-theme',
                    'dark-theme',
                    'toggleTheme()',
                    'light-icon',
                    'dark-icon'
                ]
                
                missing_elements = []
                for element in dark_theme_elements:
                    if element not in html:
                        missing_elements.append(element)
                
                if missing_elements:
                    print(f"❌ {page} - Missing dark theme elements: {missing_elements}")
                else:
                    print(f"✅ {page} - All dark theme elements found")
                
                # Check for specific dark theme styles
                dark_styles = [
                    '.dark-theme .header',
                    '.dark-theme .copyright-section',
                    'linear-gradient(135deg, #1a237e, #0d47a1)'
                ]
                
                missing_styles = []
                for style in dark_styles:
                    if style not in html:
                        missing_styles.append(style)
                
                if missing_styles:
                    print(f"⚠️  {page} - Missing dark theme styles: {missing_styles}")
                else:
                    print(f"✅ {page} - All dark theme styles found")
                    
        except requests.exceptions.RequestException as e:
            print(f"❌ {page} - Connection error: {e}")
    
    print("\n" + "="*50 + "\n")

def test_theme_toggle_functionality():
    """Test that theme toggle JavaScript is properly implemented"""
    print("Testing theme toggle functionality...")
    
    try:
        response = requests.get(BASE_URL, timeout=5)
        if response.status_code == 200:
            html = response.text
            
            # Check for theme toggle JavaScript
            js_elements = [
                'toggleTheme()',
                'localStorage.setItem',
                'localStorage.getItem',
                'classList.toggle',
                'classList.add',
                'classList.remove'
            ]
            
            missing_js = []
            for element in js_elements:
                if element not in html:
                    missing_js.append(element)
            
            if missing_js:
                print(f"❌ Missing JavaScript elements: {missing_js}")
            else:
                print("✅ All theme toggle JavaScript elements found")
                
            # Check for theme persistence
            if 'localStorage.setItem(\'theme\'' in html and 'localStorage.getItem(\'theme\'' in html:
                print("✅ Theme persistence functionality found")
            else:
                print("❌ Theme persistence functionality missing")
                
    except requests.exceptions.RequestException as e:
        print(f"❌ Connection error: {e}")
    
    print("\n" + "="*50 + "\n")

def main():
    """Run all dark theme tests"""
    print("🌙 Testing Dark Theme Functionality")
    print("="*50)
    
    # Wait a moment for the server to be ready
    time.sleep(2)
    
    test_dark_theme_elements()
    test_theme_toggle_functionality()
    
    print("🎉 Dark theme testing complete!")
    print("\n📋 Manual Testing Instructions:")
    print("1. Open http://127.0.0.1:5000 in your browser")
    print("2. Click the theme toggle button (🌙/☀️) in the header")
    print("3. Verify the following elements change to dark theme:")
    print("   - Header background (should be dark blue gradient)")
    print("   - Main content background (should be dark)")
    print("   - File selection box (should be dark)")
    print("   - Copyright section (should be dark blue gradient)")
    print("   - All text colors (should be light)")
    print("4. Refresh the page and verify theme persists")
    print("5. Navigate to other pages and test theme consistency")
    print("6. Check browser console for any JavaScript errors")

if __name__ == "__main__":
    main() 