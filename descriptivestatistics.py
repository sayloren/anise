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
	return description.T

def seperate_data_frames(df):
	intdf = df[['mean','std','min','25%','50%','75%','max']]
	strdf = df[['count','unique','top','freq']]
	return intdf,strdf

def two_graphs(intdf,strdf,stringname):
	if stringname:
		pp = PdfPages('Descriptive_Stats{0}.pdf'.format(stringname))
	else:
		pp = PdfPages('Descriptive_Stats.pdf')
	
	sns.set_style('ticks')
	sns.set_palette("husl")
	gs = gridspec.GridSpec(1,2,height_ratios=[1,1])
	gs.update(hspace=.5)
	ax0 = plt.subplot(gs[0,0])
	ax1 = plt.subplot(gs[0,1])
	plt.title('{0} by {1} '.format(colxaxis,colyaxis),size=10)


	print intdf
	print strdf

# 	if both int and str
# 	plot two
# 	else 
# 	plot one

# number of non-na values in each column

# 	int values
# 	sns.barplot(,ax=ax0)
# 	str values
# 	sns.barplot(,ax=ax1)


	plt.tight_layout()
	sns.despine()
	plt.savefig(pp, format='pdf',bbox_inches='tight')
	pp.close()

def main():
	# Collect arguments
	args = get_args()
	file = args.file
	
	# Read in the file
	pdfile = read_file_to_panda(file)

	# subset columns, if argument provided
	if args.columns:
		subsetcols = pdfile.iloc[:,args.columns]
	else:
		subsetcols = pdfile
	
	# get descriptive stats
	description = descriptive_stats(subsetcols)
	
	# separate the int vs str dfs
	intdf,strdf = seperate_data_frames(description)
	
	# graph
	two_graphs(intdf,strdf,args.stringname)


if __name__ == "__main__":
	main()