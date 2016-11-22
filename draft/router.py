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
home ('/')
    Parameters: None

    Renders home page with list of events for the week
'''
@app.route('/')
def home():
    weekEvents = getWeekEvents()
    return render_template('home_child.html', events=weekEvents)



'''
register ('/register/')
    Parameters: None

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
        org_contact = request.form['org-contact']
        cont_bnum = request.form['org-cont-bnum']
        org_cont_email = request.form['org-cont-email']
        org_cont_type = request.form['org-cont-type']
        cont_bnum = addContact(org_contact, cont_bnum, org_cont_email, org_cont_type)
	result = addOrg(name, des, email, website, org_type, cont_bnum)
	if cont_bnum is 'error' or result is 'error':
	    flash('Please fill in all required fields before submitting.')
	    return redirect(url_for('register'))
	if result is not None:
	    flash('The organization ' + result + ' is already registered.')
	    return redirect('/add_event/' + str(getOrgId(name)))
	    #return redirect(url_for('update_org'), org=name)
	else:
	    flash('Success! Your organization ' + name + ' has been registered. Now add an upcoming event to the master calendar.')
	    return redirect('/add_event/' + str(getOrgId(name)))



'''
addEvent ('/add_event/')
    Parameters: None

    Select one's organization and create an event to add onto the home page calendar
'''
@app.route('/add_event/', defaults={'org_id':""}, methods=["GET","POST"])
@app.route('/add_event/<org_id>', methods=['GET', 'POST'])
def addEvent(org_id):
    if request.method == 'GET':
        orgsList = getOrgsList()
        orgsList.insert(0, ("none", "Choose One"))
        if org_id != "":
            orgsList = getOrgsDropDown(org_id)
            print org_id
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
        if name == "" or date == "" or start == "" or location == "" or description == "" or org_id == "none":
            flash("One of the required fields is missing.")
            return redirect("/add_event/")
	else:
	    event_id = insertEvent(org_id, name, date, start, end, location, description, spam, event_type)
 	    if event_id == 'conflict':
	     	flash("Another event is happening at the same location and time")
	    	return redirect(url_for('addEvent'))
	    else:
	# TO DO: with event_id, redirect to that event's information
	# TO DO: change to redirect to their event page
	        return redirect(url_for('home'))


'''
event_info
    Parameters:
        (1) eventid - the id of the event given during registration
    
    Lists the information of the given event (based upon the event id). Allows the user to potentially update the event.
'''
@app.route('/event_info/<eventid>', methods=["GET","POST"])
def event_info(eventid):
    if request.method == "POST":
        return redirect("/update_event/" + str(eventid))
    eventInfo = getEventInfo(eventid)
    return render_template("eventInfo_child.html", events=eventInfo, meth="/event_info/" + str(eventid))
    


'''
select_org ('/select_org/')
    Parameters: None

    Allows an individuat to select an organization from a list of registratered organizations to either update or find an event from.
'''
@app.route('/select_org/',methods=["GET","POST"])
def select_org():
    if request.method == "POST" and request.form["org-id"] != "none":
        orgid = request.form["org-id"]
        if request.form["submit"] == "Update":
            return redirect(url_for("updateOrg", orgid=orgid))
        else:
            events = getEvents(orgid)
            return render_template("select_child.html", orgs=getOrgsList(), events=events)
    elif request.method == "POST" and request.form["org-id"] == "none":
        flash("Please choose an organization to get started.")
        return redirect("/select_org/")
    else:
        return render_template("select_child.html", orgs=getOrgsList())


'''
update_event
    Parameters:
        (1) event_id - the id of the event

    Provides the currently stored information from the database, allows the user to make edits, and make the appropriate updates to the event information. The link also allows you to delete the event entirely.
'''
@app.route('/update_event/<event_id>',methods=["GET","POST"])
def update_event(event_id):
    if request.method == "POST":
        eventInfo = {"org-id": request.form["org-id"],
                     "event-name": request.form["event-name"],
                     "event-date": request.form["event-date"],
                     "event-startTime": request.form["event-startTime"],
                     "event-endTime": request.form["event-endTime"],
                     "event-location": request.form["event-location"],
                     "event-description": request.form["event-description"],
                     "event-spam": request.form["event-spam"],
                     "event-type": request.form["event-type"]
            }
        if request.form["submit"] == "Update":
            updateEvent(eventInfo, event_id)
            success = "Event (" + eventInfo["event-name"] + ") was successfully updated."
            flash(success)
            return redirect("/update_event/" + str(event_id))
        else:
            deleteEvent(event_id)
            success = "Event (" + eventInfo["event-name"] + ") was successfully deleted."
            flash(success)
            return redirect("/select_org/")
    else:
        eventInfo = getEventInfo(event_id)
        return render_template("updateEvent_child.html",
                               meth="/update_event/" + str(event_id),
                               events=eventInfo)



'''
updateOrg ('/updateOrg/')
    Parameters:
        (1) orgid - the id of the organization as from registration
    
    Provides the currently stored information about the organization and allows you to edit the information to update the organization. This also allows you to delete the org entirely.
'''
@app.route('/updateOrg/<orgid>',methods=["GET","POST"])
def updateOrg(orgid):
    if request.method == "POST":
        orgInfo = {"org-name":request.form["org-name"],
                   "org-description": request.form["org-description"],
                   "org-email":request.form["org-email"],
                   "org-website":request.form["org-website"],
                   "org-type":request.form["org-type"],
                   "org-contact":request.form["org-contact"],
                   "org-cont-bnum":request.form["org-cont-bnum"],
                   "org-cont-email":request.form["org-cont-email"],
                   "org-cont-type":request.form["org-cont-type"]}
        if request.form["submit"] == "update":
            update_org(orgInfo, orgid)
            success = "Organization (" + orgInfo["org-name"] + ") was successfully updated."
            flash(success)
            return redirect("/updateOrg/" + str(orgid))
        else:
            deleteOrg(orgid)
            success = "Organization (" + orgInfo["org-name"] + ") was successfully deleted."
            flash(success)
            return redirect("/select_org/")
    else:
        orgInfo = getOrgInfo(orgid)
        return render_template("updateOrg_child.html", 
                               meth="/updateOrg/" + str(orgid), 
                               orgInfo=orgInfo)


'''
main
'''
if __name__ == '__main__':
    app.debug = True
    app.run('0.0.0.0', os.getuid())
    #app.run('0.0.0.0', 3050)

