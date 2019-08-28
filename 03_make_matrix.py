#!/usr/bin/env python3
"""format centrifuge output with contig id and taxid"""

import argparse
import os
import sys
import csv
import re
from collections import defaultdict

# --------------------------------------------------
def get_args():
	"""get args"""
	parser = argparse.ArgumentParser(description='format centrifuge output')
	parser.add_argument('-l', '--file_list', help='list of filename',
						type=str, metavar='FILE', required=True)
	parser.add_argument('-d', '--input_dir', help='dir of input file',
						type=str, metavar='PATH', required=True)
	parser.add_argument('-t', '--total_name', help='total names of bac',
						type=str, metavar='FILE', required=True)
	parser.add_argument('-o', '--outfile', help='Output file',
						type=str, metavar='FILE', required=True)
	return parser.parse_args()

# --------------------------------------------------
def main():
	"""main"""
	args = get_args()
	file_list = args.file_list
	path = args.input_dir
	row_name = args.total_name
	out_file = open(args.outfile,'w')
	
	
	t_d = {}
	out_d = defaultdict(list)
	header = ['kingdom','phylum','class','order','family','genus','species']
	with open(row_name, 'r') as in_h:
		reader = csv.reader(in_h, delimiter = '\t')
		for row in reader:
			t_d[row[0]] = '0'
	
	with open(file_list) as fl:
		filenames = fl.read().splitlines()

	for i in filenames:
		header.append(i)
		in_d = {}
		in_file = path+'/'+i
		with open(in_file,'r') as in_f:
			reader = csv.reader(in_f,delimiter = '\t')
			next(reader)
			for row in reader:
				in_d[row[0]] = row[1]
		for key in sorted(t_d):
			if key in in_d:
				out_d[key].append(in_d[key])	
			else:
				out_d[key].append(t_d[key])

	print('{}'.format(','.join(header)),file=out_file)
	for tax in sorted(out_d):
		print('{},{}'.format(tax,','.join(out_d[tax])),file=out_file)	

# --------------------------------------------------
if __name__ == '__main__':
	main()
