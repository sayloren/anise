"""
Script to make a simple correlative line plot for each two int/float columns in file

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
	parser.add_argument("-y","--columnony",type=int,help="Column to correlate to all other columns")
	parser.add_argument("-s","--stringname",type=str,help="string to add to out file name to avoid overwriting files")
	return parser.parse_args()

def read_file_to_panda(filename):
	dataframe = pd.read_csv(filename,sep=',')
	return dataframe

def main():
	# Collect arguments
	args = get_args()
	file = args.file
	ycolumn = args.columnony
	stringname =args.stringname
	
	# Read in the file
	pdfile = read_file_to_panda(file)

if __name__ == "__main__":
	main()