
from flask import Flask, render_template
import os

app = Flask(__name__)

@app.route('/')
def index():
    # List all files in the static/uploads directory
    problem_files = [f for f in os.listdir('static/uploads/problems') if f.endswith('.pdf')]
    solution_files = [f for f in os.listdir('static/uploads/solutions') if f.endswith('.pdf')]
    return render_template('index.html', problems=problem_files, solutions=solution_files)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
