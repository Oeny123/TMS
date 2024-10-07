from flask import request, flash, url_for, redirect, session
from controllers.models import global_notif_db, man_notif_db
from datetime import datetime, date

global_notif = global_notif_db()
man_notif = man_notif_db()

def global_notif_function():
    
    if request.method == "POST":

        title = request.form['title']
        message = request.form  ['message']
        d_crtd = date.today().isoformat()

        date_obj = datetime.strptime(d_crtd, '%Y-%m-%d')

        # Format datetime object to 'Oct 6 2024'
        formatted_date = date_obj.strftime('%b %d %Y')

        if not message:
            flash('Empty Message')
            return redirect(url_for('admin_notification'))
        else:
            global_notif.insert_one({
                "sender" : session['name'],
                "title" : title,
                "reciever" : "Global",
                "message" : message,
                "date" : formatted_date
            })
            flash('Message Sent')
            return redirect(url_for('admin_notification'))
        
def man_notif_funtion():

    if request.method == "POST":

        title = request.form['title']
        message = request.form['message']
        receiver = request.form['receiver']
        d_crtd = date.today().isoformat()

        # Convert string to datetime object
        date_obj = datetime.strptime(d_crtd, '%Y-%m-%d')

        # Format datetime object to 'Oct 6 2024'
        formatted_date = date_obj.strftime('%b %d %Y')

        if not message:
            flash('Empty Message')
            return redirect(url_for('admin_notification'))
        else:
            man_notif.insert_one({
                "sender" : session['name'],
                "title" : title,
                "reciever" : receiver,
                "message" : message,
                "date" : formatted_date
            })
            flash('Message Sent')
            return redirect(url_for('admin_notification'))