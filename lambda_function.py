
# coding: utf-8

# In[118]:


import gspread
from oauth2client.service_account import ServiceAccountCredentials
import re
from xlsxwriter.utility import xl_rowcol_to_cell
import pprint
import requests
from datetime import datetime
from dateutil.parser import parse
import re
import time


# In[119]:

def lambda_handler(event, context):
    # TODO implement
    #hex = hashlib.sha256((event['queryStringParameters']['string']+salt).encode('UTF-8')).hexdigest()
    #name=event['queryStringParameters']['name']
    #date=event['queryStringParameters']['date']
    #output=findworks(getarray(),name,date)
    #if output=='':
    #    output="no work"
    #response ={"statusCode": 200,"headers": {"my_header": "my_value"},"body": str(output),"isBase64Encoded": False}
    #return response
    t0=time.time()
    #get the worksheet
    gc = authenticate()
    ss = gc.open_by_key('1viBmXjVgHwbm5mbHQglLJH1g8rMDXKwceBlYJtKVy8k')
    ws = ss.worksheet('mould shop autoplan2')

    #updatevalue
    updatevalue(createinput(getarray(),ws),ws)
    return time.time()-t0

##### convert numerical column and row to a1 text label
def rowtolabel(row,column):
    return xl_rowcol_to_cell(row-1,column-1)


# In[120]:


def authenticate():
    scope = ['https://spreadsheets.google.com/feeds',
        'https://www.googleapis.com/auth/drive']
    credentials = ServiceAccountCredentials.from_json_keyfile_name('Test1-346bf3e76a74.json',scope)
    return gspread.authorize(credentials)


# In[121]:


## find work for each column

def getworklink(arrayinput,outputcol,i,j):
    return findworks(arrayinput,outputcol[i][j][0],outputcol[i][j][1])

######create input array for the date and name
def createinput(arrayinput,ws):
    #get all data in the sheet for checking
    dat=ws.get_all_values()
    #pp=[i for i in dat]
    name=[]
    date=dat[3]
    for i in dat:
        if i[0]== None:
            name.append("")
        else:
            name.append(i[0])
    # Creates a list containing 5 lists, each of 8 items, all set to 0
    w, h = len(date), len(name);
    outputcol = [[0 for x in range(w)] for y in range(h)] 

    for i,n in enumerate(name):
        outputcol.append("")
        for j,d in enumerate(date):
            if (n and d) and n != ' ' and d != ' ':
                outputcol[i][j]=[n,d]
                work=getworklink(arrayinput,outputcol,i,j)
                if not work:
                    outputcol[i][j].append("no work")
                else:
                    outputcol[i][j].append(work)
                #ws.update_cell(i,j+1,outputcol[i][j][2])
            else:
                outputcol[i][j]=''
    #print(name)
    #print(date)
    #print(outputcol)
    return outputcol
#arrayinput=getarray()
#createinput(arrayinput)


# In[116]:


##########run this function#########
def updatevalue(arrayinput,ws):
    cell_list = ws.range('e6:r22')
    for cell in cell_list:#cell = ws.cell(1,2)
        cell.value=arrayinput[cell.row-1][cell.col-1][2]
        oldval=cell.value
        #cell.value="new cell value"+str(20+cell.row)
        #print(xl_rowcol_to_cell(cell.row-1,cell.col-1),cell.value)
        #print ('the cell column %s row %s was updated from %s to %s label %s' %(cell.col,cell.row,oldval,cell.value,xl_rowcol_to_cell(cell.row-1,cell.col-1)))
    ws.update_cells(cell_list)
    #print([i.value for i in cell_list])
#updatevalue(createinput(getarray()))


# In[124]:


#convert column and row to letter
#rowtolabel(2,1)


# In[130]:


#get data from google sheets

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
##get data and parse into array##
def getarray():
    return parseIntoArray(getdata())
## converting date and time to datetime string
def convertTodate(datestring):
    try:
        d=datetime.strptime(datestring,'%d-%b-%Y')
    except:
        d="error"
    return d
##find work using the if elsif function

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


# In[131]:




