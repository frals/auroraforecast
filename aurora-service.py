#!/usr/bin/python
import urllib2
import re
import datetime

import lxml.html
from lxml.cssselect import CSSSelector


BASE_URL = "http://www.aurora-service.eu/aurora-forecast/"
KP_THRESHOLD = 4

def get_response():
    request = urllib2.Request(BASE_URL, headers={"Accept" : "text/html", "User-Agent": "Mozilla/5.0 (Windows NT 6.3; WOW64; rv:26.0) Gecko/20100101 Firefox/26.0 frals/aurora-spy"})
    html = urllib2.urlopen(request).read()
    return html

def get_forecast_from_html(html):
    tree = lxml.html.fromstring(html)
    sel = CSSSelector('.transtab > pre:nth-child(11) > p:nth-child(1) > strong:nth-child(1)')
    forecast = sel(tree)
    forecast = forecast[0].text_content()
    return forecast

def parse_and_print_activity_level_if_above_threshold(forecast):
    # tab separated table, first line is header
    today = datetime.date.today()
    lines = forecast.split("\n")
    visibles = []
    for line in lines:
        if re.search("[\d]{2}-[\d]{2}UT", line) is not None:
            # seems its a forecast line, split on whitespace to get
            # index 0: time, index 1: today, index 2: tomorrow, index 3: day after tomorrow
            # trim whitespace and spliut
            kpvalues = line.rstrip().lstrip().split()
            time = kpvalues[0]
            # first index = time, so lets remove it
            kpvalues = kpvalues[1:]
            # and to Integer land we go
            kpvalues = [int(x) for x in kpvalues]
            auroras = [("%s %s: Aurora might be visible: KP %d" % (today + datetime.timedelta(days=index), time, x)) if x >= KP_THRESHOLD else None for index, x in enumerate(kpvalues)]
            for forecast in [x for x in auroras if x is not None]:
                visibles.append(forecast)
    for vis in sorted(visibles):
        print vis


if __name__ == '__main__':
    html = get_response();
    forecast = get_forecast_from_html(html)
    parse_and_print_activity_level_if_above_threshold(forecast)
