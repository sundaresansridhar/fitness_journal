"""
Module to generate the monthly entries

Created on Thu Aug 29 18:55:51 2024

@author: sundaresan_sridhar
"""

import os
from generate_daily_entries import input_dict, foldernames
from merge_pdfs import merge_pdfs

""" current directory"""
current_directory = os.path.abspath(os.path.dirname(__file__))


def get_input_for_merging(folder_type: str, month: int):
    """base directory"""
    base_directory = os.path.join(
        current_directory, f"version_{input_dict['version']}", folder_type
    )

    """ filepath of the monthly designs"""
    month_design_filepath = os.path.join(
        base_directory, "..", "common", "compressed", "4_month_designs.pdf"
    )

    """ daily entries for the given month"""
    daily_entries_filepath = os.path.join(base_directory, "daily_entries")
    all_filenames = os.listdir(daily_entries_filepath)
    reference_text = str(input_dict["year"]) + str(month).zfill(2)
    daily_filepaths = [
        os.path.join(daily_entries_filepath, filename)
        for filename in all_filenames
        if reference_text in filename
    ]
    daily_filepaths.sort()

    """ end of month filepath"""
    month_end_filepath = os.path.join(base_directory, "compressed", "5_end_of_month.pdf")

    input_filepaths = [month_design_filepath] + daily_filepaths + [month_end_filepath]
    page_to_merge = [month] + [None for i in range(len(input_filepaths) - 1)]
    output_filepath = os.path.join(base_directory, "monthly_entries", reference_text + ".pdf")

    return input_filepaths, page_to_merge, output_filepath


def get_monthly_merging_details():
    merging_details = {}
    for folder_type in foldernames:
        merging_details.setdefault(folder_type, dict(input_filepaths=[], page_to_merge=[]))
        for month in range(1, 13):
            temp_inputs, temp_pages, __ = get_input_for_merging(folder_type, month)
            merging_details[folder_type]["input_filepaths"] += temp_inputs
            merging_details[folder_type]["page_to_merge"] += temp_pages
    return merging_details
