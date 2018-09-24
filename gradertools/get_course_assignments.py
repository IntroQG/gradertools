# -*- coding: utf-8 -*-
"""
get_course_exercise_list.py

Exercise list of the whole course in a way how nbgrader wants them.

Created on Tue Sep 18 15:04:36 2018

@author: Henrikki Tenkanen
"""


def generate_assignments(assignment_list, due_dates=None):
    """Creates assignments dictionary in a way how nbgrader wants them."""
    if due_dates is None:
        assignments = []
        for assignment in assignment_list:
            a = dict(name=assignment)
            assignments.append(a)
        return assignments
    # TODO: Figure out how due_dates should be passed
        
def create_assignments():
    from graderconfig.assignments_conf import assignments, due_dates
    
    # Generate assignments (Due dates not supported yet, needs to be None)
    return generate_assignments(assignment_list=assignments, due_dates=due_dates)
    