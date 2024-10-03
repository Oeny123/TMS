from flask import Flask
from controllers.user_controller import login_function, logout_function, admin_function, manager_function, staff_function 
from controllers.acount_crud import edit_account_function, delete_user_account, account_image_function, remove_image_function, account_setting_update_info_function, admin_setting_image_function, admin_remove_image_function
from controllers.admin import admin_staff_function, admin_open_projects_funtion, admin_finish_projects_function, admin_trash_projects_function, admin_add_user_function
from controllers.project_controller import add_project_function, update_project_function, trash_project_function, add_task_function, edit_task_function, delete_task_function, recover_open_function, recover_finish_function, delete_project_funcion
from controllers.dept_crud import create_dept_function, delete_dept_function
import secrets
    
app = Flask(__name__)
app.secret_key = secrets.token_hex(32)


# login
@app.route('/', methods=['GET','POST'])
def login():
    return login_function()


# user routes  ============================================================================
@app.route('/admin')
def admin():
    return admin_function()

@app.route('/manager')
def manager():
    return manager_function()

@app.route('/staff')
def staff():
    return staff_function()

@app.route('/logout')
def logout():
    return logout_function()


# Admin pages / routes  ============================================================================
@app.route('/admin-staff', methods=['GET', 'POST'])
def admin_staff():
    return admin_staff_function()

@app.route('/admin-add-user', methods=['GET','POST'])
def admin_add_user():
    return admin_add_user_function()

@app.route('/admin-open-project', methods=['GET','POST'])
def admin_open_project():
    return admin_open_projects_funtion()

@app.route('/admin-finish-project', methods=['GET','POST'])
def admin_finish_project():
    return admin_finish_projects_function()

@app.route('/admin-trash-project', methods=['GET','POST'])
def admin_trash_project():
    return admin_trash_projects_function()


# Account Crud ============================================================================
@app.route('/edit-account/<id>', methods=['GET', 'POST'])
def edit_account(id):
    return edit_account_function(id)

@app.route('/delte-account/<id>', methods=['GET', 'POST'])
def delete_account(id):
    return delete_user_account(id)

@app.route('/acc-image/<id>', methods=['GET', 'POST'])
def acc_image(id):
    return account_image_function(id)

@app.route('/rem-pfp/<id>', methods=['GET','POST'])
def rem_acc(id):
    return remove_image_function(id)

@app.route('/account-update/<id>', methods=['GET','POST'])
def account_setting_update(id):
    return account_setting_update_info_function(id)

@app.route('/admin-setting-image/<id>', methods=['GET','POST'])
def admin_setting_account(id):
    return admin_setting_image_function(id)

@app.route('/admin-remove-image/<id>', methods=['GET','POST'])
def admin_remove_image(id):
    return admin_remove_image_function(id)

# Project Crud  ============================================================================
@app.route('/add-project', methods=['GET','POST'])
def add_project():
    return add_project_function()

@app.route('/update-project/<id>', methods=['GET','POST'])
def update_project(id):
    return update_project_function(id)

@app.route('/trash-project/<id>', methods=['GET','POST'])
def trash_project(id):
    return trash_project_function(id)

@app.route('/recover-to-open/<id>', methods=['GET','POST'])
def recover_open(id):
    return recover_open_function(id)

@app.route('/recover-to-finish/<id>', methods=['GET','POST'])
def recover_finish(id):
    return recover_finish_function(id)

@app.route('/delete_project/<id>', methods=['GET', 'POST'])
def delete_project(id):
    return delete_project_funcion(id)

# Task Crud
@app.route('/add-task/<id>', methods=['GET','POST'])
def add_task(id):
    return add_task_function(id)

@app.route('/edit-task/<id>', methods=['GET','POST'])
def edit_task(id):
    return edit_task_function(id)

@app.route('/delete-tasl/<id>', methods=['GET','POST'])
def delete_task(id):
    return delete_task_function(id)

# Departmetn ========================================================

@app.route('/create-department', methods=['GET','POST'])
def create_dept():
    return create_dept_function()

@app.route('/delete-department/<id>/<dept>', methods=['GET','POST'])
def delete_dept(id, dept):
    return delete_dept_function(id, dept)

if __name__ == "__main__":
    app.run(debug=True)