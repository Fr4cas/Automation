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

for filename in os.listdir(folder):
    if filename.lower().endswith(".pdf"):
        file_path = os.path.join(folder, filename)

        doc = pymupdf.open(file_path)

        #print(f"\n{'=' * 60}")
        #print(f"File: {filename}")
        #print(f"Number of pages: {len(doc)}")

        for page_number, page in enumerate(doc, start=1):
            # Convert the PDF page into an image
            pix = page.get_pixmap(dpi=300)
            image = pix.pil_image()

            # Recognize Traditional Chinese and English
            text = pytesseract.image_to_string(
                image,
                lang="chi_tra+eng"
            )

            print(f"\n--- Page {page_number} ---")

            page_info = extract_page_number(text)

            if page_info:
                current_page, total_pages = page_info
                print(f"Document page: {current_page} of {total_pages}")
            else:
                print("Document page: Not found")
                
            print(text if text.strip() else "No text found")

        doc.close()
