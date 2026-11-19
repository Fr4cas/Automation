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

DEFAULT_STAMP_SETTINGS = {
    "document_number": {"x": 90, "y": 1, "scale": 80},
    "received_stamp": {"x": 90, "y": 95, "scale": 100},
}


def get_stamp_rect(page_rect, base_width, base_height, placement):
    x_percent = placement.get("x", 50)
    y_percent = placement.get("y", 50)
    scale = placement.get("scale", 100)

    if not all(
        isinstance(value, (int, float)) and 0 <= value <= 100
        for value in (x_percent, y_percent)
    ):
        raise ValueError("Stamp position values must be between 0 and 100.")

    if not isinstance(scale, (int, float)) or not 10 <= scale <= 300:
        raise ValueError("Stamp scale must be between 10 and 300 percent.")

    width = base_width * scale / 100
    height = base_height * scale / 100
    available_x = max(0, page_rect.width - width)
    available_y = max(0, page_rect.height - height)
    x = page_rect.x0 + available_x * x_percent / 100
    y = page_rect.y0 + available_y * y_percent / 100

    return pymupdf.Rect(x, y, x + width, y + height), scale


def get_pdf_files(folder):
    folder = Path(folder)

    pdf_files = sorted(
        file for file in folder.iterdir()
        if file.is_file() and file.suffix.lower() == ".pdf"
    )

    return pdf_files

def apply_document_number(
    pdf_path, number, received_date, placement=None
):
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

    image = Image.open(stamp_image_path)
    stamp_height = 18
    stamp_rect, _ = get_stamp_rect(
        page.rect,
        stamp_height * image.width / image.height,
        stamp_height,
        placement or DEFAULT_STAMP_SETTINGS["document_number"],
    )

    page.insert_image(
        stamp_rect,
        filename=str(stamp_image_path)
    )

    image.close()
    stamp_image_path.unlink()

    return doc


def apply_received_stamp(doc, received_date, placement=None):
    page = doc[-1]

    # Load received stamp template
    stamp_path = (
        Path(__file__).resolve().parent.parent
        / "assets"
        / "received_stamp_template.png"
    )

    stamp_width = 130
    stamp_height = 72
    stamp_rect, scale = get_stamp_rect(
        page.rect,
        stamp_width,
        stamp_height,
        placement or DEFAULT_STAMP_SETTINGS["received_stamp"],
    )

    # Insert stamp artwork
    page.insert_image(
        stamp_rect,
        filename=str(stamp_path)
    )

    # Date area inside the stamp
    date_rect = pymupdf.Rect(
        stamp_rect.x0 + stamp_rect.width * 0.27,
        stamp_rect.y0 + stamp_rect.height * 0.38,
        stamp_rect.x0 + stamp_rect.width * 0.73,
        stamp_rect.y0 + stamp_rect.height * 0.68
    )

    # Format date
    date_text = received_date.strftime("%b %d %Y").upper()

    fontsize = 10 * scale / 100

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

def stamp_documents(
    folder, start_number, received_date, stamp_settings=None
):
    stamp_settings = stamp_settings or DEFAULT_STAMP_SETTINGS
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
            doc = apply_document_number(
                pdf_path,
                number,
                received_date,
                stamp_settings.get("document_number"),
            )
            doc = apply_received_stamp(
                doc,
                received_date,
                stamp_settings.get("received_stamp"),
            )

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