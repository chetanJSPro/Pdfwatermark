import tkinter as tk
from tkinter import filedialog, messagebox
from PyPDF2 import PdfWriter, PdfReader
from reportlab.pdfgen import canvas
import os

def create_watermark(text, page_width, page_height):
    watermark_path = "watermark.pdf"
    c = canvas.Canvas(watermark_path, pagesize=(page_width, page_height))
    
    # Set a fixed font size
    font_size = 20  # Set your desired font size
    c.setFont("Helvetica", font_size)

    # Position watermark at the top-left corner
    c.drawString(20, float(page_height) - 20, text)  # Ensure page_height is a float
    c.save()
    return watermark_path

def add_watermark_to_pdf(input_pdf, output_pdf):
    reader = PdfReader(input_pdf)
    writer = PdfWriter()

    for page in reader.pages:
        # Get the page dimensions and convert them to float
        page_width = float(page.mediabox.width)
        page_height = float(page.mediabox.height)
        
        watermark_path = create_watermark("https://chetan.pro", page_width, page_height)
        watermark = PdfReader(watermark_path)

        page.merge_page(watermark.pages[0])
        writer.add_page(page)

    with open(output_pdf, "wb") as output_file:
        writer.write(output_file)

def upload_pdfs():
    file_paths = filedialog.askopenfilenames(filetypes=[("PDF files", "*.pdf")])
    if file_paths:
        for file_path in file_paths:
            output_pdf = f"watermarked_output_{os.path.basename(file_path)}"
            add_watermark_to_pdf(file_path, output_pdf)
            full_output_path = os.path.abspath(output_pdf)
            messagebox.showinfo("Success", f"Watermarked PDF saved at:\n{full_output_path}")
    else:
        messagebox.showwarning("No files selected", "Please select one or more PDF files.")

# GUI setup
root = tk.Tk()
root.title("PDF Watermarking Tool")

upload_button = tk.Button(root, text="Upload PDFs", command=upload_pdfs)
upload_button.pack(pady=20)

root.mainloop()
