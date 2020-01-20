from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import base64
import email
from apiclient import errors
import re
from datetime import datetime, timedelta
import csv

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def main():
    """Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('gmail', 'v1', credentials=creds)

    # Call the Gmail API

      
    # Get messages from date 
    N = 1 # How many days to check
    date_N_days_ago = datetime.now() - timedelta(days=N) 
    format_date = date_N_days_ago.strftime("%Y/%m/%d")
    searchVal = 'after:' + format_date + ' subject:Coffee Brew Stats in:inbox'
    
    Message_ID_List = ListMessagesMatchingQuery(service, 'me',searchVal)
    print(Message_ID_List)
    print(len(Message_ID_List))
    for i in range(len(Message_ID_List)):
      Recent_ID = Message_ID_List[i].get('id')       
      MessageResults = GetMessage(service, 'me', str(Recent_ID))
      Snippet = MessageResults['snippet']
      ExtractData(Snippet)
      print('\nBreak \n')


def ListMessagesMatchingQuery(service, user_id, query=''):
  """List all Messages of the user's mailbox matching the query.

  Args:
    service: Authorized Gmail API service instance.
    user_id: User's email address. The special value "me"
    can be used to indicate the authenticated user.
    query: String used to filter messages returned.
    Eg.- 'from:user@some_domain.com' for Messages from a particular sender.

  Returns:
    List of Messages that match the criteria of the query. Note that the
    returned list contains Message IDs, you must use get with the
    appropriate ID to get the details of a Message.
  """
  try:
    response = service.users().messages().list(userId=user_id,
                                               q=query).execute()
    messages = []
    if 'messages' in response:
      messages.extend(response['messages'])

    while 'nextPageToken' in response:
      page_token = response['nextPageToken']
      response = service.users().messages().list(userId=user_id, q=query,
                                         pageToken=page_token).execute()
      messages.extend(response['messages'])

    return messages
  except errors.HttpError as error:
    print('An error occurred: %s' % error)      


def GetMessage(service, user_id, msg_id):
  """Get a Message with given ID.

  Args:
    service: Authorized Gmail API service instance.
    user_id: User's email address. The special value "me"
    can be used to indicate the authenticated user.
    msg_id: The ID of the Message required.

  Returns:
    A Message.
  """
  try:
    message = service.users().messages().get(userId=user_id, id=msg_id).execute()

    #print('Message snippet: %s' % message['snippet'])

    return message
  except errors.HttpError as error:
    print('An error occurred: %s' % error)

def ExtractData(SnippetData):

  #print(SnippetData)
  try:
    CoffeeMass = re.search('Coffee Mass: (.+?) W',SnippetData)
  except AttributeError:
    print('Failed to find Coffee Mass')
    CoffeeMass = 0
  try:  
    WaterMass = re.search('Water Mass: (.+?) T', SnippetData)
  except AttributeError:
    print('Failed to find Water Mass')
    WaterMass = 0
  try:
    Temperature = re.search('Temperature: (.+?) B', SnippetData)
  except AttributeError:
    print('Failed to find Temperature')
    Temperature = 0
  try:
    BloomTime = re.search('Bloom Time: (.+?) B', SnippetData)
  except AttributeError:
    print('Failed to find Bloom Time')
    BloomTime = 0
  try:
    BrewTime = re.search('BrewTime: (.+?) M', SnippetData)
  except AttributeError:
    print('Failed to find Brew Time')
    BrewTime = 0
  try:
    Method = re.search('Method: (.+?) G', SnippetData)
  except AttributeError:
    print('Failed to find Method')
    Method = 0
  try:
    Grind = re.search('Grind Setting: (.+?) C', SnippetData)
  except AttributeError:
    print('Failed to find Grind Size')
    Grind = 0
  try:
    Company = re.search('CoffeeCompany: (.+?) O', SnippetData)
  except AttributeError:
    print('Failed to find Coffee Company')
    Company = 0
  try:
    Origin = re.search('Origin: (.+?) E', SnippetData)
  except AttributeError:
    print('Failed to find Origin')
    Origin = 0
  try:
    Elev = re.search('Elevation: (.+?) MASL',SnippetData)
  except AttributeError:
    print('Failed to find Elevation')
    Elev = 0

  try:
    foundCM = CoffeeMass.group(1)
    print(foundCM)
    foundWM = WaterMass.group(1)
    print(foundWM)
    foundT = Temperature.group(1)
    print(foundT)
    foundBT = BloomTime.group(1)
    print(foundBT)
    foundBrT = BrewTime.group(1)
    print(foundBrT)
    foundM = Method.group(1)
    print(foundM)
    foundG = Grind.group(1)
    print(foundG)
    foundC = Company.group(1)
    print(foundC)
    foundO = Origin.group(1)
    print(foundO)
    foundE = Elev.group(1)
    print(foundE)
  except AttributeError:
    print('Failed: ', AttributeError)

   
if __name__ == '__main__':
    main()