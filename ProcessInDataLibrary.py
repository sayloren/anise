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
	nonUniqueCols = [k for (k,v) in Counter(stringCols).iteritems() if v > 1]
	return nonUniqueCols

def reducebyColumnName(listDataFrame,nonUniqueCols):
	reduceDataFrame = reduce(lambda left,right: pd.merge(left,right,on=column), catDataFrames)
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
# 	mergeDataFrames = reducebyColumnName(collectDataFrames,nonUniqueCols)


if __name__ == "__main__":
    main()
