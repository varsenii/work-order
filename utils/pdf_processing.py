from pypdf import PdfReader
import fitz


# def extract_text_from_pdf(pdf_path):
#     reader = PdfReader(pdf_path)
#     page = reader.pages[0]
#     return page.extract_text()


def extract_text_from_pdf(pdf_path):
    # Open the provided PDF file
    doc = fitz.open(pdf_path)

    # text = ""
    # for page_num in range(len(doc)):
    #     page = doc.load_page(page_num)
    #     text += page.get_text()
    text = doc.load_page(0).get_text()

    doc.close()
    return text
