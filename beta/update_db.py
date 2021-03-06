#!/usr/local/bin/python2.7
'''
Grace Hu and Cece Tsui
update_db.py
Wellesley Events Calendar

This file modifies the content in the events_cal database.
'''

import sys
import MySQLdb
import dbconn
import dsn
#import time
#import datetime
import os
from time_date import *
import random
from werkzeug.utils import secure_filename

'''
getConn
    Parameters: 
        None.
    
    Set up database connection and return cursor.
'''
def getConn():
    dsn = dbconn.read_cnf('my.cnf') # changed by Scott
    dsn['db'] = 'eventscal_db'
    conn = dbconn.connect(dsn)
    conn.autocommit(True)
    return conn

'''
addContact
    Parameters:
        (1) name - the contact's name, string
        (2) bnum - the contact's Wellesley B Number, string
        (3) email - the contact's Wellesley email, string
        (4) stype - the contact's type (Student or Staff), string

        Adds the org's contact into the table (president) 
'''
def addContact(name, bnum, email, stype):
    if name == "" or bnum == "" or email == "":
	return 'error'  #required fields missing
    conn = getConn()
    curs = conn.cursor((MySQLdb.cursors.DictCursor))
    curs.execute('select * from head_contacts where bnumber=%s', (bnum,))
    row = curs.fetchone()
    if row is None:
        curs.execute('insert into head_contacts(bnumber, name, email, contact_type) values (%s, %s, %s, %s)', (bnum, name, email, stype))
    else:
        curs.execute('update head_contacts set name=%s, email=%s, contact_type=%s where bnumber=%s', (name, email, stype, bnum))
    return bnum


'''
addOrg
    Parameters:
        (1) name - the name of the organization, string
        (2) des - the description of the organization, string
        (3) email - the email of the org, string
        (4) website - the website of the org, string
        (5) org_type - the type of organization, string
        (6) pres_bnum - the head contact's b number, string

    Adds a new organization to the orgs table with the given information. In addition, it associates the main contact with the organization.
'''
def addOrg(name, des, email, website, org_type, pres_bnum):
    if name == "" or pres_bnum == "": #required field missing
	return 'error'

    conn = getConn()
    curs = conn.cursor((MySQLdb.cursors.DictCursor))
    
    #check if org exists by searching exact matching names; org names are usually unique
    curs.execute('select * from orgs where name=%s', (name,))
    row = curs.fetchone()
    
    #if org does not exist, insert into orgs table
    if row is None:
  	curs.execute('insert into orgs(name, description, email, website, org_type) values (%s, %s, %s, %s, %s)', (name, des, email, website, org_type))
        curs.execute('select org_id from orgs where name=%s', (name, ))
        org_id = curs.fetchone()["org_id"]
        curs.execute('insert into orgs_contacts(org_id, bnumber, date_added) values (%s, %s, %s)', (org_id, pres_bnum, time.strftime("%Y-%m-%d %H:%M:%S")))
    	return None
    else:
	return name


'''
getOrgId
    Parameters:
        (1) name - the name of the organization

    Returns the organization id.
'''
def getOrgId(name):
    conn = getConn()
    curs = conn.cursor((MySQLdb.cursors.DictCursor))
    curs.execute('select org_id from orgs where name=%s', (name,))
    return curs.fetchone()["org_id"]


