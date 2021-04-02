"""
	Convert a json file to csv.
	input reqd: 
		- infile_path: file to read from
		- out_dir: directory for output files 
"""

import sys
import pandas as pd
import os

def main(infile_path, out_dir):

	file_base_path = os.path.basename(infile_path)
	file_name = os.path.splitext(file_base_path)[0]

	if not os.path.exists(out_dir):
		os.makedirs(out_dir)

	with open(infile_path, encoding='utf-8-sig') as f_input:
		df = pd.read_json(f_input)
	df.to_csv(out_dir + file_name + '.csv', encoding='utf-8', index=False)


if __name__ == '__main__':
	infile_path = sys.argv[1]
	out_dir = sys.argv[2]
	main(infile_path)

