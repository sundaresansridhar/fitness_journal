#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Module to generate the journal PDF

Created on Thu Aug 29 18:55:51 2024

@author: sundaresan_sridhar
"""
from PyPDF2 import PdfMerger, PdfReader, PdfWriter
import os
from generate_daily_entries import types,version, year
from io import BytesIO

""" current directory """
current_directory = os.path.abspath(os.path.dirname(__file__))
 
def merge_pdfs(filepath_list, output_path, page_to_merge = None):
    """
    Merges multiple PDF files into a single PDF.

    Parameters:
        filepath_list (list): List of paths to the PDF files to be merged.
        output_path (str): Path where the merged PDF will be saved.
    """
    merger = PdfMerger()
    if page_to_merge is None:
        page_to_merge = [None for i in filepath_list]
    try:
        # Iterate over the list of PDF files
        for ipdf,pdf in enumerate(filepath_list):
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
            print(f"PDFs {pdf.split('/')[-1]} merged successfully into {output_path}")
                
        # Write the merged PDF to the specified output path
        merger.write(output_path)
        
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # Close the merger object
        merger.close()
    

if __name__=='__main__':
    ''' getting all the filepaths'''
    intro_filepaths = [
        [os.path.join(current_directory, "all_files", filename),None] for filename in ["1_Intro.pdf", "2_vision_board.pdf"]
    ]
    for file_type, folder_name in types.items():
        all_filepaths = []
        all_filepaths += intro_filepaths
        ''' gears filepath'''
        gears_filepath = os.path.join(current_directory, folder_name, "3_Gears and equipments.pdf")
        all_filepaths += [[gears_filepath,None]]
        ''' getting the monthly data'''
        for imonth in range(1,13):
            ''' cover path'''
            month_cover_path = os.path.join(current_directory, 'all_files', "4_month_designs.pdf")
            all_filepaths += [[month_cover_path,imonth-1]]
            ''' getting the pdf of the months'''
            daily_entries_folder = f'daily_entries_{version}_{file_type}'
            all_files = os.listdir(os.path.join(current_directory,daily_entries_folder))
            selected_files = [filename for filename in all_files if f'entry_{year}{str(imonth).zfill(2)}' in filename]
            selected_files.sort()
            daily_entry_paths = [[os.path.join(current_directory,daily_entries_folder,filename),None] for filename in selected_files]
            all_filepaths += daily_entry_paths
            ''' end of month '''
            all_filepaths += [[os.path.join(current_directory,folder_name,'5_end_of_month.pdf'),None]]
    
        ''' merging the pdfs '''
        filepaths = [sel_data[0] for sel_data in all_filepaths]
        page_to_merge = [sel_data[1] for sel_data in all_filepaths]
    
        ''' merging the pdfs'''
        output_filepath = os.path.join(current_directory,f"fitness_journal_{version}_{file_type}.pdf")
        merge_pdfs(filepaths, output_filepath,page_to_merge=page_to_merge)
