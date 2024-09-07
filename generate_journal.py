#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Module to generate the journal PDF

Created on Thu Aug 29 18:55:51 2024

@author: sundaresan_sridhar
"""

import os
from generate_daily_entries import foldernames, input_dict
from generate_intro import get_intro_merging_details
from generate_monthly_entries import get_monthly_merging_details
from merge_pdfs import merge_pdfs

""" current directory"""
current_directory = os.path.abspath(os.path.dirname(__file__))


def get_journal_merging_details():
    details_intro = get_intro_merging_details()
    details_monthly = get_monthly_merging_details()

    merging_details = {}
    for folder_type in foldernames:
        merging_details.setdefault(folder_type, {})
        merging_details[folder_type]["input_filepaths"] = (
            details_intro[folder_type]["input_filepaths"]
            + details_monthly[folder_type]["input_filepaths"]
        )
        merging_details[folder_type]["page_to_merge"] = (
            details_intro[folder_type]["page_to_merge"]
            + details_monthly[folder_type]["page_to_merge"]
        )

        """ output filepath"""
        merging_details[folder_type]["output_filepath"] = os.path.join(
            current_directory,
            f"version_{input_dict['version']}",
            folder_type,
            f"journal_{input_dict['year']}.pdf",
        )
    return merging_details


if __name__ == "__main__":
    merging_details = get_journal_merging_details()
    for folder_type, folder_data in merging_details.items():
        merge_pdfs(
            folder_data["input_filepaths"],
            folder_data["output_filepath"],
            page_to_merge=folder_data["page_to_merge"],
            debug=True,
        )
