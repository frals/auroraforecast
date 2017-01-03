#!/usr/bin/python
import urllib2
import re
import datetime

import lxml.html
from lxml.cssselect import CSSSelector


BASE_URL = "http://www.aurora-service.eu/aurora-forecast/"
KP_THRESHOLD = 5

class Forecast:
    def __init__(self, **kwargs):
            self.__dict__ = kwargs

def get_response():
    request = urllib2.Request(BASE_URL, headers={"Accept" : "text/html", "User-Agent": "Mozilla/5.0 (Windows NT 6.3; WOW64; rv:26.0) Gecko/20100101 Firefox/26.0 frals/aurora-spy"})
    html = urllib2.urlopen(request).read()
    return html

def get_forecast_from_html(html):
    tree = lxml.html.fromstring(html)
    sel = CSSSelector('.transtab > pre:nth-child(6)')
    forecast = sel(tree)
    forecast = forecast[0].text_content()
    return forecast

def parse_and_print_activity_level_if_above_threshold(forecast):
    # tab separated table, first line is header
    today = datetime.date.today()
    now = datetime.datetime.utcnow()
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

            ### conver to integer and catch the case when theres a storm: (G1), (G2) etc
            kpvalue = []
            # and to Integer land we go
            for value in kpvalues:
                try:
                    kpvalue.append(int(value))
                except:
                    pass

            kpvalues = kpvalue
            auroras = [(Forecast(date=today + datetime.timedelta(days=index), time=time, kp=x)) if x >= KP_THRESHOLD else None for index, x in enumerate(kpvalues)]
            for forecast in [x for x in auroras if x is not None]:
                # ignore if this forecast is for a time already passed
                hourthreshold = int(time[:2]) 
                if not (forecast.date == now.date() and now.hour > hourthreshold):
                    fcast = ("%s %s: Aurora might be visible: KP %d" % (forecast.date, forecast.time, forecast.kp))
                    visibles.append(fcast)


    for vis in sorted(visibles):
        print vis


if __name__ == '__main__':
    html = get_response();
    forecast = get_forecast_from_html(html)
    parse_and_print_activity_level_if_above_threshold(forecast)
