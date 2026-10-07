import os
import json

from playwright.sync_api import sync_playwright

folder = os.path.join(os.path.dirname(__file__), "files")

with open("destinations.json", "r", encoding="utf-8") as file:
    destinations = json.load(file)

def identify_file(filename):
    for name in sorted(destinations, key=len, reverse=True):
        if name in filename:
            return destinations[name]
            
    return "其他"

for filename in os.listdir(folder):
    destination = identify_file(filename)

    print(filename)
    print(f" {destination}")

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()

    page.goto("https://erp.formosa94.com.tw/Cogoces4/Main/fwMdiMain.htm")
    input("Press Enter to exit...")
    browser.close()