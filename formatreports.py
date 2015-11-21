#!/usr/bin/python
# -*- coding: utf-8 -*-
import re
import csv
from geopy.geocoders import Nominatim
from geopy.geocoders import GoogleV3

geolocator = Nominatim()
googlocator = GoogleV3()

months = {
    'Janvier': '01',
    'Fevrier': '02',
    'Mars': '03',
    'Avril': '04',
    'Mai': '05',
    'Juin': '06',
    'Juillet': '07',
    'Aout': '08',
    'Septembre': '09',
    'Octobre': '10',
    'Novembre': '11',
    'Decembre': '12'
    }

nonlocs = []

fin = open('infile.txt', 'rb')
rowtext = fin.read()
for month in months:
    rowtext = rowtext.replace(month, '/{}/'.format(months[month]))
rowtext = rowtext.replace(' /', '/')
rowtext = rowtext.replace('/ ', '/')
rows = rowtext.split('\r')
fin.close()

fout = open('outfile.csv', "wb")
csvout = csv.writer(fout, quoting=csv.QUOTE_NONNUMERIC)
csvout.writerow(['date', 'text'])

rowdate = ''
rowcontent = ''
for rawrow in rows:
    row = rawrow.strip()
    if row != '' and row[0] == '-' and len(re.findall('[0-9]', row)) > 0:
        # print("{} content: {}".format(rowdate, rowcontent))
        csvout.writerow([rowdate[1:].strip(), rowcontent])
        rowsplit = row.split("\xca:")
        rowdate = rowsplit[0]
        if len(rowsplit) > 1:
            rowcontent = ":".join(rowsplit[1:])
        else:
            rowcontent = ''
    else:
        rowcontent += row

fout.close()

# Some stuff for finding addresses... 
address = "Nairobi, Kenya"
result = geolocator.geocode(address, timeout=10)
if result is None:
    result = googlocator.geocode(address, timeout=10)
if result is None:
    latlon = (0.0, 0.0)
else:
    latlon = (float(result.latitude), float(result.longitude))

