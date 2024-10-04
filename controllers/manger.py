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

def man_edit_account_function(id):
    
    if request.method == "POST":

        name = request.form['name']
        username = request.form['username']
        password = request.form['password']
        department = request.form['department']
        role = request.form['role']
        status = request.form['status']
        d_up = date.today().isoformat()

        if users.find_one({"username" : username}):
            flash("Username must be Changed")
            return redirect(url_for("manager"))
        else:
            users.update_one(
                {"_id" : ObjectId(id)}, 
                {"$set": {
                       "name" : name,
                        "username" : username,
                        "password" : password,
                        "department" : department,
                        "role" : role,
                        "status" : status,
                        "date_updated" : d_up
                }})
            flash("Account Updated")
            return redirect(url_for('manager'))
    else:
        flash('Invalid Actions')
        return redirect(url_for('manager'))

def man_delete_user_account(id):

    if request.method == "POST":

        users.delete_one({"_id" : ObjectId(id)})
        images.delete_many({"user_id" : ObjectId(id)})

        flash('Account Deleted')
        return redirect(url_for('manager'))
    
def man_account_image_function(id):
    
    image = request.files['image']

    if not image:
        flash('No Image was Uploaded')
        return redirect(url_for('manager'))

    if image:
        image_data = image.read()
        encoded_image = base64.b64encode(image_data).decode('utf-8')
   
        if images.find_one({"user_id": ObjectId(id) }):
            images.update_one(
                {"user_id" : ObjectId(id)},
                {"$set": {
                    'name': image.filename,
                    'image': encoded_image,
                    "user_id" : ObjectId(id)
                }})
            flash("Profile Uploaded")
        else:    
            images.insert_one({
                'name': image.filename,
                'image': encoded_image,
                "user_id" : ObjectId(id)
            })
            flash("Images Updated")

    if session['role'] == "Manager":
        return redirect(url_for('manager'))
    elif session['role'] == "Staff":
        return redirect(url_for('staff'))


def man_remove_image_function(id):

    if request.method == "POST":
        
        images.delete_one({"user_id" : ObjectId(id)})
        flash("Profile Removed")
        if session['role'] == "Manager":
            return redirect(url_for('manager'))
        elif session['role'] == "Staff":
            return redirect(url_for('staff'))
            
    
def man_open_proj_funtion():

    r_user = list(users.find())
    r_image = list(images.find())
    c_dept = list(depts.find())
    c_projects = list(projects.find())
    c_tasks = list(tasks.find())

    if 'username' in session and session['role'] == "Manager" and session['status'] == "Enable":
        
        for project in projects.find():
        
            tasks_count = list(tasks.find({"project_id" : project['_id'] }))
            total_tasks = len(tasks_count)

            non_open_tasks = sum(1 for task in tasks_count if task['task_status'] != 'Open')
            
            progress = (non_open_tasks / total_tasks * 100) if total_tasks > 0 else 0   

            projects.update_one(
                {'_id': project['_id']},
                {'$set': {'progress': round(progress, 2)}}
            )
        
        return render_template('manager/man_open.html', depts = c_dept, users = r_user, projects = c_projects, tasks = c_tasks, images = r_image, name = session['name'] , userid = session['user-id'], user_dept = session['user-department'])
    else:
        session.clear()
        flash("Unauthorized Access")
        return redirect(url_for('login'))
    
def man_finish_proj_funtion():

    r_user = list(users.find())
    r_image = list(images.find())
    c_dept = list(depts.find())
    c_projects = list(projects.find())
    c_tasks = list(tasks.find())

    if 'username' in session and session['role'] == "Manager" and session['status'] == "Enable":
        return render_template('manager/man_finish.html', depts = c_dept, users = r_user, projects = c_projects, tasks = c_tasks, images = r_image, name = session['name'] , userid = session['user-id'], user_dept = session['user-department'])
    else:
        session.clear()
        flash("Unauthorized Access")
        return redirect(url_for('login'))
    
def man_trash_proj_funtion():

    if 'username' in session and session['role'] == "Manager" and session['status'] == "Enable":

        c_projs = list(projects.find())
        c_tasks = list(tasks.find())
        c_depts = list(depts.find())
        r_images = list(images.find())
        return render_template('manager/man_trash.html', projects = c_projs, tasks = c_tasks, depts = c_depts, images = r_images, name = session['name'], userid = session['user-id'], user_dept = session['user-department'])
    
    else :
        flash('Unauthorized Access')
        session.clear
        return redirect(url_for('login'))