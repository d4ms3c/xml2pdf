import os
import io
import xhtml2pdf.pisa as pisa
from tkinter import filedialog
from tkinter import Tk
from lxml import etree
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.pdfgen.canvas import Canvas

# Open a file selection dialog
root = Tk()
root.withdraw()
filepath = filedialog.askopenfilename(filetypes=[("XML files", "*.xml")])

#Read the XML file
with open(filepath, 'rb') as f:
    xml_string = f.read()
    

def xml_to_pdf(xml_string, pdf_file):
    # Parse the XML string
    xml = etree.fromstring(xml_string)

    # Create a PDF document
    pdf = Canvas(pdf_file, pagesize=A4)
    pdf.setFont('Courier', 10)

    # Recursively process the XML elements and add them to the PDF
    def process_element(element, x, y, level):
        # Add the tag name to the PDF
        tag = element.tag.upper()
        value = element.text
        if value is None:
            pdf.drawString(x, y, f"{'  ' * level}{tag}")
        else:
            pdf.drawString(x, y, f"{'  ' * level}{tag}:{value}")
            
        # Calculate the new Y position for the next element
        y -= 15

        # Recursively process the children of this element
        for child in element:
            y = process_element(child, x, y, level + 1)

        return y

    # Start at the top of the page and process the root element
    process_element(xml, 1*cm, 29*cm, 0)

    # Save the PDF
    pdf.save()

# Convert the XML to a PDF and save it to a file
filename, file_extension = os.path.splitext(filepath)
with open(f'{filename}.pdf', 'wb') as f:
    xml_to_pdf(xml_string, f)
print(f'Successfully converted {filepath} to {filename}.pdf')
