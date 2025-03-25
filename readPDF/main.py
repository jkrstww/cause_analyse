import fitz

with fitz.open('./Dr.ECI.pdf') as pdf:
    for page in pdf:
        print(page.get_text())