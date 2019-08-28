#!/usr/bin/env python3
"""count bowtie output sam"""

import argparse
import os
import sys
import csv

# --------------------------------------------------
def get_args():
	"""get args"""
	parser = argparse.ArgumentParser(description='count bowtie sam')
	parser.add_argument('-i', '--infile', help='bowtie sam',
						type=str, metavar='FILE', required=True)
	parser.add_argument('-od', '--out_dir', help='output dir',
						type=str, metavar='PATH', required=True)	
	parser.add_argument('-o', '--outfile', help='output file',
						type=str, metavar='FILE', required=True)
	return parser.parse_args()

# --------------------------------------------------
def main():
	"""main"""
	args = get_args()
	infile = args.infile
	out_dir = args.out_dir
	outfile = args.outfile

	in_dir = os.path.dirname(os.path.abspath(infile))
	output = out_dir+'/'+outfile
	temp_bam = 'temp_'+outfile+'.bam'	
	temp_sort_bam = 'temp_'+outfile+'_sorted.bam'
	temp_count = 'temp_'+outfile

	os.chdir(in_dir)
	#os.system('module load samtools')
	os.system('samtools view -bS '+infile+'> '+temp_bam)
	os.system('samtools sort '+temp_bam+' -o '+temp_sort_bam)
	os.system('samtools index '+temp_sort_bam)
	os.system('samtools idxstats '+temp_sort_bam+'> '+temp_count)
	
	os.system('awk -F"\t" \'$3 > 0\' '+temp_count+' > '+output)
	os.system('rm -rf temp_'+outfile+'*')

# --------------------------------------------------
if __name__ == '__main__':
	main()
