import os
import pymupdf
import pytesseract

folder = os.path.join(os.path.dirname(__file__), "pdfs")

pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Tesseract-OCR\tesseract.exe"
)

for filename in os.listdir(folder):
    if filename.lower().endswith(".pdf"):
        file_path = os.path.join(folder, filename)

        print(filename)

        doc = pymupdf.open(file_path)
        page = doc[0]

        # Convert the PDF page into an image
        pix = page.get_pixmap(dpi=300)
        image = pix.pil_image()

        # Recognize Traditional Chinese and English
        text = pytesseract.image_to_string(
            image,
            lang="chi_tra+eng"
        )

        doc.close()

        print("First page text:")
        print(text if text and text.strip() else "No text found")
