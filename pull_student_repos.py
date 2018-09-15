# -*- coding: utf-8 -*-
"""

Pull GitHub Repositories of Automating GIS processes / Python for Geo-people based on a 
list of usernames. Organizes repositories in a way that NBgrader can be used to automatically 
grade the assignments. This means that:
    
    - Repositories are inserted into 'submitted' folder
    - In the submitted folder there will be a subfolder for each student, e.g. 'htenkanen' 
    - If nbgrader style is used, the GitHub Classroom name is changed from 'exercise-3-htenkanen' to 'Exercise-3' having a full path of './submitted/htenkanen/Exercise-3'
    - Notice: if nbgrader style is used, .git file is removed from the directory which conflicts with the nbgrader (at least on Windows)

Requirements:
    
    - This script requires that you have cached your GitHub credentials to your computer, see help: https://help.github.com/articles/caching-your-github-password-in-git/
    - Requires installation of 'gitpython' package: conda install -c conda-forge gitpython

Notes:
    It is safest to run this code from command prompt. 

Created on Wed Jan 11 13:55:44 2017

@author: hentenka
"""

from git import Repo
import os
from sys import platform
from git_tools_conf import base_folder, organization, user_names, exercise_list, additional_classroom_repos, extra_repos, use_nbgrader_style

def create_remote(repo, github_remote_url):
    """Creates a remote to specified url."""
    origin = repo.create_remote('origin', github_remote_url)
    return origin

def pull_repo(repo, github_remote):
    """Pulls a GitHub repository"""
    try:
        # Create remote connection to GitHub
        origin = create_remote(repo, github_remote)
        assert origin.exists()

        # Fetch the repo from GitHub
        origin.fetch()

        # Pull the repo from GitHub
        origin.pull(origin.refs[0].remote_head)
        
    except Exception as e:
        print("Could not pull following remote: %s" % github_remote)
        print(e)

def create_student_folder(base_f, uname):
    """Creates a folder for a student based on username if it does not exist."""
    # Student folder
    student_f = os.path.join(base_f, uname)
        
    # Check if the folder exists, if not create one
    if not os.path.isdir(student_f):
        os.mkdir(student_f)
    return student_f

def create_submitted_folder(base_f):
    """Creates a submitted folder if it does not exist."""
    # Submitted folder
    submitted_f = os.path.join(base_f, "submitted")
    
    # Check if the folder exists, if not create one
    if not os.path.isdir(submitted_f):
        os.mkdir(submitted_f)
    return submitted_f

def rename_directory_for_nbgrader(repo_path, exercise_number):
    """Renames the GitHub Classroom directory name to format supported by NBgrader"""
    new_name = os.path.join(os.path.dirname(repo_path), "Exercise-%s" % exercise_number)
    os.rename(repo_path, new_name)
    print("Renamed directory:", os.path.basename(repo_path), "\nto:\n", os.path.basename(new_name))
    return new_name
    
def remove_git_folder(repo_path):
    """Git file conflicts with nbgrader on Windows, hence, if automatic grading is used, it git needs to be disabled (removing .git folder)"""
    git_dir = os.path.join(repo_path, ".git")
    os.system('rmdir /S /Q "{}"'.format(git_dir)) 
    print("Removed .git file so it does not conflict with nbgrader.")

def run_git(repo_path, repo_name, organization):
    """Runs Git commands"""
    # Initialize local Git repository
    repo = Repo.init(repo_path)

    print("Pulling repository '%s'" % repo_name)
    
    # Create origin
    github_remote = 'https://github.com/%s/%s.git' % (organization, repo_name)
    
    # Pull remote
    pull_repo(repo, github_remote)

def main():
    
    # Iterate over usernames
    for uname in user_names:
        
        print("Gathering repositories of: %s" % uname)
        
        # Iterate over exercises if they are defined
        if len(exercise_list) > 0:
            for enumber in exercise_list:
                
                # Create submitted folder if it does not exist
                submitted_f = create_submitted_folder(base_folder)
                
                # Parse user directory and create it if it does not exist
                student_f = create_student_folder(submitted_f, uname)
                
                # Repository name in GitHub
                repo_name = "exercise-%s-%s" % (enumber, uname)
                
                # Local Git Repository
                repo_path = os.path.join(student_f, repo_name)
                
                # Run Git stuff - initialize local Git repo and pull the repository from remote
                run_git(repo_path=repo_path, organization=organization, repo_name=repo_name)
                
                # Change the folder name 
                if use_nbgrader_style:
                    # Convert the directory name into format supported by nbgrader
                    new_path = rename_directory_for_nbgrader(repo_path=repo_path, exercise_number=enumber)
                    
                    # Remove .git file on Windows so that it does not conflict with nbgrader
                    if 'win' in platform:
                        remove_git_folder(new_path)
    
        # Iterate over any other Github Classroom repos if they are defined
        if len(additional_classroom_repos) > 0:
            for add in additional_classroom_repos:
                
                # Create submitted folder if it does not exist
                submitted_f = create_submitted_folder(base_folder)
                
                # Parse user directory and create it if it does not exist
                student_f = create_student_folder(submitted_f, uname)
                
                # Repository name
                repo_name = "%s-%s" % (add, uname)
                
                # Local Git Repository
                repo_path = os.path.join(student_f, repo_name)
                
                # Run Git stuff - initialize local Git repo and pull the repository from remote
                run_git(repo_path=repo_path, organization=organization, repo_name=repo_name)
        
        print("Successfully gathered repositories for: %s" % uname)
        
    # Iterate over any other Github repos if they are defined and pull them under the base_f 
    if len(extra_repos) > 0:
        print("Gathering extra repos ...")
            
        for repo_name in extra_repos:
            print("Gathering repo: %s" % repo_name)
            
            # Create submitted folder if it does not exist
            submitted_f = create_submitted_folder(base_folder)
                
            # Parse user directory and create it if it does not exist
            student_f = create_student_folder(submitted_f, uname)
            
            # Local Git Repository
            repo_path = os.path.join(student_f, repo_name)
            
            # Run Git stuff - initialize local Git repo and pull the repository from remote
            run_git(repo_path=repo_path, organization=organization, repo_name=repo_name)
        
    
if __name__ == '__main__':
    main()
        
        
