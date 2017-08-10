"""
Script to take in the data files and return an easy to work with data frame

Wren Saylor
August 2 2017
"""

import argparse
from collections import Counter
import numpy as np
import pandas as pd

def readData(filename):
	dataframe = pd.read_csv(filename,sep=',')
	return dataframe

def collectnonUniqueColNames(pdDataFrame):
	stringCols = pdDataFrame.columns
	print '{0} columns read in from data'.format(len(stringCols))
	nonUniqueCols = [k for (k,v) in Counter(stringCols).iteritems() if v > 1]
	print '{0} columns repeated'.format(len(nonUniqueCols))
	return nonUniqueCols

def reducebyColumnName(listDataFrame,nonUniqueCols):
	reduceDataFrame = reduce(lambda left,right: pd.merge(left,right,on=nonUniqueCols), listDataFrame)
	return reduceDataFrame

def savePanda(pdDataFrame,fileName):
	pdDataFrame.to_csv(fileName,sep='\t')

def main(dFiles):
	collectDataFrames = []
	for fileName in dFiles:
		pdDataFrame = readData(fileName)
		collectDataFrames.append(pdDataFrame)
	catDataFrames = pd.concat(collectDataFrames,axis=1)
	nonUniqueCols = collectnonUniqueColNames(catDataFrames)
	# use column names to merge data frames, if name present in two data frames
	mergeDataFrames = reducebyColumnName(collectDataFrames,nonUniqueCols)
	print mergeDataFrames


if __name__ == "__main__":
	main()
