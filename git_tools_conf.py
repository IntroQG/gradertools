# -*- coding: utf-8 -*-
"""
git_tools_conf.py

Configuration file for Git tools.

In here you can modify:
    - which users you to pull and push
    - which organization to use
    - which exercises to pull
    - where to locate those repositories locally
    - behaviour whether GitHub Classroom repo name should be converted to format supported by NBgrader (bool)

Created on Sat Sep 15 19:57:24 2018

@author: Henrikki Tenkanen
"""

# Base folder where repositories will be collected
base_folder = r"C:\HY-DATA\HENTENKA\KOODIT\Opetus\Geo-Python\Exercises-2018"
    
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

# Convert GitHub repository name to format supported by NBgrader
use_nbgrader_style = True

# Generate pdf from the feedback
generate_pdf = True