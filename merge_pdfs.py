"""
Module to generate the journal PDF

Created on Thu Aug 29 18:55:51 2024

@author: sundaresan_sridhar
"""

from PyPDF2 import PdfMerger, PdfReader, PdfWriter
import os
from io import BytesIO

""" current directory """
current_directory = os.path.abspath(os.path.dirname(__file__))


def merge_pdfs(
    filepath_list: list, output_path: str, page_to_merge: int = None, debug: bool = False
):
    """
    Merges multiple PDF files into a single PDF.

    Parameters:
        filepath_list (list): List of paths to the PDF files to be merged.
        output_path (str): Path where the merged PDF will be saved.
        page_to_merge (int): Page to merge. If None, all pages are merged
        debug (bool): Printing for debugging.
    """
    merger = PdfMerger()
    if page_to_merge is None:
        page_to_merge = [None for i in filepath_list]
    try:
        # Iterate over the list of PDF files
        for ipdf, pdf in enumerate(filepath_list):
            if page_to_merge[ipdf] is None:
                # Append each PDF file to the merger object
                merger.append(pdf)
            else:

                # Read the PDF file
                reader = PdfReader(pdf)
                # Extract the selected page
                selected_page = reader.pages[page_to_merge[ipdf]]

                # Create a PdfWriter object to write the first page to a new PDF
                writer = PdfWriter()
                writer.add_page(selected_page)

                # Write the single page PDF to a BytesIO object (in-memory buffer)
                temp_pdf = BytesIO()
                writer.write(temp_pdf)
                temp_pdf.seek(0)

                # Append the in-memory PDF (first page) to the merger
                merger.append(temp_pdf)
            if debug:
                print(f"PDFs {pdf.split('/')[-1]} merged successfully into {output_path}")

        # Write the merged PDF to the specified output path
        merger.write(output_path)

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # Close the merger object
        merger.close()
