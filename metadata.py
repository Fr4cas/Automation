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

        print(f"Reading: {filename}")
        print("Receipt number:", receipt_number)
        print("Receipt date: ", receipt_date)
        print("Issue date:", issue_date)
        print(text)