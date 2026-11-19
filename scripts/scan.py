import os
import sys
import time
import numpy as np
import pymupdf
from paddleocr import PaddleOCR
from opencc import OpenCC

# Input & Output folders
project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
folder = os.path.join(project_dir, "output", "stamped")
output_folder = os.path.join(project_dir, "output", "extracted_text")

os.makedirs(output_folder, exist_ok=True)

# PaddleOCR init
ocr = PaddleOCR(
    use_doc_orientation_classify=False,
    use_doc_unwarping=False,
    use_textline_orientation=False,
    lang="ch",
    enable_mkldnn=False
)

converter = OpenCC("s2t")

def recognize_text(image):
    results = ocr.predict(np.array(image))

    texts = []
    boxes = []

    for result in results:
        texts.extend(result["rec_texts"])
        boxes.extend(result["dt_polys"])

    return texts, boxes

def improve_subject(page, texts, boxes):
    subject_index = next(
        (i for i, text in enumerate(texts) if "主旨" in text),
        None
    )

    if subject_index is None:
        return texts

    explanation_index = next(
        (
            i for i, text in enumerate(texts)
            if "說明" in text and i > subject_index
        ),
        None
    )

    if explanation_index is None:
        return texts

    top = max(0, int(np.min(boxes[subject_index][:, 1])) - 20)
    bottom = int(np.min(boxes[explanation_index][:, 1])) - 10

    clip = pymupdf.Rect(0, top, page.rect.width, bottom)
    crop_pix = page.get_pixmap(clip=clip, dpi=300)
    crop_image = crop_pix.pil_image()

    start = time.perf_counter()
    crop_texts, _ = recognize_text(crop_image)
    crop_time = time.perf_counter() - start

    print("Improved subject OCR:")
    print("\n".join(crop_texts))
    print(f"Subject OCR={crop_time:.2f}s")
    print(f"Subject crop: top={top}, bottom={bottom}")

    return texts[:subject_index] + crop_texts + texts[explanation_index:]

def extract_pdf_text(file_path):
    all_pages = []

    with pymupdf.open(file_path) as doc:
        for page_number, page in enumerate(doc, start=1):
            pix = page.get_pixmap()
            image = pix.pil_image()

            start = time.perf_counter()
            texts, boxes = recognize_text(image)

            if page_number == 1:
                texts = improve_subject(page, texts, boxes)

            text = converter.convert("\n".join(texts))
            ocr_time = time.perf_counter() - start

            print(
                f"Page {page_number}: "
                f"OCR={ocr_time:.2f}s"
            )

            all_pages.append(
                f"--- Page {page_number} ---\n{text}"
            )

    return "\n\n".join(all_pages)

def process_pdf_folder(input_folder, output_folder):
    os.makedirs(output_folder, exist_ok=True)
    pdf_files = sorted(
        filename 
        for filename in os.listdir(input_folder)
        if filename.lower().endswith(".pdf") 
    )

    if not pdf_files:
        print(f"no PDF files found in: {input_folder}")
        return

    for filename in pdf_files:
        pdf_path = os.path.join(input_folder, filename)

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
    input_folder = sys.argv[1] if len(sys.argv) > 1 else folder
    output_path = sys.argv[2] if len(sys.argv) > 2 else output_folder

    process_pdf_folder(input_folder, output_path)
