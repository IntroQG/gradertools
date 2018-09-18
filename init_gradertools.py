# -*- coding: utf-8 -*-
"""
init_gradertools.py

Script for initializing the gradertools environment and testing that everything works.

@author: Henrikki Tenkanen
"""

import os
import sys
import shutil

print("======================================\nInitializing gradertools environment\n======================================\n\n")

# Get the directory path to the current and parent directory
parent_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
current_path = os.path.dirname(os.path.realpath(__file__))

# Copy the nbgrader configuration file to the parent directory
nbgrader_config = os.path.join(current_path, 'gradertools', 'config', 'nbgrader_config.py')
target_path = os.path.join(parent_path, 'nbgrader_config.py')

if not os.path.exists(target_path):
    print("Copying nbgrader configuration file to the root ..")
    shutil.copy(nbgrader_config, target_path)
else:
    answer = input("nbgrader_config.py file exists already. Overwrite? (y / n)\n")
    if answer == 'y':
        print("Copying nbgrader configuration file to the root ..")
        shutil.copy(nbgrader_config, target_path)
    else:
        print("nbgrader configuration file was not updated.")
        
# Conduct tests that packages are installed
failed_tests = []        
try:
    import nbgrader
    print("Nbgrader installed: [ok]")
except:
    failed_tests.append("Nbgrader Python package is not installed. You need to install it first:\n\nconda install -c conda-forge nbgrader")
try:
    import git
    print("GitPython installed: [ok]")
except:
    failed_tests.append("Gitpython Python package is not installed. You need to install it first:\n\nconda install -c conda-forge gitpython ")
try:
    import slackclient
    print("Slackclient installed: [ok]")
except:
    failed_tests.append("slackclient Python package is not installed. You need to install it first:\n\nconda install -c conda-forge slackclient")
try:
    import jinja2
    print("Jinja2 installed: [ok]")
except:
    failed_tests.append("Jinja2 Python package is not installed. You need to install it first:\n\nconda install -c conda-forge jinja2")
try:
    import pdfkit
    print("pdfkit installed: [ok]")
    # If pdfkit is installed test if wkhtmltopdf package works 
    try:
        # Try to produce pdf with pdfkit to test if wkhtmltopdf package works and is in the system path
        test_html = os.path.join(current_path, 'gradertools', 'testdata', 'test_feedback.html')
        test_pdf = os.path.join(current_path, 'gradertools', 'testdata', 'test_feedback.pdf')
        
        import pdfkit
        pdfkit.from_file(test_html, test_pdf)
        # Remove test pdf
        os.remove(test_pdf)
    except:
        failed_tests.append("wkhtmltopdf software is not installed. You need to install it first by downloading it from:\n\nhttps://wkhtmltopdf.org/downloads.html\n\nYou also need to insert the `../wkhtmltopdf/bin` folder to system path.")
except:
    failed_tests.append("pdfkit Python package is not installed. You need to install it first:\n\pip install pdfkit")
if len(failed_tests) > 0:
    for failed in failed_tests:
        print("\n\n==================\nERRORS:", failed + "\n")
else:
    print("==================\nALL TESTS PAST!\n\nNow you are ready to start using nbgrader and gradertools. :)")
    
