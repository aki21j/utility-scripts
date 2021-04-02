import pandas as pd 
import sys
import os

out_dir = './split-files/'

infile_path = sys.argv[1]

file_base_path = os.path.basename(infile_path)
file_name = os.path.splitext(file_base_path)[0]

rows = pd.read_csv(infile_path, chunksize=500000) 
for i, chuck in enumerate(rows):
	split_file_path = out_dir + file_name + '_' + str(i) + '.csv'
	chuck.to_csv(split_file_path, index=False) # i is for chunk number of each iteration 