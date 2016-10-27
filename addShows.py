import pymysql
import urllib2
import xml.etree.ElementTree as ET


connection = pymysql.connect(host="127.0.0.1",
                             user="root",
                             password="root",
                             db="spoiless",
                             charset='utf8mb4',
                             port=8889,
                             cursorclass=pymysql.cursors.DictCursor)

cursor = connection.cursor()

#shows txt file

f = open("allShowsList.txt", "r")

allData = f.read()
listOfShows = allData.split("\n")
listOfShows = filter(lambda x: x!="",listOfShows)

print len(listOfShows),listOfShows[0]


def extractTVDBdata(title):
    baseurl = "http://thetvdb.com/api/GetSeries.php?seriesname="
    title = str(title.replace(" ","%20"))
    url = baseurl+title
    #making the url actually able to produce something.
    #print url
    try:
        print title
        

        xmlstring = urllib2.urlopen(url).read()

        #print xmlstring[0:30]
        #print xmlstring
        root = ET.fromstring(xmlstring)
        #print root.tag
        try:

            series = root.find('Series')

            data = {}
            data['seriesid'] = series.find('seriesid').text
            data['language'] = series.find('language').text
            data['SeriesName'] = series.find('SeriesName').text
            data['Overview'] = series.find('Overview').text
            data['FirstAired'] = series.find('FirstAired').text
            data['Network'] = series.find('Network').text
            data['IMDB_ID'] = series.find('IMDB_ID').text
            data['zap2it_id'] = series.find('zap2it_id').text
            sql_query = "INSERT INTO shows (seriesid,language,SeriesName,Overview,FirstAired,Network,IMDB_ID,zap2it_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",data['seriesid'],data['language'],data['SeriesName'],data['Overview'],data['FirstAired'],data['Network'],data['IMDB_ID'],data["zap2it_id"]

            #sql_query += data['seriesid']+"','"+data['language']+"','"+data['SeriesName']+"','"+data['Overview']+"','"+data['FirstAired']+"','"+data['Network']+"','"
            #sql_query += data['IMDB_ID']+"','"+data["zap2it_id"]+"');"
            #print sql_query
            execution_reciept = cursor.execute(sql_query[0],sql_query[1:])
            return data
        except AttributeError:
            return {"success":False}

    except urllib2.HTTPError as err:
        return {"success":False}

for show in listOfShows:

    extractTVDBdata(show)


connection.commit()
connection.close()
