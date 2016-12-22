#!/usr/local/bin/python2.7
'''
Grace Hu and Cece Tsui
router.py
Wellesley Events Calender

This file uses Flask to facilitate routing among different pages.
'''

from flask import Flask, render_template, url_for, request, redirect, flash, make_response, session, send_from_directory
import os
import imghdr
from update_db import *
#from time_date import *
from werkzeug.utils import secure_filename
import random
from flask_cas import CAS

app = Flask(__name__)
app.secret_key = 'secret'
#PATH_LINK = "https://cs.wellesley.edu/~eventscal/eventscal/beta/img"
PATH_LINK = "https://cs.wellesley.edu/~eventscal/img"
UPLOAD_FOLDER = "./../../public_html/img"


ALLOWED_EXTENSIONS = set(["png", "jpg", "jpeg"])
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config['PATH_LINK'] = PATH_LINK


CAS(app)
app.config['CAS_SERVER'] = 'https://login.wellesley.edu:443'
app.config['CAS_AFTER_LOGIN'] = 'logged_in'
app.config['CAS_LOGIN_ROUTE'] = '/module.php/casserver/cas.php/login'
app.config['CAS_LOGOUT_ROUTE'] = '/module.php/casserver/cas.php/logout'
# app.config['CAS_AFTER_LOGOUT'] = 'http://cs.wellesley.edu:1942/'
app.config['CAS_AFTER_LOGOUT'] = 'https://cs.wellesley.edu:1942/logged_out'
app.config['CAS_VALIDATE_ROUTE'] = '/module.php/casserver/serviceValidate.php'

'''
logged_in ('/logged_in/')
    Parameters:
        None

    Logged in. 
'''
@app.route('/logged_in/')
def logged_in():
    flash('You are successfully logged in!')
    return redirect('/' )


'''
logged_out ('/logged_out/')
    Parameters:
        None

    Logged out.
'''
@app.route('/logged_out/')
def logged_out():
    flash('You are successfully logged out!')
    return redirect('/' )


'''
home ('/')
    Parameters: None

    Renders home page with list of events for the week
'''
@app.route('/')
def index():
    print session.keys()
    for k in session.keys():
        print k, ' => ', session[k]
    if '_CAS_TOKEN' in session:
        token = session['_CAS_TOKEN']
    if 'CAS_ATTRIBUTES' in session:
        attribs = session['CAS_ATTRIBUTES']
        for k in attribs:
            print k, ' => ', attribs[k]
    if 'CAS_USERNAME' in session:
        is_logged_in = True
        username = session['CAS_USERNAME']
        this_week = getThisWeekDates()
        monday = this_week[0]
        sunday = this_week[len(this_week) - 1]
        return redirect('/' + monday + '_' + sunday )
    else:
        is_logged_in = False
        username = None
    return render_template('main.html', username=username, is_logged_in=is_logged_in)

'''
homeWithRange ('/<date_range>/')
    Parameters:
        (1) date_range - the range of dates
    
    This function displays all the events happening in a week given by the
    date_range input, which is of the format YYYY-MM-DD_YYYY-MM-DD
    (Monday_Sunday).
'''
@app.route('/<date_range>', methods=['POST', 'GET'])
def homeWithRange(date_range):
    if date_range == '' or date_range == "favicon.ico":
	return redirect('/')

    monday_sunday_list = date_range.split('_')
    if request.method == 'GET':
    	#weekEvents = getWeekEvents(monday_sunday_list)
        dates = str_to_datetime(monday_sunday_list)
        monDate = dates["mon"]
        events = getDayEvents(getDayList(monDate))
	monday = convertDate(monday_sunday_list[0]) 
	sunday = convertDate(monday_sunday_list[1])	

    	flash('Events from ' + monday + ' to ' + sunday)
    	return render_template("home_child.html",
                               meth="/" + date_range,
                               events=events,username=session["CAS_USERNAME"])
    else:
	#convert to datetime objects
	dates = str_to_datetime(monday_sunday_list)
        
	monDate = dates['mon']
	sunDate = dates['sun']
	updatedWeek = ''
	if request.form['submit'] == 'Previous Week':
	    updatedWeek = getPrevWeekRange(monDate, sunDate)
	else:
	    updatedWeek = getNextWeekRange(monDate, sunDate)
	return redirect(url_for('homeWithRange', date_range=updatedWeek))


