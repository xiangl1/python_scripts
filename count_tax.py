#!/usr/bin/env python3
"""count taxonomy from mapped reads"""

import argparse
import os
import sys
import csv

# --------------------------------------------------
def get_args():
	"""get args"""
	parser = argparse.ArgumentParser(description='count taxonomy reads')
	parser.add_argument('-i', '--infile', help='contig reads map input file',
						type=str, metavar='FILE', required=True)
	parser.add_argument('-t', '--header', help='contig taxonomy file',
						type=str, metavar='FILE', required=True)
	parser.add_argument('-c', '--classify_order', help='domain;phylum;class;order;family;genus;species;taxon_name',
						type=str, metavar='STR', default='phylum')
	parser.add_argument('-o', '--outfile', help='Output file',
						type=str, metavar='FILE', required=True)
	return parser.parse_args()

# --------------------------------------------------
def main():
	"""main"""
	args = get_args()
	infile = args.infile
	header = args.header
	level = args.classify_order
	out_file = open(args.outfile,'w')

	contig_tax = {}
	with open(header,'r') as h_file:
		reader = csv.reader(h_file, delimiter = '\t')
		for row in reader:
			d = {
				"superkingdom": row[1],
				"phylum": row[2],
				"class": row[3],
				"order": row[4],
				"family": row[5],
				"genus": row[6],
				"species": row[7],
				}
			contig_tax[row[0]] = d

	with open(infile,'r') as i_file:
		reader = csv.reader(i_file,delimiter='\t')
		for row in reader:
			if row[0] in contig_tax.keys():
				print("{}\t{}\t{}".format(row[0],contig_tax[row[0]][level],row[2]),file=out_file)
				#print("{}\t{}\t{}".format(row[0],contig_tax[row[0]],row[2]),file=out_file)
			else:
				print("{}\t{}\t{}".format(row[0],'NA',row[2]),file=out_file)

# --------------------------------------------------
if __name__ == '__main__':
	main()
