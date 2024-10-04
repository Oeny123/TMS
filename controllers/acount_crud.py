from flask import request, flash, redirect, url_for, session
from controllers.models import users_db, image_db
from bson.objectid import ObjectId
import base64
from bson import Binary
from datetime import date

users = users_db()
images= image_db()

def edit_account_function(id):
    
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
            return redirect(url_for("admin_staff"))
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
            if session['role'] == "Admin":
                return redirect(url_for('admin_open_project'))
            elif session['role'] == "Manager":
                return redirect(url_for('man_open_proj'))

    else:
        flash('Invalid Actions')
        return redirect(url_for('admin_staff'))

def delete_user_account(id):

    if request.method == "POST":

        users.delete_one({"_id" : ObjectId(id)})
        images.delete_many({"user_id" : ObjectId(id)})

        flash('Account Deleted')
        return redirect(url_for('admin_staff'))


def account_image_function(id):
    
    image = request.files['image']

    if not image:
        flash('No Image was Uploaded')
        return redirect(url_for('admin_staff'))

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

    return redirect(url_for('admin_staff'))

def remove_image_function(id):

    if request.method == "POST":
        
        images.delete_one({"user_id" : ObjectId(id)})
        flash("Profile Removed")

    return redirect(url_for('admin_staff'))

def account_setting_update_info_function(id):
    
    if request.method == "POST":
        
        new_name = request.form['name']
        username = request.form['username']
        password = request.form['password']

        if not new_name or not username or not password:
            flash('Important fields Empty')
            return redirect(url_for('login'))
        else:
            users.update_one(
                {"_id" : ObjectId(id)},
                {"$set" : {
                    "name" : new_name,
                    "username" : username,
                    "password" : password
                }})
            flash('User Account Updated')
            session.clear()
            return redirect(url_for('login'))


def admin_setting_image_function(id):
    
    image = request.files['image']

    if not image:
        flash('No Image was Uploaded')
        return redirect(url_for('admin'))

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

    return redirect(url_for('admin'))

def admin_remove_image_function(id):

    if request.method == "POST":
        
        images.delete_one({"user_id" : ObjectId(id)})
        flash("Profile Removed")

    return redirect(url_for('admin'))
