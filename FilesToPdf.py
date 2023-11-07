# -*- coding: utf-8 -*-
"""
Created on Thu Mar 30 10:24:15 2023

@author: jonas
A simple procedure to combine a random mess of files to one pdf file
"""
import os
import tempfile
from reportlab.lib.pagesizes import letter
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas
from PyPDF2 import PdfFileMerger

# Directory containing files to merge
file_dir = 'D:/Users/jonas/Desktop/Python/FilesToPdf/Input/'

# Initialize PDF merger
merger = PdfFileMerger()

# Loop through all files in the directory
for filename in os.listdir(file_dir):
    if filename.endswith('.jpg') or filename.endswith('.png'):
        # Convert each image file to PDF using reportlab
        img_file = os.path.join(file_dir, filename)
        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            img = ImageReader(img_file)
            width, height = img.getSize()
            c = canvas.Canvas(tmp.name)
            c.drawImage(img, 0, 0, width=width, height=height)
            c.showPage()
            c.save()

            # Append each PDF to the merger
            merger.append(open(tmp.name, 'rb'))
    elif filename.endswith('.txt') or filename.endswith('.svg') or filename.endswith('.odt'):
        # Convert each text file or document file to PDF using reportlab
        pdf_file = os.path.splitext(filename)[0] + '.pdf'
        txt_file = os.path.join(file_dir, filename)
        with open(os.path.join(file_dir, pdf_file), 'wb') as pdf_out_file:
            c = canvas.Canvas(pdf_out_file, pagesize=letter)
            with open(txt_file, 'r') as txt:
                for line in txt:
                    c.drawString(72, 720, line)
                    c.showPage()
                c.save()

        # Append each PDF to the merger
        merger.append(open(os.path.join(file_dir, pdf_file), 'rb'))
    elif filename.endswith('.pdf'):
        # Append each PDF to the merger
        merger.append(open(os.path.join(file_dir, filename), 'rb'))

# Write the merged PDF to a file
with open('D:/Users/jonas/Desktop/Python/FilesToPdf/merged.pdf', 'wb') as output:
    merger.write(output)


