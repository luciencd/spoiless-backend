from flask import Flask
from flask import request
from flask_cors import CORS, cross_origin

import os
import pymysql
import requests
import json
import networkx as nx
import re
##Get the sql database values from configuration file:

##Use VCAP_SERVICES by IBM to store values on bluemix.
#database = json.loads(os.environ['VCAP_SERVICES'])['cleardb'][0]
#credentials = database['credentials']

'''
connection = pymysql.connect(host=credentials['hostname'],
                             user=credentials['username'],
                             password=credentials['password'],
                             db=credentials['name'],
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

'''


connection = pymysql.connect(host="mysql",
                             user="root",
                             password="root",
                             database= "spoiless",
                             charset='utf8mb4',
                             port=3306,
                             cursorclass=pymysql.cursors.DictCursor)
cursor = connection.cursor()
print "PYTHON STARTING UP ------$$$$66"
###Create database?
sqlSetupQuery = ""
with open("databasedumps/spoiless_2016-11-01.sql", 'r') as inp:
    for line in inp:
        sqlSetupQuery = sqlSetupQuery + line
inp.close()
db = connection.cursor()

db.execute(sqlSetupQuery)

print "PYTHON READ FILE EXECUTED UP ------$$$$66"
more = True
while more:
    print db.fetchall()
    more = db.nextset()
###
connection.commit()
print "PYTHON DATABASE COMMITTED UP ------$$$$66"
##here we accept changes to the user configurations via requests from the front end.

##use flask.

app = Flask(__name__)
CORS(app)


#apparently this will require environment variables?
#port = int(os.getenv('VCAP_APP_PORT', 8080))


def checkAPIkey(api_key):
    return True

@app.route('/')
def hello():
    return "hello"



@app.route('/getShows',methods=['GET','POST'])
def getShows():
    sql_query = "SELECT series_id,seriesName FROM series;"

    cursor.execute(sql_query)

    json_result = {"Success":True,"guid":"randomnumber","Series":[]}

    result = cursor.fetchall()
    for row in result:
        json_result["Series"].append(row)

    connection.commit()
    return json.dumps(json_result)

@app.route('/createUser',methods=['GET','POST'])
def createUser():
    #don't need a user_id
    #user_id = request.args.get('user_id')
    sql_query = "INSERT INTO users (id) VALUES (NULL);"
    cursor.execute(sql_query)
    sql_query = "SELECT LAST_INSERT_ID() AS user_id;"
    cursor.execute(sql_query)

    result = cursor.fetchone()
    print result

    json_result = {"Success":True,"guid":"randomnumber","user_id":result["user_id"]}

    #getting the most recent auto_incremented value in users.
    #create user in sql database.
    connection.commit()
    return json.dumps(json_result)

@app.route('/addUserSpoiler',methods=['GET','POST'])
def addUserSpoiler():
    user_id = request.args.get('user_id')
    api_key = request.args.get('api_key')
    series_id = request.args.get('series_id')
    print user_id,api_key,series_id

    ##check key to make sure user is who he says he is.
    if(checkAPIkey(api_key)):
        ##parametrising the API data
        sql_query = "INSERT INTO userspoilers (user_id,series_id,current) VALUES (%s,%s,1);",int(user_id),int(series_id)
        sql_query = sql_query[0]%tuple(sql_query[1:])
        print sql_query

        ##If query returns wrong result, must return failure.
        result = cursor.execute(sql_query)


        json_result = {"Success":True,"guid":"randomnumber"}#,"Response":{"user_id":user_id,"series_id":series_id,"current":True}}

        ##committing transaction
        connection.commit()
        return json.dumps(json_result)
    else:
        ##not allowed action.
        json_result =  {"Response":{"Type":"add",\
                            "Asset":"series",\
                            "api_key":api_key,\
                            "series_id":series_id,\
                            "user_id":user_id,\
                            "return":"Access Denied"}}
        return json.dumps(json_result)


    ##return well formed json to confirm addedge

@app.route('/removeUserSpoiler',methods=['GET','POST'])
def removeUserSpoiler():
    user_id = request.args.get('user_id')
    api_key = request.args.get('api_key')
    series_id = request.args.get('series_id')
    ##check key to make sure user is who he says he is.
    if(checkAPIkey(api_key)):

        sql_query = "DELETE FROM userspoilers WHERE user_id=%s AND series_id=%s;",int(user_id),int(series_id)
        sql_query = sql_query[0]%tuple(sql_query[1:])
        print sql_query

        ##If query returns wrong result, must return failure.
        result = cursor.execute(sql_query)


        json_result = {"Success":True,"guid":"randomnumber"}#{"Response":{"Type":"removeUserSpoiler","user_id":user_id,"series_id":series_id,"current":False,"return":"Access Granted"}}

        connection.commit()
        return json.dumps(json_result)
    else:
        ##not allowed action.
        return {"yes":"False"}
@app.route('/hideUserSpoiler',methods=['GET','POST'])
def hideUserSpoiler():
    user_id = request.args.get('user_id')
    api_key = request.args.get('api_key')
    series_id = request.args.get('series_id')
    ##check key to make sure user is who he says he is.
    if(checkAPIkey(api_key)):
        sql_query = "UPDATE userspoilers SET current = 0 WHERE user_id=%s AND series_id=%s;",int(user_id),int(series_id)
        sql_query = sql_query[0]%tuple(sql_query[1:])
        print sql_query
        result = cursor.execute(sql_query)
        connection.commit()
        return {"success":True,"guid":"randomnumber"}
    else:
        ##not allowed action.
        return {"success":False,"guid":"randomnumber"}

@app.route('/showUserSpoiler',methods=['GET','POST'])
def showUserSpoiler():
    user_id = request.args.get('user_id')
    api_key = request.args.get('api_key')
    series_id = request.args.get('series_id')
    ##check key to make sure user is who he says he is.
    if(checkAPIkey(api_key)):
        sql_query = "UPDATE userspoilers SET current = 1 WHERE user_id=%s AND series_id=%s;",int(user_id),int(series_id)
        sql_query = sql_query[0]%tuple(sql_query[1:])
        print sql_query
        result = cursor.execute(sql_query)

        connection.commit()
        return {"success":True,"guid":"randomnumber"}
    else:
        ##not allowed action.
        return {"success":False,"guid":"randomnumber"}

@app.route('/getUserSpoilers',methods=['GET','POST'])
def getUserSpoilers():
    user_id = request.args.get('user_id')
    api_key = request.args.get('api_key')
    if(checkAPIkey(api_key)):
        sql_query = "SELECT series_id,seriesName FROM userspoilers NATURAL JOIN series WHERE user_id = %s",int(user_id);
        sql_query = sql_query[0]%tuple(sql_query[1:])
        print sql_query
        result = cursor.execute(sql_query)

        result = cursor.fetchall()
        json_result = {"Success":True,"Series":[]}#what if I want to return the name too? should i duplicate it in the table or something?
        #should i just return ids to the controller, and then the controller can find the ids in the giant json list
        #we sent originally?
        for row in result:
            json_result["Series"].append(row)

        connection.commit()
        print json_result
        return json.dumps(json_result)
    else:
        ##not allowed action.
        return {"success":False,"guid":"randomnumber"}



if __name__ == '__main__':

    app.run()
    #app.run(host='0.0.0.0', port=port)
