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
	parser.add_argument("-c","--columns",type=int,nargs='*',help="0 based columns to get stats for")
	parser.add_argument("-s","--stringname",type=str,help="string to add to out file name to avoid overwriting files")
	return parser.parse_args()

def read_file_to_panda(filename):
	dataframe = pd.read_csv(filename,sep=',')
	return dataframe

def descriptive_stats(df):
	description = df.describe(include='all')
	print description
	return description

def graph_on_facet(df,stringname):
	pp = PdfPages('Descriptive_Stats{0}.pdf'.format(stringname))
	sns.set_style('ticks')
	sns.set_palette("husl")

	s = sns.FacetGrid(df)


# 	plt.title('{0} by {1} '.format(colxaxis,colyaxis),size=10)
# 	sns.set_context(font_scale=.5)
	sns.despine()
# 	plt.tight_layout()
	plt.savefig(pp, format='pdf',bbox_inches='tight')
	pp.close()





def main():
	# Collect arguments
	args = get_args()
	file = args.file
	statscolumns = args.columns
	
	# Read in the file
	pdfile = read_file_to_panda(file)

	# Select the columns we are looking for
	subsetcols = pdfile.iloc[:,statscolumns]
	description = descriptive_stats(subsetcols)
	graph_on_facet(df,args.stringname)
	
	# number of non-na values in each column
	# range, mean, std
	# hist on facet grid

if __name__ == "__main__":
	main()