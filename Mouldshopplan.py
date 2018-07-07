#!/usr/bin/env python3
import requests
from datetime import datetime
from dateutil.parser import parse


# In[173]:


def lambda_handler(event, context):
    # TODO implement
    #hex = hashlib.sha256((event['queryStringParameters']['string']+salt).encode('UTF-8')).hexdigest()
    name=event['queryStringParameters']['name']
    date=event['queryStringParameters']['date']
    output=findworks(getarray(),name,date)
    response ={"statusCode": 200,"headers": {"my_header": "my_value"},"body": str(output),"isBase64Encoded": False}
    return response


# In[174]:


#get data from google sheets
def getdata(url='https://docs.google.com/spreadsheets/d/e/2PACX-1vQUZvwS_Uue7j4zfhZcw1AIujz_fZvAh7RSRnmozQJmE6j69-djrGYuZWcGTwGa446b6CtU-k-I3rkh/pub?gid=1649651434&single=true&output=csv'):
    t=requests.get(url)
    t.encoding='utf-8'
    infostring=t.text
    return infostring
##parse google sheet data into array r
def parseIntoArray(infostring):
    line = infostring.split('\r\n')
    s = []
    for i in line:
        s.append(i.split(','))
    return s
def getarray():
    return parseIntoArray(getdata())
def testGetdata():
    print(getarray())
def convertTodate(datestring):
    try:
        d=datetime.strptime(datestring,'%d-%b-%Y')
    except:
        d="error"
    return d
def findworks(data,workername,todaystring):
    today=parse(todaystring, fuzzy=True)
    printout = ''
    for i,j in enumerate(data):
        try:
            condition1= j[11]==workername
            condition2= j[0]!='finished'
            condition3= convertTodate(j[6]) <= today
            condition4= j[12]==workername
            if (condition1 * condition2 * condition3)or(condition4 * condition2 * condition3): 
                if printout != '':
                    printout +='\n'
                printout += j[3]
        except:
            continue
    return printout
#findworks(getarray(),'A ปรีชา','2 jul 18')


# In[175]:


#findworks(getarray(),'G ทวี','2 jul 18')

