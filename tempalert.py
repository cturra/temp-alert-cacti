#!/usr/bin/python
# 
# tempalert.py 
# Takes in one server argument then makes an HTTP request to the
# target temperature@lert device to retrieve the XML status file.
# Returns a result set of the current termperature in both F and C.
# 
#   Example output:
#   fahrenheit:84.0 celcius:28.9
# 
# Written by: Chris Turra <cturra@gmail.com>
#

import httplib, libxml2, sys

if len(sys.argv) < 2:
        print "Usage: tempalert.py <server>"
        sys.exit(1)
else:
	server = sys.argv[1]

conn = httplib.HTTPConnection(server, timeout=10)
try:
	conn.request("GET", "/xmlfeed.rb")
	req = conn.getresponse()
except:
        print "Unable to complete HTTP request"
        sys.exit(1)

# check response code
if req.status == 200:
        data = req.read()
        doc = libxml2.parseDoc(data)
        root = doc.children
        for child in root:
                if child.name == "currentReading":
                        # calculate celcius (5/9) * (F-32)a nd round to 1 decimal place
                        c = round(((5.0/9) * (eval(child.content) - 32)), 1)
                        # round fahrenheit to 1 decimal place
                        f = round(eval(child.content), 1)
                        # output results to stdout
                        print "fahrenheit:"+str(f)+" celcius:"+str(c)
        # close XML document
        doc.freeDoc()

# non HTTP/200 OK was returned
else:
        print "An HTTP/200 OK was NOT returned."
        sys.exit(1)

# close connection
conn.close()
