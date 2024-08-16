from pdfminer.high_level import extract_text

def data_2(pdf_file):
    # Replace 'your_pdf_file.pdf' with the path to your PDF file
    text = extract_text(pdf_file, page_numbers=[0]).split("\n\n")
    title = text[0]
    authors = text[1]
    return title, authors
        