'''
getOrgInfo
    Parameter(s):
        (1) orgid - the organiation's id as when first registered

    Returns all the current information about the organization (inclusive of the information of the main contact) that is stored in the database.The type options are used such that the type of the organiation is listed first [so that in the form, the option is selected).
'''
def getOrgInfo(orgid):
    conn = getConn()
    curs = conn.cursor((MySQLdb.cursors.DictCursor))
    curs.execute('select * from orgs where org_id=%s', (orgid,))
    org = curs.fetchone()
    if org is None:
        return 'no org error'
    curs.execute('select * from orgs_contacts where org_id=%s ORDER BY date_added DESC LIMIT 1',(orgid,))
    bnum = curs.fetchone()
    bnum = bnum["bnumber"]
    if bnum is None or bnum == "":
        return 'no bnum error'
    curs.execute('select * from head_contacts where bnumber=%s',(bnum,))
    org_contact = curs.fetchone()
    org_type = org["org_type"]
    type_options = "<option value='" + org_type + "' selected>" + org_type
    all_types = ['Academic' , 'Career', 'CGHP Affiliates', 'Cultural', 'Media & Publication', 'Performance & Arts', 'Political', 'Religious', 'Social Justice & Awareness', 'Societies', 'Sports & Teams', 'Volunteer']
    for t in all_types:
        if t != org_type:
            type_options += "<option value='" + t + "'>" + t
    
    cont_type = org_contact["contact_type"]
    all_cont_types = ["Staff","Student"]
    cont_type_options = "<option value='" + cont_type + "'selected>" + cont_type
    for t in all_cont_types:
        if t != cont_type:
            cont_type_options += "<option value='" + t + "'>" + t

    orgInfo = {"org-name":org["name"],
                   "org-description": org["description"],
                   "org-email":org["email"],
                   "org-website":org["website"],
                   "org-type":type_options,
                   "single-type":org_type,
                   "org-contact":org_contact["name"],
                   "org-cont-bnum": org_contact["bnumber"],
                   "org-cont-email": org_contact["email"],
                   "org-cont-type": cont_type_options,
    		   "org-id": orgid
	        }
    return orgInfo


'''
update_org
    Parameters
        (1) orgInfo - a dictionary that stores all of the information of the organization (inclusive of the main contact's information).
        (2) orgid - the id of the organization when it first registered.

    Updates the organization's information and the main contact's organization based upon given information from a form.
'''
def update_org(orgInfo, orgid):
    conn = getConn()
    curs = conn.cursor((MySQLdb.cursors.DictCursor))
    curs.execute('update orgs set name=%s, description=%s, email=%s, website=%s, org_type=%s where org_id=%s', (orgInfo["org-name"], orgInfo["org-description"],
                            orgInfo["org-email"], orgInfo["org-website"],
                            orgInfo["org-type"],orgid))

    bnum = addContact(orgInfo["org-contact"],
                      orgInfo["org-cont-bnum"],
                      orgInfo["org-cont-email"],
                      orgInfo["org-cont-type"])
    curs.execute('select * from orgs_contacts where org_id=%s and bnumber=%s', (orgid, bnum))
    row = curs.fetchone()
    if row is not None:
        if row['bnumber'] != bnum:
            curs.execute('delete from orgs_contacts where org_id=%s', (orgid,))
            curs.execute('insert into orgs_contacts(org_id, bnumber, date_added) values (%s, %s, %s)', (orgid, bnum, time.strftime("%Y-%m-%d")))
    if row is None:
        curs.execute('insert into orgs_contacts(org_id, bnumber, date_added) values (%s, %s, %s)', (orgid, bnum, time.strftime("%Y-%m-%d")))
    

'''
deleteOrg
    Parameter:
        (1) orgid - the id of the organization upon when it first registered

    Deletes the organization from the database (orgs_contacts and orgs)
'''
def deleteOrg(orgid):
    conn = getConn()
    curs = conn.cursor((MySQLdb.cursors.DictCursor))
    curs.execute('select * from orgs_events where org_id=%s', (str(orgid),))
    events = curs.fetchall()
    for e in events:
        curs.execute('delete from orgs_events where event_id=%s', (e["event_id"],))
        curs.execute('delete from events where event_id=%s', (e["event_id"],))
    curs.execute('delete from orgs_contacts where org_id=%s', (orgid,))
    curs.execute('delete from orgs where org_id=%s', (orgid,))
    

