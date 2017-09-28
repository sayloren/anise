"""
Script to merge two csv files

To Do:
Is perhaps a little sloppy, find way to merge list of dfs

Wren Saylor
August 22 2017
"""

import argparse
import pandas as pd
import collections
import re

def get_args():
	parser = argparse.ArgumentParser(description="Description")
	parser.add_argument("afile", type=str, help='Your first csv file, comma separation expected')
	parser.add_argument("bfile", type=str, help='Your second csv file, comma separation expected')
	return parser.parse_args()

def read_file_to_panda(filename):
	dataframe = pd.read_csv(filename,sep=',')
	return dataframe

def collect_nonunique_column_names(pdDataFrame):
	stringCols = pdDataFrame.columns
	print '{0} columns read in from data'.format(len(stringCols))
	nonUniqueCols = [k for (k,v) in collections.Counter(stringCols).iteritems() if v > 1]
	print '{0} columns repeated'.format(len(nonUniqueCols))
	return nonUniqueCols

def reduce_by_multiple_column_names(listDataFrame,nonUniqueCols):
	reduceDataFrame = reduce(lambda left,right: pd.merge(left,right,on=nonUniqueCols), listDataFrame)
	return reduceDataFrame

def merge_dataframes_on_single_column(frameA,frameB,sharedcolumn):
	pdMerge = pd.merge(frameA,frameB,how='inner',on=sharedcolumn)
	return pdMerge

def savePanda(pdDataFrame,fileName):
	pdDataFrame.to_csv(fileName,sep='\t')

def main():
	# Collect arguments
	args = get_args()
	afile = args.afile
	bfile = args.bfile
	print 'Collecting the data files from {0} and {1}'.format(afile,bfile)
	
	# make panda data frame
	pda = read_file_to_panda(afile)
	pdb = read_file_to_panda(bfile)
	
	concatFiles = pd.concat([pda,pdb],axis=1)
	nonUniqueCols = collect_nonunique_column_names(concatFiles)
	print 'You have {0} shared columns with labels {1}'.format(len(nonUniqueCols),nonUniqueCols)
	
	# remove file extension .csv (will have to change if txt or other extension used)
	stripa = re.sub(r'\.csv$','', args.afile)
	stripb = re.sub(r'\.csv$','', args.bfile)

	# merge df on shared columns
	mergeDataFrames = merge_dataframes_on_single_column(pda,pdb,nonUniqueCols)
	
	# strip .csv
	savePanda(mergeDataFrames,'merged_{0}_{1}.txt'.format(stripa,stripb))

if __name__ == "__main__":
	main()