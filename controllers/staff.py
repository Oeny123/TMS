from flask import request, flash, redirect, url_for, session ,render_template
from controllers.models import users_db, image_db, dept_db, project_db, task_db
from bson.objectid import ObjectId
import base64
from bson import Binary
from datetime import date

users = users_db()
depts = dept_db()
projects = project_db()
tasks = task_db()
images = image_db()

def staff_open_project_function():

    if 'username' in session and session['role'] == "Staff" and session['status'] == "Enable":

        r_user = list(users.find())
        r_image = list(images.find())
        c_dept = list(depts.find())
        c_projects = list(projects.find())
        c_tasks = list(tasks.find())

        for project in projects.find():
        
            tasks_count = list(tasks.find({"project_id" : project['_id'] }))
            total_tasks = len(tasks_count)

            non_open_tasks = sum(1 for task in tasks_count if task['task_status'] != 'Open')
            
            progress = (non_open_tasks / total_tasks * 100) if total_tasks > 0 else 0

            projects.update_one(
                {'_id': project['_id']},
                {'$set': {'progress': round(progress, 2)}}
            )

        return render_template('staff/staff_open.html', depts = c_dept, users = r_user, projects = c_projects, tasks = c_tasks, images = r_image, userid = session['user-id'], user_dept = session['user-department'], name = session['name'])
    else:
        flash('Unauthorized Access')
        return redirect(url_for('login'))