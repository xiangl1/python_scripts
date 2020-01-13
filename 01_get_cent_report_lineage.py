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
	return {'{}'.format(rank):ranks2lineage.get(rank,1) for rank in desired_ranks}

# --------------------------------------------------
def main():
	"""main"""
	args = get_args()
	infile = args.infile
	out_file = args.outfile
	
	desired_ranks = [
					"superkingdom",
					"phylum",
					"class",
					"order",
					"family",
					"genus",
					"species"]

	l = []
	new_l = []
	with open(infile,'r') as in_f:
		reader = csv.reader(in_f,delimiter = '\t')
		next(reader)
		for row in reader:
			if int(row[5]) != 0:
				t = (row[1], row[5])
				l.append(t)

	with open(out_file, 'w') as out_f:	
		print(*desired_ranks, 'Count', sep='\t', file=out_f)
		for (taxid,count) in l:
			try:
				d = get_desired_ranks(taxid, desired_ranks)
			except ValueError:
				pass
			new_l = []
			for rank in desired_ranks:
				new_l.append(d[rank])
			print("{}\t{}".format(','.join(ncbi.translate_to_names(new_l)), count), file=out_f)
# --------------------------------------------------
if __name__ == '__main__':
	main()
