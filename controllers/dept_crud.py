from flask import request, redirect, url_for, flash, session
from controllers.models import dept_db,  project_db, task_db
from bson.objectid import ObjectId

depts = dept_db()
projects = project_db()
tasks = task_db()

def create_dept_function():

    if request.method == "POST":

        department = request.form['department']

        if not department:
            flash('Empty Field')
            return redirect(url_for('admin'))
        else:
            depts.insert_one({
                "dept" : department,
                "dept_craetor" : session['name']
            })
            flash('New Department Created')
            return redirect(url_for('admin'))
    
def delete_dept_function(id, dept):

    c_projects = list(projects.find())

    if request.method == "POST":

        depts.delete_one({
            "_id" : ObjectId(id)
        })
        
        projects.delete_many({
            "project_department" : dept
        })

        for project in c_projects:
            if project['_id'] ==  dept:
                tasks.delete_many({
                    "project_id" : project['id']
                })


        flash('Department Deleted')
        return redirect(url_for('admin'))
