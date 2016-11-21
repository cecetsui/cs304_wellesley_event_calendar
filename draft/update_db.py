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


'''
set up database connection and return cursor
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
adds a new organization to the orgs table
'''
def addOrg(name, des, email, website, org_type):
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
  	curs.execute('insert into orgs(name, description, email, website, org_type) values (%s, %s, %s, %s, %s)', (name, des, email, website, org_typ,))
    	return None
    else:
	return name

'''
returns the list of all currently registered organizations
'''
def getOrgsList():
    conn = getConn()
    curs = conn.cursor((MySQLdb.cursors.DictCursor))
    curs.execute('select org_id, name from orgs')
    orgs = []
    while True:
	row = curs.fetchone()
	if row is None:
   	    return orgs
	else:
	    orgs.append((unicode(row['org_id']), unicode(row['name'])))


'''
returns the list of all events for the week
TO DO: add parameters for start day, and end day
for now, it returns all the events in the events table
along with the hosting orgs 
'''
def getWeekEvents():
    conn = getConn()
    curs = conn.cursor((MySQLdb.cursors.DictCursor))
    curs.execute('select * from events')
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
Returns all orgs that are hosting this event
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
	    return orgs[0]
	else:
	    orgs.append(row['org_id'])



'''
adds new event into the events table
returns this event's event_id 
'''
def insertEvent(org_id, name, date, start, end, loc, des, spam, event_type):
    conn = getConn()
    curs = conn.cursor((MySQLdb.cursors.DictCursor))
    #check that the event already exists
    curs.execute('select * from events where name=%s and event_date=%s and location=%s', (name, str(date), loc))
    row = curs.fetchone()
    #if event does not exist, insert into events table
    if row is None:
	# add event into events table
	curs.execute('insert into events(spam, name, event_date, time_start, time_end, description, location, event_type) values (%s, %s,%s, %s, %s, %s, %s, %s)', (spam, name, date, start, end, des, loc, event_type))
	# find this new event's id
	curs = conn.cursor((MySQLdb.cursors.DictCursor))
	#curs.execute('select event_id from events where name=%s and event_date=%s and time_start=%s', (name, date, start,))
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











