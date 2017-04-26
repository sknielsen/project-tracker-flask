"""A web application for tracking projects, students, and student grades."""

from flask import Flask, request, render_template

import hackbright

app = Flask(__name__)


@app.route('/')
def show_projects_students():
    """Shows list of students and list of projects"""

    students = hackbright.get_all_students()
    projects = hackbright.get_all_projects()
    return render_template('homepage.html', students=students, projects=projects)


@app.route("/student")
def get_student():
    """Show information about a student."""

    github = request.args.get('github')

    first, last, github = hackbright.get_student_by_github(github)
    grades = hackbright.get_grades_for_student(github)
    print grades
    html = render_template("student_info.html",
                           first=first,
                           last=last,
                           github=github,
                           grades=grades)
    return html

@app.route("/student-search")
def get_student_form():
    """Show form for searching for a student."""

    return render_template("student_search.html")

@app.route("/student-add")
def add_student():
    """ Show form for adding new student."""

    return render_template("student_add.html")


@app.route("/student-success", methods=["POST"])
def confirm_add():
    """ Acknowledge new student was added."""

    first_name = request.form.get('firstname')
    last_name = request.form.get('lastname')
    github = request.form.get('github')

    hackbright.make_new_student(first_name, last_name, github)
    return render_template('student_success.html', first=first_name, last=last_name, github=github)


@app.route("/project")
def show_project_details():
    """Shows details for project"""

    title = request.args.get('title')

    project_info = hackbright.get_project_by_title(title)
    description = project_info[2]
    grade = project_info[3]
    grades = hackbright.get_grades_by_title(title)

    return render_template('project_info.html', title=title, description=description, grade=grade, grades=grades)


@app.route("/project-add")
def add_project():
    """ Show form for adding new project"""

    return render_template('project_add.html')


@app.route('/project-success', methods=["POST"])
def confirm_project_add():
    """ Acknowledge new project was added"""

    title = request.form.get('title')
    description = request.form.get('description')
    grade = request.form.get('grade')

    hackbright.add_new_project(title, description, grade)

    return render_template("project_success.html", title=title)
if __name__ == "__main__":
    hackbright.connect_to_db(app)
    app.run(debug=True)
