#!/usr/bin/env python3
"""format centrifuge output with contig id and taxid"""

import argparse
import os
import sys
import csv
import re

# --------------------------------------------------
def get_args():
	"""get args"""
	parser = argparse.ArgumentParser(description='format centrifuge output')
	parser.add_argument('-i', '--infile', help='centrifuge result file',
						type=str, metavar='FILE', required=True)
	parser.add_argument('-t', '--total_name', help='total names of each sample',
						type=str, metavar='STR', required=True)
	parser.add_argument('-o', '--outfile', help='Output file',
						type=str, metavar='FILE', required=True)
	return parser.parse_args()

# --------------------------------------------------
def main():
	"""main"""
	args = get_args()
	infile = args.infile
	row_name = args.total_name
	out_file = args.outfile
	
	h = {}
	with open(row_name, 'r') as in_h:
		reader = csv.reader(in_h, delimiter = '\t')
		next(reader)
		for row in reader:
			h[row[0]] = 0

	filename = os.path.basename(infile)
	column_name = re.search('([0-9].*[0-9])',filename)

	with open(infile,'r') as in_f:
		reader = csv.reader(in_f,delimiter = '\t')
		for row in reader:
			if row[0] in h:
				h[row[0]] = int(row[1])	
	
	with open(out_file, 'w') as o_f:
		#print ('name','\t',column_name.group(0), file=o_f)
		print (column_name.group(0), file=o_f)
		for key in sorted(h):
			#print(key,'\t',h[key], file=o_f)	
			print(h[key], file=o_f)	

# --------------------------------------------------
if __name__ == '__main__':
	main()
