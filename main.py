import calendarAPI
import requests
import os
from os.path import join, dirname
from dotenv import load_dotenv
import datetime
from tqdm import tqdm

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

#Load our enviroment variables
NOTION_KEY = os.environ.get("NOTION_KEY")
CALENDAR_ID = os.environ.get("CALENDAR_ID")
DATABASE_ID = os.environ.get("DATABASE_ID")

headers = {
    "Authorization": NOTION_KEY,
    "Notion-Version": "2022-06-28",
    "Content-Type": "application/json"
}

pages = []

def requestAllDatabaseEntries(start_cursor = ''):
    if start_cursor == '':
        data = {}
    else:
        data = {
            'start_cursor': start_cursor
        }
    databasePages = requests.post(f"https://api.notion.com/v1/databases/{DATABASE_ID}/query", headers=headers, json=data)
    pages.append(databasePages)
    if databasePages.json()["has_more"]:
        next_cursor = databasePages.json()['next_cursor']
        requestAllDatabaseEntries(next_cursor)

service = calendarAPI.createService()

def processDate(date, eventData):
    startDate = datetime.datetime.fromisoformat(date['start'])
    try:
        #We have a start time and an end time
        endDate = datetime.datetime.fromisoformat(date['end'])
        eventData['start']['dateTime'] = startDate.isoformat()
        eventData['end']['dateTime'] = endDate.isoformat()
    except TypeError:
        #We don't have an end date, it's an all day event OR just has a due date
        #If the start date's at 00:00:00, then it's an all day
        #If the start date's at anything else, than its a simple time
        if startDate.strftime("%H:%M:%S") == "00:00:00":
            #All Day Event
            eventData['start']['date'] = startDate.strftime("%Y-%m-%d")
            eventData['end']['date'] = startDate.strftime("%Y-%m-%d")
        else:
            #Point in time
            eventData['start']['dateTime'] = startDate.isoformat()
            eventData['end']['dateTime'] = startDate.isoformat()

def createEventData(page):
    eventData = {
        'start': {
            'timeZone': 'America/Los_Angeles',
        },
        'end': {
            'timeZone': 'America/Los_Angeles',
        }
    }
    
    #Set the event's ID to prevent duplicates
    pageProperties = page["properties"]
    pageID = page['id'].replace('-', '')
    eventData['id'] = pageID

    #Set the event's title to the page's title
    pageTitle = pageProperties['Name']['title'][0]['text']['content']
    eventData['summary'] = pageTitle

    #Get the date and process it
    date = pageProperties['Date']['date']
    processDate(date, eventData)

    return eventData

requestAllDatabaseEntries()

for apiPage in tqdm(pages, desc="API Pagination Blocks"):
    for page in tqdm(apiPage.json()['results'], leave=False, desc="Database Pages"):
        eventData = createEventData(page)
        try:
            calendarAPI.addEvent(service, CALENDAR_ID, eventData)
        except:
            #Already exists, skip
            continue