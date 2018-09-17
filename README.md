# Tools

This repository contains a few scripts that helps to manage Geo-Python and AutoGIS Exercises.

## Contents

- [Automate pulling repos](#automate-pulling-repos)
- [Grade student assignments](#grading-student-assignments)
  - [Autograde assignments](#grade-assignments-automatically)
  - [Grade assignment manually / modify credits from autograding](#grade-assignments-manually-or-modify-given-credits)
- [Generate feedback reports](#generate-feedback-reports)
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

## Grading student assignments

Once, you have pulled GitHub repositories with `pull_student_repos.py`, you can autograde them using nbgrader. Notice, that most of our **exercises include also manual grading** such as checking that the students have answered to the questions, and commented their code etc.

### Requirements

This part requires nbgrader to be installed:

 - `$ conda install -c conda-forge nbgrader`

### Grade assignments automatically

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
For this purpose, we have a dedicated tool [generate_feedback.py](generate_feedback.py)
that automates the process. What this tools does:

 - It triggers nbgrader's feedback functionality, i.e. `$ nbgrader feedback ...` that produces feedback html files into `feedback` folder.
 - It collects all separate feedback html files (one for each problem), and merges them together so that we can share only 1 html with students (instead of multiple)
 - It generates pdf-report from that merged html-files that can be easily shared with students in Slack

### Requirements

This tool requires following packages:

 - nbgrader:

    - `conda install -c conda-forge nbgrader`

 - jinja2 (merges html files), should come with Anaconda but if not, install:

    - `conda install -c conda-forge jinja2`

 - python-pdfkit package:

    - Windows:

       - `pip install pdfkit`
       - You also need to install *Wkhtmltppdf* package before pdfkit starts working (complicated, but let's live with this for now):
          - [download page](https://wkhtmltopdf.org/downloads.html)
          - After installing *wkhtmltopdf*, you need to add the `bin/` folder to system environment path (ask help if you don't know how)

### How to use the tool?

It is straightforward. All you need to do is to configure the tool from [git_tools_conf.py](git_tools_conf.py).
It uses by default the same settings than the `pull_student_repos.py` tool. Hence, you don't necessarily need to do any changes.
There is one parameter in the configuration file that is relevant for this tool, that controls the pdf building (if pdfkit does not work, you might want to disable this):

```python
# Generate pdf from the feedback (True or False)
generate_pdf = True
```

## Send feedback reports to students in Slack

Final step after grading and generating the feedback reports, is to share those reports to students.
This can be done many ways, but as we are using Slack for communication anyways, let's distribute the feedback
via that as Slack is providing an API that fits nicely for this purpose!

[send_feedback.py](send_feedback.py) script will automate the sending of feedbacks.
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
You can configure the parameters from the [git_tools_conf.py](git_tools_conf.py) as shown below (example).

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
student_info_file = r"C:\HY-DATA\HENTENKA\KOODIT\Opetus\Geo-Python\Exercises-2018\tools\data\Geopy_Autogis_students_with_Slack_info.csv"

# Required column names
github_username_column = 'Githubname'
name_column = 'Name'
slack_id_column = 'id'
slack_display_name_column = 'display_name'

```





