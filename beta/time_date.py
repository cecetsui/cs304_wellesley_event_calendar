#!/usr/local/bin/python2.7
'''
Grace Hu and Cece Tsui
time_date.py
Wellesley Events Calendar

This file contains methods that are helpful in parsing and manipulating time and dates.
'''

import datetime
import time

'''
getThisWeekDates
    Parameters:
        None
    
    Finds the current date, and based off of that, returns a list
    that contains all the dates within that week, from Monday to Sunday
'''
def getThisWeekDates():
    today = datetime.date.today()
    dates = [str(today + datetime.timedelta(days=i)) for i in range(0 - today.weekday(), 7 - today.weekday())]
    return dates

'''
getWeek
    Parameters:
        (1) date_str - the date string

        Given some date string, return a list that contains
        all the dates within that week, from Monday to Sunday
'''
def getWeek(date_str):
    date = datetime.datetime.strptime(date_str, '%Y-%m-%d').date()
    dates = [str(date + datetime.timedelta(days=i)) for i in range(0 - date.weekday(), 7 - date.weekday())]
    return dates


'''
str_to_datetime
    Parameters:
        (1) monday_sunday_list - a list of 2 dates (in strings)

    Given a list of 2 elements, conver thte stings in it to datetime
    objects. Function returns a dictionary with datetimes of Monday and 
    Sunday.
'''
def str_to_datetime(monday_sunday_list):
    monday = monday_sunday_list[0]
    sunday = monday_sunday_list[1]
    monDate = datetime.datetime.strptime(monday, '%Y-%m-%d')
    sunDate = datetime.datetime.strptime(sunday, '%Y-%m-%d')
    return { 'mon': monDate, 'sun': sunDate}

'''
getDayList

    Parameters:
        (1) monDate - the date for the week's Monday

    Given the date for Monday of a given week, it should return a list of dates for each day in the week (from Monday to Sunday), where each date is represented as a list.
'''
def getDayList(monDate):
    dateList = []
    currentDate = monDate
    for i in range(7):
        day = currentDate + datetime.timedelta(days=i)
        dateList.append(str(day.strftime('%Y-%m-%d')))
    return dateList


'''
str_to_datetime
    Parameters:
        (1) monday_sunday_list - a list of 2 dates (in strings)

    Given a list of 2 elements, conver thte stings in it to datetime
    objects. Function returns a dictionary with datetimes of Monday and 
    Sunday.
'''
def str_to_datetime(monday_sunday_list):
    monday = monday_sunday_list[0]
    sunday = monday_sunday_list[1]
    monDate = datetime.datetime.strptime(monday, '%Y-%m-%d')
    sunDate = datetime.datetime.strptime(sunday, '%Y-%m-%d')
    return { 'mon': monDate, 'sun': sunDate}


'''
getDayList

    Parameters:
        (1) monDate - the date for the week's Monday

    Given the date for Monday of a given week, it should return a list of dates for each day in the week (from Monday to Sunday), where each date is represented as a list.
'''
def getDayList(monDate):
    dateList = []
    currentDate = monDate
    for i in range(7):
        day = currentDate + datetime.timedelta(days=i)
        dateList.append(str(day.strftime('%Y-%m-%d')))
    return dateList


'''
convertTime
    Parameters:
        (1) time_obj - a time object

    Inputs a time object and converts from military time into PM AM format
'''
def convertTime(time_obj):
    string_time = str(time_obj)
    return datetime.datetime.strptime(string_time, '%H:%M:%S').strftime( '%I:%M%p').lower()


'''
convertDate
    Parameters:
        (1) date_obj - a date object

    Converts date object from format YYYY-MM-DD into format: Month day, year
'''
def convertDate(date_obj):
    string_date = str(date_obj)
    d = datetime.datetime.strptime(string_date, '%Y-%m-%d')
    return d.strftime('%B %d, %Y')

'''
getPrevWeekRange
    Parameters:
        (1) monDate - datetime object of Monday
        (2) sunDate - datetime object of Sunday

    Given the datetime objects of Monday and Sunday, return a string of the
    range of days in the previous week.
'''
def getPrevWeekRange(monDate, sunDate):
    updatedMon = monDate - datetime.timedelta(days=7)
    updatedSun = sunDate - datetime.timedelta(days=7)
    previousWeekMon = updatedMon.strftime('%Y-%m-%d')
    previousWeekSun = updatedSun.strftime('%Y-%m-%d')
    updatedWeek = str(previousWeekMon) + '_' + str(previousWeekSun)
    return updatedWeek



'''
getNextWeekRange
    Parameters:
        (1) monDate - the datetime object of Monday
        (2) sunDate - the datetime object of Sunday

    Given the datetime objects of Monday and Sunday, return a string of the 
    range of days in the next week.
'''
def getNextWeekRange(monDate, sunDate):
    updatedMon = monDate + datetime.timedelta(days=7)
    updatedSun = sunDate + datetime.timedelta(days=7)
    nextWeekMon = updatedMon.strftime('%Y-%m-%d')
    nextWeekSun = updatedSun.strftime('%Y-%m-%d')
    updatedWeek = str(nextWeekMon) + '_' + str(nextWeekSun)
    return updatedWeek


'''
timeLeadZero
    Parameters:
        (1) time - the time object

    Given the time object, if the time object is represented as: "#:00:00" where
    "#" is a whole number, add a 0 in the front so that the format is
    acceptable to input into a time field.
'''
def timeLeadZero(time):
    time = str(time)
    tList = time.split(":")
    if len(tList[0]) == 1:
        tList[0] = "0" + tList[0]
    return ":".join(tList)
