# -*- coding: utf-8 -*-
"""
get_students_of_assistant.py

Helper tool to configure nbgrader, and add students for nbgrader belonging to the assistant.

Created on Mon Sep 17 22:21:02 2018

@author: Henrikki Tenkanen
"""
from graderconfig.tools_conf import inspector_user_name, student_info_file, github_username_column,name_column, assistant_column
import pandas as pd

def get_students_of_assistant_df(user_name, student_info_file):
    """Return DataFrame of the students belonging to an assistant"""
    # Read the student info
    data = pd.read_csv(student_info_file)
    
    # Assistant column of the instructors contains the name that is used to specify for each student who is the assistant for them
    assistant_name = data.loc[data[github_username_column]==inspector_user_name, assistant_column].values[0]
    
    # Select students belonging to an assistant
    students = data.loc[data[assistant_column] == assistant_name]
    return students

def generate_student_dictionary(student_df):
    """Generates student dictionary for nbgrader"""
    students = []
    for idx, row in student_df.iterrows():
        split = row[name_column].split(' ')
        if len(split) > 1:
            fname, lname = split[0].capitalize(), split[1].capitalize()
        else:
            fname, lname = split[0].capitalize(), None
        
        student = dict(id=row[github_username_column].strip(), first_name=fname.strip(), last_name=lname.strip())
        students.append(student)
    return students

def get_course_students():
    # Get students of an assistant
    df = get_students_of_assistant_df(inspector_user_name, student_info_file)

    # Generate the student names
    students = generate_student_dictionary(df)
    return students

