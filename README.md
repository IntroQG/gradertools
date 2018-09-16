# Tools

This repository contains a few scripts that helps to manage Geo-Python and AutoGIS Exercises.

## Contents

- [Automate pulling repos](#automate-pulling-repos)
- [Generate feedback for students]()
- [Send feedback to Slack automatically (TODO)]()

## Automate pulling repos

Contents:

- [Overview](#overview)
- [Requirements](#requirements)
- [Configuration](#configuration)
- [How to run?](#how-to-run)

### Overview 

[pull_student_repos.py](pull_student_repos.py) is a script that helps to pull multiple repositories for specified students.
It also manages everything in a way that the student repositories can be automatically graded with NBgrader. 
Compliance with NBgrader  requires a few special tricks: 

 - Student repositories will be stored in folder called `submitted`
 - The GitHub Classroom repository that is pulled will be renamed from `exercise-3-username` to `Exercise-3`
 - On Windows, the .git folder needs to be removed because it conflicts with the automatic grading 
    - this is okay, it is not needed to push any changes to the repo
    - if for some reason there is a need to push some changes to that repository, [push_changes_.py]() script can be used to do that (or doing it manually by adding a remote with git commands)

### Requirements

#### gitpython -package

Requires installation of `gitpython` package:

```$ conda install -c conda-forge gitpython```

#### Cache your GitHub credentials

Requires also that the GitHub credentials (username and password) are cached in your computer.

On **Windows** you can do that on command prompt by running (see [help](https://help.github.com/articles/caching-your-github-password-in-git)):

```git config --global credential.helper wincred```

On **Mac** you can do that with credential-osxkeychain:

*Check that the tool exists* 

```$ git credential-osxkeychain```

*Cache your credentials*

```$ git config --global credential.helper osxkeychain```

On **Linux**, you can store the credentials for certain time period only:

```git config --global credential.helper 'cache --timeout=3600'```

### Configuration

The tool is managed from [git_tools_conf.py](git_tools_conf.py) file, where you can specify all the required parameters, such as:

```python
  # Base folder where repositories will be collected
  base_folder = r"C:\HY-DATA\HENTENKA\KOODIT\Opetus\Geo-Python\Exercises-2018"

  # Organization
  organization = "Geo-Python-2018"

  # List of GitHub usernames that should be pulled (e.g. ['htenkanen', 'VuokkoH', 'davewhipp']
  user_names = ['htenkanen']

  # List of exercise numbers to pull (e.g. [3], or [3,4,5] if fetching multiple)
  exercise_list = [3]

  # Additional Classroom repos (e.g. ['final-assignment'])
  additional_classroom_repos = []

  # Extra repos from the organization (not a Classroom repo, e.g. ["Grades"])
  extra_repos = [] 

  # Convert GitHub repository name to format supported by NBgrader (True | False)
  use_nbgrader_style = True
```  

### How to run?

This tool will create a folder structure that is aimed for the use of nbgrader. The structure will be organized around a root directory (which you need to specify in [git_tools_conf.py](git_tools_conf.py), which is where subfolders are going to be created according nbgrader's needs. This tool will create a folder called `submitted` which is where the student's assignments are organized and stored. 

After you have configured everything, you can run the tool from terminal or command prompt. 

Run the tool with command:

```
$ cd C:\HY-DATA\HENTENKA\KOODIT\Opetus\Geo-Python\Exercises-2018\tools
$ python pull_student_repos.py
```

## Generate feedback for students

Once, you have pulled GitHub repositories with `pull_student_repos.py`, you can autograde them using nbgrader. Notice, that most of our **exercises include also manual grading** such as checking that the students have answered to the questions, and commented their code etc. 

### How to use nbgrader automating grading?

1. From the nbgrader dashboard you will see the number of submissions (see below), and pressing that number, you will be directed to a new page where you can do the autograding for all the submissions by pressing the "lightning" -button

![](https://nbgrader.readthedocs.io/en/stable/_images/manage_assignments4.png)

2. Once you have clicked the 'autograding' button (below), nbgrader will automatically grade the exercise, and it will create a new version of the students notebook submission under `autograded` folder. E.g. `../autograded/htenkanen/Exercise-3/Exercise-3.ipynb`

    - nbgrader will also automatically collect all the exercise points of the students into a database, so you don't need to do this manually
    
![](https://nbgrader.readthedocs.io/en/stable/_images/manage_submissions1.png)

3. Typically Exercises also contain cells that require manual grading

3. Once you have done grading, it is time to give automatically feedback for the students. This can be done from command prompt with following command, in this case for Exercise-3 (you need to navigate to the root folder of your nbgrader directory):

   ``` $ nbgrader feedback "Exercise-3"```
   
   - This will create HTML files for all the student assignments and gradings into a folder `feedback`. 


