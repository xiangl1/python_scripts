#!/usr/bin/env python3
"""find virus host by virus name"""

import argparse
import os
import sys
import csv
from collections import defaultdict

# --------------------------------------------------
def get_args():
	"""get args"""
	parser = argparse.ArgumentParser(description='find virus host by virus name')
	parser.add_argument('-i', '--infile', help='virus scaffold and name file ',
						type=str, metavar='FILE', required=True)
	parser.add_argument('-t', '--header', help='virus host db file',
						type=str, metavar='FILE', required=True)
	parser.add_argument('-o', '--outfile', help='Output file',
						type=str, metavar='FILE', required=True)
	return parser.parse_args()

# --------------------------------------------------
def main():
	"""main"""
	args = get_args()
	infile = args.infile
	header = args.header
	out_file = open(args.outfile,'w')
	
	h = defaultdict(list)
	l = defaultdict(list)

	with open(header,'r') as in_h:
		reader = csv.reader(in_h,delimiter = '\t')
		next(reader)
		for line in reader:
			if len(line) >= 10:
				l[line[1]].append(line[8])
				h[line[1]].append(line[9])
	#for key in h:
	#	print('{}\t{}'.format(key,h[key]))
		
	with open(infile, 'r') as in_f:
		reader = csv.reader(in_f,delimiter = ',')
		next(reader)
		for line in reader:	
			if line[2] in h:
				print('{},{},{},{},{}'.format(line[0],line[1],line[2],max(h[line[2]],key=len),min(l[line[2]],key=len)),file=out_file)
			else:
				print('{},{},{},{},{}'.format(line[0],line[1],line[2],'NA','NA'),file=out_file)
# --------------------------------------------------
if __name__ == '__main__':
	main()
