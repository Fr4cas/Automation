import os
import json
import dotenv
import urllib.request
import urllib.error

from dotenv import load_dotenv

load_dotenv()

WEB_APP_URL = os.getenv("GOOGLE_SHEETS_URL")
SECRET_TOKEN = os.getenv("GOOGLE_SHEETS_TOKEN")

def send_metadata(metadata):

    if not WEB_APP_URL or not SECRET_TOKEN:
        raise RuntimeError("Google Sheets configuration missing")

    payload = {
        "token": SECRET_TOKEN,
        "recvNum": metadata.get("recvNum", ""),
        "recvDate": metadata.get("recvDate", ""),
        "fromNum": metadata.get("fromNum", ""),
        "fromDate": metadata.get("fromDate", ""),
        "fromObj": metadata.get("fromObj", ""),
        "docuType": metadata.get("docuType", ""),
        "pSubject": metadata.get("pSubject", ""),
        "pTreatment": metadata.get("pTreatment", "")
    }

    data = json.dumps(
        payload, ensure_ascii=False
    ).encode("utf-8")

    request = urllib.request.Request(
        WEB_APP_URL,
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST"
    )

    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            result = json.loads(
                response.read().decode("utf-8")
            )

        if not result.get("success"):
            raise RuntimeError(result.get("error"))

        print(f"Added to Google Sheets: row {result.get('row')}")
        return result

    except urllib.error.HTTPError as error:
        print(f"HTTP Error: {error.code}")
        raise

    except urllib.error.URLError as error:
        print(f"Connection Error: {error.reason}")
        raise
