Takes in one server argument then makes an HTTP request to the
target temperature@lert WiFi 220 to retrieve the XML status file.
Returns a result set of the current termperature in both F and C.

Example run:

    $ python tempalert.py <device_ip>
    fahrenheit:84.0 celcius:28.9


Debian/Ubuntu installation notes
-----------

libxml2 is required for parsing the xml feed on the temperature@lert.

    $ apt-get install python-libxml2
