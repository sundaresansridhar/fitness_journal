"""
Module to generate the journal PDF

Created on Thu Aug 29 18:55:51 2024

@author: sundaresan_sridhar
"""

import os
from generate_daily_entries import input_dict, foldernames

""" current directory"""
current_directory = os.path.abspath(os.path.dirname(__file__))

""" base directory"""
base_directory = os.path.join(current_directory, f"version_{input_dict['version']}", "common")


def get_intro_merging_details():
    common_input_filepaths = [
        os.path.join(base_directory, "compressed", filename)
        for filename in ["1_Intro.pdf", "2_vision_board.pdf"]
    ]
    merging_details = {}
    for folder_type in foldernames:
        merging_details.setdefault(folder_type, dict(input_filepaths=[], page_to_merge=[]))
        merging_details[folder_type]["input_filepaths"] = common_input_filepaths + [
            os.path.join(
                base_directory, "..", folder_type, "compressed", "3_Gears and equipments.pdf"
            )
        ]

    merging_details[folder_type]["page_to_merge"] = [
        None for i in range(len(merging_details[folder_type]["input_filepaths"]))
    ]
    return merging_details


if __name__ == "__main__":
    aa = get_intro_merging_details()
