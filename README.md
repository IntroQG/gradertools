# Tools for autograding

This repository contains a few scripts that helps to manage Geo-Python and AutoGIS Exercises.
This is a simplified version of the original gradertools developed by Henkka: https://github.com/geo-python/gradertools 

what is different compared with the original tool:
- folder structure (less subfolders)
- separate steps for pulling student repo and fetching exercise templates
- no printing to pdf or sending feedback via slack.

## Contents

- [Requirements](#requirements)
- [Setting up things for the first time](#setting-up-things-for-the-first-time)
- [Automate pulling repos](#automate-pulling-repos)
- [Grade student assignments](#grading-student-assignments)
  - [Autograde assignments](#grade-assignments-automatically)
  - [Grade assignment manually / modify credits from autograding](#grade-assignments-manually-or-modify-given-credits)
- [Generate feedback reports](#generate-feedback-reports)
- [Send feedback to Slack automatically](#send-feedback-reports-to-students-in-slack)

## Requirements

### Cache your GitHub credentials

These tools require that the GitHub credentials (username and password) are cached in your computer.
See directions how to do that from [here](cache_git_credentials.MD).

### Install packages.

The tools requires a few packages that needs to be installed before using them.

 - [**gitpython**](https://gitpython.readthedocs.io/en/stable/) package:

    - ```$ conda install -c conda-forge gitpython```

 - [**nbgrader**](https://nbgrader.readthedocs.io/en/stable/) is essential for automatic grading and you can install it with conda:
    *check that you get nbgrader 0.6.0!*

    - `$ conda install -c conda-forge nbgrader`


## Folder structure

TODO: Explain folder structure

## Setting up things for the first time

When doing this for the first time, you basically need to create a root folder where all the course assignments,
feedbacks etc. will be collected.

This can be for example (as set in these scripts):

 ```
 # Base folder
 C:\HY-DATA\...\Geo-Python\autograding-2019
 ```

When you have created the base folder for your exercises, you **need to clone this `gradertools` repository** into the base folder:

 ```
 $ cd C:\HY-DATA\...\Geo-Python\autograding-2019

 $ git clone https://github.com/geo-python-2019/gradertools

 ```


After you have created that folder, go into it in terminal or command line and **initilize the nbgrader for the first time** by running [init_gradertools.py](init_gradertools.py) (you only need to do this once when using the environment for the very first time!):

Navigate to folder C:\HY-DATA\...\Geo-Python\autograding-2019\gradertools that you just cloned:

 ```bash
 $ cd gradertools
 $ python init_gradertools.py
 ```

This will run some tests and initialize your grading environment. If everything is okay, the program will say that you are good to go,
otherwise it will give you hints about what you need to do, to get things working. You need to do this step only once.

After this initiliazing step, you are ready to start using the tools below (separate instructions for each of them).

## Automate pulling repos

### Overview

[gradertools/pull_student_repos.py](pull_exercise_repos.py) is a script that helps to pull multiple repositories for specified students.
It also manages everything in a way that the student repositories can be automatically graded with NBgrader. 
Compliance with NBgrader  requires a few special tricks (done automatically by the tool):

 - Student repositories will be stored in folder called `submitted`
 - The GitHub Classroom repository that is pulled will be renamed from `exercise-3-username` to `Exercise-3`
 - On Windows, the .git folder needs to be removed because it conflicts with the automatic grading 
    - this is okay, it is not needed to push any changes to the repo
    - if for some reason there is a need to push some changes to that repository, [push_changes_.py]() script can be used to do that (or doing it manually by adding a remote with git commands)

### Configuration

The tool is managed from [gradertools/graderconfig/tools_conf.py](graderconfig/tools_conf.py) file, where you can specify all the required parameters, such as:

```python

  # GitHub Organization where the exercises will be stored
  organization = "Geo-Python-2019"

  # Suffix for source repository for autograded Exercises
  autograding_suffix = "-autograding"

  # List of GitHub usernames that should be pulled (e.g. ['htenkanen', 'VuokkoH', 'davewhipp']
  user_names = ['VuokkoH', 'saratodorovic']

  # List of exercise numbers to pull (e.g. [3], or [3,4,5] if fetching multiple)
  exercise_list = [1,2]

  # Additional Classroom repos (e.g. ['final-assignment'])
  additional_classroom_repos = []

  # Extra repos from the organization (not a Classroom repo, e.g. ["Grades"])
  extra_repos = [] 

  # Convert GitHub repository name to format supported by NBgrader (True | False)
  use_nbgrader_style = True

  # Generate pdf from the feedback
  generate_pdf = False # disabled!
```  

## OLD DOCS BELOW : UPDATE!

### How to run?

This tool will create a folder structure that is aimed for the use of nbgrader. The structure will be organized around a root directory (which you need to specify in [gradertools/graderconfig/tools_conf.py](graderconfig/tools_conf.py), which is where subfolders are going to be created according nbgrader's needs. This tool will create a folder called `submitted` which is where the student's assignments are organized and stored.

After you have configured everything (see above), you can run the tool from terminal or command prompt.

Run the tool with command in the gradertools-folder:

```
$ cd C:\HY-DATA\...\Geo-Python\autograding-2019\gradertools
$ python pull_student_reposl.py
```

*Note: pull student repos pulls the student repos to subfolders in \autograding-2019\submitted\ ! Folder "submitted" is created if it does not exits*

## Grading student assignments

Once, you have pulled GitHub repositories with `pull_student_repos.py`, you can autograde them using nbgrader. Notice, that most of our **exercises include also manual grading** such as checking that the students have answered to the questions, and commented their code etc.

### Start Nbgrader

You can start nbgrader from command line. You should first navigate to the base-folder that you defined in the [initial step above](#setting-up-things-for-the-first-time).

```
$ cd C:\HY-DATA\...\Geo-Python\autograding-2019

$ jupyter notebook
```

### Grade assignments automatically

0. Open nbgrader tab:

![](https://nbgrader.readthedocs.io/en/stable/_images/formgrader_tab.png)

1. From the nbgrader dashboard you will see the number of submissions (see below), and pressing that number, you will be directed to a new page where you can do the autograding for all the submissions by pressing the "lightning" -button

![](https://nbgrader.readthedocs.io/en/stable/_images/manage_assignments4.png)

2. Once you have clicked the 'autograding' button (below), nbgrader will automatically grade the exercise, and it will create a new version of the students notebook submission under `autograded` folder. E.g. `../autograded/htenkanen/Exercise-3/Exercise-3.ipynb`

    - nbgrader will also automatically collect all the exercise points of the students into a database, so you don't need to do this manually
    
![](https://nbgrader.readthedocs.io/en/stable/_images/manage_submissions1.png)

### Grade assignments manually or modify given credits

Typically exercises also contain cells that require manual grading, or there might be situations
where you need to add comments to the students answers or code, or modify the points given by the
automatic grading system. Luckily, this is easy to do with nbgrader.

1. Typically you can see from Nbgrader dashboard information that the assignment requires manual grading:

![](img/manual-grading-needed.png)

2. If the exercise requires manual grading, you can do that by opening the **Manual Grading** -tab:

![](img/manual-grading-button.png)

3. On the following page you can see the overview of the assignments and there should also be a symbol indicating which of the
problems need manual grading (we always ask questions, so do check.). Click the link for each problem:

![](img/manual-grading-overview.png)

4. On the following page, you will see the current credits of that specific problem. Click the `Submission` button to start manual grading:

![](img/manual-grade-submission.png)

5. After this, you will land to the manual grading page, where you can manually modify credits for each task, and add comments for students codes. Giving feedback for students is important!:

![](img/change-autograding.png)

6. There are also sections that cannot be automatically graded, such as written answers to our questions. Those you need to assess yourself and give credits according the grading criteria (discuss with instructors):

![](img/grade-manually.png)

That's it! This is the basic workflow for grading the students exercises with nbgrader. "Enjoy!" :P

## Generate feedback reports

Once you have done grading, it is time to generate feedback reports for the students.
For this purpose, we have a dedicated tool [gradertools/generate_feedback.py](generate_feedback.py)
that automates the process. What this tools does:

 - It triggers nbgrader's feedback functionality, i.e. `$ nbgrader feedback ...` that produces feedback html files into `feedback` folder.
 - It collects all separate feedback html files (one for each problem), and merges them together so that we can share only 1 html with students (instead of multiple)
 - It generates pdf-report from that merged html-files that can be easily shared with students in Slack

### How to use the tool?

It is straightforward.
The tool uses by default the same settings than the `pull_student_repos.py` tool. Hence, you don't necessarily need to do any changes.
If you still need to do some changes you can configure this from [gradertools/graderconfig/tools_conf.py](graderconfig/tools_conf.py).
There is one parameter in the configuration file that is relevant for this tool, that controls the pdf building (if pdfkit does not work, you might want to disable this):

```python
# Generate pdf from the feedback (True or False)
generate_pdf = True
```

After configuring you can run the tool from command line (you need to be in the directory where the Python file is located):

```bash
$ python generate_feedback.py
```

## Send feedback reports to students in Slack

Final step after grading and generating the feedback reports, is to share those reports to students.
This can be done many ways, but as we are using Slack for communication anyways, let's distribute the feedback
via that as Slack is providing an API that fits nicely for this purpose!

[gradertools/send_feedback.py](send_feedback.py) script will automate the sending of feedbacks.
Again we control this process from configuration files as demonstrated below.

### Configuring Slack

Before you can start to use the tool, you need to create **`slack_conf.py`** configuration file in the same folder where **send_feedback.py** file is located. The file should contain the token for Slack API that makes it possible
to send messages automatically. You need to add the token to that file (ask the token from Henrikki), edit the file in following way:

```python
"""
slack_conf.py
Configuration file for Slack API.
"""

slack_token = "ReplaceThisWithCorrectSlackToken"
```

### Configuring the feedback sending procedures

There are a few parameters in configuration file and
one CSV-file ([data/Geopy_Autogis_students_with_Slack_info.csv](data/Geopy_Autogis_students_with_Slack_info.csv)) that are crucial for this tool to work.
The CSV-file contains information about the students GitHub usernames, and their Slack-userid's etc,
that are needed communicate to students.
You can configure the parameters from the [gradertools/graderconfig/tools_conf.py](graderconfig/tools_conf.py) as shown below (example).

```
# ===============================
# Exercise / Classroom parameters
# ===============================

# Inspector (the GitHub username of assistant/instructor)
inspector_user_name = 'htenkanen'

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
student_info_filename = "Geopy_Autogis_students_with_Slack_info.csv"

# You can manually specify path to 'student_info_file' below if needed. The 'gradertools/data' -folder is the default location for student information
data_dir = get_data_directory_path()
student_info_file = os.path.join(data_dir, student_info_filename)

# Required column names
github_username_column = 'Githubname'
name_column = 'Name'
slack_id_column = 'id'
slack_display_name_column = 'display_name'

```

### How to run the tool?

After configuring you can run the tool from command line (you need to be in the directory where the Python file is located):

``` $ python send_feedback.py```




