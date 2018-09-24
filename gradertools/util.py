# -*- coding: utf-8 -*-
"""
util.py 

Utility functions.

Created on Tue Sep 18 17:03:45 2018

@author: Henrikki Tenkanen
"""
import glob
import os

def get_autograded_user_notebook_files(base_folder, exercise_number, user):
    """Collects all autograded notebook files of a user"""
    tmpl = os.path.join(base_folder, 'autograded', user, "Exercise-%s" % exercise_number,"Exercise-%s*.ipynb" % exercise_number)
    files = glob.glob(tmpl)
    return (files, os.path.dirname(tmpl))

def get_source_notebook_files(base_folder, exercise_number):
    """Collects all autograded notebook files of a user"""
    tmpl = os.path.join(base_folder, 'source', "Exercise-%s" % exercise_number, "Exercise-%s*.ipynb" % exercise_number)
    files = glob.glob(tmpl)
    return files

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