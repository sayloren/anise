"""
Script to look at the distribution of a data set through swarm plot

Wren Saylor
September 13 2017

To Do:
Swarm for none/na/nan
add two y columns for swarm
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
	parser.add_argument("-x","--columnxaxis",type=str,default="LengthofMatchMonths",help="Integer column to go along the x axis")
	parser.add_argument("-y","--columnyaxis",type=str,default="ReasonEnded",help="String column to graph on y axis")
	parser.add_argument("-s","--stringname",type=str,help="string to add to out file name to avoid overwriting files")
	return parser.parse_args()

def read_file_to_panda(filename):
	dataframe = pd.read_csv(filename,sep=',')
	return dataframe

def print_unique(pdFile,ColYAxis):
	unique = pdFile[ColYAxis].unique()
	print unique

def split_compound_string(subsetCols,ColXAxis,ColYAxis):
	# could do column.strip() to remove first space before string
	toSplit = subsetCols[subsetCols[ColYAxis].str.contains("; ")]
	noSplit = subsetCols[~subsetCols[ColYAxis].str.contains("; ")]
	dfSplit = pd.DataFrame(toSplit[ColYAxis].str.split('; ').tolist(), index=toSplit[ColXAxis]).stack()
	dfSplit = dfSplit.reset_index()[[0, ColXAxis]]
	dfSplit.columns = [ColYAxis,ColXAxis]
	frames = [dfSplit,noSplit]
	catSplit = pd.concat(frames,axis=0)
	return catSplit

def graph_swarm(catSplit,ColXAxis,ColYAxis,stringname):
	sns.set_style('ticks')
	pp = PdfPages('SwarmPlots_{0}.pdf'.format(stringname))
# 	plt.figure(figsize=(5,5))
	sns.set_palette("husl")

	gs = gridspec.GridSpec(1,1,height_ratios=[1])
	gs.update(hspace=.5) # setting the space between the graphs
	ax0 = plt.subplot(gs[0,0])
	sns.swarmplot(x=ColXAxis,y=ColYAxis,data=catSplit,ax=ax0)
	plt.title('{0} by {1} '.format(ColXAxis,ColYAxis),size=10)
	sns.set_context(font_scale=.5)
	sns.despine()
# 	plt.tight_layout()
	plt.savefig(pp, format='pdf',bbox_inches='tight')
	pp.close()

def remove_nan_values(subsetCols,ColXAxis,ColYAxis):
	print 'There are {0} rows with NA in {1} column, which will be dropped'.format(subsetCols[ColYAxis].isnull().sum(),ColYAxis)
	print 'There are {0} rows with NA in {1} column, which will be dropped'.format(subsetCols[ColXAxis].isnull().sum(),ColXAxis)
	notNA = subsetCols.dropna()
	return notNA

def main():
	# Collect arguments
	args = get_args()
	file = args.file
	ColXAxis = args.columnxaxis
	ColYAxis = args.columnyaxis
	stringname =args.stringname
	
	# Read in the file
	pdFile = read_file_to_panda(file)
	
	# Select the columns we are looking for
	subsetCols = pdFile[[ColXAxis,ColYAxis]]
	
	# Remove rows with NA in the columns we are looking at
	subsetNA = remove_nan_values(subsetCols,ColXAxis,ColYAxis)
	
	# Print out the unique values for Y axis column
	print_unique(subsetNA,ColYAxis)
	print 'List of unique options before split on ;'
	
	# Split any ; into separate rows so as not to miss data
	catSplit = split_compound_string(subsetNA,ColXAxis,ColYAxis)
	
# 	threshdf = (catSplit[catSplit[ColXAxis] <= 25])
	
	# Print out the unique values for Y axis column
	print_unique(catSplit,ColYAxis)
	print 'List of unique options after split on ;'
	
	
	# Graph
	graph_swarm(threshdf,ColXAxis,ColYAxis,stringname)

if __name__ == "__main__":
	main()