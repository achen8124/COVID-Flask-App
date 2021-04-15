# Authors: CS For Insight (Summer19 - JG) + Andrea and Katie

try:
    from flask import render_template, redirect, url_for, request, send_from_directory, flash
except:
    print("Not able to import all of the calls needed from the Flask library.")

from app import app
import os

from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage


from app import checkAvailability  # our Python functions are in checkAvailability.py
from app import emailAvailability

# Home page, renders the index.html template
@app.route('/index')
@app.route('/')
def index():
    return render_template('index.html', title='Home')

# Appointments by (City, State) page
@app.route('/appointments',methods=['GET','POST'])
def appointments():
    if request.method == 'POST':
        # # larger textarea
        # old_textarea = request.form['textarea_input']
        # city and state (their replacements)
        city = request.form['city']
        state = request.form['state']
        receiver_email = request.form['email']
        new_text = checkAvailability.get_vacc_by_city(city, state)
        send_availability_email(receiver_email, new_text)
        return render_template('apptResults.html', old_text=city+", " + state, new_text=new_text)
    return render_template('appt.html', title='Home')
