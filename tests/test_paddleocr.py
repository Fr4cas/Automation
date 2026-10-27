from paddleocr import PaddleOCR

ocr = PaddleOCR(
    use_doc_orientation_classify=False,
    use_doc_unwarping=False,
    use_textline_orientation=False,
    lang="ch",
    enable_mkldnn=False,
)

results = ocr.predict("paddle_test_page.png")

with open("paddle_ocr_result.txt", "w", encoding="utf-8") as file:
    for result in results:
        for text, score in zip(result["rec_texts"], result["rec_scores"]):
            file.write(f"{score:.3f}\t{text}\n")

print("OCR text saved to paddle_ocr_result.txt")
