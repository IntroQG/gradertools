# -*- coding: utf-8 -*-
"""
get_slack_users.py

Script to collect user information from Slack users in the workspace. 
Needed for automatic communication between teachers and students.
Uses Slack API. 

Created on Fri Sep 14 20:24:39 2018

@author: Henrikki Tenkanen
"""
from slackclient import SlackClient
from slack_conf import slack_token
import pandas as pd

def get_workspace_users(client):
    """Returns info about the users of a workspace."""
    return client.api_call("users.list")

def generate_slack_user_dataframe(users):
    """Generates a Pandas DataFrame from the users"""
    df = pd.DataFrame()

    # Generate table of the users
    for user in users['members']:
        id = user['id']
        team_id = user['team_id']
        name = user['name']
        real_name = user['real_name']
        display_name = user['profile']['display_name']
        
        df = df.append([[id, team_id, name, real_name, display_name]], ignore_index=True)
        
    # Set columns
    cols = ['id', 'team_id', 'name', 'real_name', 'display_name']
    df.columns = cols
    return df

sc = SlackClient(slack_token)

# Get users
users = get_workspace_users(sc)

# Generate DataFrame
df = generate_slack_user_dataframe(users)

# Save
outfp = r"C:\HY-DATA\HENTENKA\KOODIT\Opetus\Geo-Python\Exercises-2018\tools\data\Geopy_Autogis_students_with_Slack_info.csv"
df.to_csv(outfp, index=False, encoding='latin1')

