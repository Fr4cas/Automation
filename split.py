import os
from pypdf import PdfReader

folder = os.path.join(os.path.dirname(__file__), "pdfs")

for filename in os.listdir(folder):
    if filename.lower().endswith(".pdf"):
        file_path = os.path.join(folder, filename)

        reader = PdfReader(file_path)

        print(filename)
        print(f"  Number of pages: {len(reader.pages)}")