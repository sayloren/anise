"""
Script to analyze FrienshipsWorks data

Wren Saylor
July 23 2017
"""

import pandas as pd
import numpy as np
import argparse
import seaborn as sns
import matplotlib as mpl
import matplotlib.pyplot as plt

def get_args():
	parser = argparse.ArgumentParser(description="Description")
	parser.add_argument("dfile", type=argparse.FileType('rU'), help='A file containing a list of paths to the element files with unique names separated by newlines')
	return parser.parse_args()

def readData(filename):
	dataframe = pd.read_csv(filename,sep=',')
	return dataframe

def collectnonUniqueColNames(pdDataFrame):
	stringCols = pdDataFrame.columns
	return stringCols

def reducebyColumnName(listDataFrame):
	reduceDataFrame = reduce(lambda left,right: pd.merge(left,right,on=column), catDataFrames)
	return reduceDataFrame

def savePanda(pdDataFrame,fileName):
	pdDataFrame.to_csv(fileName,sep='\t')

def main():
	# Collect arguments
	args = get_args()
	dFiles = [line.strip() for line in args.dfile]
	collectDataFrames = []
	for fileName in dFiles:
		pdDataFrame = readData(fileName)
		collectDataFrames.append(pdDataFrame)
	catDataFrames = pd.concat(collectDataFrames,axis=1)
# 	mergeDataFrames = reducebyColumnName(collectDataFrames)
	stringCol = collectnonUniqueColNames(catDataFrames)
	# collect column names, get non-unique, use to reduce in loop
	print stringCol
	savePanda(stringCol,'check.txt')


if __name__ == "__main__":
	main()