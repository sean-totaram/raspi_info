from pymongo import MongoClient
from datetime import datetime
from pytz import timezone
import os
import time

#gets CPU temp
def getTemp():
    res = os.popen('vcgencmd measure_temp').readline()
    return(res.replace("temp=","").replace("'C\n",""))

#gets freespace
def getSpace():
    p = os.popen("df -h /")
    i = 0
    while 1:
        i = i +1
        line = p.readline()
        if i==2:
            return(line.split()[3])

#gets information to post
def getPost(fmt):
    post = {"time":date.strftime(fmt),
            "temp":getTemp(),
            "free space":getSpace()
           }
    return post

#username and password for MongoDB
usr = input("Please enter Username\n")
pwd = input("Please enter Password\n")

#sets datetime to Eastern Time Zone
tz = timezone('EST')
date = datetime.now(tz)

#formats datetime to YYYY-MM-DD HH:MM:SS
fmt = "%Y-%m-%d %H:%M:%S"
timestart = time.time()

#connect to Mongo Server
client = MongoClient("mongodb://192.168.1.240:27017", username = usr, password = pwd)
db = client.raspi
collection = db.pitemp

post = getPost(fmt)
db.pitemp.insert(post)

while True:
    timenow = time.time()
    #write to DB every 30 mins
    if (timenow - timestart) >= 1800.00000000:
        post = getPost(fmt)
        db.pitemp.insert(post)
        timestart = time.time()
