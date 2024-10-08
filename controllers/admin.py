from flask import render_template, session, request, flash, redirect,url_for
from controllers.models import users_db, dept_db, image_db, project_db, task_db, global_notif_db, man_notif_db
from datetime import date

users = users_db()
depts = dept_db()
images = image_db()
projects = project_db()
tasks = task_db()
global_notifs = global_notif_db()
man_notifs = man_notif_db()

def admin_staff_function():

    if 'username' in session and session['role'] == "Admin" and session['status'] == "Enable":

        # r_user = list(users.find())
        c_dept = list(depts.find())
        r_images = list(images.find())
        
        search_query = request.form.get('search', '')
        if search_query:
            r_user = users.find({
            "$or": [
            {"name": {"$regex": search_query, "$options": "i"}},
            {"username": {"$regex": search_query, "$options": "i"}},
            {"password": {"$regex": search_query, "$options": "i"}},
            {"status": {"$regex": search_query, "$options": "i"}},
            {"role": {"$regex": search_query, "$options": "i"}},
            {"department": {"$regex": search_query, "$options": "i"}},
            {"date_created": {"$regex": search_query, "$options": "i"}}]})
        else:
            r_user = users.find()
            c_dept = list(depts.find())
        
        return render_template('admin/staff.html', users = r_user, depts = c_dept ,images = r_images, name = session['name'], userid = session['user-id'])
   
    else:
        flash("Unaithorized Access")
        session.clear()
        return redirect(url_for('login'))

def admin_add_user_function():

    r_user = list(users.find())
    c_dept = list(depts.find())
    r_images = list(images.find())

    if request.method == "POST":

        name = request.form['name']
        username = request.form['username']
        password = request.form['password']
        department = request.form['department']
        role = request.form['role']
        status = request.form['status']
        d_crtd = date.today().isoformat() 

        if not name or not username or not password or not department or not role or not status:
            flash('Empty Fields')
            return redirect(url_for('admin_staff'))

        if username.endswith('@gmail.com'):
            if users.find_one({"username" : username}):
                flash("Username Already Exist")
                return redirect(url_for("admin_staff"))
            else:
                users.insert_one({
                    "name" : name,
                    "username" : username,
                    "password" : password,
                    "department" : department,
                    "role" : role,
                    "status" : status,
                    "date_created" : d_crtd,
                    "date_updated" : "n/a"
                })

                flash("Account Created")
            return redirect(url_for('admin_staff'))
        else :
            flash('Invalid Email')
        
    return render_template('admin/staff.html', users = r_user, depts = c_dept ,images = r_images, name = session['name'], userid = session['user-id'])

def admin_open_projects_funtion():
    
    if 'username' in session and session['role'] == "Admin" and session['status'] == "Enable":

        c_projs = list(projects.find())
        c_tasks = list(tasks.find())
        c_depts = list(depts.find())
        r_images = list(images.find())
        r_users = list(users.find())

        for project in projects.find():
        
            tasks_count = list(tasks.find({"project_id" : project['_id'] }))
            total_tasks = len(tasks_count)

            non_open_tasks = sum(1 for task in tasks_count if task['task_status'] != 'Open')
            
            progress = (non_open_tasks / total_tasks * 100) if total_tasks > 0 else 0


            projects.update_one(
                {'_id': project['_id']},
                {'$set': {'progress': round(progress, 2)}}
            )


        return render_template('admin/open.html',users = r_users, projects = c_projs, tasks = c_tasks, depts = c_depts, images = r_images, name = session['name'], userid = session['user-id'])
    else :
        flash('Unauthorized Access')
        session.clear
        return redirect(url_for('login'))
    
def admin_finish_projects_function():
    if 'username' in session and session['role'] == "Admin" and session['status'] == "Enable":
        c_projs = list(projects.find())
        c_tasks = list(tasks.find())
        c_depts = list(depts.find())
        r_images = list(images.find())
        return render_template('admin/finish.html', projects = c_projs, tasks = c_tasks, depts = c_depts, images = r_images, name = session['name'], userid = session['user-id'])
    else :
        flash('Unauthorized Access')
        session.clear
        return redirect(url_for('login'))
    
def admin_trash_projects_function():

    if 'username' in session and session['role'] == "Admin" and session['status'] == "Enable":
        c_projs = list(projects.find())
        c_tasks = list(tasks.find())
        c_depts = list(depts.find())
        r_images = list(images.find())
        return render_template('admin/trash.html', projects = c_projs, tasks = c_tasks, depts = c_depts, images = r_images, name = session['name'], userid = session['user-id'])
    else :
        flash('Unauthorized Access')
        session.clear
        return redirect(url_for('login'))
    

def admin_notification_fnction():

    if 'username' in session and session['role'] == "Admin" and session['status'] == "Enable":
        c_projs = list(projects.find())
        c_tasks = list(tasks.find())
        c_depts = list(depts.find())
        r_users = list(users.find())
        r_images = list(images.find())
        all_notifs = list(global_notifs.find())
        mans_notifs = list(man_notifs.find())

        return render_template('admin/notif.html', images = r_images, g_notifs = all_notifs, users = r_users, man_notifs = mans_notifs, userid = session['user-id'], name = session['name'])
    else :
        flash('Unauthorized Access')
        session.clear
        return redirect(url_for('login'))