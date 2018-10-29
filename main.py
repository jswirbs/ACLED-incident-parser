import firebase_admin
from firebase_admin import credentials, firestore

import sys
import urllib2
import json
from parser import parse_data


### Python parser to read data from ACLED database (www.acleddata.com)
### and upload formatted incidents to a firebase firestore database.
### Used for incident visualization.

def main():

	if len(sys.argv) < 2:
		print "Usage: 'python main.py <country>'"

	else:

		country = sys.argv[1]
		weekly_update(country)



def weekly_update(country):

	# 500 most recent incidents pulled per page by default
	response = urllib2.urlopen('https://api.acleddata.com/acled/read?country=' + country)
	json_response = json.load(response)
	
	if json_response['success']:
		### Parses all data ('count' is acled response for count of incidents)
		#parse_data(json_response['data'], json_response['count'], country)

		### Just parse first 3 incidents and add to 'test' region
		parse_data(json_response['data'], 3, 'test')

	else:
		print "Error retrieving data from acled api ..."
	return False



if __name__ == '__main__':
    main()



