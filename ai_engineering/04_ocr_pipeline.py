"""
Topic: OCR Pipeline
Exercise: Scanned Document Extraction and Cleanup

Problem Description:
When extracting information from physical scans (like receipts or invoices), text outputs 
frequently contain OCR artifacts (spelling mistakes, wrong characters like '1' for 'I', 
messy line breaks). A robust pipeline corrects formatting, cleans up syntax, 
and extracts structured fields.

Implement an OCR processing pipeline containing:
1. `ocr_spelling_cleaner(text: str) -> str`:
   Corrects common OCR character confusions (e.g. replacing '1nvo1ce' with 'invoice', 
   fixing common key terms).
2. `extract_document_fields(cleaned_text: str) -> dict`:
   Extracts `invoice_id` (pattern: INV-xxxx), `date` (pattern: DD/MM/YYYY or YYYY-MM-DD), 
   and `total_amount` (numeric currency value) from text using regular expressions.
3. `llm_cleanup_simulation(extracted_data: dict) -> dict`:
   Post-processes fields (formatting currency float numbers, standardizing date formats to YYYY-MM-DD).
"""

import re
from typing import Dict, Any

def ocr_spelling_cleaner(text: str) -> str:
    """
    Cleans common OCR character mapping errors and formatting glitches.
    """
    # Replace common character replacement glitches
    replacements = {
        r"\b1nvo1ce\b": "invoice",
        r"\bt0ta1\b": "total",
        r"\bd4te\b": "date",
        r"\|": "",  # strip column boundaries from table scans
    }
    
    cleaned = text.lower()
    for pattern, replacement in replacements.items():
        cleaned = re.sub(pattern, replacement, cleaned)
        
    # Compress multiple spaces
    cleaned = re.sub(r"\s+", " ", cleaned).strip()
    return cleaned

def extract_document_fields(cleaned_text: str) -> Dict[str, Any]:
    """
    Extracts structured fields from raw OCR output using pattern matching.
    """
    fields = {
        "invoice_id": None,
        "date": None,
        "total_amount": None
    }
    
    # 1. Match invoice_id (INV- followed by digits)
    inv_match = re.search(r"inv-\d+", cleaned_text, re.IGNORECASE)
    if inv_match:
        fields["invoice_id"] = inv_match.group(0).upper()
        
    # 2. Match date (DD/MM/YYYY or YYYY-MM-DD)
    date_match = re.search(r"(\d{2}/\d{2}/\d{4}|\d{4}-\d{2}-\d{2})", cleaned_text)
    if date_match:
        fields["date"] = date_match.group(0)
        
    # 3. Match total amount (total: $XX.XX or total XX.XX)
    total_match = re.search(r"total\D*?(\d+\.\d{2})", cleaned_text)
    if total_match:
        fields["total_amount"] = total_match.group(1)
        
    return fields

def llm_cleanup_simulation(extracted_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Simulates LLM correction block by standardizing fields.
    """
    cleaned_data = extracted_data.copy()
    
    # Standardize total_amount to float
    if cleaned_data["total_amount"]:
        try:
            cleaned_data["total_amount"] = float(cleaned_data["total_amount"])
        except ValueError:
            cleaned_data["total_amount"] = 0.0
            
    # Standardize date format to YYYY-MM-DD
    if cleaned_data["date"] and "/" in cleaned_data["date"]:
        parts = cleaned_data["date"].split("/")
        # Assumes DD/MM/YYYY -> YYYY-MM-DD
        if len(parts) == 3:
            cleaned_data["date"] = f"{parts[2]}-{parts[1]}-{parts[0]}"
            
    return cleaned_data

# --- Verification Tests ---
if __name__ == "__main__":
    print("Running tests for OCR Pipeline...")
    
    # Messy scanned invoice document text output from OCR scanner
    scanned_text = (
        "|  1NVO1CE: iNv-88349  |\n"
        "|  D4te: 18/12/2026   |\n"
        "|  Company: Acme Corp  |\n"
        "|  T0ta1 Due: $450.99  |"
    )
    
    # 1. OCR cleanup
    cleaned = ocr_spelling_cleaner(scanned_text)
    print(f"Cleaned Text: {cleaned}")
    assert "invoice:" in cleaned
    assert "total due: $450.99" in cleaned
    
    # 2. Extract fields
    raw_fields = extract_document_fields(cleaned)
    print(f"Extracted: {raw_fields}")
    assert raw_fields["invoice_id"] == "INV-88349"
    assert raw_fields["date"] == "18/12/2026"
    assert raw_fields["total_amount"] == "450.99"
    
    # 3. Post-process cleanup
    final_fields = llm_cleanup_simulation(raw_fields)
    print(f"Final Data: {final_fields}")
    assert final_fields["invoice_id"] == "INV-88349"
    assert final_fields["date"] == "2026-12-18"  # parsed and reformatted
    assert isinstance(final_fields["total_amount"], float)
    assert final_fields["total_amount"] == 450.99
    
    print("All tests passed successfully!")
