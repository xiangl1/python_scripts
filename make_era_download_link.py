#!/usr/bin/env python3
"""make ERA download link from ERA accession number for ascp"""

import argparse
import os
import sys
import csv

# --------------------------------------------------
def get_args():
	"""get args"""
	parser = argparse.ArgumentParser(description='download ERA seq by ERA acc for ascp')
	parser.add_argument('-i', '--infile', help='list file of ERA acc number',
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
	args = get_args()
	infile = args.infile
	out_file = open(args.outfile,'w')

	pre_fix= "era-fasp@fasp.sra.ebi.ac.uk:/vol1/fastq"

	contig_tax = {}
	with open(infile,'r') as in_file:
		for acc_num in in_file:
			acc_num = acc_num.rstrip('\n')
			pre_dir = acc_num[:6] 
			
			if len(acc_num) == 9:
				print("{}/{}/{}/{}_1.fastq.gz".format(pre_fix,pre_dir,
					  acc_num,acc_num),file=out_file)
				print("{}/{}/{}/{}_2.fastq.gz".format(pre_fix,pre_dir,
					  acc_num,acc_num),file=out_file)
			
			if len(acc_num) == 10:	
				print("{}/{}/00{}/{}/{}_1.fastq.gz".format(pre_fix,pre_dir,
					  acc_num[-1],acc_num,acc_num),file=out_file)
				print("{}/{}/00{}/{}/{}_2.fastq.gz".format(pre_fix,pre_dir,
					  acc_num[-1],acc_num,acc_num),file=out_file)

# --------------------------------------------------
if __name__ == '__main__':
	main()
