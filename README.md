Takes in two arguments: (1) device IP and (2) condition type, then makes an 
HTTP request to the target temperature@lert WiFi 220 to retrieve the XML 
status file. Returns a result set of the current termperature in both F and C.

*Humidity is only available if you are using a temperature/humidity sensors with your
temperature@lert WiFi 220. 

Example runs:

    $ python tempalert.py <device_ip> temperature
    fahrenheit:84.0 celcius:28.9

    $ python tempalert.py <device_ip> humidity
    humidity:42.2


Debian/Ubuntu installation notes
-----------

libxml2 is required for parsing the xml feed on the temperature@lert.

    $ apt-get install python-libxml2
