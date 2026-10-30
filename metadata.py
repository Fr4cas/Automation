import os
import re

folder = os.path.join(os.path.dirname(__file__), "extracted_text")

output_file = os.path.join(
    os.path.dirname(__file__),
    "metadata_results.txt"
)

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
        r"發文日期[:：]?\s*中華民[國园]\s*(\d{2,3})年\s*(\d{1,2})月\s*(\d{1,2})日",
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

def extract_subject(text):
    clean_text = re.sub(r"\s", "", text)

    end_keywords = [
        "請查照", "敬請查照", "惠請查照",
        "請備查", "敬請備查", "惠請備查",
        "鑒核", "鑑定", "鑑核",
        "請鑒核", "請參辦", "請參核",
        "請鑑定", "請檢送", "審定。",
        "請依說明二辦理", "建請同意核定"
    ]

    end_pattern = "|".join(end_keywords)

    match = re.search(
        rf"主旨[:：](.*?({end_pattern}))",
        clean_text
    )

    if match:
        subject = match.group(1).strip()
        subject = subject.replace(",", "，")
        return subject

    return ""

def extract_explanation(text):
    explanation_start = re.search(r"說明[:：]", text)

    if not explanation_start: 
        return ""

    explanation_text = text[explanation_start.end():]

    explanation_text = re.split(
        r"^\s*正本[:：]",
        explanation_text,
        maxsplit=1,
        flags=re.MULTILINE
    )[0]

    explanation_text = re.split(
        r"^\s*正本[:：]",
        explanation_text,
        maxsplit=1,
        flags=re.MULTILINE
    )[0]

    noise_patterns = [
        r"^騎縫入", r"^騎縫", r"^訂",
        r"^電于", r"^電文骑", r"^騎后",
        r"^文", r"^卷文", r"^公換章", r"^換章",
        r"^--- Page [\d123456789] ---",
        r"^第[\d一二三四五六七八九十]+[頁員負貝页]",
        r"^共[\d一二三四五六七八九十]+[頁員負貝页]",
        r"^\d+\s*$", r"^\d+/\d+[頁員負貝页]"
    ]

    cleaned_lines = []

    for line in explanation_text.splitlines():
        trimmed = line.strip()

        if not any(re.search(pattern, trimmed) for pattern in noise_patterns):
            cleaned_lines.append(line)

    return "\n".join(cleaned_lines).strip()


def extract_attachment(text):
    match = re.search(
        r"附件[:：]\s*([\s\S]*?)(?=\n\s*(?:主旨|說明|正本|副本|$))",
        text
    )

    if match:
        return match.group(1).strip()

    return ""

if __name__ == "__main__":
    with open(output_file, "w", encoding="utf-8") as file:
        file.write("Metadata Extraction Results\n")

    txt_files = sorted(
        filename for filename in os.listdir(folder)
        if filename.lower().endswith(".txt")
    )

    if not txt_files:
        print(f"No text files found in {folder}")
    
    for filename in txt_files:
        file_path = os.path.join(folder, filename)

        print(f"Scanned: {filename}")

        text = read_text_file(file_path)
        receipt_number = extract_receipt_number(text)
        receipt_date = extract_receipt_date(text)
        issue_date = extract_issue_date(text)
        reference_number = extract_reference_number(text)
        issuing_authority = extract_issuing_authority(text)
        document_type = extract_document_type(text)
        subject = extract_subject(text)
        explanation = extract_explanation(text)
        attachment = extract_attachment(text)

        with open(output_file, "a", encoding="utf-8") as file:
            file.write(f"\n{'=' * 50}\n")
            file.write(f"File: {filename}\n")
            file.write(f"{'=' * 50}\n")

            file.write(f"收文單號: {receipt_number}\n")
            file.write(f"收文日期: {receipt_date}\n")
            file.write(f"發文日期: {issue_date}\n")
            file.write(f"發文字號: {reference_number}\n")
            file.write(f"發文機關: {issuing_authority}\n")
            file.write(f"文別: {document_type}\n")
            file.write(f"附件: {attachment}\n")
            file.write(f"主旨: {subject}\n")
            file.write(f"說明: {explanation}\n")