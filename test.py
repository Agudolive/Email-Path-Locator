#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import re
import urllib.request
import threading
import pprint
import webbrowser
import json
from datetime import datetime
import time
from shutil import copyfile
import shutil
import os
import fileinput

gmaps = open("gmaps.html", "r+")
content_gmaps = gmaps.read()
with open("gmaps_temp.html", "w") as outr:
    outr.write(content_gmaps)

gmaps.close()

mail_file = open("COPY_YOUR_MAIL_HERE.html", "r+")
contenu = mail_file.read()
longitude = []
latitude = []

tmp_str1 = ""
tmp_str2 = ""

my_ip = urllib.request.urlopen('http://ip.42.pl/raw').read()
my_ip=bytes.decode(my_ip)

ip = re.findall(r'[0-9]+(?:\.[0-9]+){3}', contenu)
clean_ip = set(ip)
clean_ip = list(clean_ip)

for n in range(len(clean_ip)):
    url = ("http://ip-api.com/xml/%s" %(clean_ip[n]))
    localise = urllib.request.urlopen(url).read()
    loc = BeautifulSoup(localise, "html.parser")
    long = str(loc.query.lon)
    long = long[14:-9]
    lat = str(loc.query.lat)
    lat = lat[14:-9]
    if lat != '':
        latitude.append(lat)
    if long != '':
        longitude.append(long)

mon_html = open("gmaps_temp.html", "r+")
contenu_html = mon_html.read()
soup = BeautifulSoup(contenu_html, "html.parser")
soup.body.append(str('<div id="map"></div><script>function initMap(){'))
for i in range(len(longitude)):
    tmp_str1 = tmp_str1 + ("var myLatLng%s = {lat: %s, lng: %s};" % (i , latitude[i], longitude[i]))
soup.body.append(tmp_str1)
soup.body.append("var map = new google.maps.Map(document.getElementById('map'),{zoom: 4,center: myLatLng0});")
for i in range(len(longitude)):
    tmp_str2 = tmp_str2 + ("var marker = new google.maps.Marker({position: myLatLng%s,map: map,title: 'myLatLng%s'});" % (i,i))
soup.body.append(tmp_str2)
soup.body.append('}</script><script async defer src="https://maps.googleapis.com/maps/api/js?key=AIzaSyDwz_tf40NpSWZ11pZW33kJtD-cTAcwvJM&signed_in=true&callback=initMap"></script>')


with open("gmaps_temp.html", "w") as outf:
    outf.write(str(soup))

filedata = None
with open('gmaps_temp.html', 'r') as file :
  filedata = file.read()

filedata = filedata.replace('&lt;', '<')
filedata = filedata.replace('&gt;', '>')

with open('gmaps_temp.html', 'w') as file:
  file.write(filedata)

webbrowser.open_new("gmaps_temp.html")

print("\n")
print(" IP addresses found in mail header :")
print("\n")
for i in range(len(clean_ip)):
    if clean_ip[i] != my_ip:
        print ("     * %s" % clean_ip[i])
