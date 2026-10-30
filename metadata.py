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


def extract_receipt_date(text):
    matches = re.findall(r"26(\d{4})-\d{2}", text)

    if not matches:
        return ""

    dates = []

    for digits in matches:
        month = digits[:2]
        day = digits[2:4]
        dates.append(f"2026/{month}/{day}")

    return ", ".join(dates)

def extract_issue_date(text):
    match = re.search(
        r"發文日期[:：]?\s*中華民國\s*(\d{2,3})年\s*(\d{1,2})月\s*(\d{1,2})日",
        text
    )

    if match:
        year = int(match.group(1)) + 1911
        month = int(match.group(2))
        day = int(match.group(3))

        return f"{year:04d}/{month:02d}/{day:02d}"

    return ""

def extract_reference_number(text):
    match = re.search(
        r"發文字號[:：]?\s*([^\s\n]+)",
        text
    )

    if match:
        return match.group(1)

    return ""

def extract_issuing_authority(text):
    match = re.search(
        r"([^\s\n\r]{2,}?)(?=\s*(及)?書?函)",
        text
    )

    if match:
        return match.group(1)

    return ""

def extract_document_type(text):
    match = re.search(
        r"說明[:：]",
        text
    )

    if not match:
        return "正本"

    after_explanation = text[match.start():]

    match = re.search(
        r"副本[:：]?\s*([^\n\r]+)",
        after_explanation
    )

    if match:
        copy_content = match.group(1)
    
        if re.search(r"宏昇營造|新雄營造", copy_content):
            return "副本"
    
    return "正本"

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
        receipt_date = extract_receipt_date(text)
        issue_date = extract_issue_date(text)
        reference_number = extract_reference_number(text)
        issuing_authority = extract_issuing_authority(text)
        document_type = extract_document_type(text)

        print(f"Reading: {filename}")
        print("Receipt number:", receipt_number)
        print("Receipt date:", receipt_date)
        print("Issue date:", issue_date)
        print("Reference number:", reference_number)
        print("Issuing authority:", issuing_authority)
        print("Document type:", document_type)
        print(text)