'''
register ('/register/')
    Parameters: None

    Register a new organization if it does not already exist
'''
@app.route('/register/', methods = ['POST', 'GET'])
def register():
    if request.method == 'GET':
	return render_template('register_child.html', username=session["CAS_USERNAME"])
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
	return render_template('addEvent_child.html', username=session["CAS_USERNAME"], orgs=orgsList)
    else:
        spam = request.files["file"]
        spamName = getFilename(spam, ALLOWED_EXTENSIONS, app.config['UPLOAD_FOLDER'])
	spamMessage = ""
	if spamName == "No spam":
	    spamMessage = ""
        elif spamName is None:
            spamMessage = "Unfortunately, we could not upload your file because it was of the wrong extension"
	    spamName = "No spam"
	else:
            spam.save(os.path.join(app.config['UPLOAD_FOLDER'], spamName))
	    os.chmod(os.path.join(app.config['UPLOAD_FOLDER'], spamName), 0444)
	org_id = request.form['org-id']
	#event details
	name = request.form['event-name']
	date = request.form['event-date']
	start = request.form['event-startTime']
	end = request.form['event-endTime']
	location = request.form['event-location']
	description = request.form['event-description']
	event_type = request.form['event-type']
        if name == "" or date == "" or start == "" or location == "" or description == "" or org_id == "none":
            flash("One of the required fields is missing.")
            return redirect("/add_event/")
	else:
	    event_id = insertEvent(org_id, name, date, start, end, location, description, spamName, event_type)
 	    if event_id == 'conflict':
	     	flash("Another event is happening at the same location and time")
	    	return redirect(url_for('addEvent'))
	    else:
                flash(spamMessage)
		event_week = getWeek(date)
	        monday = event_week[0]
    		sunday = event_week[len(event_week) - 1]
    		return redirect('/' + monday + '_' + sunday )


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
    if eventInfo['event-spam'] != 'No spam':
    	path = app.config['PATH_LINK'] + "/" + eventInfo['event-spam']
	eventInfo['event-spam'] = path
    emails = getEmails(eventid)
    return render_template("eventInfo_child.html", events=eventInfo, meth="/event_info/" + str(eventid), emails=emails, username=session["CAS_USERNAME"])
    

'''
org_info ('/org_info/<orgid>')
    Parameters:
        (1) orgid - the id of the org

    Takes in the id of an organization and returns information about that org.
    Allows the user to update org if desired.
'''
@app.route('/org_info/<orgid>', methods=["GET","POST"])
def org_info(orgid):
    if request.method == "POST":
        return redirect("/updateOrg/" + str(orgid))
    else:
        orgInfo = getOrgInfo(orgid)
        #the following errors should not happen but if they do, we address them
        #check for errors: if org_id does not exist, re route to register
        if orgInfo == "no org error":
            return redirect(url_for('register'))
        #if org info is missing head contact, redirect to updateOrg page
        elif orgInfo == "no bnum error":
            return redirect("/updateOrg/" + str(orgid))
        else: #no errors - we have organization and head contact info
            emails = [ ['Organization', orgInfo['org-email']], ['Head Contact', orgInfo['org-cont-email']] ]
            return render_template("orgInfo_child.html", orgs=orgInfo, meth="/org_info/" + str(orgid), emails=emails, username=session["CAS_USERNAME"])



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
        '''
	else:
            events = getEvents(orgid)
            return render_template("select_child.html", orgs=getOrgsList(), events=events)
    '''
    elif request.method == "POST" and request.form["org-id"] == "none":
        flash("Please choose an organization to get started.")
        return redirect("/select_org/")
    else:
        return render_template("select_child.html", orgs=getOrgsList(), username=session["CAS_USERNAME"])


