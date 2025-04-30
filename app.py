from flask import Flask, render_template
import os
import re

app = Flask(__name__)

def extract_week_number(filename):
    match = re.search(r'Week_(\d+)', filename)
    return int(match.group(1)) if match else float('inf')

@app.route('/')
def index():
    problem_files = sorted(
        [f for f in os.listdir('static/uploads/problems') if f.endswith('.pdf')],
        key=extract_week_number
    )
    solution_files = sorted(
        [f for f in os.listdir('static/uploads/solutions') if f.endswith('.pdf')],
        key=extract_week_number
    )
    return render_template('index.html', problems=problem_files, solutions=solution_files)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/problems')
def problems():
    problem_files = sorted(
        [f for f in os.listdir('static/uploads/problems') if f.endswith('.pdf')],
        key=extract_week_number
    )
    return render_template('problems.html', problems=problem_files)

@app.route('/solutions')
def solutions():
    solution_files = sorted(
        [f for f in os.listdir('static/uploads/solutions') if f.endswith('.pdf')],
        key=extract_week_number
    )
    return render_template('solutions.html', solutions=solution_files)
