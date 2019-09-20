"""
edit_readme.py

For generated html feedback file, read the scores and append lines to readme file.

The tool uses the same configuration file as the other tools.
        
@author: Yijun Wang
"""

import re
import os
from graderconfig.tools_conf import base_folder, user_names, exercise_list, inspector_user_name

def read_html(path, exercise):
	
	file_path = path+"/Exercise-"+str(exercise)+".html"
	feedbackhtml = open(file_path,'r').readlines()
	rmtags = re.compile('<.*?>')
	score_dict = {'Problem 1':[]}
	scores = [line for line in feedbackhtml if '(Score:' in line]
	read_next = True
	problem = 1
	index = 1
	while (read_next):
		strip_score = re.sub(rmtags, '', scores[index]).strip().split(" ")
		if "problem_"+str(problem) in scores[index]:
			if "Problem "+str(problem) in score_dict:
				score_dict["Problem "+str(problem)].append([strip_score[-3],strip_score[-1][:-1]])
			index += 1
		else:
			problem += 1
			score_dict["Problem "+str(problem)] = []
		if index >= len(scores):
			read_next = False
	strip_total = re.sub(rmtags, '', scores[0]).strip().split(" ")
	score_dict["Exercise "+str(exercise)] = [[strip_total[-3],strip_total[-1][:-1]]]
	
	return score_dict

"""
Example:
## Grading (12.11.2018 by LY): 25/30 points for exercise 7

### Problem 1 - 4.5/5

### Problem 2 - 0/7

### Problem 3 - 0/7

### Problem 4 - 0/6

### Problem 5 - 0/5
"""
def edit_readme(path, score_dict, exercise_num):
	file_path = path+"/Readme.md"
	file = open(file_path,'a')
	total = score_dict["Exercise "+str(exercise_num)][0]
	file.write("\n##Grading (by "+ inspector_user_name+ "): "+ total[0]+ " / "+ \
		total[1]+ " points for exercise "+ str(exercise_num)+ "\n")
	for problem in score_dict:
		if "Exercise" not in problem:
			file.write("### "+problem+" - ")
			score = 0
			total = 0
			for score_list in score_dict[problem]:
				score += float(score_list[0])
				total += float(score_list[1])
			file.write(str(score)+" / "+str(total)+" \n")
	return

def main():

	# Iterate over all student's submitted repository
	for name in user_names:
		student_f = os.path.join(base_folder, "submitted/"+name)
		for exercise in exercise_list:
			ex_f = os.path.join(student_f, "Exercise-"+str(exercise))
			scores_dict = read_html(ex_f, exercise)
			edit_readme(ex_f, scores_dict, exercise)
			
if __name__ == '__main__':
    main()