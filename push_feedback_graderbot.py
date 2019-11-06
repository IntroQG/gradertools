""""
Push files to student repository
By default pushes only README.md

Control student list and exercise number in graderconfig/tools_conf.py

Assumes that the local student exercise repository has the student's GitHub repo as remote

"""

from git import Repo
import os
from graderconfig.tools_conf import base_folder, user_names, exercise_list


def get_token():
    """Gets secure GitHub token for committing"""
    token = os.environ['GITHUB_TOKEN']
    return token

def git_push(repo_path, commit_msg, files=["README.md"], token=None):
    """ add, commit and push listed files """
    try:
        repo = Repo(repo_path)
        orig_remote = repo.remotes[0].url[8:]
        new_remote = 'https://'+token+'@'+orig_remote
        remote = repo.create_remote('autograde', url=new_remote)
        repo.index.add(files)
        repo.index.commit(commit_msg)
        autograde = repo.remote(name='autograde')
        autograde.push('autograde', 'master')
    except:
        print('Some error occured while pushing the code')

def main():

    # Define submitted -folder path
    submitted_f = os.path.join(base_folder, "submitted")

    # Get token
    token = get_token()

    # Iterate over exercises if they are defined
    if len(exercise_list) > 0:

        for exercise_number in exercise_list:

            # Commit message per exercise
            commit_msg = "Graderbot added points to exercise %s" % exercise_number

            # Iterate over usernames
            for user in user_names:

                print("USER: %s" % user)

                # Set repo path
                exercise_repo_path = os.path.join(submitted_f, user, "Exercise-%s" % exercise_number)

                # Push listed files
                git_push(exercise_repo_path, commit_msg, files=["README.md"], token=token)


if __name__ == '__main__':
    main()