'''
update_event
    Parameters:
        (1) event_id - the id of the event

    Provides the currently stored information from the database, allows the user to make edits, and make the appropriate updates to the event information. The link also allows you to delete the event entirely.
'''
@app.route('/update_event/<event_id>',methods=["GET","POST"])
def update_event(event_id):
    if request.method == "POST":
        spam = request.files["file"]
	spamName = getFilename(spam, ALLOWED_EXTENSIONS, app.config['UPLOAD_FOLDER'])
        spamMessage = ""
        if spamName == "No spam":
            spamMessage = ""
        elif spamName is None:
            spamMessage = "Unfortunately, we could not upload your file because it was of the wrong extension"
    	    spamName = "No spam"
        else:
            spam.save(os.path.join(app.config['UPLOAD_FOLDER'], spamName))
	    os.chmod(os.path.join(app.config['UPLOAD_FOLDER'], spamName), 0444)
	
	#if spam already existed and no new file was uploaded, then keep the old spam
        thiseventInfo = getEventInfo(event_id)
        event_spam = thiseventInfo["event-spam"]
	if spamName == "No spam" and event_spam != "No spam":
	    spamName = event_spam 
	
	eventInfo = {"org-id": request.form["org-id"],
                     "event-name": request.form["event-name"],
                     "event-date": request.form["event-date"],
                     "event-startTime": request.form["event-startTime"],
                     "event-endTime": request.form["event-endTime"],
                     "event-location": request.form["event-location"],
                     "event-description": request.form["event-description"],
                     "event-spam": spamName,
                     "event-type": request.form["event-type"]
            }
	if request.form["submit"] == "Update":
            updateEvent(eventInfo, event_id)
            success = "Event (" + eventInfo["event-name"] + ") was successfully updated." + spamMessage
	    flash(success)
            return redirect("/event_info/" + str(event_id))
        if request.form["submit"] == "Delete":
	    deleteEvent(event_id)
            success = "Event (" + eventInfo["event-name"] + ") was successfully deleted."
            flash(success)
            return redirect("/")
    else: #GET
        eventInfo = getEventInfo(event_id)
   	if eventInfo['event-spam'] != 'No spam':
            path = app.config['PATH_LINK'] + "/" + eventInfo['event-spam']
            eventInfo['event-spam'] = path
        return render_template("updateEvent_child.html",
                               meth="/update_event/" + str(event_id),
                               events=eventInfo, username=session["CAS_USERNAME"])



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
        if request.form["submit"] == "Update":
            update_org(orgInfo, orgid)
            success = "Organization (" + orgInfo["org-name"] + ") was successfully updated."
            flash(success)
            return redirect("/org_info/" + str(orgid))
        else: #Delete button selected
            deleteOrg(orgid)
            success = "Organization (" + orgInfo["org-name"] + ") was successfully deleted."
            flash(success)
            return redirect("/select_org/")
    else:
        orgInfo = getOrgInfo(orgid)
        return render_template("updateOrg_child.html", 
                               meth="/updateOrg/" + str(orgid), 
                               orgInfo=orgInfo, username=session["CAS_USERNAME"])


'''
filter ('/filter/')
    Parameters:
        None

        This filter function enables users to filter events by name, type, date, time. At least one field must be filled out. Otherwise, an error message appears.
'''
@app.route("/filter/", methods=["GET","POST"])
def filter():
    org_types = ['Academic' , 'Career', 'CGHP Affiliates', 'Cultural', 'Media & Publication', 'Performance & Arts', 'Political', 'Religious', 'Social Justice & Awareness', 'Societies', 'Sports & Teams', 'Volunteer']
    event_types = ['Lecture', 'Meeting', 'Performance', 'Rehearsal', 'Workshop', 'Conference', 'Exhibit', 'Film Showing', 'Panel', 'Party', 'Recital', 'Seminar', 'Reception', 'Community Service', 'Other']
    info = {"event-type":event_types, "org-type":org_types,"events":[]}
    if request.method == "POST":
        if request.form["event-name"] == "" and request.form["date"] == "" and request.form["event-type"] == "Choose One" and request.form["org-name"] == "" and request.form["org-type"] == "Choose One":
            flash("All fields to filter from are empty. Cannot filter.")
            return render_template("filter_child.html",
                               meth="/filter/",
                               info=info,
				orgs=getOrgsList(), username=session["CAS_USERNAME"])
        filterInfo = {"event-name":request.form["event-name"],
                      "date":request.form["date"],
                      "event-type":request.form["event-type"],
                      "org-name":request.form["org-name"],
                      "org-type":request.form["org-type"]}
        events = getFilteredEvents(filterInfo)
        info["events"] = events
        message = "Looking for events"
        if filterInfo["event-name"] != "":
            message += " with event name similar to " + filterInfo["event-name"]
        if filterInfo["date"] != "":
            message += " on " + filterInfo["date"]
        if filterInfo["event-type"] != "Choose One":
            message += " of event type " + filterInfo["event-type"]
        if filterInfo["org-name"] != "":
            message += " hosed by the organizations with names similar to " + filterInfo["org-name"]
        if filterInfo["org-type"] != "Choose One":
            message += " related to the organization type " + filterInfo["org-type"]
        flash(message)
        return render_template("filter_child.html",
                               meth="/filter/",
                               info=info, orgs=getOrgsList(), username=session["CAS_USERNAME"])
    else:
        return render_template("filter_child.html",
                               meth="/filter/",
                               info=info, orgs=getOrgsList(), username=session["CAS_USERNAME"])
        



'''
main
'''
if __name__ == '__main__':
    app.debug = True
    app.run('0.0.0.0', 1942)
    #app.run('0.0.0.0', os.getuid())
