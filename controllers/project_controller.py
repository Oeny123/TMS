from flask import request, flash, redirect, url_for, session
from controllers.models import project_db, task_db
from bson.objectid import ObjectId
projects = project_db()
tasks = task_db()

def add_project_function():
    
    if request.method == "POST":
        
        project_name = request.form['project_name']
        project_department = request.form['department']
        project_description = request.form['description']
        
        if not project_name or not project_department:
            flash('Empty Fields')
            if session['role'] == "Admin":
                return redirect(url_for('admin_open_project'))
            elif session['role'] == "Manager":
                return redirect(url_for('man_open_proj'))
        
        if projects.find_one({ "project_name" : project_name, "project_department" : project_department }):
            flash('Project already Exist')
            if session['role'] == "Admin":
                return redirect(url_for('admin_open_project'))
            elif session['role'] == "Manager":
                return redirect(url_for('man_open_proj'))
        else:
            projects.insert_one({
                "project_name" : project_name, 
                "project_description" : project_description,
                "project_department" : project_department,
                "project_creator" : session['name'],
                "progress" : 0,
                "project_status" : "Open"
            })
            flash('Project Created for ' + project_department)
            if session['role'] == "Admin":
                return redirect(url_for('admin_open_project'))
            elif session['role'] == "Manager":
                return redirect(url_for('man_open_proj'))
            

def update_project_function(id):
    
    if request.method == "POST":

        project_name = request.form['project_name']
        project_department = request.form['department']
        project_status = request.form['project_status']

        if not project_name or not project_department or not project_status:
            flash('Empty Fields')
            if session['role'] == "Admin":
                return redirect(url_for('admin_open_project'))
            elif session['role'] == "Manager":
                return redirect(url_for('man_open_proj'))
        else:
            projects.update_one(
                {"_id": ObjectId(id)}, 
                { "$set" : {
                    "project_name" : project_name, 
                    "project_department" : project_department,
                    "project_status" : project_status
                }})
            flash('Project Updated')
            if session['role'] == "Admin":
                return redirect(url_for('admin_open_project'))
            elif session['role'] == "Manager":
                return redirect(url_for('man_open_proj'))

def trash_project_function(id):
    
    if request.method == "POST":
        projects.update_one(
            {"_id" : ObjectId(id)},
            {"$set" : {
                "project_status" : "Trash"
            }})
        flash('Project Moved to Trash')
        if session['role'] == "Admin":
            return redirect(url_for('admin_open_project'))
        elif session['role'] == "Manager":
            return redirect(url_for('man_open_proj'))

def add_task_function(id):

    if request.method == "POST":

        task_name = request.form['task_name']
        task_description = request.form['description']
        assign_to = request.form.getlist('assign[]')
        start_date = request.form['start_date']
        due_date = request.form['due_date']
        task_status = request.form['task_status']
        
        if not task_name or not assign_to:
            flash('Task Name and Asignee Needed')
            if session['role'] == "Admin":
                return redirect(url_for('admin_open_project'))
            elif session['role'] == "Manager":
                return redirect(url_for('man_open_proj'))
            elif session['role'] == "Staff":
                return redirect(url_for('staff_open_proj'))
        else:
            tasks.insert_one({
                "task_name" : task_name,
                "task_description" : task_description,
                "task_creator" : session['name'],
                "start_date" : start_date,
                "due_date" : due_date,
                "task_status" : task_status,
                "project_id" : ObjectId(id),
                "assigned_to" : assign_to 
            })
            flash('Task Added')
            if session['role'] == "Admin":
                return redirect(url_for('admin_open_project'))
            elif session['role'] == "Manager":
                return redirect(url_for('man_open_proj'))
            elif session['role'] == "Staff":
                return redirect(url_for('staff_open_proj'))

def edit_task_function(id):

    if request.method == "POST":

        task_name = request.form['new_task_name']
        task_description = request.form['new_description']
        assign_to = request.form.getlist('new_assign[]')
        start_date = request.form['new_start_date']
        due_date = request.form['new_due_date']
        task_status = request.form['new_task_status']

        if not task_name:
            flash('Task Name Needed')
            if session['role'] == "Admin":
                return redirect(url_for('admin_open_project'))
            elif session['role'] == "Manager":
                return redirect(url_for('man_open_proj'))
        else:
            tasks.update_one(
                {"_id" : ObjectId(id)}, 
                {"$set": {
                    "task_name" : task_name,
                    "task_description" : task_description,
                    "start_date" : start_date,
                    "due_date" : due_date,
                    "task_status" : task_status,
                    "assigned_to" : assign_to 
                }})
            flash("Task Updated")
            if session['role'] == "Admin":
                return redirect(url_for('admin_open_project'))
            elif session['role'] == "Manager":
                return redirect(url_for('man_open_proj'))
        

def delete_task_function(id):
    if request.method == "POST":
        tasks.delete_one({ "_id" : ObjectId(id) })
        flash("Task Deleted")
        if session['role'] == "Admin":
            return redirect(url_for('admin_open_project'))
        elif session['role'] == "Manager":
            return redirect(url_for('man_open_proj'))

def recover_open_function(id):
    if request.method == "POST":
        projects.update_one(
            { "_id" : ObjectId(id) },
            {"$set" : {
                "project_status" : "Open"
            }})
        flash("Project Recovered")
        if session['role'] == "Admin":
            return redirect(url_for('admin_open_project'))
        elif session['role'] == "Manager":
            return redirect(url_for('man_open_proj'))
        
def recover_finish_function(id):
    if request.method == "POST":
        projects.update_one(
            { "_id" : ObjectId(id) },
            {"$set" : {
                "project_status" : "Finish"
            }})
        flash("Project Recovered")
        if session['role'] == "Admin":
            return redirect(url_for('admin_open_project'))
        elif session['role'] == "Manager":
            return redirect(url_for('man_open_proj'))
    
def delete_project_funcion(id):
    if request.method == "POST":
        projects.delete_one({ "_id" : ObjectId(id) })
        flash('Project Deleted')
        tasks.delete_many({"project_id" : ObjectId(id)})
        if session['role'] == "Admin":
            return redirect(url_for('admin_open_project'))
        elif session['role'] == "Manager":
            return redirect(url_for('man_open_proj'))