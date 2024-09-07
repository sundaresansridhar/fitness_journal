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
#     ''' getting all the filepaths'''
#     intro_filepaths = [
#         [os.path.join(current_directory, "all_files", filename),None] for filename in ["1_Intro.pdf", "2_vision_board.pdf"]
#     ]
#     for file_type, folder_name in types.items():
#         all_filepaths = []
#         all_filepaths += intro_filepaths
#         ''' gears filepath'''
#         gears_filepath = os.path.join(current_directory, folder_name, "3_Gears and equipments.pdf")
#         all_filepaths += [[gears_filepath,None]]
#         ''' getting the monthly data'''
#         for imonth in range(1,13):
#             ''' cover path'''
#             month_cover_path = os.path.join(current_directory, 'all_files', "4_month_designs.pdf")
#             all_filepaths += [[month_cover_path,imonth-1]]
#             ''' getting the pdf of the months'''
#             daily_entries_folder = f'daily_entries_{version}_{file_type}'
#             all_files = os.listdir(os.path.join(current_directory,daily_entries_folder))
#             selected_files = [filename for filename in all_files if f'entry_{year}{str(imonth).zfill(2)}' in filename]
#             selected_files.sort()
#             daily_entry_paths = [[os.path.join(current_directory,daily_entries_folder,filename),None] for filename in selected_files]
#             all_filepaths += daily_entry_paths
#             ''' end of month '''
#             all_filepaths += [[os.path.join(current_directory,folder_name,'5_end_of_month.pdf'),None]]

#         ''' merging the pdfs '''
#         filepaths = [sel_data[0] for sel_data in all_filepaths]
#         page_to_merge = [sel_data[1] for sel_data in all_filepaths]

#         ''' merging the pdfs'''
#         output_filepath = os.path.join(current_directory,f"fitness_journal_{version}_{file_type}.pdf")
#         merge_pdfs(filepaths, output_filepath,page_to_merge=page_to_merge)