'''
getEvents 
    Parameter:
        (1) orgid = the organization's id upon when it first registered
    
    Gets all the currently registered (and stored in the database) events. Returns a tuple where the first element is the name of the organization associated with all the events, and the second element is the list of events it holds. Each event in the list is represented by a tuple where the first element is the link to find more information about the event and the second element is the name of the event.
''' 
def getEvents(orgid):
    conn = getConn()
    curs = conn.cursor((MySQLdb.cursors.DictCursor))
    curs.execute('select * from events inner join (select event_id from orgs_events where org_id=%s) t2 on events.event_id = t2.event_id', (orgid,))
    all_events = curs.fetchall()
    events = []
    for event in event_ids:
        single_event = ("/event_info/" + str(event["event_id"]), event["name"])
        events.append(single_event)
    curs.execute('select name from orgs where org_id=%s', (orgid,))
    return (curs.fetchone()["name"], events)


'''
updateEvent
    Parameters:
        (1) eventInfo - the inforamtion of an event collected from a form. It is a dictionary
        (2) event_id - the id of the event as from registration
    
    Updates the event information with the given information based upon the form.
'''
def updateEvent(eventInfo, event_id):
    conn = getConn()
    curs = conn.cursor((MySQLdb.cursors.DictCursor))
    print eventInfo
    curs.execute('update events set name=%s , description=%s, event_date=%s, time_start=%s, time_end=%s, location=%s, spam=%s, event_type=%s where event_id=%s', 
                 (eventInfo["event-name"], eventInfo["event-description"],
                  eventInfo["event-date"], eventInfo["event-startTime"],
                  eventInfo["event-endTime"],eventInfo["event-location"], 
                  eventInfo["event-spam"], eventInfo["event-type"], event_id))
    curs.execute("update orgs_events set org_id=%s where event_id=%s", (eventInfo["org-id"],event_id))


'''
deleteEvent
    Parameters:
        (1) event_id - the id of the event as from registration

    Delete the event entirely from the database.
'''
def deleteEvent(event_id):
    conn = getConn()
    curs = conn.cursor((MySQLdb.cursors.DictCursor))
    curs.execute("delete from orgs_events where event_id=%s", (event_id,))
    curs.execute("delete from events where event_id=%s",(event_id,))


'''
getEventInfo
    Parameters:
        (1) event_id - the id of the event as from registration
ema
    Gets all the current information (from the database) of the event. The org_id is represented as a list where the org it is attached to first is the first in the list. In addtion, the event type is represented as a list where the type of the event (as per held from the database) is the first in the list. This is such that when creating the form and having the drop down, the event type and org that the event is attached to is shown.
'''
def getEventInfo(event_id):
    print "$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$"
    print event_id
    print "%%%%%%%%%%%"
    conn = getConn()
    curs = conn.cursor((MySQLdb.cursors.DictCursor))
    curs.execute("select * from events where event_id=%s", (event_id,))
    event = curs.fetchone()
    curs.execute("select * from orgs_events where event_id=%s",(event_id,))
    org_id = curs.fetchone()["org_id"]

    allOrgs = getOrgsDropDown(org_id)
    current_type = event["event_type"]
    allTypes = ['Lecture', 'Meeting', 'Performance', 'Rehearsal', 'Workshop', 'Conference', 'Exhibit', 'Film Showing', 'Panel', 'Party', 'Recital', 'Seminar', 'Reception', 'Community Service', 'Other']
    eventTypes = [current_type]
    for t in allTypes:
        if t != current_type:
            eventTypes.append(t)
    
    date_end = event["event_date"]
    
    if str(timeLeadZero(event["time_start"])) > str(timeLeadZero(event["time_end"])):
        date_end += datetime.timedelta(days=1)


    eventInfo = {"org-id": allOrgs, #select menu of orgs with this org at top
                     "current-orgid": org_id, #current org's id
                     "event-name": event["name"],
                     "event-date": event["event_date"],
                     "event-done": date_end,
                     "unconverted-start": timeLeadZero(event["time_start"]),
                     "unconverted-end": timeLeadZero(event["time_end"]),
                     "event-startTime": convertTime(event["time_start"]),
                     "event-endTime": convertTime(event["time_end"]),
                     "event-location": event["location"],
                     "event-description": event["description"],
                     "event-spam": event["spam"],
                     "event-type": eventTypes,
                     "event-id": event_id
            }
    return eventInfo



