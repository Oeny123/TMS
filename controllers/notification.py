from flask import request, flash, url_for, redirect, session, render_template
from controllers.models import notif_db, users_db, image_db
from bson.objectid import ObjectId
from datetime import datetime, date

notifs = notif_db()
users = users_db()
images = image_db()
        

def inbox_function():

    if 'username' in session and session['status'] == "Enable":

        r_users = list(users.find())
        r_images = list(images.find())
        all_notifs = list(notifs.find())


        search_query = request.form.get('search', '')
        if search_query:
            all_notifs = notifs.find({
            "$or": [
            {"name": {"$regex": search_query, "$options": "i"}},
            {"reciever": {"$regex": search_query, "$options": "i"}},
            {"message": {"$regex": search_query, "$options": "i"}},
            {"title": {"$regex": search_query, "$options": "i"}},
            {"date": {"$regex": search_query, "$options": "i"}},
            {"sender": {"$regex": search_query, "$options": "i"}},
            {"role": {"$regex": search_query, "$options": "i"}}]})
        else:
            all_notifs = notifs.find()


        return render_template('admin/notifs/inbox.html', images = r_images, notifs = all_notifs, users = r_users, userid = session['user-id'], name = session['name'], username = session['username'], role = session['role'])
        
    
    else :
        flash('Unauthorized Access')
        session.clear
        return redirect(url_for('login'))
    
def sent_function():

    if 'username' in session and session['status'] == "Enable":

        r_users = list(users.find())
        r_images = list(images.find())
        all_notifs = list(notifs.find())


        search_query = request.form.get('search', '')
        if search_query:
            all_notifs = notifs.find({
            "$or": [
            {"name": {"$regex": search_query, "$options": "i"}},
            {"reciever": {"$regex": search_query, "$options": "i"}},
            {"message": {"$regex": search_query, "$options": "i"}},
            {"title": {"$regex": search_query, "$options": "i"}},
            {"date": {"$regex": search_query, "$options": "i"}},
            {"sender": {"$regex": search_query, "$options": "i"}},
            {"role": {"$regex": search_query, "$options": "i"}}]})
        else:
            all_notifs = notifs.find()


        return render_template('admin/notifs/sent.html', images = r_images, notifs = all_notifs, users = r_users, userid = session['user-id'], name = session['name'], username = session['username'], role = session['role'])
    
    else :
        flash('Unauthorized Access')
        session.clear
        return redirect(url_for('login'))

def trash_function():

    if 'username' in session and session['status'] == "Enable":

        r_users = list(users.find())
        r_images = list(images.find())
        all_notifs = list(notifs.find())

        search_query = request.form.get('search', '')
        if search_query:
            all_notifs = notifs.find({
            "$or": [
            {"name": {"$regex": search_query, "$options": "i"}},
            {"reciever": {"$regex": search_query, "$options": "i"}},
            {"message": {"$regex": search_query, "$options": "i"}},
            {"title": {"$regex": search_query, "$options": "i"}},
            {"date": {"$regex": search_query, "$options": "i"}},
            {"sender": {"$regex": search_query, "$options": "i"}},
            {"role": {"$regex": search_query, "$options": "i"}}]})
        else:
            all_notifs = notifs.find()

        return render_template('admin/notifs/trash.html', images = r_images, notifs = all_notifs, users = r_users, userid = session['user-id'], name = session['name'], username = session['username'], role = session['role'])
        
    else :
        flash('Unauthorized Access')
        session.clear
        return redirect(url_for('login'))

def compose_notification_funtion():

    if request.method == "POST":

        usr = list(users.find())

        title = request.form['title']
        message = request.form['message']
        receiver = request.form['receiver']
        d_crtd = date.today().isoformat()

        # Convert string to datetime object
        date_obj = datetime.strptime(d_crtd, '%Y-%m-%d')

        # Format datetime object to 'Oct 6 2024'
        formatted_date = date_obj.strftime('%b %d %Y')


        for user in usr:
            if user['username'] == receiver:
                print(user['role'])
                role = user['role']
                department = user['department']
                name = user['name']
                receiver_id = user['_id']

        if not message:
            flash('Empty Message')
            return redirect(url_for('inbox_notification'))
            
        else:
            notifs.insert_one({

                "sender" : session['name'],
                "sender_id" : session['user-id'],
                "title" : title,
                "reciever" : receiver,
                "reciever_id" : receiver_id,
                "name" : name,
                "role" : role,
                "department" : department,
                "message" : message,
                "date" : formatted_date,
                "status" : "Open"
            })
            flash('Message Sent')
            return redirect(url_for('inbox_notification'))

def recove_notif(id):
    if request.method == "POST":
        notifs.update_one(
            {"_id" : ObjectId(id)},
            {"$set" : {
                "status" : "Open"
            }})
        flash('Notification Recovered')
        return redirect(url_for('inbox_notification'))

def trash_notif(id):
    if request.method == "POST":
        notifs.update_one(
            {"_id" : ObjectId(id)},
            {"$set" : {
                "status" : "Trash"
            }})
        flash('Notification Trashed')
        return redirect(url_for('inbox_notification'))

def delete_notif(id):
    if request.method == "POST":
        notifs.delete_one({"_id" : ObjectId(id)})
        flash('Notification Deleted')
        return redirect(url_for('inbox_notification'))