import fitz

def read_pdf(pdf_file):
    content = []
    with fitz.open(pdf_file) as file:
        for page in file: 
            content.append(page.get_text())

    content = ' '.join(content)
    return content