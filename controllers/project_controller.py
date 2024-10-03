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
            return redirect(url_for('admin_open_project'))
        
        if projects.find_one({ "project_name" : project_name, "project_department" : project_department }):
            flash('Project already Exist')
            return redirect(url_for('admin_open_project'))
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
            return redirect(url_for('admin_open_project'))
    
def update_project_function(id):
    
    if request.method == "POST":

        project_name = request.form['project_name']
        project_department = request.form['department']
        project_status = request.form['project_status']

        if not project_name or not project_department or not project_status:
            flash('Empty Fields')
            return redirect(url_for('admin_open_project'))
        
        else:
            projects.update_one(
                {"_id": ObjectId(id)}, 
                { "$set" : {
                    "project_name" : project_name, 
                    "project_department" : project_department,
                    "project_status" : project_status
                }})
            flash('Project Updated')
            return redirect(url_for("admin_open_project"))
        

def trash_project_function(id):
    
    if request.method == "POST":
        projects.update_one(
            {"_id" : ObjectId(id)},
            {"$set" : {
                "project_status" : "Trash"
            }})
        flash('Project Moved to Trash')
        return redirect(url_for('admin_open_project'))
    

def add_task_function(id):

    if request.method == "POST":

        task_name = request.form['task_name']
        task_description = request.form['description']
        assign_to = request.form.getlist('assign[]')
        start_date = request.form['start_date']
        due_date = request.form['due_date']
        task_status = request.form['task_status']
        
        if not task_name:
            flash('Task Name Needed')
            return redirect(url_for('admin_open_project'))
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
            return redirect(url_for('admin_open_project'))


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
            return redirect(url_for('admin_open_project'))
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
            return redirect(url_for('admin_open_project'))
        

def delete_task_function(id):
    if request.method == "POST":
        tasks.delete_one({ "_id" : ObjectId(id) })
        flash("Task Deleted")
        return redirect(url_for('admin_open_project'))
    

def recover_open_function(id):
    if request.method == "POST":
        projects.update_one(
            { "_id" : ObjectId(id) },
            {"$set" : {
                "project_status" : "Open"
            }})
        flash("Project Recovered")
        return redirect(url_for('admin_trash_project'))
    
def recover_finish_function(id):
    if request.method == "POST":
        projects.update_one(
            { "_id" : ObjectId(id) },
            {"$set" : {
                "project_status" : "Finish"
            }})
        flash("Project Recovered")
        return redirect(url_for('admin_trash_project'))
    
def delete_project_funcion(id):
    if request.method == "POST":
        projects.delete_one({ "_id" : ObjectId(id) })
        flash('Project Deleted')
        tasks.delete_many({"project_id" : ObjectId(id)})
        return redirect(url_for('admin_trash_project'))