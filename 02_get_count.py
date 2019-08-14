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
	parser.add_argument('-c', '--classify_order', help='domain;phylum;class;order;family;genus;species;taxon_name',
						type=str, metavar='STR', default='phylum')
	parser.add_argument('-o', '--outfile', help='Output file',
						type=str, metavar='FILE', required=True)
	return parser.parse_args()

# --------------------------------------------------
def main():
	"""main"""
	ncbi = NCBITaxa()
	args = get_args()
	infile = args.infile
	rank = args.classify_order
	out_file = args.outfile
	
	l = []
	level = { 'superkingdom':0,
			  'phylum':1,
			  'class':2,
			  'order':3,
			  'family':4,
			  'genus':5,
			  'species':6}

	h_num = level[rank]

	with open(infile,'r') as in_f:
		reader = csv.reader(in_f,delimiter = '\t')
		next(reader)
		for row in reader:
			if row[h_num] != 'NA':
				taxid2name = ncbi.get_taxid_translator([row[h_num]])
				name = taxid2name[int(row[h_num])]
			elif row[h_num - 1] != 'NA':
				taxid2name = ncbi.get_taxid_translator([row[h_num-1]])
				name = taxid2name[int(row[h_num-1])] + '_NA'
			elif row[h_num - 2] != 'NA':
				taxid2name = ncbi.get_taxid_translator([row[h_num-2]])
				name = taxid2name[int(row[h_num-2])] + '_NA'+'_NA'
			elif row[h_num - 3] != 'NA':
				taxid2name = ncbi.get_taxid_translator([row[h_num-3]])
				name = taxid2name[int(row[h_num-3])] + '_NA'+'_NA'+'_NA'
			elif row[h_num - 4] != 'NA':
				taxid2name = ncbi.get_taxid_translator([row[h_num-4]])
				name = taxid2name[int(row[h_num-4])] + '_NA'+'_NA'+'_NA'+'_NA'
			else:
				name = 'NA'
			t = (name, row[7])
			l.append(t)
	
	d_count = {}			
	for key, value in l:
		d_count[key] = int(d_count.get(key, 0)) + int(value)
	
	total_count = sum(d_count.values())

	with open(out_file, 'w') as o_f:
		for key in sorted(d_count, key=d_count.get, reverse=True):
			percent = float(d_count[key]/total_count * 100)
			#print(key,'\t',d_count[key],'\t','{0:.2f}'.format(percent), file=o_f)	
			print(key,'\t',d_count[key], file=o_f)	

# --------------------------------------------------
if __name__ == '__main__':
	main()
