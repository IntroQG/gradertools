# -*- coding: utf-8 -*-
"""
generate_feedback.py

Generates nbgrader feedback html file for the specified exercise. 
If the exercise has been divided into multiple notebooks, this tool will merge the feedback html files into one.
Optionally, the tool converts the merged html file into a pdf which is easy to send for students.

The tool uses the same configuration file as the other tools.

Requirements:
    
    
    - nbgrader:
        
        conda install -c conda-forge nbgrader
    
    - jinja:
        
        conda install -c conda-forge jinja2 
        
    - python-pdfkit package: 
        
        pip install pdfkit
        
Created on Sat Sep 15 21:45:53 2018

@author: Henrikki Tenkanen
"""
import os
import subprocess
from config.tools_conf import base_folder, user_names, exercise_list, generate_pdf
import glob
import shutil
from jinja2 import Environment, PackageLoader, Template

def generate_feedback(base_folder, exercise_number):
    """Generates feedback for specified exercise"""
    # Generate the feedback
    subprocess.call(['nbgrader', 'feedback', 'Exercise-%s' % exercise_number], cwd=base_folder)
    print("Generated feedback for Exercise %s" % exercise_number)
    
def convert_html_to_pdf(html_fp, output_pdf_fp):
    """Converts Html file to pdf"""
    import pdfkit
    options = {
    'page-size': 'A4',
    'margin-top': '0.0in',
    'margin-right': '0.0in',
    'margin-bottom': '0.0in',
    'margin-left': '0.0in',
    'encoding': "UTF-8",
    'custom-header' : [
        ('Accept-Encoding', 'gzip')
    ],
    'cookie': [
        ('cookie-name1', 'cookie-value1'),
        ('cookie-name2', 'cookie-value2'),
    ],
    'no-outline': None
    }
    print("Generating pdf ...")
    # Convert to pdf
    pdfkit.from_file(html_fp, output_pdf_fp, options=options)
    print("Generated pdf: %s" % output_pdf_fp)

def bn(path):
    """Return basename of a file"""
    if path:
        return os.path.basename(path)
    else:
        return None

def merge_feedback_htmls(html_files, exercise_number, user):
    """Merges feedback html files together so that it is easier to share feedback with students."""
        
    # If 'feedback' file has been already created, skip that one to regenerate feedback
    hf = [fp for fp in html_files if not "feedback" in os.path.basename(fp)]
    
    # Specify the files
    if len(hf) == 5:
        p1, p2, p3, p4, p5 = hf[0], hf[1], hf[2], hf[3], hf[4]
    elif len(hf) == 4:
        p1, p2, p3, p4, p5 = hf[0], hf[1], hf[2], hf[3], None
    elif len(hf) == 3:
        p1, p2, p3, p4, p5 = hf[0], hf[1], hf[2], None, None
    elif len(hf) == 2:
        p1, p2, p3, p4, p5 = hf[0], hf[1], None, None, None
    elif len(hf) == 1:
        p1, p2, p3, p4, p5 = hf[0], None, None, None, None
    else:
        raise ValueError("No Html files were found. Check that the feedback files exist!")
   
    env = Environment(loader=PackageLoader('mergehtml'))
    template = env.get_template('index.html')
    
    # Copy files on the same folder as the template (and remove them afterwords)
    removable_temp_files = []
    for fp in hf:
        target_fp = os.path.join(os.path.dirname(template.filename), os.path.basename(fp))
        shutil.copy(fp, target_fp)
        removable_temp_files.append(target_fp)
    merged_html = template.render(file1=bn(p1), file2=bn(p2), file3=bn(p3), file4=bn(p4), file5=bn(p5))
    
    # Produce output filepath
    output_fp = os.path.join(os.path.dirname(hf[0]), "Exercise-%s-%s-feedback.html" % (exercise_number, user))
    
    with open(output_fp, 'w') as fh:
        fh.write(merged_html)
        
    # Finally remove the copied files
    for fp in removable_temp_files:
        os.remove(fp)
        
    print("Merged feedback to: %s" % os.path.basename(output_fp))
    return output_fp
  
def get_user_feedback_files(base_folder, exercise_number, user):
    """Collects all exercise feedback html files"""
    tmp = os.path.join(base_folder, 'feedback', user, "Exercise-%s" % exercise_number,"Exercise-%s*.html" % exercise_number)
    files = glob.glob(tmp)
    return files
    

def main(base_folder, user_names, exercise_list, generate_pdf):
    """Main for running the tool"""

    # Generate the feedback html files 
    for exercise_num in exercise_list:
        
        # Generate feedback 
        generate_feedback(base_folder, exercise_num)
        
        # Merge feedback html files 
        for user in user_names:

            # Get the filepaths for feedback html files
            files = get_user_feedback_files(base_folder, exercise_num, user)
            
            # Merge feedback html files into one
            merged_html_fp = merge_feedback_htmls(files, exercise_num, user)
            
            if generate_pdf:
                convert_html_to_pdf(html_fp=merged_html_fp, output_pdf_fp=merged_html_fp.replace('.html', '.pdf'))
        
if __name__ == "__main__":
    main(base_folder, user_names, exercise_list, generate_pdf)
