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
def main():
	"""main"""
	args = get_args()
	infile = args.infile
	email = args.email
	out_file = args.outfile
	
	Entrez.email = email

	acc_list = open(infile, 'r').read().splitlines()
	acc = ','.join(acc_list)
	handle = Entrez.esummary(db = "nuccore", id = acc)
	records = Entrez.read(handle)
	handle.close()
	
	ncbi = NCBITaxa()
	
	with open(out_file, 'w') as out_f:	
		for record in records: 
			acc_version = record["AccessionVersion"] 	
			tax_id = record["TaxId"]
			lineage = ncbi.get_lineage(tax_id)
			name = ncbi.translate_to_names(lineage)
			print("{}\t{}".format(acc_version,'\t'.join(name)), file=out_f)
# --------------------------------------------------
if __name__ == '__main__':
	main()
