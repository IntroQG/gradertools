# -*- coding: utf-8 -*-
"""
send_feedback.py

Send feedback via Slack to students automatically.

Created on Fri Sep 14 20:24:39 2018

@author: Henrikki Tenkanen
"""
from slackclient import SlackClient
import pandas as pd
import glob
import os
import time

# ===========================================
# Get parameters from the configuration files
# ===========================================
from config.tools_conf import base_folder, inspector_user_name, send_to_slack, send_to_github, student_info_file, github_username_column, name_column, slack_id_column, slack_display_name_column, generate_pdf
from config.tools_conf import user_names, exercise_list
from config.slack_conf import slack_token

def main():
    
     # Inititalize client
    sc = SlackClient(slack_token)
    
    # Read student information
    student_df = read_student_info(student_info_file)
    
    # Send feedbacks
    send_feedbacks(sc, student_df, user_names, exercise_list)

def send_feedbacks(sc, student_df, user_names, exercises):
    """Send feedback files of the exercises for students"""
    # Get information about the inspector
    inspector_slack_id, inspector_name, inspector_display_name = get_inspector_info(student_df)

    # Send feedback to user
    for user in user_names:
        if send_to_slack:
            
            # Get the Slack id for the user
            slack_id = get_slack_id(student_df, github_user_name=user)
            
            # Get the real name of the user
            student_real_name = get_real_name(student_df, user)
            
            for exercise in exercise_list:
                
                # Find the feedback pdf-file if it has been generated
                if generate_pdf:
                    pdf = get_feedback_pdf(base_dir=base_folder, exercise=exercise, user=user)
                    if len(pdf) > 1:
                        if multiple_feedback_files_ok(pdf) == 0:
                            # Send multiple files
                            for file in pdf:
                                # TODO
                                raise NotImplementedError("Sorry this does not work yet.")
                        else:
                            # Skip
                            continue
                    else:
                        print("Sending feedback for Exercise %s to %s" % (exercise, user))
                        # Get the path from the list
                        pdf_path = pdf[0]
                        
                        # Send the feed back
                        send_feedback_to_slack(client=sc, file_path=pdf_path, student_slack_id=slack_id, inspector_slack_id=inspector_slack_id, inspector_name=inspector_name, inspector_slack_name=inspector_display_name, student_name=student_real_name, exercise=exercise)    
                        
                        # Slack has rate limit of sending 1 post per second, let's exceed that
                        time.sleep(1)
                
                        # Send file to Github as well
                        if send_to_github:
                            pass

def read_student_info(student_info):
    """Reads student informatin from CSV file specified in configuration file."""
    try:
        students = pd.read_csv(student_info)
    except:
        raise ValueError("Could not read the student information!\nEnsure that you have specified in the configuration file the filepath to the CSV-file including this information.\nEnsure also that the csv-file is comma-separated (',')")
    return students    

def get_slackid_by_github_user(student_df, github_user_name):
    """Returns Slack id based on GitHub username"""
    return student_df.loc[student_df[github_username_column] == github_user_name, slack_id_column].values[0]

def get_slackid_by_student_name(student_df, student_name):
    """Returns Slack id based on GitHub username"""
    return student_df.loc[student_df[name_column] == student_name, slack_id_column].values[0]

def get_slack_id(student_df, github_user_name=None, student_name=None):
    """Get the slack id that is needed to send messages to Slack."""
    
    if github_user_name is not None:
        slack_id = get_slackid_by_github_user(student_df, github_user_name)
    elif student_name is not None:
        slack_id = get_slackid_by_student_name(student_df, student_name)
    else:
        raise ValueError("You need to pass either GitHub username or student name!")
    return slack_id

def get_display_name(student_df, github_user_name):
    """Returns the real name of the user. Be default parses only the first name."""
    return student_df.loc[student_df[github_username_column] == github_user_name, slack_display_name_column].values[0]
    
