"""
edit_readme.py

For generated html feedback file, read the scores and append lines to readme file.

The tool uses the same configuration file as the other tools.
        
@author: Yijun Wang
"""

import re
import os
from graderconfig.tools_conf import base_folder, user_names, exercise_list, inspector_user_name

def read_html_ex2(path, exercise, name):
	file_path = os.path.join(path, "Exercise-"+str(exercise)+"-feedback.html")

	# Print feedback file info, student name, exercise number
	print("Getting points for user", name, "exercise", exercise)
	print(file_path)

	try:
		feedbackhtml = open(file_path,'rb').readlines()
	except FileNotFoundError:
		print("html feedback not found. Generate it for", name, "exercise", exercise)
		return {}

	# Set up regular expression to remove html tags
	rmtags = re.compile('<.*?>')
	score_dict = {}
	scores = [line.decode('ISO-8859-1') for line in feedbackhtml \
		if ('(Score:' in line.decode('ISO-8859-1'))]

	# Check whether it's able to fetch scores from html feedback
	read_next = True
	problem = 0
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

def read_html(path, exercise, name):
	file_path = os.path.join(path, "Exercise-"+str(exercise)+"-feedback.html")

	# Print feedback file info, student name, exercise number
	print("Getting points for user", name, "Exercise", exercise)
	print(file_path)

	try:
		feedbackhtml = open(file_path,'rb').readlines()
	except FileNotFoundError:
		print("html feedback not found. Generate it for", name, "exercise", exercise)
		return []

	# Set up regular expression to remove html tags
	rmtags = re.compile('<.*?>')
	score_dict = {}
	scores = [line.decode('ISO-8859-1') for line in feedbackhtml \
		if (('(Score:' in line.decode('ISO-8859-1')) & \
			('problem_' in line.decode('ISO-8859-1')))]

	# Check whether it's able to fetch scores from html feedback
	read_next = True
	problem = 0
	index = 0
	while (read_next):

		strip_score = re.sub(rmtags, '', scores[index]).strip().split(" ")
		if "problem_"+str(problem) in scores[index]:
			if "Problem "+str(problem) in score_dict:
				score_dict["Problem "+str(problem)].append([strip_score[-3],strip_score[-1][:-1]])
			else:
				score_dict["Problem "+str(problem)] = [[strip_score[-3],strip_score[-1][:-1]]]
			index += 1
		else:
			problem += 1
		if index >= len(scores) or problem > 7:
			read_next = False

	for problem in score_dict:
		score_get = 0
		score_total = 0
		for i in range(len(score_dict[problem])):
			score_get += float(score_dict[problem][i][0])
			score_total += float(score_dict[problem][i][1])
		score_dict[problem] = [str(score_get), str(score_total)]

	score_get = 0
	score_total = 0
	for problem in score_dict:
		score_get += float(score_dict[problem][0])
		score_total += float(score_dict[problem][1])
	score_dict["Exercise "+str(exercise)] = [str(score_get), str(score_total)]

	return score_dict

def edit_readme_ex2(path, score_dict, exercise_num, name):#, html_link):
	file_path = os.path.join(path,"README.md")

	# Print README.md file info
	print("Editing readme for student", name, "Exercise", exercise_num)
	print(file_path)

	file = open(file_path,'a')
	total = score_dict["Exercise "+str(exercise_num)][0]
	file.write("## Grading (by "+ inspector_user_name+ "): "+ total[0]+ " / "+ \
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
	# if html_link:
	# 	file.write("### Go to the feedback file [Exercise-"+str(exercise_num)+ \
	# 		"-feedback.html](Exercise-"+str(exercise_num)+"-feedback.html)")
	return

def edit_readme(path, score_dict, exercise_num, name):#, html_link):
	file_path = os.path.join(path,"README.md")

	# Print README.md file info
	print("Editing readme for student", name, "Exercise", exercise_num)
	print(file_path)

	# Check is already graded
	file = open(file_path, 'r')
	graded = any("## Grading (by " in line for line in file)
	if graded:
		print("This exercise is already graded. Proceed")
		return

	file = open(file_path,'a')
	total = score_dict["Exercise "+str(exercise_num)]
	file.write("## Grading (by "+ inspector_user_name+ "): "+ total[0]+ " / "+ \
		total[1]+ " points for exercise "+ str(exercise_num)+ "\n")
	for problem in score_dict:
		if "Exercise" not in problem:
			file.write("### "+problem+" - ")
			file.write(score_dict[problem][0]+" / "+score_dict[problem][1]+" \n")
	# if html_link:
	# 	file.write("### Go to the feedback file [Exercise-"+str(exercise_num)+ \
	# 		"-feedback.html](Exercise-"+str(exercise_num)+"-feedback.html)")
	return

def main():

	# Iterate over all student's feedback repository
	for name in user_names:
		# feedback_f = os.path.join(base_folder, "feedback", name)
		submitted_f = os.path.join(base_folder, "submitted", name)
		for exercise in exercise_list:
			# Whether to add html link to the README and share the file or not
			# commented out for now
			# share_html = input("Do you want to share the html feedback with the student for Exercise "\
			# 	+str(exercise)+" ? (y/n)")
			# if share_html == "n":
			# 	html_link = False
			# else:
			# 	html_link = True
			file_path = os.path.join(submitted_f, "Exercise-"+str(exercise))
			if exercise == 2:
				scores_dict = read_html_ex2(file_path, exercise, name)
				if scores_dict != {}:
					edit_readme_ex2(file_path, scores_dict, exercise, name)#, html_link)
				else:
					print("Unable to fetch scores.")
			else: 
				scores_dict = read_html(file_path, exercise, name)
				if scores_dict != []:
					edit_readme(file_path, scores_dict, exercise, name)#, html_link)
				else:
					print("Unable to fetch scores.")

if __name__ == '__main__':
    main()
