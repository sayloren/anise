"""
Script to print a pair of over/under histogram for int

Wren Saylor
September 2 2017
"""

import argparse
import FlowChart
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
	parser.add_argument("-colh","--columnhistogram",type=str,default="ReasonEnded",help="Column to subset data by")
	parser.add_argument("-v","--subsetvalue",type=int,nargs='+',default="6",help="Largest increment to subset by")
	parser.add_argument("-cols","--columnsubset",type=str,default="LengthofMatchMonths",help="Column to make histogram from subseted data")
	parser.add_argument("-i","--ignoregroups",nargs='*',type=str,default=["Unknown","Other"],help="Groups to ignore in the column that you want to make a histogram from")
	parser.add_argument("-n","--numberbars",type=int,default="6",help="Of the most common values, how many of the top do you want to see")
	return parser.parse_args()

def read_file_to_panda(filename):
	dataframe = pd.read_csv(filename,sep=',')
	return dataframe

def subset_data_by_value(pdFile,columnSubsetValue,subsetFinal):
	underVal = pdFile.loc[pdFile[columnSubsetValue] <= subsetFinal]
	overVal = pdFile.loc[pdFile[columnSubsetValue] > subsetFinal]
	return overVal,underVal

def aggregate_most_common(df,numBars,columnHistogram,ignoreCols):
	if ignoreCols:
		columnList = df[columnHistogram].unique().tolist()
		for item in ignoreCols:
			if item in columnList:
				columnList.remove(item)
		subOver = df[df[columnHistogram].isin(columnList)]# == False
		overAgg = subOver.groupby([columnHistogram])[columnHistogram].agg({"count": len})
	else:
		overAgg = df.groupby([columnHistogram])[columnHistogram].agg({"count": len})
	sortOver = overAgg.sort_values("count", ascending=False)
	numOver = sortOver.head(numBars).reset_index()
	return numOver

def graph_histogram(overAgg,underAgg,columnHistogram,subsetFinal,numBars):
	gs = gridspec.GridSpec(2,1,height_ratios=[1,1])
	gs.update(hspace=.5) # setting the space between the graphs
	
# 	ax0 = plt.subplot(gs[0])
	sns.set_style('ticks')
	pp = PdfPages('HistogramSplit.pdf')
	plt.figure(figsize=(7,7))
	sns.set_palette("husl",n_colors=numBars)# number different columns
	ax0 = plt.subplot(gs[0,:])
	sns.barplot(underAgg['count'],underAgg[columnHistogram],linewidth=0.3,ax=ax0)
	ax0.set_title('Top {0} Under {1} Months'.format(numBars,subsetFinal),size=10)
	sns.set_context(font_scale=.5)
	sns.despine()
	ax1 = plt.subplot(gs[1,:])
	sns.barplot(overAgg['count'],overAgg[columnHistogram],linewidth=0.3,ax=ax1)
	ax1.set_title('Top {0} Over {1} Months'.format(numBars,subsetFinal),size=10)
	sns.set_context(font_scale=.5)
	sns.despine()
	plt.savefig(pp, format='pdf',bbox_inches='tight')
# 	plt.tight_layout()
	pp.close()

def main():
	# Collect arguments
	args = get_args()
	file = args.file
	columnSubsetValue = args.columnsubset
	subsetFinal = args.subsetvalue
	columnHistogram = args.columnhistogram
	numBars = args.numberbars
	ignoreCols = args.ignoregroups
	
	pdFile = read_file_to_panda(file)
	overVal,underVal = subset_data_by_value(pdFile,columnSubsetValue,subsetFinal)
	
	overAgg = aggregate_most_common(overVal,numBars,columnHistogram,ignoreCols)
	underAgg = aggregate_most_common(underVal,numBars,columnHistogram,ignoreCols)
	
	graph_histogram(overAgg,underAgg,columnHistogram,subsetFinal,numBars)

if __name__ == "__main__":
	main()