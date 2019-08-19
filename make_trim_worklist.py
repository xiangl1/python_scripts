#!/usr/bin/env python3
"""make trim_galore parall work list"""

import argparse
import os
import sys
import csv

# --------------------------------------------------
def get_args():
	"""get args"""
	parser = argparse.ArgumentParser(description='make trim paralle list')
	parser.add_argument('-i', '--infile', help='list file of ERA acc number',
						type=str, metavar='FILE', required=True)
	parser.add_argument('-rd', '--reads_dir', help='raw reads dir',
						type=str, metavar='FILE', required=True)
	parser.add_argument('-od', '--out_dir', help='output dir for trim_galore',
						type=str, metavar='FILE', required=True)
 
	parser.add_argument('-of', '--out_file', help='output file',
						type=str, metavar='FILE', required=True)
	return parser.parse_args()

# --------------------------------------------------
def main():
	"""main"""
	args = get_args()
	infile = args.infile
	raw_dir = args.reads_dir
	out_dir = args.out_dir
	out_file = open(args.out_file,'w')

	pre_fix = 'trim_galore --paired -o'

	contig_tax = {}
	with open(infile,'r') as in_file:
		for acc_num in in_file:
			acc_num = acc_num.rstrip('\n')
			print("{} {} {}/{}_1.fastq.gz {}/{}_2.fastq.gz".format(pre_fix,out_dir,
				  raw_dir,acc_num,raw_dir,acc_num),file=out_file)

# --------------------------------------------------
if __name__ == '__main__':
	main()
