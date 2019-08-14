#!/usr/bin/env python3
"""format centrifuge output with contig id and taxid"""

import argparse
import os
import sys
import csv
from ete3 import NBITaxa

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
ncbi = NCBITaxa()

def get_desired_ranks(taxid,desired_ranks):
	"""get ranks by taxid"""
	lineage = ncbi.get_lineage(taxid)
	lineage2ranks = ncbi.get_rank(lineage)
	ranks2lineage = dict((rank, taxid) for (taxid, rank) in lineage2ranks.items())
	return {'{}'.format(rank):ranks2lineage.get(rank,'N/A') for rank in desired_ranks}

# --------------------------------------------------
def main():
	"""main"""
	args = get_args()
	infile = args.infile
	#header = args.header
	#level = args.classify_order
	out_file = open(args.outfile,'w')
	
	desired_ranks = [
					"domain",
					"phylum",
					"class",
					"order",
					"family",
					"genus",
					"species"]

	with open(infile,'r') as in_f:
		reader = csv.reader(in_f,delimiter = '\t')
		next(reader)
		for row in reader:
			contig_id = row[0]
			taxid = row[2] 
			wirter.writerow(get_desired_ranks(taxid, desired_ranks))

# --------------------------------------------------
if __name__ == '__main__':
	main()
