#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generate google sheet

Created on Thu Aug 29 09:50:40 2024

@author: sundaresan_sridhar
"""
from datetime import datetime, timedelta
import fitz  # PyMuPDF
from PIL import Image
import io
import matplotlib.pyplot as plt
import os
from time import strptime
import numpy as np


def plot_pdf(pdf_path: str):
    doc = fitz.open(pdf_path)

    # Select the page to render (e.g., first page)
    page_number = 0
    page = doc.load_page(page_number)

    # Render the page to a Pixmap (image)
    pix = page.get_pixmap()

    # Convert the Pixmap to a PIL Image
    image = Image.open(io.BytesIO(pix.tobytes()))

    # Plot the image using matplotlib
    plt.figure(figsize=(10, 10))
    plt.imshow(image)
    plt.axis("off")  # Hide axes
    plt.show()


def duplicate_pdf(pdf_path_input, pdf_path_output):
    # Open the existing PDF
    pdf_document = fitz.open(pdf_path_input)
    # Save the modified PDF to a new file
    pdf_document.save(pdf_path_output)
    # Close the document
    pdf_document.close()


def add_text_to_pdf(pdf_path_input, pdf_path_output, text, position, fontsize=40, color=(0, 0, 0)):
    # Open the existing PDF
    pdf_document = fitz.open(pdf_path_input)

    # Select the first page (0-indexed)
    page = pdf_document.load_page(0)  # Load the first page

    # Define the text and its properties
    text_position = position  # (x, y) coordinates
    text_fontsize = fontsize
    text_color = color  # RGB color

    # Add the text to the page
    page.insert_text(text_position, text, fontsize=text_fontsize, color=text_color)

    # Save the modified PDF to a new file
    pdf_document.save(pdf_path_output)

    # Close the document
    pdf_document.close()


def list_dates_of_year(year):
    # Start date for the given year
    start_date = datetime(year, 1, 1)
    # End date for the given year
    end_date = datetime(year + 1, 1, 1)
    # Initialize the current date to start date
    current_date = start_date
    # List to hold all dates
    all_dates_raw = []
    all_days = []
    while current_date < end_date:
        # Append the current date to the list
        all_dates_raw.append(current_date.strftime("%Y-%B-%d"))
        all_days.append(current_date.strftime("%A"))
        # Move to the next day
        current_date += timedelta(days=1)

    """ formatting the dates"""
    all_dates = []
    for date in all_dates_raw:
        date_split = date.split("-")
        date_split[1] = date_split[1][:3]
        date_split.reverse()
        all_dates += [date_split]
    return all_dates, all_days


input_dict = dict(
    version="v1",
    year=2025,
    date_settings=dict(
        x_values=[1260, 1335, 1435],
        y_value=345,
        fontsize=40,
        color=(0, 0, 0),
    ),
    days_settings=dict(
        x_values=[1075, 1165, 1260, 1350, 1445, 1535, 1630],
        y_value=455,
        fontsize=40,
        color=(0, 0, 0),
    ),
)

foldernames = ['printable','editable']

""" paths """
base_directory = os.path.abspath(os.path.dirname(__file__))

""" filepaths of the daily entries"""
filepaths_daily_entry = {
    filetype: os.path.join(
        base_directory,
        f"version_{input_dict['version']}/{filetype}/compressed/6_Daily_Entry.pdf",
    )
    for filetype in foldernames
}

def create_daily_entries():
    """List all dates in 2025"""
    all_dates, all_days = list_dates_of_year(input_dict["year"])
    for filetype, input_filepath in filepaths_daily_entry.items():
        ''' base save directory'''
        base_save_directory = os.path.join(
            base_directory,
            f"version_{input_dict['version']}/{filetype}/daily_entries",
        )
        try:
            os.mkdir(base_save_directory)
        except:
            pass
        
        temp_filepath = os.path.join(base_save_directory, "entry_temp.pdf")
        for idate, date in enumerate(all_dates):
            day = all_days[idate]

            """ duplicating the pdf page"""
            output_filepath = os.path.join(
                base_save_directory,
                f'daily_entry_{date[2]}{str(strptime(date[1],"%b").tm_mon).zfill(2)}{date[0]}.pdf',
            )
            duplicate_pdf(input_filepath, temp_filepath)
            print(output_filepath)

            """ adding the date"""
            for ielement, date_element in enumerate(date):
                position = (
                    input_dict["date_settings"]["x_values"][ielement],
                    input_dict["date_settings"]["y_value"],
                )
                add_text_to_pdf(
                    temp_filepath,
                    output_filepath,
                    str(date_element),
                    position,
                    fontsize=input_dict["date_settings"]["fontsize"],
                    color=input_dict["date_settings"]["color"],
                )
                duplicate_pdf(output_filepath, temp_filepath)
    
            """adding the day"""
            days_order = np.array(
                ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
            )
            position = (
                input_dict["days_settings"]["x_values"][int(np.where(days_order == day)[0][0])],
                input_dict["days_settings"]["y_value"],
            )
            add_text_to_pdf(
                temp_filepath,
                output_filepath,
                "X",
                position,
                fontsize=input_dict["days_settings"]["fontsize"],
                color=input_dict["days_settings"]["color"],
            )
    
            """ removing the temporary pdf"""
            os.remove(temp_filepath)


if __name__ == "__main__":
    create_daily_entries()