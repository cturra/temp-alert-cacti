#!/usr/bin/python

import sys, re
import httplib, libxml2

# complete the http connect and return connection object if successful
def http_connect(server):
	conn = httplib.HTTPConnection(server, timeout=10)
        try:
                conn.request("GET", "/xmlfeed.rb")
                return conn
        except:
                print "Unable to complete HTTP request"
                sys.exit(1)


# calculate celcius from fahrenheit. if celcius is provided, just round.
def calc_celcius(temp):
	if (unit.lower() == "f"):
		# calculate celcius (5/9) * (F-32) and round to 1 decimal place
		return round(((5.0/9) * (eval(temp) - 32)), 1)
	else:
		# round celcius to 1 decminal place
		return round(eval(temp),1)

# calculate fahrenheit from celcius. if fahrenheit is provided, just round.
def calc_fahrenheit(temp):
	global unit

	if (unit.lower() == "c"):
		# calculate fahrenheit (C) * (9/5) + 32 and round to 1 decimal place
		return round((eval(temp) * (9/5.0) + 32),1)
	else:
		# round fahrenheit to 1 decimal place
		return round(eval(temp),1)


# print temperature results to standard out
def print_results(type,content):
	if type == "temperature":
		c = calc_celcius(content)
		f = calc_fahrenheit(content)
		print "fahrenheit:"+str(f)+" celcius:"+str(c)
	else:
		print "humidity:"+str(content)


# pull the currentReading out of the XML child provided
def find_current_reading_details(type,doc):
	for children in doc:
		if children.name == "currentReading":
			print_results(type,children.content)
			break


# validate that the content type is either temperature or humidity
def validate_content_type(type):
	if type.lower() == "temperature" or type.lower() == "temp":
		return "temperature"
	elif type.lower() == "humidity":
		return "humidity"
	else:
		print "Invalid content_type. Only temperature and humidity supported at this time."
		sys.exit(1)


# the business end. main logic in here \o/
def main():
	content_type = validate_content_type(sys.argv[2])
        conn = http_connect(sys.argv[1])
	req = conn.getresponse()

        # check response code
        if req.status == 200:
                doc = libxml2.parseDoc(req.read())
                root = doc.children
                for child in root:
			# check what units are configured for reporting
			if content_type == "temperature" and child.name == "tempUnits":
				global unit
				unit = "f" if str(child.content).lower() == "fahrenheit" else "c"

			# found temperature elements!
			if content_type == "temperature" and (child.type == "element" and re.search("temperature",str(child.properties))):
				find_current_reading_details("temperature",child)

			# found humidity elements!
			if content_type == "humidity" and (child.type == "element" and re.search("humidity",str(child.properties))):
				find_current_reading_details("humidity",child)

                # close XML document
                doc.freeDoc()

        # non HTTP/200 OK was returned
        else:
                print "An HTTP/200 OK was NOT returned."
                sys.exit(1)

        # close connection
        conn.close()



if __name__ == "__main__":
        if len(sys.argv) < 3:
                print "Usage: tempalert.py <server> <condition_type>"
		print "  - condition type: temperature OR humidity"
                sys.exit(1)
        else:
                main()
