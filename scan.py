import os
import time
import numpy as np
import pymupdf
from paddleocr import PaddleOCR

# Input & Output folders
folder = os.path.join(os.path.dirname(__file__), "split_pdfs")
output_folder = os.path.join(os.path.dirname(__file__), "extracted_text")
os.makedirs(output_folder, exist_ok=True)

# PaddleOCR init
ocr = PaddleOCR(
    use_doc_orientation_classify=False,
    use_doc_unwarping=False,
    use_textline_orientation=False,
    lang="ch",
    enable_mkldnn=False
)

def recognize_text(image):
    results = ocr.predict(np.array(image))

    texts = []

    for result in results:
        texts.extend(result["rec_texts"])

    return "\n".join(texts)

def extract_pdf_text(file_path):
    all_pages = []

    with pymupdf.open(file_path) as doc:
        for page_number, page in enumerate(doc, start=1):
            pix = page.get_pixmap()
            image = pix.pil_image()

            start = time.perf_counter()
            text = recognize_text(image)
            ocr_time = time.perf_counter() - start

            print(
                f"Page {page_number}: "
                f"OCR={ocr_time:.2f}s"
            )

            all_pages.append(
                f"--- Page {page_number} ---\n{text}"
            )

    return "\n\n".join(all_pages)

def process_pdf_folder():
    pdf_files = sorted(
        filename 
        for filename in os.listdir(folder)
        if filename.lower().endswith(".pdf") 
    )

    if not pdf_files:
        print(f"no PDF files found in: {folder}")
        return

    for filename in pdf_files:
        pdf_path = os.path.join(folder, filename)

        try:
            print(f"Processing: {filename}")

            text = extract_pdf_text(pdf_path)

            txt_filename = os.path.splitext(filename)[0] + ".txt"
            txt_path = os.path.join(output_folder, txt_filename)

            with open(txt_path, "w", encoding="utf-8") as file:
                file.write(text)

            print(f"Saved OCR text: {txt_filename}")

        except Exception as error:
            print(f"Failed to process {filename}: {error}")


if __name__ == "__main__":
    process_pdf_folder()
