#!/usr/bin/python3
    
import requests
from html.parser import HTMLParser
import sys
import time

INTERVAL = 60

if len(sys.argv) < 3:
    print("ERROR: Not enough args")
    print("Usage: %s <switch_hostname> <password>" % sys.argv[0])
    exit(-1)

hostname = sys.argv[1]
password = sys.argv[2]

session = requests.Session()

headers = {'content-type': 'application/x-www-form-urlencoded'}

# Login
session.post("http://{0}/login.cgi".format(hostname), data="password={0}".format(password), headers=headers)

# Fetch the traffic data
response = session.get("http://{0}/portStatistics.cgi".format(hostname))

# Logout - to clean up cookies
session.get("http://{0}/logout.cgi".format(hostname))

# Class to scrape the HTML output from the netgear website
class MyHTMLParser(HTMLParser):
    portno = None
    gotsomething = False
    def handle_starttag(self, tag, attrs):
        if tag == 'input' and attrs[2][0] == 'value':
            print("PUTVAL {0}/exec-port{1}/{2} N:{3}".format(hostname, self.portno, attrs[1][1], int(attrs[2][1], 16)))
            self.gotsomething = True

    def handle_endtag(self, tag):
        pass

    def handle_data(self, data):
        try:
            self.portno = int(data)
        except ValueError:
            pass

start_time = int(time.time())

while True:

    # Login
    session.post("http://{0}/login.cgi".format(hostname), data="password={0}".format(password), headers=headers)

    # Fetch the traffic data
    response = session.get("http://{0}/portStatistics.cgi".format(hostname))

    # Logout - to clean up cookies
    session.get("http://{0}/logout.cgi".format(hostname))


    data = bytes.decode(response.content)

    # Instantiate the parser and feed it some HTML
    parser = MyHTMLParser()
    parser.feed(data)

    if not parser.gotsomething:
        print("Didn't get anything, check your hostname and password")


    delay = ((start_time - int(time.time()))%INTERVAL)
    if(delay == 0):
        delay = INTERVAL
    time.sleep(delay)
