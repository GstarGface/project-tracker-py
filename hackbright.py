"""Hackbright Project Tracker.

A front-end for a database that allows users to work with students, class
projects, and the grades students receive in class projects.
"""

import sqlite3

db_connection = sqlite3.connect("hackbright.db", check_same_thread=False)
db_cursor = db_connection.cursor()


def get_student_by_github(github):
    """Given a github account name, print information about the matching student."""

    QUERY = """
        SELECT first_name, last_name, github
        FROM Students
        WHERE github = ?
        """
    db_cursor.execute(QUERY, (github,))
    row = db_cursor.fetchone()

    print "Student: %s %s\nGithub account: %s" % (
        row[0], row[1], row[2])


def make_new_student(first_name, last_name, github):
    """Add a new student and print confirmation.
    Given a first name, last name, and GitHub account, add student to the
    database and print a confirmation message.
    """

    QUERY = """INSERT INTO Students VALUES (?, ?, ?)"""
    db_cursor.execute(QUERY, (first_name, last_name, github))

    db_connection.commit()
    print "Successfully added student: %s %s" % (first_name, last_name)


def get_project_by_title(title):
    """Given a project title, print information about the project."""
    
    QUERY = """
        SELECT title, description, max_grade, id
        FROM Projects
        WHERE title = ?
        """

    db_cursor.execute(QUERY, (title,))
    row = db_cursor.fetchone()
    title, description, max_grade, project_id = row #unpacked row

    print "Project ID: %s \n Project Title: %s \n Description: %s \n Maximum Grade: %s" % (project_id, title, description, max_grade)


def get_grade_by_github_title(github, title):
    """Print grade student received for a project."""
    
    QUERY = """
            SELECT first_name, last_name, github, grade, project_title
            FROM Students
            JOIN Grades ON Students.github = Grades.student_github
            WHERE github = ? AND project_title = ?
            """

    db_cursor.execute(QUERY, (github, title))
    row = db_cursor.fetchone()
    print "Student %s %s (github: %s) received a grade of %s on the %s project." % (row[0], row[1], row[2], row[3], row[4])

def assign_grade(github, title, grade):
    """Assign a student a grade on an assignment and print a confirmation."""
    
    QUERY = """INSERT INTO Grades VALUES (?, ?, ?)"""
    db_cursor.execute(QUERY, (github, title, grade))

    db_connection.commit()
    print "Successfully added grade of %s for %s on the project %s." % (grade, github, title)


def handle_input():
    """Main loop.

    Repeatedly prompt for commands, performing them, until 'quit' is received as a
    command."""

    command = None # setting command equal to None enables the while loop to access the DB until we enter quit

    while command != "quit":
        input_string = raw_input("HBA Database> ")
        tokens = input_string.split()
        command = tokens[0]
        args = tokens[1:]

        if command == "student":
            github = args[0]
            get_student_by_github(github)

        elif command == "new_student":
            first_name, last_name, github = args   # unpacked!
            make_new_student(first_name, last_name, github)

        elif command == "project_title":
            title = args[0]
            get_project_by_title(title)

        elif command == "project_grade":
            github = args[0]
            title = args[1]
            get_grade_by_github_title(github, title)

        elif command == "new_grade":
            github, title, grade = args
            assign_grade(github, title, grade)

if __name__ == "__main__":
    handle_input()

    # To be tidy, we'll close our database connection -- though, since this
    # is where our program ends, we'd quit anyway.

    db_connection.close()
