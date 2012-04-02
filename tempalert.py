#!/usr/bin/python

import httplib, libxml2, sys

def main():
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
                                # calculate celcius (5/9) * (F-32) and round to 1 decimal place
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


if __name__ == "__main__":
        if len(sys.argv) < 2:
                print "Usage: tempalert.py <server>"
                sys.exit(1)
        else:
                main()
