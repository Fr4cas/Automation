import os

folder = os.path.join(os.path.dirname(__file__), "extracted_text")

def read_text_file(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()

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

        print(f"Reading: {filename}")
        print(text)