import fitz  # PyMuPDF
import os
from typing import Optional


class PDFLoader:
    """Load and extract text from PDF files using PyMuPDF"""
    
    def __init__(self):
        pass
    
    def load_pdf(self, file_path: str) -> Optional[str]:
        """
        Load a PDF file and extract all text content
        
        Args:
            file_path: Path to the PDF file
            
        Returns:
            Extracted text as string, or None if loading fails
        """
        try:
            if not os.path.exists(file_path):
                raise FileNotFoundError(f"PDF file not found: {file_path}")
            
            # Open the PDF
            doc = fitz.open(file_path)
            text_content = ""
            
            # Extract text from each page
            for page_num in range(len(doc)):
                page = doc.load_page(page_num)
                text_content += page.get_text()
            
            doc.close()
            
            # Clean up the text
            cleaned_text = self._clean_text(text_content)
            return cleaned_text
            
        except Exception as e:
            print(f"Error loading PDF {file_path}: {str(e)}")
            return None
    
    def _clean_text(self, text: str) -> str:
        """
        Clean and normalize extracted text
        
        Args:
            text: Raw extracted text
            
        Returns:
            Cleaned text
        """
        # Remove excessive whitespace
        text = " ".join(text.split())
        
        # Normalize line breaks
        text = text.replace("\n\n", "\n").replace("\n \n", "\n")
        
        # Remove common PDF artifacts
        text = text.replace("  ", " ")
        
        return text.strip()
    
    def load_text_file(self, file_path: str) -> Optional[str]:
        """
        Load a plain text file
        
        Args:
            file_path: Path to the text file
            
        Returns:
            File content as string, or None if loading fails
        """
        try:
            if not os.path.exists(file_path):
                raise FileNotFoundError(f"Text file not found: {file_path}")
            
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
            
            return self._clean_text(content)
            
        except Exception as e:
            print(f"Error loading text file {file_path}: {str(e)}")
            return None 