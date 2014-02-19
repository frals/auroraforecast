#!/usr/bin/python
import urllib2
import re
import datetime

BASE_URL = "http://www.gi.alaska.edu/AuroraForecast/Europe/"

def get_response(dyn = None):
    request = urllib2.Request(BASE_URL + dyn, headers={"Accept" : "text/html", "Cookie": "aurora_view=3", "User-Agent": "Mozilla/5.0 (Windows NT 6.3; WOW64; rv:26.0) Gecko/20100101 Firefox/26.0"})
    html = urllib2.urlopen(request).read()
    return html

def get_activity_from_html(html):
    pattern = "<div class=\"levels\">(.*)</div>"
    match = re.search(pattern, html)
    if match == None:
        noforecast = "<div class=\"no-forecast\">(.*)</div>"
        match = re.search(noforecast, html)

    return match.groups()[0]

def get_activity_level(actstring):
    actlevel = re.search("level-([0-9])l", activity)
    if actlevel == None:
        print "No forecast for date"
        return None
     
    return actlevel.groups()[0]

if __name__ == '__main__':
    today = datetime.date.today()
    for x in range(0, 5):
        datetocheck = today + datetime.timedelta(days=x)
        html = get_response(str(datetocheck.year) + "/" + str(datetocheck.month) + "/" + str(datetocheck.day));
        activity = get_activity_from_html(html)
        actlevel = get_activity_level(activity)
        if actlevel != None and int(actlevel) >= 4:
            print "%s: Aurora might be visible. Activity level: %s" % (datetocheck, actlevel)
