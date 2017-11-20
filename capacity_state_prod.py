import pandas as pd
import requests
import json
from pandas.io.json import json_normalize
import argparse
import time


get_url = 'https://fulfillment-api.celectengine.com/api/v2/stores'
patch_url = 'https://fulfillment-api.celectengine.com/api/v2/stores/'
client_id = '<YOUR_CLIENT_ID>'
api_key = '<YOUR_API_KEY>'


def get_state(brand):
	file = region + '_capacity_state.csv'
	payload = {
		'client_id': client_id,
		'api_key': api_key,
		'data': {'brand': brand}}
	head = {
		'X-Http-Method-Override': 'GET',
		'Content-Type': 'application/json'
	}
	r = requests.post(get_url, headers=head, data=json.dumps(payload))
	# print(r.status_code)  # debug
	# print(r.text)  # debug
	data = json.loads(r.text)
	d2 = json_normalize(data['results'])  # returns df
	cap_state = d2[['country', 'store_id', 'shipments_capacity']]
	print('Store Count: ', len(cap_state.index))
	# print(cap_state.head(5))
	cap_state.to_csv(file)


def write_state():
	count = 0
	rawData = file
	df = pd.read_csv(rawData)
	df['store_id'] = df['store_id'].astype(str)
	# SET BRAND BASED ON 'country'
	if df.loc[0, 'country'] == 'US':
		brand = '01'
	else:
		brand = '02 '
	# READ store_id and shipments_capacity into dictionary
	df = df[['store_id', 'shipments_capacity']]
	cap_dict = dict(zip(df.store_id, df.shipments_capacity))
	# print(cap_dict)  # debug
	for key, value in cap_dict.items():
		# print(key, value)
		x_id = key
		url2 = patch_url + x_id
		# print(url2)  # debug
		# request goes here
		payload = {
			'client_id': client_id,
			'api_key': api_key,
			'data': {
				'store': {
			'shipmentsCapacity': value
			},
			'brand': brand}}
		head = {
		'Content-Type': 'application/json'
		}
		# print(payload)  # debug
		r = requests.patch(url2, headers=head, data=json.dumps(payload))
		print(r.text)
		count += 1
		# print(count)
		if r.status_code > 200:
			print('ERROR', r.status_code)
			exit()
		elif count % 20 == 0:
			time.sleep(3)


parser = argparse.ArgumentParser()
parser.add_argument('--state', choices=['get', 'set'],
	help='Either get current state or set state to a previous get.')
parser.add_argument('--region',  choices=['ca', 'us'],
	help="Required with --state get Must be either 'ca' for Canada or 'us' for United States")
parser.add_argument("--file",
	help="Required with --state set. The file to process - include path if necessary")
args = parser.parse_args()
# region = args.region
file = args.file
state = args.state
region = args.region

if state == 'get':
	if region == 'ca':
		print('Getting current state for region ', region)
		brand = '02'
		get_state(brand)
	else:
		region = 'us'
		print('Getting current state for region ', region)
		brand = '01'
		get_state(brand)
elif state == 'set':
	if file.endswith('.csv'):
		print("Processing file...")
		write_state()
	else:
		print("ERROR: Incorrect file format : Exiting")
		exit()
