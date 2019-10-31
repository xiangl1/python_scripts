#!/usr/bin/env python3
"""NCBI Esearch and Efetch download"""

import argparse
import os
import sys
import csv
import requests
import re

# --------------------------------------------------
def get_args():
	"""get args"""
	parser = argparse.ArgumentParser(description='ncbi download')
	parser.add_argument('-i', '--infile', help='NCBI E-utility formatted search term or file with accession number list',
						type=str, metavar='STR or FILE', required=True)
	parser.add_argument('-db', '--database', help='NCBI E-utility database (default: nucletide)',
						type=str, metavar='STR', default='nucleotide')
	parser.add_argument('-r', '--rettype', help='NCBI efetch rettype (default: fasta)',
						type=str, metavar='STR', default='fasta')
	parser.add_argument('-o', '--outfile', help='Output file name',
						type=str, metavar='FILE', required=True)
	return parser.parse_args()

# --------------------------------------------------
def main():
	"""main"""
	args = get_args()
	infile = args.infile
	database = args.database
	rettype = args.rettype
	outfile = args.outfile
	
	# E-utils base
	base = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/'
	
	# retrieve by accession number list
	if os.path.isfile(infile):
		acc_list = open(infile,'r').read().splitlines()
		count = len(acc_list)
		
		# write to output file
		with open(outfile,'w') as out_f:
		
		# retrieve with batch of 50
			batch = 50
			for start in range(0,count+batch,batch):
				end = start + batch
				id_list = ''
				if (end <= count):
					id_list = ','.join(acc_list[start:end])
				else:
					id_list = ','.join(acc_list[start:count])
			
				efetch_url = base + 'efetch.fcgi?db={}&id={}&rettype={}&retmode=text'.format(database,id_list,rettype)
				efetch_url_content = requests.get(efetch_url).text
				print('{}'.format(efetch_url_content),file=out_f)
	
	# retrieve by ncbi search term
	else:
		query = infile
	
		# assemble the esearch URL
		url = base+'esearch.fcgi?db={}&term={}&usehistory=y'.format(database,query)
	
		# get the content of esearch URL
		output = requests.get(url).text

		# parse WebEnv, QueryKey and Count
		web = re.search(r'<WebEnv>(\S+)<\/WebEnv>',output).group(1)
		key = re.search(r'<QueryKey>(\d+)<\/QueryKey>',output).group(1)
		count = re.search(r'<Count>(\d+)<\/Count>',output).group(1)
		
		# write to output file
		with open(outfile,'w') as out_f:
			# retrieve data in batches of 500
			retmax = 500

			for ret in range(0,int(count),retmax):
				efetch_url = base + 'efetch.fcgi?db={}&WebEnv={}'.format(database,web)
				efetch_url = efetch_url + '&query_key={}&retstart={}'.format(key,ret)
				efetch_url = efetch_url + '&retmax={}&rettype={}&retmode=text'.format(retmax,rettype)
				efetch_url_content = requests.get(efetch_url).text
				print('{}'.format(efetch_url_content),file=out_f)
# --------------------------------------------------
if __name__ == '__main__':
	main()
