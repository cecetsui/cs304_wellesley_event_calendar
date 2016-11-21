#!/usr/local/bin/python2.7
'''
Grace Hu and Cece Tsui
router.py
Wellesley Events Calender

This file uses Flask to facilitate routing among different pages.
'''

from flask import Flask, render_template, url_for, request, redirect, flash
from jinja2 import Environment, FileSystemLoader
import os
from update_db import *

app = Flask(__name__)
app.secret_key = 'secret'


'''
Renders home page with list of events for the week
'''
@app.route('/')
def home():
    weekEvents = getWeekEvents()
    return render_template('home_child.html', events=weekEvents)



'''
Register a new organization if it does not already exist
'''
@app.route('/register/', methods = ['POST', 'GET'])
def register():
    if request.method == 'GET':
	return render_template('register_child.html')
    else:
	name = request.form['org-name']
	des = request.form['org-description']
	email = request.form['org-email']
	website = request.form['org-website']
	org_type = request.form['org-type']
	result = addOrg(name, des, email, website, org_type)
	if result is not None:
	    flash('The organization ' + result + ' is already registered.')
	    return redirect(url_for('home'))
	    #return redirect(url_for('update_org'), org=name)
	else:
	    flash('Success! Your organization ' + name + ' has been registered.')
	    return redirect(url_for('home'))



'''
Select one's organization and create an event to add onto the home page calendar
'''
@app.route('/add_event/', methods=['POST', 'GET'])
def addEvent():
    if request.method == 'GET':
	orgsList = getOrgsList()
	return render_template('addEvent_child.html', orgs=orgsList)
    else:
	org_id = request.form['org-id']
	#event details
	name = request.form['event-name']
	date = request.form['event-date']
	start = request.form['event-startTime']
	end = request.form['event-endTime']
	location = request.form['event-location']
	description = request.form['event-description']
	spam = request.form['event-spam']
	event_type = request.form['event-type']
	event_id = insertEvent(org_id, name, date, start, end, location, description, spam, event_type)
	flash("event id is " + str(event_id))
	# with event_id, redirect to that event's information
	#change to redirect to their event page
	return redirect(url_for('home'))
	

if __name__ == '__main__':
    app.debug = True
    app.run('0.0.0.0', os.getuid())


