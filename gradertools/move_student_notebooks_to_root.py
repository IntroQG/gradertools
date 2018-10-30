# -*- coding: utf-8 -*-
"""
move_student_notebooks_to_root.py

Moves student Exercise Notebooks from either Numpy or Pandas directory to repository root. 
This is needed to enable autograding for some exercises at Geo-Python.

Created on Sat Oct 13 17:59:48 2018

@author: Henrikki Tenkanen
"""
import os
import shutil
import sys
import argparse
import glob
from graderconfig.tools_conf import base_folder, organization, user_names, exercise_list, autograding_suffix

def move_file_to_parent(fp):
    """Moves file one level up from the directory where it is located."""
    basename = os.path.basename(fp)
    current_dir = os.path.dirname(fp)
    parent_dir = os.path.dirname(current_dir)
    
    # Parse filepath
    target_fp = os.path.join(parent_dir, basename)
    try:
        shutil.move(fp, target_fp)
    except:
        print("[WARNING] Could not move %s" % basename)
    print("Moved %s to %s" % (basename, parent_dir))
    return target_fp
    
def get_notebooks(directory):
    """Returns filepaths of all notebooks that can be found from given directory"""
    fps = glob.glob(os.path.join(directory, '*.ipynb'))
    return fps

def move_data_directory_to_parent(directory_path):
    """Moves directory to parent folder"""
    parent_dir = os.path.dirname(os.path.dirname(directory_path))
    folder_name = os.path.basename(directory_path)
    
    # Filenames
    fnames = os.listdir(directory_path)
    
    # Create directory to upper level if it does not exist
    target_dir = os.path.join(parent_dir, folder_name)
    if not os.path.exists(target_dir):
        os.mkdir(target_dir)
    
    # Move to folder
    for fname in fnames:
        # source path
        src = os.path.join(directory_path, fname)
        target = os.path.join(target_dir, fname)
        try:
            shutil.copy2(src, target)
        except:
            print("[WARNING] Could not move %s" % fname)
    

def move_notebooks_to_parent(notebooks):
    """Moves a list of notebooks to their parent folder"""
    new_fps = []
    for nb in notebooks:
        new_fp = move_file_to_parent(nb)
        new_fps.append(new_fp)
    return new_fps
        
def move_user_notebooks_to_parent(user, exercise_number, etype, na_users):
    """Moves notebooks of specified exercise of a user to parent directory"""
    # Parse folder containing the exercises
    if etype.lower() == 'numpy':
        src_dir = os.path.join(base_folder, 'submitted', user, "Exercise-%s" % exercise_number, 'Numpy')
    elif etype.lower() == 'pandas':
        src_dir = os.path.join(base_folder, 'submitted', user, "Exercise-%s" % exercise_number, 'Pandas')
    else:
        raise ValueError("'etype' -parameter needs to be either 'numpy' or 'pandas'. %s was given." % etype)
    
    # Get notebooks
    nbs = get_notebooks(src_dir)
    
    if len(nbs) == 0: 
        print("Could not find any notebooks from %s" % src_dir)
        na_users.append(user)
    else:
        # Move notebooks to parent directory
        new_fps = move_notebooks_to_parent(nbs)
        
        # Move data directory if it can be found
        data_dir = os.path.join(src_dir, 'data')
        if os.path.exists(data_dir):
            print("Moving exercise data directory to root.. ")
            move_data_directory_to_parent(data_dir)
        
        return (new_fps, na_users)

def main():
    
    # Set up the argument parser
    ap = argparse.ArgumentParser()
    
    # Define arguments
    ap.add_argument("-t", "--type", required=True,
                    help="Exercise type. Possible values are 'numpy' or 'pandas'. ")
    
    # Parse arguments
    args = vars(ap.parse_args())   
    
    # List for users whom files could not be moved
    not_found_users = []
    
    # Iterate over exercises
    for enumber in exercise_list:
        # Iterate over users
        for user in user_names:
            new_fps, not_found_users = move_user_notebooks_to_parent(user, enumber, etype=args['type'], na_users=not_found_users)
            print("Moved %s version of Exercise %s files of user %s" % (args['type'], enumber, user, ))
        if len(not_found_users) > 0:
            print("Could not move Exercise %s files of following users:" % enumber)
            print(not_found_users)
            # Reset
            not_found_users = []
                
if __name__ == '__main__':
    main()
    
    
        
    




