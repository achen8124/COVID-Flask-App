# Authors: CS For Insight (Summer19 - JG) + Andrea and Katie

try:
    from flask import render_template, redirect, url_for, request, send_from_directory, flash
except:
    print("Not able to import all of the calls needed from the Flask library.")

from app import app
import os

from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage


from app import checkAvailability  
from app import emailAvailability

STATES = ["AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DC", "DE", "FL", "GA", \
          "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD", \
          "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ", \
          "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC", \
          "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"]

# Home page, renders the index.html template
@app.route('/index')
@app.route('/')
def index():
    return render_template('index.html', title='Home')

# Appointments by (City, State) page
@app.route('/appointments',methods=['GET','POST'])
def appointments():
    if request.method == 'POST':
        city = request.form['city']
        state = request.form['state']
        location = city + ", " + state
        new_text = checkAvailability.get_vacc_by_city(city, state)
        return render_template('apptResults.html', city=city, state=state, new_text=new_text, title='by city', use_zip=False)
    return render_template('appt.html', stateList=STATES, title='by city', use_zip=False)

# Appointments by zipcode page
@app.route('/appointments_zip',methods=['GET','POST'])
def appointments_zip():
    if request.method == 'POST':
        zip = request.form['zip']
        new_text = checkAvailability.get_vacc_by_zip(zip)
        return render_template('apptResults.html', use_zip=True, zipcode=zip, new_text=new_text)
    return render_template('appt.html', stateList=STATES, title='by zip', use_zip=True)

# Email info for city/state searches
@app.route('/email_info/<city>/<state>',methods=['GET','POST'])
def email_info(city = "San Diego", state = "CA"):
    if request.method == 'POST':
        receiver_email = request.form['email']
        new_text = checkAvailability.get_vacc_by_city(city, state)
        search_term = city + ", " + state
        emailAvailability.send_availability_email(receiver_email, search_term, new_text)
        return render_template('apptResults.html', use_zip=False, city=city, state=state, new_text=new_text, email=receiver_email)
    return render_template('apptResults.html', title='emailed', use_zip=False)

# Email info for zipcode searches
@app.route('/email_info_zip/<zipcode>',methods=['GET','POST'])
def email_info_zip(zipcode="12345"):
    if request.method == 'POST':
        receiver_email = request.form['email']
        new_text = checkAvailability.get_vacc_by_zip(zipcode)
        emailAvailability.send_availability_email(receiver_email, zipcode, new_text)
        return render_template('apptResults.html', use_zip=True, zipcode=zipcode, new_text=new_text, email=receiver_email)
    return render_template('apptResults.html', title='emailed', use_zip=True)
