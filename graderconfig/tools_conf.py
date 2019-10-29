# -*- coding: utf-8 -*-
"""
tools_conf.py

Configuration file for Git tools.

In here you can modify / choose:
    - base folder where everything will be stored (required)
    - your (GitHub) name as an inspector (required) 
    - which users you to pull and push (required)
    - which organization to use (required)
    - which exercises to pull (required)
    - behaviour whether GitHub Classroom repo name should be converted to format supported by NBgrader (bool)
    - whether to produce pdf-file from feedback (optional but practically required for now)
    - whether to send feedback automatically to Slack (optional)
    - the filepath to csv-file with student information (GitHub username, Slack id/name, etc.)
        - you can also specify which column names the student-info csv-file has (4 required ones, at the bottom of this file)  

Created on Sat Sep 15 19:57:24 2018

@author: Henrikki Tenkanen
"""

import os

# =============================================
# Functions to get default directory paths
#   Do not touch
# =============================================

def get_current_path():
    """Returns current path of the file that is being excecuted."""
    current_path = os.path.dirname(os.path.realpath(__file__))
    return current_path

#def get_data_directory_path():
#    """Returns a default path to data directory of gradertools (two levels up)"""
#    current_path = get_current_path()
#    # Data path is one level up from graderconfig folder
#    data_dir = os.path.join(os.path.dirname(current_path), 'data')
#    if os.path.exists(data_dir):
#        return data_dir
#   else:
#       raise ValueError("Data directory was not in it's default location. Looked from: %s" % data_dir)


def get_project_root_path():
    """Returns a default path to data directory of gradertools (three levels up)"""
    current_path = get_current_path()
    # Path is two levels up
    root_dir = os.path.dirname(os.path.dirname(current_path))
    return root_dir

# ===============================
# Exercise / Classroom parameters
# ===============================

# Inspector (the GitHub username of assistant/instructor)
inspector_user_name = 'GRADER_NAME_GOES_HERE'

# Organization
organization = "IntroQG-2019"

# Suffix for source repository for autograded Exercises
autograding_suffix = "-autograding"




# Generate list of usernames:
# Uncomment lines below to directly list student names
#user_names = """Copy
#paste
#here
#users
#from 
#excel
#one
#per
#line"""

# Placeholder for graderbot (comment out if using list above)
user_names = NAMES_GO_HERE

user_names = user_names.split("\n")

# List of GitHub usernames that should be pulled
# Comment out this line if you use the split-approach above :)
#user_names = ['saratodorovic', 'VuokkoH', 'hunajaiivari']


# List of exercise numbers to pull (e.g. [3], or [3,4,5] if fetching multiple)
# Uncomment to list exercises directly
#exercise_list = [2]

# Exercise list if using graderbot (comment out if listing exercises above)
exercise_list = TO_BE_GRADED

# Additional Classroom repos (e.g. ['final-assignment'])
additional_classroom_repos = []
    
# Extra repos from the organization (not a Classroom repo, e.g. ["Grades"])
extra_repos = [] 

# ===================
# Nbgrader parameters
# ===================

# Base folder where repositories will be collected 
# You can modify this but the default value should be okay (three levels up from the location of this file)
base_folder = get_project_root_path()

# Convert GitHub repository name to format supported by NBgrader
use_nbgrader_style = True

# Generate pdf from the feedback
generate_pdf = True

# ===================
# Feedback parameters
# ===================

# Send feedback to Slack (True / False)
send_to_slack = False

# Send feedback to GitHub (True / False)
send_to_github = True

# ===============================
# Student information parameters
# ===============================


# File containing the student info (e.g. Slack info + GitHub usernames)
# You can manually specify path to 'student_info_file' below if needed. The 'gradertools/data' -folder is the default location for student information
#data_dir = get_data_directory_path()
#student_info_filename = "Geopy_Autogis_students_with_Slack_info.csv"
#student_info_file = os.path.join(data_dir, student_info_filename)

# Required column names
github_username_column = 'Githubname'
name_column = 'Name'
real_name_column = 'real_name'
assistant_column = 'Assistant'
slack_id_column = 'id'
slack_display_name_column = 'display_name'
