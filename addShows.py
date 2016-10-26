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
    url = baseurl+str(title.replace(" ","%20"))
    #making the url actually able to produce something.
    print url
    xmlstring = urllib2.urlopen(url).read()
    print xmlstring
    root = ET.fromstring(xmlstring)
    print root.tag
    series = root.find('Series')

    data = {}
    data['seriesid'] = series.find('seriesid').text
    data['language'] = series.find('language').text
    data['SeriesName'] = series.find('SeriesName').text
    data['Overview'] = series.find('Overview').text
    data['FirstAired'] = series.find('FirstAired').text
    data['Network'] = series.find('Network').text
    data['IMDB_ID'] = series.find('IMDB_ID').text
    data['zap2id_id'] = series.find('zap2it_id').text
    
    return data
    
    
    
    

extractTVDBdata(listOfShows[0])
