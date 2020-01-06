#!/usr/bin/env python3
"""blast output reference acc number to taxanomy ranks"""

import argparse
import os
import sys
import csv
from ete3 import NCBITaxa
from Bio import Entrez
# --------------------------------------------------
def get_args():
	"""get args"""
	parser = argparse.ArgumentParser(description='change acc id to taxonomy from blast output file')
	parser.add_argument('-i', '--infile', help='blast picked output',
						type=str, metavar='FILE', required=True)
	parser.add_argument('-r', '--reference', help='reference file with acc number and ranks',
						type=str, metavar='STR', required=True)
	parser.add_argument('-o', '--outfile', help='Output file',
						type=str, metavar='FILE', required=True)
	return parser.parse_args()

# --------------------------------------------------
def main():
	"""main"""
	args = get_args()
	infile = args.infile
	ref_file = args.reference
	out_file = open(args.outfile,'w')

	"""save reference file"""
	h={}
	
	with open(ref_file,"r") as ref_f:
		reader = csv.reader(ref_f, delimiter = '\t')
		for line in reader:
			h[line[0]] = line[1]
	ref_f.close()

	with open(infile,"r") as in_f:
		reader = csv.reader(in_f,delimiter = '\t')
		for line in reader:
			seq_id = line[0]
			acc_id = line[1]
			try:
				print('{}\t{}'.format(seq_id,h[acc_id]),file=out_file)
			except KeyError:
				continue
	out_file.close()			
# --------------------------------------------------
if __name__ == '__main__':
	main()
