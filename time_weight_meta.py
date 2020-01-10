#!/usr/bin/env python3
"""environmental variable time weighted"""

import argparse
import os
import sys
import csv
import re
from collections import defaultdict

# --------------------------------------------------
def get_args():
	"""get args"""
	parser = argparse.ArgumentParser(description='time weighted environmental variables calculation')
	parser.add_argument('-e', '--env_file', help='original environmental data with sampling day of year',
						type=str, metavar='FILE', required=True)
	parser.add_argument('-b', '--bio_file', help='biological sample with sampling day of year',
						type=str, metavar='FILE', required=True)
	parser.add_argument('-i', '--index', help='environmental variable column index',
						type=int,metavar='INT',required=True)

	parser.add_argument('-o', '--outfile', help='Output file',
						type=str, metavar='FILE', required=True)
	return parser.parse_args()

# --------------------------------------------------
def weight_calculate(bio_doy,env_doy,variable):
	if variable != 'NA' and 0 < 17 - abs(int(bio_doy)-int(env_doy)) < 17:	
		weight = 17 - abs(int(bio_doy)-int(env_doy))
		return((weight, variable))

# --------------------------------------------------
def calculate_new_value(variable_weight_list):
	y_d = 0
	y_n = 0
	for weight, value in variable_weight_list:
		if value == '':
			continue
		y_d += int(weight)*float(value)
		y_n += int(weight)
	return(round(y_d/y_n,3))

# --------------------------------------------------
def main():
	"""main"""
	args = get_args()
	env_file = args.env_file
	bio_file = args.bio_file
	var_index = int(args.index)
	out_file = open(args.outfile,'w')
	
	
	"""save bio sample informations"""
	tp_list = []
	with open(bio_file,'r') as bio_f:
		reader = csv.reader(bio_f,delimiter = ',')
		next(reader)
		for line in reader:
			(sample_id,year,doy) = (line[0],line[1],line[2])
			tp_list.append((sample_id,year,doy))

	""" save env sample informations """
	env_tp_list = []
	with open(env_file, 'r') as env_f:
		reader = csv.reader(env_f, delimiter = ',')
		next(reader)
		for line in reader:
			(year,doy,chl) = (line[0],line[3],line[var_index])
			env_tp_list.append((year,doy,chl))
	
	""" calculate time-weigted env value"""
	same_doy = []
	for (sample_id,year_1,doy) in tp_list:
		for (year_2,env_doy,chl) in env_tp_list:
			if year_1 == year_2 and doy == env_doy and chl != 'NA':
				same_doy.append(sample_id)
				print('{},{},{},{}'.format(sample_id,year_1,doy,chl),file=out_file)
				continue
	for (sample_id, year_1,doy) in tp_list:
		if sample_id in same_doy:
			continue
		chl_w = []
		for (year_2,env_doy,chl) in env_tp_list:
			chl_w.append(weight_calculate(doy,env_doy,chl))
		filter_list = list(filter(None,chl_w)) 
		#print(filter_list)
		if len(filter_list) != 0:	
			#print(filter_list)
			chl_new = calculate_new_value(filter_list)
			#print(chl_new)
			print('{},{},{},{}'.format(sample_id,year_1,doy,chl_new),file = out_file)
		else:
			print('{},{},{},{}'.format(sample_id,year_1,doy,'NA'),file = out_file)	
# --------------------------------------------------
if __name__ == '__main__':
	main()
