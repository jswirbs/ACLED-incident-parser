import firebase_admin
from firebase_admin import credentials, firestore

from datetime import datetime


def parse_data(data_list, count, docName):
	### Initialize firebase
	cred = credentials.Certificate('./ServiceAccountKey.json')
	default_app = firebase_admin.initialize_app(cred)
	db = firestore.client()

	counter = 0

	while counter < count:
		d = data_list[counter]
		counter = counter + 1


		# attribution and target set to 'unknown'' by default
		attribution = 'unknown'
		target = 'unknown'
		if d['actor1'] is not "":
			attribution = d['actor1']
		if d['actor2'] is not "":
			target = d['actor2']


		# severity guaged by casualties
		severity = 1
		if int(d['fatalities']) > 0:
			if int(d['fatalities']) > 5:
				severity = 3
			else: 
				severity = 2


		description = d['notes']
		primaryEventType = ""
		eventType = {}
		
		# eventType (can be multiple) read from description and primaryEventType set
		# by following order of importance (defaults to assault)
		if (d['event_type'] == 'Riots/Protests'):
			primaryEventType = u"riot"
			eventType['riot'] = True
		if ("militants" in description) or ("militia" in description) or ("army" in description) or ("armed group" in description):
			primaryEventType = u"armed group"
			eventType['armed group'] = True
		if ("theft" in description) or ("stole" in description) or ("loot" in description):
			primaryEventType = u"theft"
			eventType['theft'] = True
		if ("shoot" in description) or ("shot" in description) or ("gunfire" in description) or ("gunmen" in description) or ("sniping" in description) or ("snipe" in description):
			primaryEventType = u"shooting"
			eventType['shooting'] = True
		if ("kidnap" in description):
			primaryEventType = u"kidnapping"
			eventType['kidnapping'] = True
		if ("explosive" in description) or ("explosion" in description) or ("exploded" in description) or ("bomb" in description) or ("IED" in description):
			primaryEventType = u"explosives"
			eventType['explosives'] = True
		if len(eventType) == 0:
			primaryEventType = u"assault"
			eventType['assault'] = True
		

		# Create and add new doc to input region's intelReports sub-collection
		db.collection('regions').document(docName).collection('intelReports').add({
			'operator': d['source'],
			'timestamp' : datetime.now(),
			'location': {
				'type': u'address',
				'address': [ (d['location']), (d['admin2'] + ", " + d['admin1'] + ", " + d['country'])],
				'coordinates': firestore.GeoPoint(float(d['latitude']), float(d['longitude']))
			},
			'timeOfEvent': datetime.strptime(d['event_date'] + ' 04:00', '%Y-%m-%d %H:%M'),
		    'eventType': eventType,
		    'primaryEventType': primaryEventType,
		    'numberInvolved': 1,
		    'casualties': int(d['fatalities']),
		    'attribution': attribution,
		    'target': target,
		    'description': d['notes'],
		    'severity': severity,
		    # 'verification': {...}
		})

	print "Parsed " + str(counter) + " incidents into /regions/" + docName + "/intelReports . . . "


