# Notion_Calendar_Sync

A Python script to sync a Notion database to Google Calendar

## Notion Setup
Create a database that contains a `Date` property  
Create an integration with the Notion API, and add it to your database

## Environment Setup
### .env File
```
NOTION_KEY = Bearer [YOUR_NOTION_INTEGRATION_KEY]
DATABASE_ID = [YOUR_NOTION_DATABASE_ID]
CALENDAR_ID = [YOUR_GOOGLE_CALENDAR_ID]
```

### Other
Download OAuth Client Credentials to `client_secrets.json`   
[Link to Google Instructions](https://developers.google.com/calendar/api/quickstart/python#:~:text=to%20Dashboard.-,Authorize%20credentials%20for%20a%20desktop%20application,credentials.json%2C%20and%20move%20the%20file%20to%20your%20working%20directory.,-Install%20the%20Google)