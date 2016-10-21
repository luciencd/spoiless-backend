from flask import Flask
from flask import request
from flask_cors import CORS, cross_origin

import pymysql
import requests
import json
import networkx as nx
import re
##Get the sql database values from configuration file:

##Use VCAP_SERVICES by IBM to store values on bluemix.
database = json.loads(os.environ['VCAP_SERVICES'])['cleardb'][0]
credentials = database['credentials']

connection = pymysql.connect(host=credentials['hostname'],
                             user=credentials['username'],
                             password=credentials['password'],
                             db=credentials['name'],
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
cursor = connection.cursor()
##here we accept changes to the user configurations via requests from the front end.

##use flask.

app = Flask(__name__)
CORS(app)
port = int(os.getenv('VCAP_APP_PORT', 8080))

def getConnection():
    return 
def checkAPIkey():
    return True

@app.route('/getShows',methods=['GET','POST'])
def getShows():
    sql_query = "SELECT id,name,year FROM shows;"
    cursor.execute(sql)

    json_result = {"Shows":[]}
    
    result = cursor.fetchall()
    for row in result:
        json["Shows"].append({"id":row["id"],"name":row["name"],"year":row["year"]})

    return json
    
@app.route('/addUserSpoiler',methods=['GET','POST'])
def addUserSpoiler():
    user_id = request.args.get('user_id')
    api_key = request.args.get('api_key')
    show_id = request.args.get('show_id')
    ##check key to make sure user is who he says he is.
    if(checkAPIkey(api_key)):
        
    else:
        ##not allowed action.
        return {"Response":{"Type":"add",\
                            "Asset":"show",\
                            "show_id":show_id,\
                            "user_id":user_id,\
                            "return":"Access Denied"}}
    

    ##return well formed json to confirm addedge

@app.route('/removeUserSpoiler',methods=['GET','POST'])
def removeUserSpoiler(user_id,api_key,show_id):
    ##check key to make sure user is who he says he is.
    if(checkAPIkey(api_key)):

    else:
        ##not allowed action.

@app.route('/hideUserSpoiler',methods=['GET','POST'])
def hideUserSpoiler(user_id,api_key,show_id):
    ##check key to make sure user is who he says he is.
    if(checkAPIkey(api_key)):

    else:
        ##not allowed action.

@app.route('/showUserSpoiler',methods=['GET','POST'])
def showUserSpoiler(user_id,api_key,show_id):
    ##check key to make sure user is who he says he is.
    if(checkAPIkey(api_key)):

    else:
        ##not allowed action.

@app.route('/getUserSpoilers',methods=['GET','POST'])
def getUserSpoilers(user_id,api_key):
    if(checkAPIkey(api_key)):

    else:
        ##not allowed action.


if __name__ == '__main__':
    #analyzeTweets('yahoo',10000,"")
    app.run(host='0.0.0.0', port=port)
