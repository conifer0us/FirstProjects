from flask import Flask, jsonify, request
import sqlite3
import os
import hashlib
import time
import re

database = "nease360.db" # Change to db filename (in relation to the current directory)
dbpath = None #Set automatically; do not alter

def create_connection(db_file):
    conn = sqlite3.connect(db_file)
    print(sqlite3.version)
    return conn

def validateHexString(input_str):
    if not re.match("^[a-fA-F0-9]*$", input_str):
        return False
    return True

def hash(string : str): 
    hashlib.sha256(string.encode()).hexdigest()

def getDBValue(db_file, table, column, id : str):
    connection = create_connection(db_file)
    return connection.execute("SELECT {} FROM {} WHERE id='{}'".format(column, table, id)).fetchall()[0][0]

def getLastPostTime(user : str): 
    return getDBValue(dbpath, "users", "last_post", user)

def userExists(user : str) -> bool: 
    tempcursor = create_connection(dbpath)
    tempval = tempcursor.execute('SELECT EXISTS(SELECT 1 FROM users WHERE id="{}");'.format(user)).fetchall()[0]
    tempcursor.close()
    if tempval != 0:
        return True
    else: 
        return False

def setDBAttribute(table : str, user : str, attribute, value):
    tempcursor = create_connection(dbpath)
    if isinstance(value, str):
        tempcursor.execute("UPDATE {} SET {}='{}' where id='{}';".format(table, attribute, value, user))
    else:
        tempcursor.execute("UPDATE {} SET {}={} where id='{}';".format(table, attribute, value, user))
    tempcursor.commit()
    tempcursor.close()

def runSQL(curs, string):
    curs.execute(string)

def configureDB(cursor_obj):
    create_user_table = """ CREATE TABLE IF NOT EXISTS users (
    id CHAR(32) PRIMARY KEY,
    hex CHAR(64),
    last_query integer,
    last_post integer,
    register_time integer
    ); """
    create_report_table = """ CREATE TABLE IF NOT EXISTS reports (
    id CHAR(64) PRIMARY KEY,
    reported_user CHAR(32),
    reported_time integer,
    locationX integer, 
    locationY integer
    ); """
    runSQL(cursor_obj, create_user_table)
    runSQL(cursor_obj, create_report_table)

app = Flask(__name__)

# Next two API endpoints provide generic output
@app.route('/', methods=['GET'])
def returnMain():
    return returnInfo()

@app.route('/info/', methods=['GET'])
def returnInfo():
    return "Welcome to the Nease360 API! Visit nease360.ddns.net/api for documentation.", 200

# Validates User Information and Logs it in the User Database
# Potential User API Usage: 
# POST https://ip/register/ 
# with headers {"User": "random, unused 32 letter ID" , "Hashkey": "sha256 hash of encoded username, validates knowledge of API"}
@app.route('/register/', methods=['POST'])
def registerUser():
    head = request.headers
    if len(head) != 4 or not "User" in head.keys() or not "Hashkey" in head.keys():
        [print(obj) for obj in head.keys()]
        return "Invalid Header Usage", 400
    if not validateHexString(head["User"]) or not validateHexString(head["Hashkey"]):
        return "Invalid Characters", 400
    elif len(head["User"]) != 32 or hash(head["User"]) != head["Hashkey"]:
        return "Malformed User ID", 400
    if userExists(head["User"]):
        return "Cannot Register an Existing User", 400
    tempcursor = create_connection(dbpath)
    tempcursor.execute("INSERT INTO users VALUES ('{}','{}',0,0,{});".format(head["User"], head["Hashkey"], int(time.time())))
    tempcursor.commit()
    tempcursor.close()
    return "User Successfully Registered", 200

# Endpoint for a user to report a location 
# Potential Report API Usage
# POST https://ip/report/
# with headers {"User": "User ID", "LocationX": "Int Location", "LocationY":"Int Location"}
@app.route('/report/', methods=["POST"])
def reportLocation():
    head = request.headers
    requestTime = time.time()
    if len(head) != 5 or "User" not in head.keys() or "LocationX" not in head.keys() or "LocationY" not in head.keys(): 
        return "Invalid Header Information", 400
    if not userExists(head["User"]): 
        return "Malformed User Information", 400
    if (requestTime - getLastPostTime(head["User"])) < 60: 
        return "Please wait at least one minute between posting location reports."
    setDBAttribute("users", head["User"], "last_post", requestTime)
    locationX, locationY = 0
    try: 
        locationX = int(head["LocationX"])
        locationY = int(head["LocationY"])
    except:
        return "Malformed Location Data", 400
    tempcursor = create_connection(dbpath)
    tempcursor.execute("INSERT INTO reports VALUES ('{}','{}',{},{},{});".format(hashlib.sha256().hexdigest(), head["User"], requestTime, locationX, locationY))
    tempcursor.commit()
    tempcursor.close()

if __name__ == "__main__":
    dbpath = os.getcwd() + "/" + database
    conn = create_connection(dbpath) 
    cursor = conn.cursor()
    configureDB(cursor)
    app.run(host='0.0.0.0', port=5000)