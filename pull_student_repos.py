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

Modified on  Wed Sept 11 2019 by Vuokko (removed actions related to autograding and focused this script on pulling student exercises).

"""

from git import Repo
import pandas as pd
import git
import os
import shutil
from sys import platform
import subprocess
from graderconfig.tools_conf import base_folder, organization, user_names, exercise_list, additional_classroom_repos, extra_repos, use_nbgrader_style, autograding_suffix
from util import get_source_notebook_files
import time
import warnings

def create_remote(repo, github_remote_url):
    """Creates a remote to specified url."""
    try:
        origin = repo.create_remote('origin', github_remote_url)
        return origin
    except:
        return repo.remotes.origin

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


def is_git_repo(directory):
    """Validates if directory is Git repository"""
    try:
        _ = git.Repo(directory).git_dir
        return True
    # If directory can be found but it is not a Git repository
    except git.exc.InvalidGitRepositoryError:
        return False
    # If directory does not exist
    except git.exc.NoSuchPathError:
        return False


def is_student_classroom(repo, user, exercise):
    """Validates if repository is an actual remote for the Exercise source files. Returns the remote if it is."""
    # Check remotes
    url = repo.remotes.origin.url
    # Validate 
    split = url.split('/')
    assert split[-2] == organization, "Organization of the remote does not match with the project!"
    if split[-1] == "exercise-%s-%s.git" % (exercise, user):
        return True
    else:
        return False


def update_course_repo(student_folder, organization, user=None, exercise=None):
    """Update course repository from GitHub"""
    
    # Get token
    token = get_token()

    # Directory name locally
    directory_path = os.path.join(student_folder, "Exercise-%s" % exercise)
    
    # Check if exercise repository is initialized
    if is_git_repo(directory_path):

        # If repository exists locally it can be either format "Exercise-3" or "exercise-3-username"
        repo_path = os.path.join(student_folder, "exercise-%s-%s" % (exercise, user))
        
        if os.path.exists(repo_path):
            pass
        else:
            repo_path = os.path.join(student_folder, "Exercise-%s" % (exercise))
        
        # Get the repo
        repo = Repo(repo_path)
        
        # Check if the repo is correct student Classroom
        if user is not None:
            if is_student_classroom(repo, user, exercise):
                # Remote url
                url = repo.remotes.origin.url
                print("Updating Exercise files of %s" % url)
                pull_repo(repo, url)
            else:
                raise ValueError("%s directory contains something else than the student files for Exercise-%s. Please check and ensure that the directory contains valid materials." % (repo_path, exercise))
                
    else:
        # If repository has not been cloned yet
        # -------------------------------------
        
        # Remove Exercise directory if it exists (so that it can be updated)
        remove_normal_directory(directory_path)
        
        # Repository name in GitHub
        repo_name = "exercise-%s-%s" % (exercise, user)
        
        # Local Git Repository
        repo_path = os.path.join(student_folder, repo_name)
        
        # Create origin
        github_remote = generate_github_remote(organization, repo_name)
        
        # If cloning it should be done on the parent folder of the 'repo_path'
        was_found = git_clone(github_remote, repo_path, token)
        
        # If the student has not started the assignment the repo path does not exist
        if was_found is False:
            repo_path = None
        
    return repo_path

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
    print("Renamed directory:", os.path.basename(repo_path), " to ", os.path.basename(new_name))
    return new_name
    
def remove_git_folder(repo_path):
    """Git file conflicts with nbgrader on Windows, hence, if automatic grading is used, it git needs to be disabled (removing .git folder)"""
    git_dir = os.path.join(repo_path, ".git")
    os.system('rmdir /S /Q "{}"'.format(git_dir)) 
    print("Removed .git file so it does not conflict with nbgrader.")
    
def fix_git_perms(repo_path):
    """Git directory has files with read-only permissions that cause trouble with nbgrader. This fixes that issue."""
    git_dir = os.path.join(repo_path, ".git")
    for root, dirs, files in os.walk(git_dir):
        for d in dirs:
            os.chmod(os.path.join(root, d), 0o755)
        for f in files:
            os.chmod(os.path.join(root, f), 0o644)
    print("Setting appropriate git directory permissions for nbgrader.")
    
def remove_normal_directory(folder_path):
    """Removes a folder if it exists"""
    if os.path.exists(folder_path):
        shutil.rmtree(folder_path)

def get_token():
    """Gets secure GitHub token for committing"""
    token = os.getenv('GH_TOKEN')
    return token

def git_clone(github_remote, repo_path, token=None):
    """Clones remote repository to path"""
    # Clone remote
    orig_remote = github_remote[8:]
    if token != None:
        github_remote = 'https://'+token+'@'+orig_remote
    print("Cloning repository '%s'" % github_remote)
    try:
        Repo.clone_from(github_remote, repo_path)
    except Exception as e:
        warning = str(e)
        if "Repository not found" in warning:
            pass
        else:
            warnings.warn(str(e))
        return False


def generate_github_remote(organization, repository_name):
    """Generates remote url"""
    return 'https://github.com/%s/%s.git' % (organization, repository_name)


def add_assignment(base_folder, exercise_number):
    """Adds assignment """
    # Assignment name
    assignment = "Exercise-%s" % exercise_number
    print("Adding assignment %s" % assignment)
    
    subprocess.call([ "nbgrader", "db", "assignment", "add", "%s" % assignment], cwd=base_folder)
    return True


def get_age_of_file(fp):
    """Returns the age of a file (last modification) in seconds"""
    last_modification_time = os.path.getmtime(fp)
    current_time = time.time()
    # Return the age
    return round(current_time - last_modification_time, 0)

    
def init_missing_repo_log(log_fp, exercise_number, username):
    """Initializes a log file of the missing GitHub Classroom files into csv -file. Notice will always overwrite the older one if the file is older than 1 hour."""
    log = pd.DataFrame([["Exercise-%s" % exercise_number, username]], columns=['Exercise', 'Username'])
    # Save to file
    log.to_csv(log_fp, index=False)

    
def log_missing_repos(exercise_number, username):
    """Writes a log file of the missing GitHub Classroom files into csv -file. Notice will always overwrite the older one if the file is older than 1 hour."""
    # Parse filename
    log_fp = os.path.join(base_folder, "Exercise_%s_missing_classroom_submissions.csv" % exercise_number)
    
    # Check if the log exists
    if os.path.exists(log_fp):
        # Check if file is older than 1 hour
        if not get_age_of_file(log_fp) > 3600:
            # Read the file
            log = pd.read_csv(log_fp)
            
            # If the student name does not exist add it into the file
            if not username in log['Username'].values:
                log = log.append([["Exercise-%s" % exercise_number, username]], ignore_index=True)
                log.to_csv(log_fp)
        else:
            # Initialize the file
            init_missing_repo_log(log_fp, exercise_number, username)
    else:
        # Initialize the file
        init_missing_repo_log(log_fp, exercise_number, username)


def main():
    
    # Get token
    token = get_token()

    # Iterate over exercises if they are defined
    if len(exercise_list) > 0:
    
        for enumber in exercise_list:

            # Create submitted folder if it does not exist
            submitted_f = create_submitted_folder(base_folder)
            
            # Iterate over usernames
            for uname in user_names:
        
                print("Gathering repositories of: %s" % uname)
            
                # Parse user directory and create it if it does not exist
                student_f = create_student_folder(submitted_f, uname)
                
                # Update Exercise repository (clone or pull)
                repo_path = update_course_repo(student_f, organization, user=uname, exercise=enumber)
                
                # Change the folder name if the repo was successfully cloned
                if repo_path:
                    if use_nbgrader_style:
                        # Convert the directory name into format supported by nbgrader
                        new_path = rename_directory_for_nbgrader(repo_path=repo_path, exercise_number=enumber)
                        
                        # Remove .git file on Windows so that it does not conflict with nbgrader

                        if 'win' in platform:
                            #remove_git_folder(new_path)
                            fix_git_perms(new_path)
                
                # If the student's exercise was not found, print info to screen
                else:
                    print("Could not clone student repository. Student", uname, "has probably not started the Exercise.", enumber)
                    # Log to file
                    # log_missing_repos(enumber, uname)
                
    
    # Iterate over any other Github Classroom repos if they are defined
    if len(additional_classroom_repos) > 0:
        for add in additional_classroom_repos:
            
            # Create submitted folder if it does not exist
            submitted_f = create_submitted_folder(base_folder)

            for uname in user_names:
            
                # Parse user directory and create it if it does not exist
                student_f = create_student_folder(submitted_f, uname)

                # Repository name
                repo_name = "%s-%s" % (add, uname)

                # Local Git Repository
                repo_path = os.path.join(student_f, repo_name)

                # CLone repository
                git_clone(repo_path=repo_path, github_remote=generate_github_remote(organization=organization, repository_name=repo_name), token=token)

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
            
            # CLone repository
            git_clone(repo_path=repo_path, github_remote=generate_github_remote(organization=organization, repository_name=repo_name), token=token)
        
    
if __name__ == '__main__':
    main()
        
        