'''
getOrgsDropDown
    Parameters:
        (1) event_id - the event id
    
    Returns a list of orgs used for the drop down, but with the currently associated org for the event_id at the top.
'''
def getOrgsDropDown(org_id):
    conn = getConn()
    curs = conn.cursor((MySQLdb.cursors.DictCursor))
    allOrgs = getOrgsList()
    indexofcurorg = 0
    for i in range(len(allOrgs)):
        if str(allOrgs[i][0]) == str(org_id):
            indexofcurorg = i
            break
    org = allOrgs.pop(indexofcurorg)
    allOrgs.insert(0, org)
    return allOrgs


'''
getOrgsList
    Parameters: None

    Returns the list of all currently registered organizations. Each org is represented as a tuple where the first element is the org id and the second element is the name of the org.
'''
def getOrgsList():
    conn = getConn()
    curs = conn.cursor((MySQLdb.cursors.DictCursor))
    curs.execute('select org_id, name from orgs order by name')
    orgs = []
    row = curs.fetchone()
    while row is not None:
        orgs.append((unicode(row['org_id']), unicode(row['name'])))
        row = curs.fetchone()
    return orgs


'''
getOrgHosts
    Parameters: 
        (1) event_id - the id of the event as from registration

    Returns a dictionary of all names and ids of the orgs that are hosting this event.
'''
def getOrgHosts(event_id):
    conn = getConn()
    curs = conn.cursor((MySQLdb.cursors.DictCursor))
    curs.execute('select org_id from orgs_events where event_id=%s', (event_id,))
    orgs = []
    row = curs.fetchone()
    while row is not None:
        orgs.append([ getOrgName(row['org_id']) ,  row['org_id'] ])
        row = curs.fetchone()
    return orgs


'''
getOrgName
    Parameters:
        (1) org_id - the id of the organization as from registration

    Returns name of organization given the org_id
'''
def getOrgName(org_id):
    conn = getConn()
    curs = conn.cursor((MySQLdb.cursors.DictCursor))
    curs.execute('select name from orgs where org_id=%s', (int(org_id)))
    row = curs.fetchone()
    if row['name'] is None:
	return None
    else:
	return row['name']


'''
insertEvent 
    Parameters:
        (1) org_id - the id of the organization as from registration; this is the organization associated with the event
        (2) name - the name of the event, string
        (3) date - the date of the event, string
        (4) start - the start time of the event, string
        (5) end - the end time of the event, string
        (6) loc - the location of the event, string
        (7) des - the description of the event, string
        (8) spam - the link to the spam/picture for the event, string
        (9) event_type - the type of the event, string

    Adds new event into the events table. Returns this event's event_id 
'''
def insertEvent(org_id, name, date, start, end, loc, des, spam, event_type):
    conn = getConn()
    curs = conn.cursor((MySQLdb.cursors.DictCursor))
    
    #check that the event already exists
    curs.execute('select * from events where name=%s and event_date=%s and location=%s', (name, str(date), loc))
    row = curs.fetchone()
    
    #if event does not exist, insert into events table
    if row is None:
	#check that another event is not happening at the same time
	curs.execute('select * from events where event_date=%s and location=%s and time_start=%s', (date, loc, start))
	conflict = curs.fetchone()
	# if another event conflicts with location and time, display error
	if conflict is not None:
	    return 'conflict'
	else:
    	    # add event into events table
	    curs.execute('insert into events(spam, name, event_date, time_start, time_end, description, location, event_type) values (%s, %s,%s, %s, %s, %s, %s, %s)', (spam, name, date, start, end, des, loc, event_type))
	    # find this new event's id
	    curs = conn.cursor((MySQLdb.cursors.DictCursor))
	    curs.execute('select event_id from events where name=%s and event_date=%s and location=%s', (name, str(date), loc))
	    this_event = curs.fetchone()
	    event_id = this_event['event_id']
	    # add into orgs_events relationship between org and event ???	
	    curs = conn.cursor((MySQLdb.cursors.DictCursor))
	    curs.execute('insert into orgs_events(org_id, event_id) values (%s, %s)', (int(org_id), int(event_id)))
	    return event_id

    #else, event already exists, return event_id
    else:  	 
	return row['event_id']


