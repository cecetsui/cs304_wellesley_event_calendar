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
import time


'''
getConn
    Parameters: 
        None.
    
    Set up database connection and return cursor.
'''
def getConn():
    #dsn = dsn.dsn
    dsn = dbconn.read_cnf('/home/cs304/.my.cnf')
    dsn['db'] = 'eventscal_db'
    conn = dbconn.connect(dsn)
    conn.autocommit(True)
    #curs = conn.cursor((MySQLdb.cursors.DictCursor)
    return conn

'''
adds the org's contact into the table (president) 
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
        print "###############"
        print name
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
    if name == "": #required field missing
	return 'error'

    conn = getConn()
    curs = conn.cursor((MySQLdb.cursors.DictCursor))
    '''
    check if org exists by searching exact matching names
    names of orgs are usually unique
    '''
    curs.execute('select * from orgs where name=%s', (name,))
    row = curs.fetchone()
    #if org does not exist, insert into orgs table
    if row is None:
  	curs.execute('insert into orgs(name, description, email, website, org_type) values (%s, %s, %s, %s, %s)', (name, des, email, website, org_type,))
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
    curs.execute('select * from orgs_contacts where org_id=%s',(orgid,))
    bnum = curs.fetchone()
    bnum = bnum["bnumber"]
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
                   "org-contact":org_contact["name"],
                   "org-cont-bnum": org_contact["bnumber"],
                   "org-cont-email": org_contact["email"],
                   "org-cont-type": cont_type_options
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
    if row is None:
        curs.execute('insert into orgs_contacts(org_id, bnumber, date_added) values (%s, %s, %s)', (orgid, bnum, time.strftime("%Y-%m-%d %H:%M:%S")))
    

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
    
    Gets all the currently registered (and stored in the database) events. Returns a tuple where the first element is the name of hte organization associated with all the events, and the second element is the list of events it holds. Each event in the list is represented by a tuple where the first element is the link to find more information about the event and the second element is the name of the event.
''' 
def getEvents(orgid):
    conn = getConn()
    curs = conn.cursor((MySQLdb.cursors.DictCursor))
    curs.execute('select event_id from orgs_events where org_id=%s', (orgid,))
    event_ids = curs.fetchall()
    events = []
    for event in event_ids:
        curs.execute('select * from events where event_id=%s', (event["event_id"], ))
        eventInfo = curs.fetchone()
        single_event = ("/event_info/" + str(eventInfo["event_id"]), eventInfo["name"])
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

    Gets all the current information (from the database) of the event. The org_id is represented as a list where the org it is attached to first is the first in the list. In addtion, the event type is represented as a list where the type of the event (as per held from the database) is the first in the list. This is such that when creating the form and having the drop down, the event type and org that the event is attached to is shown.
'''
def getEventInfo(event_id):
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

    
    eventInfo = {"org-id": allOrgs,
                     "event-name": event["name"],
                     "event-date": event["event_date"],
                     "event-startTime": event["time_start"],
                     "event-endTime": event["time_end"],
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
    while True:
	row = curs.fetchone()
	if row is None:
   	    return orgs
	else:
	    orgs.append((unicode(row['org_id']), unicode(row['name'])))


'''
getWeekEvents
    Parameters: None

    Returns the list of all events for the week. Each event is represented as a dictionary.

TO DO: add parameters for start day, and end day
for now, it returns all the events in the events table
along with the hosting orgs 
'''
def getWeekEvents():
    conn = getConn()
    curs = conn.cursor((MySQLdb.cursors.DictCursor))
    curs.execute('select * from events order by event_date, time_start, name ASC')
    events = []
    while True:
	row = curs.fetchone()
	if row is None:
	    return events
	else:
	    org_hosts = getOrgHosts(row['event_id'])
	    events.append({
		'event_id': row['event_id'],	
		'name': row['name'],
		'date': row['event_date'],
		'spam': row['spam'],
		'start': row['time_start'],
		'end': row['time_end'],		
		'des': row['description'],
		'loc': row['location'],
		'event_type': row['event_type'],
		'org_hosts': org_hosts
	    })


'''
getOrgHosts
    Parameters: 
        (1) event_id - the id of the event as from registration

    Returns al list of all names of the orgs that are hosting this event.
'''
def getOrgHosts(event_id):
    conn = getConn()
    curs = conn.cursor((MySQLdb.cursors.DictCursor))
    curs.execute('select org_id from orgs_events where event_id=%s', (event_id,))
    orgs = []
    while True:
	row = curs.fetchone()
	if row is None:
	    #return orgs
	    return orgs
	else:
	    orgs.append(getOrgName(row['org_id']))


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
	curs = conn.cursor((MySQLdb.cursors.DictCursor))
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
	    curs.execute('select event_id from events where name=%s', (name,))
	    this_event = curs.fetchone()
	    event_id = this_event['event_id']
	    # add into orgs_events relationship between org and event ???	
	    curs = conn.cursor((MySQLdb.cursors.DictCursor))
	    curs.execute('insert into orgs_events(org_id, event_id) values (%s, %s)', (int(org_id), int(event_id)))
	    return event_id

    #else, event already exists, return event_id
    else:  	 
	return row['event_id']











