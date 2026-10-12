import os
from pypdf import PdfReader
import pymupdf
import pytesseract

folder = os.path.join(os.path.dirname(__file__), "pdfs")

pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Tesseract-OCR\tesseract.exe"
)

for filename in os.listdir(folder):
    if filename.lower().endswith(".pdf"):
        file_path = os.path.join(folder, filename)

        reader = PdfReader(file_path)

        print(filename)
        print(f"  Number of pages: {len(reader.pages)}")

        first_page = reader.pages[0]
        text = first_page.extract_text()

        if not text or not text.strip():
            print("  No text found. Attempting OCR...")

            doc = pymupdf.open(file_path)
            page = doc[0]

            pix = page.get_pixmap(dpi=300)
            image = pix.pil_image()

            text = pytesseract.image_to_string(
                image,
                lang="chi_tra+eng"
            )

            doc.close()

        print("First page text:")
        print(text[:1000] if text else "No text found")
