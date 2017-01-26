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

mon_fichier = open("COPY_YOUR_MAIL_HERE.html", "r+")
contenu = mon_fichier.read()
longitude = []
latitude = []

strong = ""
strang = ""

my_ip = urllib.request.urlopen('http://ip.42.pl/raw').read()
my_ip=bytes.decode(my_ip)

ip = re.findall(r'[0-9]+(?:\.[0-9]+){3}', contenu)
ip_sans = set(ip)
ip_sans = list(ip_sans)

for n in range(len(ip_sans)):
    url = ("http://ip-api.com/xml/%s" %(ip_sans[n]))
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
    strong = strong + ("var myLatLng%s = {lat: %s, lng: %s};" % (i , latitude[i], longitude[i]))
soup.body.append(strong)
soup.body.append("var map = new google.maps.Map(document.getElementById('map'),{zoom: 4,center: myLatLng0});")
for j in range(len(longitude)):
    strang = strang + ("var marker = new google.maps.Marker({position: myLatLng%s,map: map,title: 'myLatLng%s'});" % (j,j))
soup.body.append(strang)
soup.body.append('}</script><script async defer src="https://maps.googleapis.com/maps/api/js?key=AIzaSyDwz_tf40NpSWZ11pZW33kJtD-cTAcwvJM&signed_in=true&callback=initMap"></script>')


with open("gmaps_temp.html", "w") as outf:
    outf.write(str(soup))


# Read in the file
filedata = None
with open('gmaps_temp.html', 'r') as file :
  filedata = file.read()

# Replace the target string
filedata = filedata.replace('&lt;', '<')
filedata = filedata.replace('&gt;', '>')

# Write the file out again
with open('gmaps_temp.html', 'w') as file:
  file.write(filedata)

webbrowser.open_new("gmaps_temp.html")


print("\n")
print(" IP addresses found in mail header :")
print("\n")
for i in range(len(ip_sans)):
    if ip_sans[i] != my_ip:
        print ("     * %s" % ip_sans[i])
