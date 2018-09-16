# -*- coding: utf-8 -*-
"""
slack_message_bot.py

Send messages to Slack workspace as user automatically.

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
        
        df = df.append([[id, team_id, name, real_name]], ignore_index=True)
        
    # Set columns
    cols = ['id', 'team_id', 'name', 'real_name']
    df.columns = cols
    return df

sc = SlackClient(slack_token)

# Get users
users = get_workspace_users(sc)

# Generate DataFrame
df = generate_slack_user_dataframe(users)



