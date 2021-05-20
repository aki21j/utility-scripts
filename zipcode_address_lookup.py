"""
	Lookup state, city and country from zipcodes.
	Always appends to a file, so that same can be used to reduce computations in the future.
	input reqd: 
		- infile_path: file to read from where zipcodes are present
		- column_name: name of the column for zipcode
		- country_code: country code of the list of zipcodes. e.g: IN for india
		- zipcode_data_file: file path wherein output is to be written to. 
												For successive runs, this file will be used to compute data that has already been resolved earlier.
"""

import sys
import json
import requests
import logging
import copy
import os
import traceback
import csv
from pprint import pprint

FORMAT = '%(asctime)-15s %(message)s'
logging.basicConfig(format=FORMAT)
logger = logging.getLogger()
logger.setLevel(logging.INFO)

API_URL = "https://api.worldpostallocations.com/pincode?postalcode={}&countrycode={}"



def main():
	infile_path = sys.argv[1]
	column_name = sys.argv[2]
	country_code = sys.argv[3]
	zipcode_data_file = sys.argv[4]

	out_data = []

	with open(infile_path, mode='r') as csv_file:
		csv_data = csv.DictReader(csv_file)
		pprint(csv_data)
		line_count = 0
		for row in csv_data:
			logger.info(line_count)
			if line_count == 0:
				headers = row.keys()
				line_count += 1

			out_obj = copy.deepcopy(row)
			pincode = row[column_name]
			out_data.append(pincode)
			line_count += 1

			
	logger.info("Total Length: {}".format(len((out_data))))
	logger.info("Distinct length: {}".format(len(set(out_data))))

	processed_data = get_processed_keys(zipcode_data_file)

	distinct = set(out_data) ^ set(processed_data)

	rev_lookup_address(list(distinct), country_code, zipcode_data_file)
	
	return

def get_processed_keys(zipcode_data_file):
	if os.path.exists(zipcode_data_file):
		with open(zipcode_data_file, 'r') as infile:  
			res = json.load(infile)
			return res.keys()
	return []

def rev_lookup_address(zipcode_list, country_code, zipcode_data_file):

	counter = 0

	out_data = {}

	if os.path.exists(zipcode_data_file):
		with open(zipcode_data_file, 'r') as infile:  
			out_data = json.load(infile)

	for zipcode in zipcode_list:
		try:

			logger.info("COUNTER: {}, zipcode: {}".format(counter, zipcode))
			url = API_URL.format(zipcode, country_code)

			counter += 1
			response = requests.get(url)
			response_data = response.json()
			if response_data['status']:
				out_data[zipcode] = parse_address(response_data['result'].pop(0))

			logger.info(out_data[zipcode])

			with open(zipcode_data_file, 'w') as outfile:
				json.dump(out_data, outfile, indent = 2)
				
		except Exception as e:
			logger.error(e)
			logger.error(traceback.format_exc())


def parse_address(raw_address):
	parsed_address = {
		"country": raw_address['country'], 
		"state" : raw_address['state'],
		"city" : raw_address['district']
	}
	return parsed_address

if __name__ == "__main__":
	main()