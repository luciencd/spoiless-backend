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

connection = pymysql.connect(host="127.0.0.1",
                             user="root",
                             password="root",
                             db="spoiless3",
                             charset='utf8mb4',
                             port=8889,
                             cursorclass=pymysql.cursors.DictCursor)
cursor = connection.cursor()
##here we accept changes to the user configurations via requests from the front end.

##use flask.

app = Flask(__name__)
CORS(app)
port = int(os.getenv('VCAP_APP_PORT', 8080))

def getConnection():
    return
def checkAPIkey(api_key):
    return True

@app.route('/getShows',methods=['GET','POST'])
def getShows():
    sql_query = "SELECT seriesid,seriesName FROM shows;"

    cursor.execute(sql_query)

    json_result = {"Shows":[]}

    result = cursor.fetchall()
    for row in result:
        json_result["Shows"].append(row)

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

    json_result = {"id":result["user_id"]}

    #getting the most recent auto_incremented value in users.
    #create user in sql database.
    connection.commit()
    return json.dumps(json_result)

@app.route('/addUserSpoiler',methods=['GET','POST'])
def addUserSpoiler():
    user_id = request.args.get('user_id')
    api_key = request.args.get('api_key')
    series_id = request.args.get('series_id')
    ##check key to make sure user is who he says he is.
    if(checkAPIkey(api_key)):
        ##parametrising the API data
        sql_query = "INSERT INTO userspoilers (user_id,series_id,current) VALUES (%s,%s,1);",int(user_id),int(series_id)
        sql_query = sql_query[0]%tuple(sql_query[1:])
        print sql_query

        ##If query returns wrong result, must return failure.
        result = cursor.execute(sql_query)


        json_result = {"Response":{"Type":"addUserSpoiler","user_id":user_id,"series_id":series_id,"current":True,"return":"Access Granted"}}

        ##committing transaction
        connection.commit()
        return json.dumps(json_result)
    else:
        ##not allowed action.
        return {"Response":{"Type":"add",\
                            "Asset":"series",\
                            "series_id":series_id,\
                            "user_id":user_id,\
                            "return":"Access Denied"}}


    ##return well formed json to confirm addedge

@app.route('/removeUserSpoiler',methods=['GET','POST'])
def removeUserSpoiler():
    user_id = request.args.get('user_id')
    api_key = request.args.get('api_key')
    series_id = request.args.get('series_id')
    ##check key to make sure user is who he says he is.
    if(checkAPIkey(api_key)):

        sql_query = "DELETE * FROM userspoilers user_id=%s AND series_id=%s;",int(user_id),int(series_id)
        sql_query = sql_query[0]%tuple(sql_query[1:])
        print sql_query

        ##If query returns wrong result, must return failure.
        result = cursor.execute(sql_query)


        json_result = {"Response":{"Type":"removeUserSpoiler","user_id":user_id,"series_id":series_id,"current":False,"return":"Access Granted"}}

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
        return result
    else:
        ##not allowed action.
        return {"yes":"False"}

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
        return {"yes":"True"}
    else:
        ##not allowed action.
        return {"yes":"False"}

@app.route('/getUserSpoilers',methods=['GET','POST'])
def getUserSpoilers():
    user_id = request.args.get('user_id')
    api_key = request.args.get('api_key')
    if(checkAPIkey(api_key)):
        sql_query = "SELECT * FROM userspoilers WHERE user_id = %s",int(user_id);
        sql_query = sql_query[0]%tuple(sql_query[1:])
        print sql_query
        result = cursor.execute(sql_query)

        result = cursor.fetchall()
        json_result = {"Series":[],"user_id":user_id}#what if I want to return the name too? should i duplicate it in the table or something?
        #should i just return ids to the controller, and then the controller can find the ids in the giant json list
        #we sent originally?
        for row in result:
            json_result["Series"].append(row)

        connection.commit()
        print json_result
        print "AAAAAAABBBBBBBB"
        return json.dumps(json_result)
    else:
        ##not allowed action.
        return {"yes":"False"}

if __name__ == '__main__':
    #analyzeTweets('yahoo',10000,"")
    app.run(host='0.0.0.0', port=port)
