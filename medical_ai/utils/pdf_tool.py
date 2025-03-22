import os
import pdfplumber
import re
from collections import Counter

class PDFSearchTool:
    def __init__(self):
        # Common medical and technical terms to look for in context
        self.medical_keywords = [
            'medical', 'clinical', 'patient', 'health', 'hospital', 'device', 'equipment',
            'therapy', 'diagnostic', 'treatment', 'imaging', 'monitor', 'ventilator',
            'implant', 'surgical', 'regulation', 'safety', 'sterilization', 'FDA',
            'CE', 'ISO', 'specification', 'compliance', 'protocol', 'technology'
        ]
    
    def search(self, query, pdf_paths):
        """
        Extract and return relevant text from PDFs based on the query using
        advanced contextual matching and relevance scoring.
        """
        # Process query to extract key terms and medical concepts
        query_terms = self._extract_key_terms(query)
        
        all_results = []
        
        for pdf_path in pdf_paths:
            try:
                pdf_filename = os.path.basename(pdf_path)
                with pdfplumber.open(pdf_path) as pdf:
                    # Extract metadata if available
                    metadata = pdf.metadata if hasattr(pdf, 'metadata') else {}
                    doc_info = f"Document: {pdf_filename}"
                    if metadata:
                        if 'Title' in metadata and metadata['Title']:
                            doc_info += f"\nTitle: {metadata['Title']}"
                        if 'Author' in metadata and metadata['Author']:
                            doc_info += f"\nAuthor: {metadata['Author']}"
                    
                    # Process each page and score relevance
                    page_results = []
                    
                    for page_num, page in enumerate(pdf.pages, start=1):
                        try:
                            text = page.extract_text()
                            if not text:
                                continue
                                
                            # Score the page for relevance to query
                            relevance_score = self._calculate_relevance(text, query_terms)
                            
                            # If relevant enough, add to results
                            if relevance_score > 0:
                                # Extract the most relevant section (paragraphs containing key terms)
                                relevant_sections = self._extract_relevant_sections(text, query_terms)
                                
                                if relevant_sections:
                                    page_results.append({
                                        'page_num': page_num,
                                        'relevance': relevance_score,
                                        'content': relevant_sections
                                    })
                        except Exception as e:
                            continue
                    
                    # Sort results by relevance score
                    page_results.sort(key=lambda x: x['relevance'], reverse=True)
                    
                    # Take top 3 most relevant results from this PDF
                    top_results = page_results[:3]
                    
                    if top_results:
                        # Format results for this PDF
                        pdf_result = f"{doc_info}\n\n"
                        for result in top_results:
                            pdf_result += f"Page {result['page_num']} (Relevance: {result['relevance']:.2f}):\n"
                            pdf_result += f"{result['content']}\n\n"
                        
                        all_results.append(pdf_result)
            
            except Exception as e:
                all_results.append(f"Error processing {pdf_filename}: {str(e)}")
        
        if not all_results:
            return "No relevant information found in the provided PDFs."
        
        # Combine all results with clear separation
        final_result = "\n\n" + "="*50 + "\n\n".join(all_results)
        return final_result
    
    def _extract_key_terms(self, query):
        """Extract key terms from the query for better matching."""
        # Convert to lowercase and split
        query = query.lower()
        
        # Remove common stop words
        stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'is', 'are', 'of', 'for', 'in', 'to', 'with', 'on', 'by'}
        terms = [word for word in re.findall(r'\b\w+\b', query) if word not in stop_words]
        
        # Add medical terms that may appear in the query
        medical_terms = [term for term in self.medical_keywords if term.lower() in query]
        
        # Add phrases (2-3 words) that might be important
        words = query.split()
        phrases = []
        for i in range(len(words) - 1):
            phrases.append(f"{words[i]} {words[i+1]}")
        
        for i in range(len(words) - 2):
            phrases.append(f"{words[i]} {words[i+1]} {words[i+2]}")
        
        # Combine all terms
        all_terms = terms + medical_terms + phrases
        
        # Remove duplicates while preserving order
        seen = set()
        return [term for term in all_terms if not (term in seen or seen.add(term))]
    
    def _calculate_relevance(self, text, query_terms):
        """Calculate relevance score based on term frequency and position."""
        text_lower = text.lower()
        score = 0
        
        # Check for exact query matches (highest weight)
        for term in query_terms:
            term_count = text_lower.count(term.lower())
            if term_count > 0:
                # Score based on frequency
                score += term_count * 2
                
                # Extra points for terms appearing in headings (all caps or followed by colon)
                heading_pattern = r'([A-Z][A-Z\s]+:|\b[A-Z][A-Z\s]+\b)'
                headings = re.findall(heading_pattern, text)
                for heading in headings:
                    if term.lower() in heading.lower():
                        score += 5
        
        # Check for medical keyword matches
        for keyword in self.medical_keywords:
            if keyword.lower() in text_lower:
                score += 1
        
        # Normalize score based on text length
        words_count = len(text_lower.split())
        if words_count > 0:
            return score / (words_count / 200)  # Normalize for ~200 words of content
        return 0
    
    def _extract_relevant_sections(self, text, query_terms):
        """Extract the most relevant paragraphs containing query terms."""
        # Split text into paragraphs
        paragraphs = re.split(r'\n\s*\n', text)
        
        # Score each paragraph
        scored_paragraphs = []
        for para in paragraphs:
            para_text = para.strip()
            if not para_text:
                continue
                
            relevance = 0
            for term in query_terms:
                if term.lower() in para_text.lower():
                    relevance += 1
            
            if relevance > 0:
                scored_paragraphs.append((para_text, relevance))
        
        # Sort by relevance
        scored_paragraphs.sort(key=lambda x: x[1], reverse=True)
        
        # Return top paragraphs (up to 3)
        return "\n\n".join([p[0] for p in scored_paragraphs[:3]])