from flask import render_template, request, flash, redirect, url_for, session
from controllers.models import users_db, dept_db, project_db, task_db, image_db
from bson.objectid import ObjectId


users = users_db()
depts = dept_db()
projects = project_db()
tasks = task_db()
images = image_db()

def login_function():

    if request.method == "POST":

        username = request.form['username']
        password = request.form['password']

        if not username or not password:
            flash("Empty Fields")
            return redirect(url_for('login'))
        
        user = users.find_one({ "username" : username, "password" : password })
        
        if user:

            session['name'] = user['name']
            session['username'] = user['username']
            session['password'] = user['password']
            session['role'] = user['role']
            session['status'] = user['status']
            session['user-id'] = str(user['_id'])
            session['user-department'] = user['department']

            if user['role'] == "Admin":
                flash('Admin Login')
                return redirect(url_for('admin'))
            elif user['role'] == "Manager":
                flash('Manager Login')
                return redirect(url_for('manager'))
            elif user['role'] == "Staff":
                flash('Staff Login')
                return redirect(url_for('staff'))
            
        else:
            flash("Invalid Username or Password")
            return redirect(url_for('login'))

    return render_template("login.html")

def logout_function():
    session.clear()
    flash("Session Cleared")
    return redirect(url_for('login'))

def admin_function():
    
    if 'username' in session and session['role'] == "Admin" and session['status'] == "Enable":
       
        r_user = list(users.find())
        r_image = list(images.find())
        c_dept = list(depts.find())
        c_projects = list(projects.find())
        c_tasks = list(tasks.find())

        return render_template('admin.html', depts = c_dept, users = r_user, projects = c_projects, tasks = c_tasks, images = r_image, name = session['name'] , userid = session['user-id'])
    else:
        session.clear()
        flash("Unauthorized Access")
        return redirect(url_for('login'))
    
def manager_function():

    r_user = list(users.find())
    c_projects = list(projects.find())
    c_tasks = list(tasks.find())
    c_dept = list(depts.find())
    r_image  = list(images.find())
    
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


    if 'username' in session and session['role'] == "Manager" and session['status'] == "Enable":
        return render_template('manager.html', depts = c_dept, users = r_user, projects = c_projects, tasks = c_tasks, images = r_image, name = session['name'] , userid = session['user-id'], user_dept = session['user-department'])
    else:
        session.clear()
        flash("Unauthorized Access")
        return redirect(url_for('login'))
    
def staff_function():

    if 'username' in session and session['role'] == "Staff" and session['status'] == "Enable":
        r_image  = list(images.find())

        return render_template('staff.html',images = r_image ,name = session['name'] , userid = session['user-id'], user_dept = session['user-department'])
    else:
        session.clear()
        flash("Unauthorized Access")
        return redirect(url_for('login'))
