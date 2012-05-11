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
def calc_celcius(temp,unit):
	if (unit.lower() == "f"):
		# calculate celcius (5/9) * (F-32) and round to 1 decimal place
		return round(((5.0/9) * (eval(temp) - 32)), 1)
	else:
		# round celcius to 1 decminal place
		return round(eval(temp),1)

# calculate fahrenheit from celcius. if fahrenheit is provided, just round.
def calc_fahrenheit(temp,unit):
	if (unit.lower() == "c"):
		# calculate fahrenheit (C) * (9/5) + 32 and round to 1 decimal place
		return round((eval(temp) * (9/5.0) + 32),1)
	else:
		# round fahrenheit to 1 decimal place
		return round(eval(temp),1)


# print to temperature results to standard out
def print_temp_results(temp,unit):
	c = calc_celcius(temp,unit)
	f = calc_fahrenheit(temp,unit)	

	print "fahrenheit:"+str(f)+" celcius:"+str(c)


# the business end. main logic in here \o/
def main():
        conn = http_connect(sys.argv[1])
	req = conn.getresponse()

        # check response code
        if req.status == 200:
                data = req.read()
                doc = libxml2.parseDoc(data)
                root = doc.children
                for child in root:
			# check what units are configured for reporting
			if child.name == "tempUnits":
				if str(child.content).lower() == "fahrenheit":
					unit = "f"
				else:
					unit = "c"

			# found temperature elements!
			if child.type == "element" and re.search("temperature",str(child.properties)):
				for children in child:
		                        if children.name == "currentReading":
						print_temp_results(children.content,unit)
						break

                # close XML document
                doc.freeDoc()

        # non HTTP/200 OK was returned
        else:
                print "An HTTP/200 OK was NOT returned."
                sys.exit(1)

        # close connection
        conn.close()



if __name__ == "__main__":
        if len(sys.argv) < 2:
                print "Usage: tempalert.py <server>"
                sys.exit(1)
        else:
                main()
