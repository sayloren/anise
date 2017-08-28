"""
Script to merge two csv files

Wren Saylor
August 22 2017
"""

import argparse
import pandas as pd
import collections

def get_args():
	parser = argparse.ArgumentParser(description="Description")
	parser.add_argument("afile", type=argparse.FileType('rU'), help='Your first csv file, comma separation expected')
	parser.add_argument("bfile", type=argparse.FileType('rU'), help='Your second csv file, comma separation expected')
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
	aFile = args.afile
	bFile = args.bfile
	print 'Collecting the data files from {0} and {1}'.format(aFile,bFile)
	
	# make panda data frame
	pdA = read_file_to_panda(aFile)
	pdB = read_file_to_panda(bFile)
	
	concatFiles = pd.concat([pdA,pdB],axis=1)
	nonUniqueCols = collect_nonunique_column_names(concatFiles)
	print 'You have {0} shared columns with labels {1}'.format(len(nonUniqueCols),nonUniqueCols)
	
	print concatFiles.head()
	
	mergeDataFrames = merge_dataframes_on_single_column(pdA,pdB,nonUniqueCols)
	print mergeDataFrames.head()
	
	savePanda(mergeDataFrames,'merged.txt')

if __name__ == "__main__":
	main()