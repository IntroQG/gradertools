# -*- coding: utf-8 -*-
"""
init_gradertools.py

Script for initializing the gradertools environment and testing that everything works.

@author: Henrikki Tenkanen
"""

import os
import subprocess
import shutil

print("======================================\nInitializing gradertools environment\n======================================\n\n")

# Get the directory path to the current and parent directory
current_path = os.path.dirname(os.path.realpath(__file__))
parent_path = os.path.dirname(current_path)

# Copy the nbgrader configuration file to the parent directory (one level up from the gradertools repo!)
nbgrader_config = os.path.join(current_path, 'graderconfig', 'nbgrader_config.py')
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
    # Initialize nbgrader in a way that it opens whenever jupyter notebook is launched
    subprocess.call(["jupyter", "nbextension", "enable", "--py", "nbgrader"], cwd=parent_path)
    print("Nbgrader installed and extension enabled: [ok]")
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

if len(failed_tests) > 0:
    for failed in failed_tests:
        print("\n\n==================\nERRORS:", failed + "\n")
else:
    print("==================\nALL TESTS PAST!\n\nNow you are ready to start using nbgrader and gradertools. :)")
    
