
import pymongo
import random
from datetime import date
from datetime import datetime


mydb = ""
names = ["Sam","John","Xiaho","Jackie","Shaan","Jim","Peter","Arnold","Sanjay","Amir","Jay","Zhang"]
def connect():
  global mydb
  client = pymongo.MongoClient("mongodb+srv://mongouser1:acmmongo21@cluster0.rlyy1.mongodb.net/co2_footprint?retryWrites=true&w=majority&ssl=true&ssl_cert_reqs=CERT_NONE")
  mydb = client["co2_footprint"]

  '''
  read collection data
  Sample query
  myquery = { "name": "Shreyas" }
  '''
def readCollection(collectionName,query):
  if mydb == "": return {}
  mycol = mydb[collectionName]
  mydoc = mycol.find(query)
  result = {}
  ret = []
  for x in mydoc:
    ret.append(x)
    
  return ret

  '''
  insert into collection
  Sample dictionary
  mydict = { "name": "Sam", "date": "11/13/2021", "time":"14:51:00", "classification":["plastic", "teflon"] }
  '''
def insertIntoCollection(items):
  global names
  mycol = mydb["classification"]
  newDict = {}
  newDict["name"] = names[random.randint(0,len(names)-1)]
  
  today = date.today()
  dateNow = today.strftime("%m/%d/%y")
  newDict["date"] = dateNow

  now = datetime.now()
  dt_string = now.strftime("%H:%M:%S")
  newDict["time"] = dt_string

  newItems = []
  for item in items:
    newItem = item.replace(" ","_").lower()
    newItems.append(newItem)

  newDict["items"] = newItems

  x = mycol.insert_one(newDict)

  result = readCollection("carbonEmissionStats", { "name": { "$in": newItems } })
  min_co2 = float('inf')
  max_co2 = -float('inf')
  for kv in result:
    min_co2 = min(min_co2,float(kv["value"]))
    max_co2 = max(max_co2,float(kv["value"]))

  d = {}
  d["min"] = min_co2
  d["max"] = max_co2
  return d

def getTotalEmission():
  all = readCollection("classification",{})
  items = []
  itemCount = {}
  for i in all:
    items.extend(i["items"])
  
  for i in items:
    if i in itemCount:
      itemCount[i] = itemCount[i] + 1
    else:
      itemCount[i] = 1
  
  result = readCollection("carbonEmissionStats", { "name": { "$in": items } })
  min_co2 = float('inf')
  max_co2 = -float('inf')
  #print(itemCount)
  for kv in result:
    min_co2 = min(min_co2,float(kv["value"])*itemCount[kv["name"]])
    max_co2 = max(max_co2,float(kv["value"])*itemCount[kv["name"]])
  
  d = {}
  d["min"] = min_co2
  d["max"] = max_co2
  return d
  
'''
Sample invocation and installation
python -m pip install "pymongo[srv]"
python -m pip install pymongo
username mongouser1
password acmmongo21

connect()
print(readCollection("classification",{"name": "Shreyas" }))
d = { "name": "Sanju", "date": "11/13/2021", "time":"14:51:00", "classification":["plastic", "teflon"] }
x = insertIntoCollection("classification",d)
'''

connect()
