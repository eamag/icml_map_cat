import os
import re

import PyPDF2
import requests


def remove_surrogates(text):
    return re.sub(r"[\ud800-\udfff]", "", text)


def download_pdf(pdf_link):
    response = requests.get(pdf_link)

    if response.status_code == 200:
        with open("temp.pdf", "wb") as f:
            f.write(response.content)
        return True
    else:
        print(f"Failed to download the PDF. Status code: {response.status_code}")
        return False


def extract_pdf_text(pdf_file):
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    num_pages = len(pdf_reader.pages)
    text = []

    for page in range(num_pages):
        page_obj = pdf_reader.pages[page]
        text.append(page_obj.extract_text())

    return " ".join(text)


def find_references_start(parsed_text):
    patterns = [
        r"(?i)(\n|\r\n|\r|\.\s|-\s|\*\s|\.)(References)",
        r"(?i)(\n|\r\n|\r|\.\s|-\s|\*\s|\.)(Bibliography)",
        r"(?i)(\n|\r\n|\r|\.\s|-\s|\*\s|\.)(Acknowledgements)",
    ]
    for pattern in patterns:
        match = re.search(pattern, parsed_text)
        if match:
            return match.start() + len(match.group(1))
    return -1


def process_paper(pdf_link):
    if download_pdf(pdf_link):
        with open("temp.pdf", "rb") as pdf_file:
            text = extract_pdf_text(pdf_file)
        os.remove("temp.pdf")
        text = text[: find_references_start(text)]
        text = remove_surrogates(text)
        return text.replace("\n", "")
    else:
        return None