'''
getDayEvents
    Parameters:
        (1) dateList - the list of dates from Monday to Sunday
    
    Returns a list of lists, where each list in the list is a list of dictionaries where each dictioanry represents an event and its information. The list of dictioanries in the 0th index are events for Monday. The list of dictioanries in the 1st index are events for Tuesday, etc.
'''
def getDayEvents(dateList):
    conn = getConn()
    curs = conn.cursor((MySQLdb.cursors.DictCursor))
    dayEvents = []
    days = ["Monday","Tuesday", "Wednesday","Thursday","Friday", "Saturday", "Sunday"]
    dayIndex = 0
    for date in dateList:
        curs.execute("select * from events where event_date=%s ORDER BY time_start, name ASC",(date,))
        events = []
        selectedEvents = curs.fetchall()
        for row in selectedEvents:
            org_hosts = getOrgHosts(row["event_id"])
            events.append({
		'event_id': row['event_id'],	
		'name': row['name'],
		'date': row['event_date'],
		'spam': row['spam'],
		'start': convertTime(row['time_start']),
		'end': convertTime(row['time_end']),		
		'des': row['description'],
		'loc': row['location'],
		'event_type': row['event_type'],
		'org_hosts': org_hosts
	    })
        dayEvents.append((days[dayIndex] + " - " + convertDate(date) , events))
        dayIndex += 1
    return dayEvents



'''
getFilteredEvents
    Parameters:
        (1) filterInfo - A dictionary of all the information that the user inputted to filter the events by

    Returns a list of dictionaries where each dictioanry represents an event that is associated with the queries that the user entered.
'''
def getFilteredEvents(filterInfo):
    conn = getConn()
    curs = conn.cursor((MySQLdb.cursors.DictCursor))
    
    #Getting the events based upon the organization information entered
    orgName = filterInfo["org-name"]
    orgType = filterInfo["org-type"]
    queried = False
    if orgName != "" and orgType != "Choose One":
        curs.execute("select * from orgs where name like %s and org_type like %s", ("%" + orgName + "%", orgType))
        queried = True
    elif orgName != "":
        curs.execute("select * from orgs where name like %s", ("%" + orgName + "%",))
        queried = True
    elif orgType != "Choose One":
        curs.execute("select * from orgs where org_type like %s", (orgType,))
        queried = True
    
    eventIds_org = []
    if queried: #if the user entered queries for the organizations
        #get the information and fetch all of the event ids. 
        orgs = curs.fetchall()
        for o in orgs:
            curs.execute("select event_id from orgs_events where org_id=%s", (o["org_id"],))
            events = curs.fetchall()
            for e in events:
                eventIds_org.append(e["event_id"])
    
    #Get all the events associated with the data the user entered for the event
    eName = filterInfo["event-name"]
    date = filterInfo["date"]
    eType = filterInfo["event-type"]
    
    selects = [] #the columns
    information = []  #the information associated with the column
    if eName != "":
        selects.append("name")
        information.append("%" + eName + "%")
    if date != "":
        selects.append("event_date")
        information.append(date)
    if eType != "Choose One":
        selects.append("event_type")
        information.append(eType)
    
    eventQuery = ""
    for select in selects: #create the query
        eventQuery += "and " + select + " LIKE %s "

    eventIds_event = []
    if eventQuery != "": #if the query has something we can look for
        eventQuery = eventQuery[3::] #remove the and in the beginning
        #execute the query
        curs.execute("select event_id from events where " + eventQuery, tuple(information))
        events = curs.fetchall()
        #get all the event ids of all the events associated with the given information
        for e in events:
            eventIds_event.append(e["event_id"])

    allEvents = []
    #If information was entered to search within organizations and the events
    if eventIds_org != [] and eventIds_event != []:
        intersection = [] #Find the intersection of event ids between them
        #As in it is in both the lists
        for eId in eventIds_org:
            if eId in eventIds_event:
                intersection.append(eId)
        allEvents += extractInfoFromEventIds(intersection)
    #only information for the organization was entered
    elif eventIds_org != []:
        allEvents += extractInfoFromEventIds(eventIds_org)
    #only information for the event was entered
    elif eventIds_event != []:
        allEvents += extractInfoFromEventIds(eventIds_event)
    return allEvents


