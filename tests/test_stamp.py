from datetime import date
from scripts.stamp import stamp_documents

TEST_FOLDER = "stamp_test"

start_number = 1
received_date = date.today()

try:
    processed = stamp_documents(
        TEST_FOLDER,
        start_number,
        received_date
    )

    print(f"Successfully stamped {processed} documents.")

except Exception as e:
    print(f"Stamping failed: {e}")