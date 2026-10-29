import os
import re

folder = os.path.join(os.path.dirname(__file__), "extracted_text")

def read_text_file(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()

def extract_receipt_number(text):
    match = re.search(
        r"26\d{4}[-.]?\d{3}",
        text
    )

    if match:
        return match.group(0)

    return None


if __name__ == "__main__":
    txt_files = sorted(
        filename for filename in os.listdir(folder)
        if filename.lower().endswith(".txt")
    )

    if not txt_files:
        print(f"No text files found in {folder}")
    else:
        filename = txt_files[0]
        file_path = os.path.join(folder, filename)

        text = read_text_file(file_path)
        receipt_number = extract_receipt_number(text)

        print(f"Reading: {filename}")
        print("Receipt number:", receipt_number)
        print(text)