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

def extract_document_number(text):
    # Look for a document number near the top of the page.
    # This pattern matches numbers like 2300A-260101-001.

    # Noralize common OCR hyphen subs
    normalized = text
    for char in ("~", "～", "—", "－", "﹣", "="):
        normalized = normalized.replace(char, "-")

    # Remove spaces between digits inserted by OCR.
    normalized = re.sub(
        r"(?<=\d)\s+(?=\d)",
        "",
        normalized
    )

    match = re.search(
        r"\b([A-Z0-9]{4,})\s*-\s*(\d{6})\s*-\s*(\d{3})\b",
        normalized,
        re.IGNORECASE
    )

    if match:
        return (
            f"{match.group(1).upper()}-"
            f"{match.group(2)}-{match.group(3)}"
        )

    return None

def group_documents(page_records):
    candidates = []
    page_count = len(page_records)

    # Use every part of X of N to estimate
    for index, record in enumerate(page_records):
        page_info = record["page_info"]

        if not page_info:
            continue
        
        current_page, total_pages = page_info
        start = index - (current_page - 1)
        end = start + total_pages

        if start < 0 or end > page_count:
            continue

        # Check if other pages have conflicting page info
        valid = True
        marker_count = 0

        for position in range(start, end):
            other_info = page_records[position]["page_info"]

            if other_info:
                expected_position = position - start + 1

                if other_info != (expected_position, total_pages):
                    valid = False
                    break
                
                marker_count += 1
            
            # If a document number is detected in the sequence
            # Suggest a new file has started, so this sequence is invalid.
            if (
                position > start
                and page_records[position]["document_number"]
            ):
                valid = False
                break

        if not valid:
            continue

        # Keep proposed range only once
        candidate = {
            "start": start,
            "end": end,
            "marker_count": marker_count,
            "has_start_marker": page_records[start]["page_info"]
                == (1, total_pages),
            "has_document_number": bool(
                page_records[start]["document_number"]
            ),
        }

        if not any(
            existing["start"] == start
            and existing["end"] == end
            for existing in candidates
        ):
            candidates.append(candidate)

    # Prefer ranges with more detected markers
    candidates.sort(    
        key=lambda item: (
            item["marker_count"],
            item["has_start_marker"],
            item["has_document_number"]
        ),
        reverse=True
    )

    groups = []
    assigned_pages = set()

    for candidate in candidates:
        start = candidate["start"]
        end = candidate["end"]
        page_indexes = set(range(start, end))

        # Do not allow overlapping groups (claiming the same page)
        if assigned_pages.intersection(page_indexes):
            continue

        assigned_pages.update(page_indexes)

        groups.append({
            "pages": page_records[start:end],
            "status": "sequence match",
        })
    
    # Keep remaining pages for manual review
    for index, record in enumerate(page_records):
        if index not in assigned_pages:
            groups.append({
                "pages": [record],
                "status": "unresolved",
            })

    # Return groups in PDF page order
    groups.sort(key=lambda group: group["pages"][0]["page_number"])

    return groups

for filename in os.listdir(folder):
    if filename.lower().endswith(".pdf"):
        file_path = os.path.join(folder, filename)

        doc = pymupdf.open(file_path)

        #print(f"\n{'=' * 60}")
        #print(f"File: {filename}")
        #print(f"Number of pages: {len(doc)}")

        page_records = []

        for page_number, page in enumerate(doc, start=1):
            # Convert the PDF page into an image
            pix = page.get_pixmap(dpi=300)
            image = pix.pil_image()

            # Recognize Traditional Chinese and English
            text = pytesseract.image_to_string(
                image,
                lang="chi_tra+eng"
            )

            print(f"\n--- Scanning page: {page_number} ---")

            page_info = extract_page_number(text)

            # Scan the top of the page for document number
            width, height = image.size

            top = image.crop((0, 0, width, int(height * 0.10)))

            #enlarge the top image to improve OCR accuracy
            top = top.resize((top.width * 2, top.height * 2))

            top_text = pytesseract.image_to_string(
                top,
                lang="chi_tra+eng",
                config="--psm 6"
            )

            document_number = extract_document_number(top_text)

            # Log debug information if document number is not found.
            #if document_number is None:
                #print(f"\nDEBUG: {filename}, PDF page {page_number}")
                #print("Top-region OCR:")
                #print(repr(top_text))

            record = {
                "page_number": page_number,
                "text": text,
                "page_info": page_info,
                "document_number": document_number
            }

            page_records.append(record)
            
        doc.close()

        # Print a compact summary for boundary analysis.
        for record in page_records:
            page_info = record["page_info"]

            if page_info:
                page_label = f"{page_info[0]} of {page_info[1]}"
            else:
                page_label = "Not found"

            print(
                f"PDF page {record['page_number']}: "
                f"Document page {page_label}; "
                f"Document number: "
                f"{record['document_number'] or 'Not found'}"
            )

        documents = group_documents(page_records)

        print(f"\nProposed document groups for {filename}:")

        for index, group in enumerate(documents, start=1):
            pages = group["pages"]
            start_page = pages[0]["page_number"]
            end_page = pages[-1]["page_number"]

            page_range = (
                str(start_page)
                if start_page == end_page
                else f"{start_page}-{end_page}"
            )

            print(
                f"Document {index}: PDF pages {page_range} "
                f"[{group['status']}]"
            )