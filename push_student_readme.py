""""
Push files to student repository
Currently only pushes README.md

Assumes that the local student exercise repository has the student's GitHub repo as remote

WORK IN PROGRESS

"""

from git import Repo
import git
import os
import shutil
from sys import platform
import subprocess
from graderconfig.tools_conf import base_folder, user_names, exercise_list
from pull_student_repos import is_git_repo
from util import get_source_notebook_files


def git_push(repo_path, commit_msg, files = ["README.md"]):
    """ add, commit and push listed files """
    try:
        repo = Repo(repo_path)
        repo.index.add(files)
        repo.index.commit(commit_msg)
        origin = repo.remote(name='origin')
        origin.push()
    except:
        print('Some error occured while pushing the code')


def main():

    # Define submitted -folder path
    submitted_f = os.path.join(base_folder, "submitted")


    # Iterate over exercises if they are defined
    if len(exercise_list) > 0:

        for exercise_number in exercise_list:
            commit_msg = "added points to exercise %s" % exercise_number

            # Iterate over usernames
            for uname in user_names:

                print("USER: %s" % uname)

                # Set paths
                student_f = os.path.join(submitted_f, uname)
                exercise_path = os.path.join(student_f, "Exercise-%s" % exercise_number)
                repo_path = os.path.join(exercise_path)

                # CLone repository
                git_push(repo_path, commit_msg)




if __name__ == '__main__':
    main()