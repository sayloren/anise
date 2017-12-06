"""
Script to run some descriptive statistics for given int/float columns

Wren Saylor
September 27 2017
"""

import argparse
import pandas as pd
import seaborn as sns
import matplotlib as mpl
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.gridspec as gridspec
import matplotlib.patches as patches
import matplotlib.pyplot as plt
import numpy as np

def get_args():
	parser = argparse.ArgumentParser(description="Description")
	parser.add_argument("file", type=argparse.FileType('rU'),default="MatchesClosed.csv",help='A csv file with the data you want to look at')
	parser.add_argument("-c","--columnss",type=int,nargs='*',help="Columns with ints or floats to get statistics for")
	parser.add_argument("-s","--stringname",type=str,help="string to add to out file name to avoid overwriting files")
	return parser.parse_args()

def read_file_to_panda(filename):
	dataframe = pd.read_csv(filename,sep=',')
	return dataframe

def main():
	# Collect arguments
	args = get_args()
	file = args.file
	statscolumns = args.columnss
	stringname =args.stringname
	
	# Read in the file
	pdfile = read_file_to_panda(file)

	# Select the columns we are looking for
	subsetcols = pdfile.iloc[statscolumns]

	# number of non-na values in each column
	# range, mean, std
	# hist on facet grid

if __name__ == "__main__":
	main()