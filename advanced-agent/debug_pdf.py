#!/usr/bin/env python3
"""Debug script to test PDF loading"""

import traceback
import fitz
import os
from src.pdf_loader import PDFLoader

def test_pdf_loading():
    print("🔍 Testing PDF loading...")
    
    file_path = "src/BasicNDA.pdf"
    
    # Test 1: Check if file exists
    print(f"📁 File exists: {os.path.exists(file_path)}")
    print(f"📁 File size: {os.path.getsize(file_path) if os.path.exists(file_path) else 'N/A'} bytes")
    
    # Test 2: Try direct PyMuPDF loading with detailed analysis
    print("\n🔍 Testing direct PyMuPDF loading...")
    try:
        doc = fitz.open(file_path)
        print(f"✅ PDF opened successfully: {len(doc)} pages")
        
        total_text = ""
        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            
            # Try different text extraction methods
            text1 = page.get_text()  # Standard text extraction
            text2 = page.get_text("text")  # Explicit text mode
            text3 = page.get_text("words")  # Word-based extraction
            text4 = page.get_text("dict")   # Dictionary format
            
            print(f"📄 Page {page_num + 1}:")
            print(f"   Standard text: {len(text1)} chars")
            print(f"   Text mode: {len(text2)} chars")
            print(f"   Words mode: {len(text3)} chars")
            print(f"   Dict mode: {len(text4)} chars")
            
            if text1:
                print(f"   Sample text: {text1[:100]}...")
                total_text += text1 + "\n"
            elif text2:
                print(f"   Sample text (mode): {text2[:100]}...")
                total_text += text2 + "\n"
            elif text3:
                print(f"   Sample words: {text3[:100]}...")
                total_text += text3 + "\n"
        
        print(f"\n📝 Total extracted text: {len(total_text)} characters")
        if total_text:
            print(f"📝 First 300 chars: {total_text[:300]}")
        
        doc.close()
        
    except Exception as e:
        print(f"❌ Direct PyMuPDF error: {e}")
        traceback.print_exc()
    
    # Test 3: Try our PDF loader
    print("\n🔍 Testing our PDF loader...")
    try:
        loader = PDFLoader()
        print("✅ PDF Loader created")
        
        text = loader.load_pdf(file_path)
        
        if text:
            print(f"✅ Successfully loaded PDF: {len(text)} characters")
            print(f"📝 First 200 characters: {text[:200]}")
            return True
        else:
            print("❌ PDF loading returned None")
            return False
            
    except Exception as e:
        print(f"❌ Error loading PDF: {e}")
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_pdf_loading() 