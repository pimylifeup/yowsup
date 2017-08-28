#!/usr/bin/python
# yowsup utilities for getting new HASH and version number
# Authors: mgp25, MasBog, pimylifeup
# credit : https://github.com/mgp25/classesMD5-64
# Output :
# WhatsApp Version: 2.17.296
# WhatsApp ClassesDex: YrJNPljM3TuNFPIOZ+jziw==

import os
import requests
import sys
import base64
import zipfile
import hashlib
import cookielib
import fileinput

try:
    import urllib.request as urllib2
except ImportError:
    import urllib2

from bs4 import BeautifulSoup

try:
    os.remove("whatsapp.apk")
except OSError:
    pass


url = "https://www.whatsapp.com/android/"
response = requests.request("GET", url, verify=True)

soup = BeautifulSoup(response.text, "html.parser")
apk_url = soup.find_all('a', class_='button', href=True)
download_url = apk_url[0]['href']
print("URL download for APK : "+download_url)

file_name = "whatsapp.apk"
with open(file_name, "wb") as f:
    print ("Downloading %s" % file_name)
    response = requests.get(download_url, stream=True)
    total_length = response.headers.get('content-length')
    if total_length is None:  # no content length header
        f.write(response.content)
    else:
        dl = 0
        total_length = int(total_length)
        for data in response.iter_content(chunk_size=4096):
            dl += len(data)
            f.write(data)
            done = int(50 * dl / total_length)
            sys.stdout.write("\r[%s%s]" % ('=' * done, ' ' * (50-done)))
            sys.stdout.flush()

#  MD5 code from https://github.com/mgp25/classesMD5-64/
print("\n=== Processing APK ===")
zipFile = zipfile.ZipFile("whatsapp.apk", 'r')
classesDexFile = zipFile.read('classes.dex')
hash = hashlib.md5()
hash.update(classesDexFile)


version = classesDexFile.decode("utf-8", errors='ignore').partition('App: ')[-1].partition(',')[0]

print("WhatsApp Version: " + version)
print("WhatsApp ClassesDex: " + base64.b64encode(hash.digest()).decode("utf-8"))

print("\n=== Writing to env_android.py ===")

for line in fileinput.input('./yowsup/env/env_android.py', inplace=True):
    if "    _MD5_CLASSES =" in line:
        print ('    _MD5_CLASSES = "' + base64.b64encode(hash.digest()).decode("utf-8")+'"')
    elif "    _VERSION =" in line:
        print ('    _VERSION = "'+version+'"')
    else:
        print (line),
