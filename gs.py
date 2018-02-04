import requests
from html.parser import HTMLParser
import sys

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

# create a subclass and override the handler methods
class MyHTMLParser(HTMLParser):
    portno = None
    def handle_starttag(self, tag, attrs):
        if tag == 'input' and attrs[2][0] == 'value':
            print("PUTVAL {0}/exec-port{1}/{2} N:{3}".format(hostname, self.portno, attrs[1][1], int(attrs[2][1], 16)))

    def handle_endtag(self, tag):
        pass

    def handle_data(self, data):
        try:
            self.portno = int(data)
        except ValueError:
            pass


data = bytes.decode(response.content)

# instantiate the parser and fed it some HTML
parser = MyHTMLParser()
parser.feed(data)
