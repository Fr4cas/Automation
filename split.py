import os
import re
import pymupdf
import pytesseract

folder = os.path.join(os.path.dirname(__file__), "pdfs")

pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Tesseract-OCR\tesseract.exe"
)

def extract_page_number(text):
    # Match page numbering such as 第1頁，共2頁.
    # Allow common OCR misreadings of 頁:
    # 員, 負, and 貝.
    page_char = r"[頁員負貝]"

    match = re.search(rf"第\s*(\d+)\s*{page_char}\s*[，,、]\s*共\s*(\d+)\s*{page_char}",
     text)
    
    if match:
        current_page = int(match.group(1))
        total_pages = int(match.group(2))
        
        # A page number must be positive and cannot
        # exceed the document's total page count.
        if 1 <= current_page <= total_pages:
            return current_page, total_pages

    return None

def extract_document_number(text):
    # Look for a document number near the top of the page.
    # This pattern matches numbers like 2300A-260101-001.
    match = re.search(
        r"\b[A-Z0-9]+-\d{6}-\d+\b",
        text[:1000],
        re.IGNORECASE
    )

    return match.group(0) if match else None

for filename in os.listdir(folder):
    if filename.lower().endswith(".pdf"):
        file_path = os.path.join(folder, filename)

        doc = pymupdf.open(file_path)

        #print(f"\n{'=' * 60}")
        #print(f"File: {filename}")
        #print(f"Number of pages: {len(doc)}")

        page_records = []

        for page_number, page in enumerate(doc, start=1):
            # Convert the PDF page into an image
            pix = page.get_pixmap(dpi=300)
            image = pix.pil_image()

            # Recognize Traditional Chinese and English
            text = pytesseract.image_to_string(
                image,
                lang="chi_tra+eng"
            )

            #print(f"\n--- Page {page_number} ---")

            page_info = extract_page_number(text)
            document_number = extract_document_number(text)

            record = {
                "page_number": page_number,
                "text": text,
                "page_info": page_info,
                "document_number": document_number
            }

            page_records.append(record)
            
        doc.close()

        # Print a compact summary for boundary analysis.
        for record in page_records:
            page_info = record["page_info"]

            if page_info:
                page_label = f"{page_info[0]} of {page_info[1]}"
            else:
                page_label = "Not found"

            print(
                f"PDF page {record['page_number']}: "
                f"Document page {page_label}; "
                f"Document number: "
                f"{record['document_number'] or 'Not found'}"
            )


     
