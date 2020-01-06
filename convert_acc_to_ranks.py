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
	parser = argparse.ArgumentParser(description='find lineage from acc numbers')
	parser.add_argument('-i', '--infile', help='acc_number file',
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
	out_file = args.outfile

	"""desired ranks"""
	desired_ranks = [
					"superkingdom",
					"phylum",
					"class",
					"order",
					"family",
					"genus",
					"species"]

	"""get taxid from acc number"""	
	Entrez.email = email

	acc_list = open(infile, 'r').read().splitlines()
	acc = ','.join(acc_list)
	handle = Entrez.esummary(db = "nuccore", id = acc)
	records = Entrez.read(handle)
	handle.close()
	
	with open(out_file, 'w') as out_f:	
		for record in records: 
			acc_version = record["AccessionVersion"] 	
			tax_id = record["TaxId"]
			try:
				d_ranks = get_desired_ranks(tax_id, desired_ranks)
			except ValueError:
				pass
			new_l=[]
			for rank in desired_ranks:
				new_l.append(d_ranks[rank])
			print("{}\t{}".format(acc_version,','.join(ncbi.translate_to_names(new_l))), file=out_f)
			#print(acc_version,*ncbi.translate_to_names(new_l),sep='\t', file=out_f)
# --------------------------------------------------
if __name__ == '__main__':
	main()
