# -*- coding: utf-8 -*-
"""
nb_merging_tools.py

Functions that can be used to merge Notebooks. Might be useful in some cases.

Requirements:
    
    - nbmerge package:
        
        pip install nbmerge

Created on Sun Sep 16 14:42:28 2018

@author: Henrikki Tenkanen
"""

import nbmerge
import os
import glob

def merge_nbs(notebook_paths, base_dir, output_fp):
    """Merges Notebooks based on a list of filepaths and saves them to output filepath."""
    # Merge notebooks
    merged_notebook = nbmerge.merge_notebooks(base_dir=base_dir, file_paths=notebook_paths)
    nbmerge.write_notebook(merged_notebook, fp=output_fp)
    print("Saved merged Notebook: %s into:\n%s" % (os.path.basename(output_fp), base_dir))
    
def merge_autograded_user_notebooks(base_folder, exercise_number, user):
    """Merges Jupyter notebooks into one and saves it into the same folder as the origin files"""
    # Get notebook filepaths
    notebooks, base_dir = get_autograded_user_notebook_files(base_folder, exercise_number, user)
    
    # Parse output filepath
    outfp = os.path.join(base_dir, "Exercise-%s-%s-feedback.ipynb" % (exercise_number, user))
    
    # Merge and save
    merge_nbs(notebooks, base_dir, outfp)

def merge_submitted_user_notebooks(base_folder, exercise_number, user):
    """Merges Jupyter notebooks into one and saves it into the same folder as the origin files"""
    # Get notebook filepaths
    notebooks, base_dir = get_submitted_user_notebook_files(base_folder, exercise_number, user)
    
    # Parse output filepath
    outfp = os.path.join(base_dir, "Exercise-%s-%s-feedback.ipynb" % (exercise_number, user))
    
    # Merge and save
    merge_nbs(notebooks, base_dir, outfp)
    
def merge_notebooks(base_folder, exercise_number):
    """Merges Jupyter notebooks into one and saves it into the same folder as the origin files"""
    # Get notebook filepaths
    notebooks, base_dir = get_notebook_files(base_folder)
    
    # Parse output filepath
    outfp = os.path.join(base_folder, "Exercise-%s-merged.ipynb" % (exercise_number))
    
    # Merge and save
    merge_nbs(notebooks, base_dir, outfp)
    
def get_autograded_user_notebook_files(base_folder, exercise_number, user):
    """Collects all autograded notebook files of a user"""
    tmpl = os.path.join(base_folder, 'autograded', user, "Exercise-%s" % exercise_number,"Exercise-%s*.ipynb" % exercise_number)
    files = glob.glob(tmpl)
    return (files, os.path.dirname(tmpl))

def get_submitted_user_notebook_files(base_folder, exercise_number, user):
    """Collects all submitted exercise notebook files of a user"""
    tmpl = os.path.join(base_folder, 'submitted', user, "Exercise-%s" % exercise_number,"Exercise-%s*.ipynb" % exercise_number)
    files = glob.glob(tmpl)
    return (files, os.path.dirname(tmpl))

def get_notebook_files(base_folder):
    """Get all notebooks inside a folder"""
    tmpl = os.path.join(base_folder, "*.ipynb")
    files = glob.glob(tmpl)
    return (files, os.path.dirname(tmpl))
