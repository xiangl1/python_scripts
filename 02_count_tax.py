#!/usr/bin/env python3
"""make taxonomy count from sequence count"""

import argparse
import os
import sys
import csv
import re
from collections import defaultdict

# --------------------------------------------------
def get_args():
	"""get args"""
	parser = argparse.ArgumentParser(description='make taxonomy count from sequence count')
	parser.add_argument('-i', '--infile', help='centrifuge result file',
						type=str, metavar='FILE', required=True)
	parser.add_argument('-t', '--taxonomy', help='sequence to taxonomy file',
						type=str, metavar='FILE', required=True)
	parser.add_argument('-o', '--outfile', help='Output file',
						type=str, metavar='FILE', required=True)
	return parser.parse_args()

# --------------------------------------------------
def main():
	"""main"""
	args = get_args()
	in_file = args.infile
	tax_file = args.taxonomy
	out_file = open(args.outfile,'w')
	
	h = {}
	in_d = defaultdict(list)
	with open(tax_file, 'r') as ref_h:
		reader = csv.reader(ref_h, delimiter = '\t')
		#next(reader)
		for line in reader:
			h[line[0]] = ','.join(line[1:9])
	
	#column_name = ','.join(['kingdom','phylum','class','order','family','genus',
					#'species', 'count'])

	with open(in_file,'r') as in_f:
		reader = csv.reader(in_f,delimiter = '\t')
		for line in reader:
			try:
				in_d[h[line[0]]].append(int(line[2]))	
			except KeyError:
				continue
	
	#print('{}'.format(column_name),file=out_file)
	for key in in_d:
		print('{}\t{}'.format(key,sum(in_d[key])),file=out_file)
# --------------------------------------------------
if __name__ == '__main__':
	main()