def get_real_name(student_df, github_user_name, only_first_name = True):
    """Returns the real name of the user. Be default parses only the first name."""
    if only_first_name:
        return student_df.loc[student_df[github_username_column] == github_user_name, name_column].values[0].split(' ')[0]
    else:
        return student_df.loc[student_df[github_username_column] == github_user_name, name_column].values[0]

def get_feedback_folder(base_dir, exercise, user):
    """Returns a folder for the exercise feedback"""
    fp = os.path.join(base_dir, 'feedback', user, "Exercise-%s" % exercise)
    return fp

def get_feedback_pdf(base_dir, exercise, user):
    """Finds feedback pdf-file of specified exercise for specified user."""
    # Get the feedback folder 
    feedback_dir = get_feedback_folder(base_dir, exercise, user)
    
    # Find pdf files in there
    pdf = glob.glob(os.path.join(feedback_dir, '*.pdf'))
    if len(pdf) > 0:
        return pdf
    else:
        raise ValueError("Could not find any pdf-files from the feedback folder:\n%s\n\nAre you certain that you have generated feedback and pdf-file for user %s?" % (feedback_dir, user))
        
def multiple_feedback_files_ok(pdf):
    answer = input("I found more than one feedback pdf-file (%s files).\nDo you want to proceed and send them all? ('y' or 'n')\n" % len(pdf))
    if answer == 'y':
        return 0 
    else:
        proceed = input("Do you want to quit ('y') or skip ('n')\n")
        if proceed == 'y':
            raise StopIteration("User termination")
        else:
            return 1

def send_exercise_assessment_greeting_to_slack(client, slack_id, inspector_slack_id, student_name, inspector_name, exercise, inspector_slack_name):
    """Sends a greeting to Slack before uploading the file"""
    greeting = "Hi {student_name}!\nPlease find below the feedback for your Exercise {exercise_num}.\nIf you have any questions about it, you can contact me in Slack.\n\nCheers,\n{inspector_name}\n\n(my Slack-name is `{slack_name}`)".format(
                                student_name=student_name, 
                                inspector_name=inspector_name, 
                                exercise_num=exercise, 
                                slack_name=inspector_slack_name)
    # Send the greeting
    client.api_call(
       "chat.postMessage",
       channel=slack_id, 
       user=inspector_slack_id,
       as_user=True,
       text=greeting
    )

def send_pdf_to_slack(client, file_path, slack_channel_id, title):
    """Sends pdf file to Slack Channel"""
    client.api_call(
            "files.upload",
            channels=slack_channel_id,
            file=open(file_path, 'rb'),
            filetype='pdf',
            title=title
    )

def send_feedback_to_slack(client, file_path, student_slack_id, inspector_slack_id, inspector_name, inspector_slack_name, student_name, exercise):
    """Sends greeting and feedback to Slack for the specified user."""
    # Send greeting before sending the file
    send_exercise_assessment_greeting_to_slack(client=client, slack_id=student_slack_id, inspector_slack_id=inspector_slack_id, 
                                               student_name=student_name, inspector_name=inspector_name, 
                                               exercise=exercise, inspector_slack_name=inspector_slack_name)
    
    # Title for the file
    title="Feedback for Exercise %s" % exercise
    if file_path.endswith('.pdf'):
        # Send the pdf file
        send_pdf_to_slack(client=client, file_path=file_path, slack_channel_id=student_slack_id, title=title)

def get_inspector_info(student_df):
    """Returns information about the inspector"""
    # Get the Slack id of the inspector
    inspector_slack_id = get_slack_id(student_df, github_user_name=inspector_user_name)
    
    # Get the name of inspector
    inspector_name = get_real_name(student_df, github_user_name=inspector_user_name)
    
    # Get the display name of inspector
    inspector_display_name = get_display_name(student_df, inspector_user_name)
    return (inspector_slack_id, inspector_name, inspector_display_name)

if __name__ == "__main__":
    main()