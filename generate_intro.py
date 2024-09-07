#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Module to generate the journal PDF

Created on Thu Aug 29 18:55:51 2024

@author: sundaresan_sridhar
"""
import os
from generate_daily_entries import input_dict
from merge_pdfs import merge_pdfs

""" current directory"""
current_directory = os.path.abspath(os.path.dirname(__file__))

""" base directory"""
base_directory = os.path.join(current_directory, f"version_{input_dict['version']}", "common")


def get_intro_merging_details():
    input_filepaths = [
        os.path.join(base_directory, "compressed", filename)
        for filename in ["1_Intro.pdf", "2_vision_board.pdf"]
    ]
    page_to_merge = [None for i in range(len(input_filepaths))]
    return input_filepaths, page_to_merge


if __name__ == "__main__":
    get_intro_merging_details()