'''
extractInfoFromEventIds
    Parameters:
        (1) eventIds - a list of all the eventIds
    
    Returns a list of dictionaries, where each dictionary represents an event that was represented in the eventIds list. The dictionary should have all the information regarding the event.
'''
def extractInfoFromEventIds(eventIds):
    conn = getConn()
    curs = conn.cursor((MySQLdb.cursors.DictCursor))
    events = []
    for eId in eventIds:
            curs.execute("select * from events where event_id = %s", (eId,))
            event = curs.fetchone()
            eventInfo = {"event_id": event["event_id"],
                         "name": event["name"],
                         "date": event["event_date"],
                         "start": convertTime(event["time_start"]),
                         "loc": event["location"],
                         "org_hosts": getOrgHosts(event["event_id"])}
            events.append(eventInfo)
    return events
        
        
    

'''
getEmails
    Paramters:
        (1) event_id - the event id

    Given an event id, this function returns a list of lists, which provide
    information on the type of email and the email itself: organization email
    or head contact's email.
''' 
def getEmails(event_id):
    conn = getConn()
    curs = conn.cursor((MySQLdb.cursors.DictCursor))
             
    # get org_id
    curs.execute('select * from orgs_events where event_id=%s', (event_id))
    row = curs.fetchone()
    org_id = None
    if row['org_id'] is None:
        return org_id
    else:
         org_id = row['org_id']

    #get org's email
    curs.execute('select * from orgs where org_id=%s', (org_id))
    row = curs.fetchone()
    org_email = None
    if row['email'] is not None:
	org_email = str(row['email'])

    #get org head's email
    curs.execute('select email from head_contacts where bnumber=(select bnumber from orgs_contacts where org_id=%s order by date_added DESC LIMIT 1)', (org_id))
    row = curs.fetchone()
    head_email = None
    if row['email'] is not None:
   	head_email = str(row['email'])
    emails = [['Organization', org_email], ['Head Contact', head_email]]
    return emails
 
'''
allowed_file
    Parameters:
        (1) filename - the name of the file, string
        (2) allowed - the list of allowed extensions (list of strings)

    Given the filename and list of allowed extensions, find out if the 
    file the user is trying to upload is allowed
'''
def allowed_file(filename, allowed):
    return "." in filename and \
        filename.rsplit(".", 1)[1] in allowed

'''
getFilename
    Parameters:
        (1) spam - the name of the spam (a file)
        (2) allowed - the list of allowed extensions
        (3) folder - the path to where the file is located

    Given a spam name, the list of allowed extensions, and path to file,
    Find out if the file's extension is allowed, ensure it is below the
    limit we have, and create a random name for the file. Returns the name
    of the file (just incase there is the same name for many files).
    Otherwise, if the extension is not allowed, return none.
'''
def getFilename(spam, allowed, folder):
    if spam.filename == '':
	return "No spam"
    if spam and allowed_file(spam.filename, allowed):
	spamName = secure_filename(spam.filename)
	index = spamName.rfind(".")
	name = spamName[:index].replace(".", "")
	ext = spamName[index:]
        spamName = name + ext
	if len(name) > 95:
	    name = name[0:90]
	    spamName = name + ext
 	while os.path.exists(os.path.join(folder, spamName)):
	    index = spamName.rfind(".")
            name = list(name)
            #ext = spamName[index:]
	    random.shuffle(name)
	    spamName = "".join(name) + ext
	return spamName
    else:
	return None


