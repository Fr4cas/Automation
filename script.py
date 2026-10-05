import os

# The "files" folder is next to this script
folder = os.path.join(os.path.dirname(__file__), "files")

for filename in os.listdir(folder):
    old_path = os.path.join(folder, filename)

    # Only process files
    if os.path.isfile(old_path) and ")-" in filename:

        # Separate filename and extension
        name, extension = os.path.splitext(filename)

        # Keep everything up to and including ")-"
        new_name = name.split(")-", 1)[0] + ")-" + extension

        new_path = os.path.join(folder, new_name)

        os.rename(old_path, new_path)

        print(f"{filename}")
        print(f"  → {new_name}")