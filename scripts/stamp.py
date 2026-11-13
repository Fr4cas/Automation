import pymupdf

from pathlib import Path
from datetime import date
from PIL import Image
from scripts.stamp_font import generate_stamp

OUTPUT_FOLDER = (
    Path(__file__).resolve().parent.parent
    / "output"
    / "stamped"
)

def get_pdf_files(folder):
    folder = Path(folder)

    pdf_files = sorted(
        file for file in folder.iterdir()
        if file.is_file() and file.suffix.lower() == ".pdf"
    )

    return pdf_files

def apply_document_number(pdf_path, number, received_date):
    doc = pymupdf.open(pdf_path)
    page = doc[0]

    date_code = received_date.strftime("%y%m%d")
    document_number = f"2300A-{date_code}-{number:03d}"

    # Generate the custom document-number image
    stamp_image_path = pdf_path.with_name(
        f".{pdf_path.stem}_number.png"
    )

    generate_stamp(
        document_number,
        stamp_image_path,
        seed=number
    )

    # Set the stamp dimensions and position
    stamp_height = 18
    image = Image.open(stamp_image_path)

    stamp_width = stamp_height * image.width / image.height

    x = (page.rect.width - stamp_width) / 2
    y = 22

    stamp_rect = pymupdf.Rect(
        x,
        y,
        x + stamp_width,
        y + stamp_height
    )

    page.insert_image(
        stamp_rect,
        filename=str(stamp_image_path)
    )

    image.close()
    stamp_image_path.unlink()

    return doc


def apply_received_stamp(doc, received_date):
    page = doc[-1]

    # Load received stamp template
    stamp_path = (
        Path(__file__).resolve().parent.parent
        / "assets"
        / "received_stamp_template.png"
    )

    # Stamp dimensions
    stamp_width = 130
    stamp_height = 72

    x = (page.rect.width - stamp_width) / 2
    y = page.rect.height - stamp_height - 40

    stamp_rect = pymupdf.Rect(
        x, y,
        x + stamp_width,
        y + stamp_height
    )

    # Insert stamp artwork
    page.insert_image(
        stamp_rect,
        filename=str(stamp_path)
    )

    # Date area inside the stamp
    date_rect = pymupdf.Rect(
        x + stamp_width * 0.27,
        y + stamp_height * 0.38,
        x + stamp_width * 0.73,
        y + stamp_height * 0.68
    )

    # Format date
    date_text = received_date.strftime("%b %d %Y").upper()

    fontsize = 10

    text_width = pymupdf.get_text_length(
        date_text,
        fontname="hebo",
        fontsize=fontsize
    )

    # Center date horizontally
    date_x = date_rect.x0 + (
        date_rect.width - text_width
    ) / 2

    # Center date vertically
    date_y = date_rect.y0 + date_rect.height / 2 - 4

    page.insert_text(
        (date_x, date_y),
        date_text,
        fontsize=fontsize,
        fontname="hebo",
        color=(0.12, 0.39, 0.65)
    )

    return doc

def stamp_documents(folder, start_number, received_date):
    OUTPUT_FOLDER.mkdir(parents=True, exist_ok=True)
    pdf_files = get_pdf_files(folder)

    if not pdf_files:
        return 0

    for index, pdf_path in enumerate(pdf_files):
        number = start_number + index
        new_path = OUTPUT_FOLDER / f"{number:03d}.pdf"

        if new_path.exists() and new_path.resolve() != pdf_path.resolve():
            raise FileExistsError(
                f"Cannot save {pdf_path.name} as {new_path.name}: "
                "destination already exists."
            )

    processed = 0

    for index, pdf_path in enumerate(pdf_files):
        number = start_number + index
        new_path = OUTPUT_FOLDER / f"{number:03d}.pdf"

        doc = None
        temp_path = OUTPUT_FOLDER / f".{number:03d}_temp.pdf"

        try:
            doc = apply_document_number(pdf_path, number, received_date)
            doc = apply_received_stamp(doc, received_date)

            doc.save(temp_path)
            doc.close()
            doc = None

            temp_path.replace(new_path)

            processed += 1

        except Exception:
            if doc is not None:
                doc.close()

            if temp_path.exists():
                temp_path.unlink()

            raise

    return processed