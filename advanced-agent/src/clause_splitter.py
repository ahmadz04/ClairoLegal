import re
from typing import List


class ClauseSplitter:
    """Split contract text into individual clauses using regex patterns"""
    
    def __init__(self):
        # Common clause numbering patterns
        self.clause_patterns = [
            r'\n(?=\d+\.)',  # Numbered clauses: "1.", "2.", etc.
            r'\n(?=\d+\))',  # Numbered clauses with parentheses: "1)", "2)", etc.
            r'\n(?=[A-Z]\.)',  # Lettered clauses: "A.", "B.", etc.
            r'\n(?=[IVX]+\.)',  # Roman numeral clauses: "I.", "II.", "III.", etc.
            r'\n(?=Section \d+)',  # Section clauses: "Section 1", "Section 2", etc.
            r'\n(?=Clause \d+)',  # Explicit clause markers: "Clause 1", "Clause 2", etc.
            r'\n(?=Article \d+)',  # Article clauses: "Article 1", "Article 2", etc.
        ]
        
        # Alternative sentence-based splitting for contracts without clear numbering
        self.sentence_pattern = r'(?<=[.!?])\s+(?=[A-Z])'
    
    def split_clauses(self, contract_text: str) -> List[str]:
        """
        Split contract text into individual clauses
        
        Args:
            contract_text: Raw contract text
            
        Returns:
            List of individual clauses
        """
        if not contract_text.strip():
            return []
        
        # Try numbered clause patterns first
        for pattern in self.clause_patterns:
            clauses = re.split(pattern, contract_text)
            if len(clauses) > 1:
                # Filter out empty clauses and clean up
                cleaned_clauses = self._clean_clauses(clauses)
                if len(cleaned_clauses) > 1:
                    return cleaned_clauses
        
        # Fallback to sentence-based splitting
        sentences = re.split(self.sentence_pattern, contract_text)
        cleaned_sentences = self._clean_clauses(sentences)
        
        # Group sentences into logical clauses (3-5 sentences per clause)
        return self._group_sentences_into_clauses(cleaned_sentences)
    
    def _clean_clauses(self, clauses: List[str]) -> List[str]:
        """
        Clean and filter clauses
        
        Args:
            clauses: Raw list of clauses
            
        Returns:
            Cleaned list of clauses
        """
        cleaned = []
        for clause in clauses:
            # Remove leading/trailing whitespace
            clause = clause.strip()
            
            # Skip empty or very short clauses
            if len(clause) < 10:
                continue
            
            # Skip common headers/footers
            if self._is_header_or_footer(clause):
                continue
            
            cleaned.append(clause)
        
        return cleaned
    
    def _is_header_or_footer(self, text: str) -> bool:
        """
        Check if text appears to be a header or footer
        
        Args:
            text: Text to check
            
        Returns:
            True if text appears to be header/footer
        """
        text_lower = text.lower()
        
        # Common header/footer patterns
        header_footer_patterns = [
            r'^page \d+$',
            r'^\d+$',
            r'^confidential$',
            r'^draft$',
            r'^final$',
            r'^version \d+',
            r'^revised',
            r'^effective date:',
            r'^execution date:',
        ]
        
        for pattern in header_footer_patterns:
            if re.match(pattern, text_lower):
                return True
        
        return False
    
    def _group_sentences_into_clauses(self, sentences: List[str]) -> List[str]:
        """
        Group sentences into logical clauses when no clear numbering exists
        
        Args:
            sentences: List of individual sentences
            
        Returns:
            List of grouped clauses
        """
        if not sentences:
            return []
        
        clauses = []
        current_clause = []
        
        for sentence in sentences:
            current_clause.append(sentence)
            
            # Create a clause every 3-5 sentences, or when we hit certain keywords
            if (len(current_clause) >= 4 or 
                self._contains_clause_break_keywords(sentence)):
                
                clause_text = " ".join(current_clause)
                if len(clause_text.strip()) > 20:  # Minimum clause length
                    clauses.append(clause_text.strip())
                current_clause = []
        
        # Add any remaining sentences as the last clause
        if current_clause:
            clause_text = " ".join(current_clause)
            if len(clause_text.strip()) > 20:
                clauses.append(clause_text.strip())
        
        return clauses
    
    def _contains_clause_break_keywords(self, sentence: str) -> bool:
        """
        Check if sentence contains keywords that suggest a clause break
        
        Args:
            sentence: Sentence to check
            
        Returns:
            True if sentence contains clause break keywords
        """
        sentence_lower = sentence.lower()
        
        break_keywords = [
            'provided that',
            'provided, however,',
            'further provided',
            'in addition',
            'moreover',
            'furthermore',
            'additionally',
            'notwithstanding',
            'subject to',
            'except as',
            'unless otherwise',
        ]
        
        return any(keyword in sentence_lower for keyword in break_keywords) 