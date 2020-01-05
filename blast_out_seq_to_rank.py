#!/usr/bin/env python3
"""Creat taxonomy lineage file from NCBI accession number"""

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
	parser.add_argument('-e', '--email', help='email address for NCBI Entrez',
						type=str, metavar='STR', required=True)
	parser.add_argument('-o', '--outfile', help='Output file',
						type=str, metavar='FILE', required=True)
	return parser.parse_args()

# --------------------------------------------------
ncbi = NCBITaxa()

def get_desired_ranks(taxid,desired_ranks):
	"""get ranks by taxid"""
	lineage = ncbi.get_lineage(taxid)
	lineage2ranks = ncbi.get_rank(lineage)
	ranks2lineage = dict((rank,taxid) for (taxid, rank) in lineage2ranks.items())
	return {'{}'.format(rank):ranks2lineage.get(rank,1) for rank in desired_ranks}

# --------------------------------------------------
def main():
	"""main"""
	args = get_args()
	infile = args.infile
	email = args.email
	out_file = open(args.outfile,'w')

	"""desired ranks"""
	desired_ranks = [
					"superkingdom",
					"phylum",
					"class",
					"order",
					"family",
					"genus",
					"species"]

	Entrez.email = email
	out={}
	
	with open(infile,"r") as in_f:
		reader = csv.reader(in_f, delimiter = '\t')
		for line in reader:
			"""get taxid from acc numer"""
			acc = line[1] 
			handle = Entrez.esummary(db = "nuccore", id = acc)
			record = Entrez.read(handle)
			handle.close()
			tax_id = record[0]["TaxId"]
			try:
				d_ranks = get_desired_ranks(tax_id,desired_ranks)
			except ValueError:
				pass
			new_l=[]
			for rank in desired_ranks:
				new_l.append(d_ranks[rank])
			out[line[0]] = ','.join(ncbi.translate_to_names(new_l))
	in_f.close()
	
	for key in out:
		print('{}\t{}'.format(key,out[key]),file=out_file)
	out_file.close()			
# --------------------------------------------------
if __name__ == '__main__':
	main()
