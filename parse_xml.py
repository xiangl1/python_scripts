#!/usr/bin/env python3

import argparse
import os
import sys
import xml.etree.ElementTree as ET

# ----------------------------------------------------
def get_args():
	parser = argparse.ArgumentParser(description='get download url from xml file')
	parser.add_argument('xml', help='A positional argument',
						metavar='xml file name')
	parser.add_argument('-d', '--in_dir', help='input xml file',
						metavar='input directory', type=str)
	return parser.parse_args()

# ----------------------------------------------------
def main():
	args = get_args()
	in_file = args.in_dir + "/"+args.xml
	root = ET.parse(in_file).getroot()
	for folder in root.findall('folder'):
		if folder.get('name') == 'QC Filtered Raw Data':
			for f in folder.findall('file'):
				url = f.get('url')
				out_name = args.xml.replace(".xml","")+'_qc_raw'
		elif folder.get('name') == 'Raw Data':
			for f in folder.findall('file'):
				url = f.get('url')
				out_name = args.xml.replace(".xml","")+'_raw'
	prefix = 'https://genome.jgi.doe.gov'
	download_link = prefix + url
	print(download_link+'\t'+out_name)

# ----------------------------------------------------
if __name__ == '__main__':
	main()
