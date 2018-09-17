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

# ===============================
# Exercise / Classroom parameters
# ===============================

# Inspector (the GitHub username of assistant/instructor)
inspector_user_name = 'htenkanen'

# Organization
organization = "Geo-Python-2018"

# List of GitHub usernames that should be pulled
user_names = ['htenkanen']
    
# List of exercise numbers to pull (e.g. [3], or [3,4,5] if fetching multiple)
exercise_list = [3]
    
# Additional Classroom repos (e.g. ['final-assignment'])
additional_classroom_repos = []
    
# Extra repos from the organization (not a Classroom repo, e.g. ["Grades"])
extra_repos = [] 

# ===================
# Nbgrader parameters
# ===================

# Base folder where repositories will be collected
base_folder = r"C:\HY-DATA\HENTENKA\KOODIT\Opetus\Geo-Python\Exercises-2018"

# Convert GitHub repository name to format supported by NBgrader
use_nbgrader_style = True

# Generate pdf from the feedback
generate_pdf = True

# ===================
# Feedback parameters
# ===================

# Send feedback to Slack (True / False)
send_to_slack = True

# Send feedback to GitHub (True / False)
send_to_github = True

# ===============================
# Student information parameters
# ===============================

# File containing the student info (e.g. Slack info + GitHub usernames)
student_info_file = r"C:\HY-DATA\HENTENKA\KOODIT\Opetus\Geo-Python\Exercises-2018\tools\data\Geopy_Autogis_students_with_Slack_info.csv"

# Required column names
github_username_column = 'Githubname'
name_column = 'Name'
slack_id_column = 'id'
slack_display_name_column = 'display_name'