#!/usr/bin/env python3
"""make cat pool parall work list"""

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

	sample_run = {}
	with open(infile,'r') as in_file:
		reader = csv.reader(in_file, delimiter = ',')
		for line in in_file:
			line = line.rstrip("\n")
			temp = line.split(",")
			sample_run[temp[0]]=temp[1].split("\t")

	for sample in sample_run:
		runs = sample_run[sample]
		run_no = len(runs)
		if run_no == 1:
			print ("mv {}/{}_1_val_1.fq {}/{}_1.fq".format(raw_dir,runs[0],out_dir,sample),file=out_file)
			print ("mv {}/{}_2_val_2.fq {}/{}_2.fq".format(raw_dir,runs[0],out_dir,sample),file=out_file)
		elif run_no == 2:
			print("cat {}/{}_1_val_1.fq {}/{}_1_val_1.fq >> {}/{}_1.fq".format(raw_dir,runs[0],raw_dir,runs[1],out_dir,sample),file=out_file)
			print("cat {}/{}_2_val_2.fq {}/{}_2_val_2.fq >> {}/{}_2.fq".format(raw_dir,runs[0],raw_dir,runs[1],out_dir,sample),file=out_file)
		elif run_no == 3:	
			print("cat {}/{}_1_val_1.fq {}/{}_1_val_1.fq {}/{}_1_val_1.fq >> {}/{}_1.fq".format(raw_dir,runs[0],raw_dir,runs[1],raw_dir,runs[2],out_dir,sample),file=out_file)
			print("cat {}/{}_2_val_2.fq {}/{}_2_val_2.fq {}/{}_2_val_2.fq >> {}/{}_2.fq".format(raw_dir,runs[0],raw_dir,runs[1],raw_dir,runs[2],out_dir,sample),file=out_file)
		elif run_no == 4:
			print("cat {}/{}_1_val_1.fq {}/{}_1_val_1.fq {}/{}_1_val_1.fq {}/{}_1_val_1.fq >> {}/{}_1.fq".format(raw_dir,runs[0],raw_dir,runs[1],raw_dir,runs[2],raw_dir,runs[3],out_dir,sample),file=out_file)
			print("cat {}/{}_2_val_2.fq {}/{}_2_val_2.fq {}/{}_2_val_2.fq {}/{}_2_val_2.fq >> {}/{}_2.fq".format(raw_dir,runs[0],raw_dir,runs[1],raw_dir,runs[2],raw_dir,runs[3],out_dir,sample),file=out_file)
		else:
			print("cat {}/{}_1_val_1.fq {}/{}_1_val_1.fq {}/{}_1_val_1.fq {}/{}_1_val_1.fq {}/{}_1_val_1.fq >> {}/{}_1.fq".format(raw_dir,runs[0],raw_dir,runs[1],raw_dir,runs[2],raw_dir,runs[3],raw_dir,runs[4],out_dir,sample),file=out_file)
			print("cat {}/{}_2_val_2.fq {}/{}_2_val_2.fq {}/{}_2_val_2.fq {}/{}_2_val_2.fq {}/{}_2_val_2.fq >> {}/{}_2.fq".format(raw_dir,runs[0],raw_dir,runs[1],raw_dir,runs[2],raw_dir,runs[3],raw_dir,runs[4],out_dir,sample),file=out_file)
# --------------------------------------------------
if __name__ == '__main__':
	main()
