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
    plt.axis('off')  # Hide axes
    plt.show()


def duplicate_pdf(pdf_path_input, pdf_path_output):
    # Open the existing PDF
    pdf_document = fitz.open(pdf_path_input)
    # Save the modified PDF to a new file
    pdf_document.save(pdf_path_output)
    # Close the document
    pdf_document.close()
    print(f'{pdf_path_output} is saved!')

def add_text_to_pdf(pdf_path_input,pdf_path_output, text, position, fontsize=40, color=(0, 0, 0)):
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
        all_dates_raw.append(current_date.strftime('%Y-%B-%d'))
        all_days.append(current_date.strftime('%A'))
        # Move to the next day
        current_date += timedelta(days=1)

    ''' formatting the dates'''
    all_dates = []
    for date in all_dates_raw:
        date_split = date.split('-')
        date_split[1] = date_split[1][:3]
        date_split.reverse()
        all_dates += [date_split]
    return all_dates,all_days


List all dates in 2025
dates_2025, days_2025 = list_dates_of_year(2025)

''' base save directory'''
pdf_path_input = '/home/sundaresan_sridhar/Downloads/6_Daily_Entry.pdf'
base_directory = os.path.join('/'.join(pdf_path_input.split('/')[:-1]), 'daily_entries', '')
try:
    os.mkdir(base_directory)
except:
    pass

x_values = [1260,1335,1435]
y_value = 345
fontsize=40
color=(0, 0, 0)


date = dates_2025[100]

''' duplicating the pdf page'''
pdf_path_output = os.path.join(base_directory, f'entry_{date[2]}{str(strptime(date[1],"%b").tm_mon).zfill(2)}{date[0]}.pdf')
pdf_path_temp = os.path.join(base_directory, 'entry_temp.pdf')
duplicate_pdf(pdf_path_input,pdf_path_temp)
for ielement,date_element in enumerate(date):
    position = (x_values[ielement],y_value)
    add_text_to_pdf(pdf_path_temp,pdf_path_output, str(date_element), position,fontsize=fontsize,color=color)
    duplicate_pdf(pdf_path_output, pdf_path_temp)

os.remove(pdf_path_temp)