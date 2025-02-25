import os
from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.utils import secure_filename
from app import app, db
from models import Problem, Solution, AboutContent
import logging
from functools import wraps
from werkzeug.exceptions import RequestEntityTooLarge

logging.basicConfig(level=logging.DEBUG)

ALLOWED_EXTENSIONS = {'pdf'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'is_admin' not in session:
            flash('Please log in as admin first')
            return redirect(url_for('admin_login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/admin', methods=['GET', 'POST'])
def admin_login():
    if 'is_admin' in session:
        return redirect(url_for('admin_dashboard'))

    if request.method == 'POST':
        if request.form.get('password') == app.config['ADMIN_PASSWORD']:
            session['is_admin'] = True
            flash('Successfully logged in as admin')
            return redirect(url_for('admin_dashboard'))
        flash('Invalid password')
    return render_template('admin/login.html')

@app.route('/admin/logout')
def admin_logout():
    session.pop('is_admin', None)
    flash('Logged out successfully')
    return redirect(url_for('index'))

@app.route('/admin/dashboard')
@admin_required
def admin_dashboard():
    problems = Problem.query.all()
    solutions = Solution.query.all()
    content = AboutContent.query.first()
    return render_template('admin/dashboard.html', problems=problems, solutions=solutions, content=content)

@app.route('/problems')
def problems():
    problems = Problem.query.all()
    return render_template('problems.html', problems=problems)

@app.route('/solutions')
def solutions():
    solutions = Solution.query.all()
    return render_template('solutions.html', solutions=solutions)

@app.route('/about')
def about():
    content = AboutContent.query.first()
    return render_template('about.html', content=content)

@app.route('/admin/problem/add', methods=['GET', 'POST'])
@admin_required
def add_problem():
    if request.method == 'POST':
        try:
            title = request.form['title']
            difficulty = request.form['difficulty']
            file = request.files['pdf']

            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(file_path)

                problem = Problem(
                    title=title,
                    difficulty=difficulty,
                    pdf_path=filename
                )
                db.session.add(problem)
                db.session.commit()
                flash('Problem added successfully')
                return redirect(url_for('admin_dashboard'))
            else:
                flash('Please upload a PDF file')
        except RequestEntityTooLarge:
            flash('File is too large. Maximum size is 16MB')
        except Exception as e:
            flash('Error uploading file: ' + str(e))

    return render_template('admin/add_problem.html')

@app.route('/admin/solution/add', methods=['GET', 'POST'])
@admin_required
def add_solution():
    if request.method == 'POST':
        try:
            title = request.form['title']
            problem_id = request.form['problem_id']
            file = request.files['pdf']

            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(file_path)

                solution = Solution(
                    title=title,
                    problem_id=problem_id,
                    pdf_path=filename
                )
                db.session.add(solution)
                db.session.commit()
                flash('Solution added successfully')
                return redirect(url_for('admin_dashboard'))
            else:
                flash('Please upload a PDF file')
        except RequestEntityTooLarge:
            flash('File is too large. Maximum size is 16MB')
        except Exception as e:
            flash('Error uploading file: ' + str(e))

    problems = Problem.query.all()
    return render_template('admin/add_solution.html', problems=problems)

@app.route('/admin/about/edit', methods=['GET', 'POST'])
@admin_required
def edit_about():
    content = AboutContent.query.first()
    if request.method == 'POST':
        title = request.form['title']
        content_text = request.form['content']

        if content:
            content.title = title
            content.content = content_text
        else:
            content = AboutContent(title=title, content=content_text)
            db.session.add(content)

        db.session.commit()
        flash('About content updated successfully')
        return redirect(url_for('admin_dashboard'))

    return render_template('admin/edit_about.html', content=content)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
