#!/usr/bin/env python3
"""format centrifuge output with contig id and taxid"""

import argparse
import os
import sys
import csv
from ete3 import NCBITaxa

# --------------------------------------------------
def get_args():
	"""get args"""
	parser = argparse.ArgumentParser(description='format centrifuge output')
	parser.add_argument('-i', '--infile', help='centrifuge result file',
						type=str, metavar='FILE', required=True)
	#parser.add_argument('-t', '--header', help='contig taxonomy file',
	#					type=str, metavar='FILE', required=True)
	#parser.add_argument('-c', '--classify_order', help='domain;phylum;class;order;family;genus;species;taxon_name',
	#					type=str, metavar='STR', default='phylum')
	parser.add_argument('-o', '--outfile', help='Output file',
						type=str, metavar='FILE', required=True)
	return parser.parse_args()

# --------------------------------------------------
def main():
	"""main"""
	ncbi = NCBITaxa()
	args = get_args()
	infile = args.infile
	#header = args.header
	#level = args.classify_order
	out_file = args.outfile
	
	l = []
	with open(infile,'r') as in_f:
		reader = csv.reader(in_f,delimiter = '\t')
		for row in reader:
			if row[1] != 'NA':
				taxid2name = ncbi.get_taxid_translator([row[1]])
				name = taxid2name[int(row[1])]
			else:
				name = 'NA'
			t = (name, row[5])
			l.append(t)
	
	d_count = {}			
	for key, value in l:
		d_count[key] = int(d_count.get(key, 0)) + int(value)
	
	total_count = sum(d_count.values())

	with open(out_file, 'w') as o_f:
		for key in d_count.keys():
			percent = float(d_count[key]/total_count * 100)
			print(key,'\t',d_count[key],'\t','{0:.2f}'.format(percent), file=o_f)	
	
	#with open(out_file, 'w') as out_f:	
	#	print('contig', *desired_ranks,sep='\t', file=out_f)
	#	for (contig,tax) in l:
	#		try:
	#			d = get_desired_ranks(tax, desired_ranks)
	#		except ValueError:
	#			pass
	#		new_l = []
	#		for rank in desired_ranks:
	#			new_l.append(d[rank])
	#		print(contig, *new_l, sep='\t', file=out_f)
# --------------------------------------------------
if __name__ == '__main__':
	main()
