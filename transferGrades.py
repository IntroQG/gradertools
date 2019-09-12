import pandas as pd
from nbgrader.api import Gradebook, MissingEntry

exerciseNumber='4'
old_grades= pd.read_csv('../data/Geopy_Autogis_students.csv')
outputFilePath='../data/Geopy_Autogis_students.csv'
gradebookDatabase= 'sqlite:///../../gradebook.db'


def transferGrades(exerciseNumber, old_grades_csv,gradebookDabase, outputFilePath):
    exerciseNumber=str(exerciseNumber)
    with Gradebook(gradebookDatabase) as gb:
        missingScoreStudent=''
        for assignment in gb.assignments:
            if assignment.name=='Exercise-'+ exerciseNumber:
                for student in gb.students:
                    try:
                        submission = gb.find_submission(assignment.name, student.id)
                    except MissingEntry:
                        missingScoreStudent+=(str(student.id) + ', ')
                    else:
                        old_grades_csv.loc[(old_grades_csv['Githubname']==student.id), 'Ex'+exerciseNumber]=submission.score
                    old_grades_csv.to_csv(outputFilePath)
        print('You have not graded the following students: ' + missingScoreStudent)


transferGrades(exerciseNumber, old_grades, gradebookDatabase,outputFilePath)