"""
Script to make a histogram for a column, based on the subseted data fraom another column

Wren Saylor
July 23 2017
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
	parser.add_argument("file", type=argparse.FileType('rU'), help='A csv file with the data you want to look at')
	parser.add_argument("-colh","--columnhistogram",type=str,default="ReasonEnded",help="Column to subset data by")
	parser.add_argument("-v","--subsetvalue",type=int,nargs='+',default="6",help="Largest increment to subset by")
	parser.add_argument("-s","--subsetstep",type=int,nargs='+',default="3",help="Increment to step the subset by")
	parser.add_argument("-cols","--columnsubset",type=str,default="LengthofMatchMonths",help="Column to make histogram from subseted data")
	parser.add_argument("-i","--ignoregroups",nargs='*',type=str,default=["Unknown","Other"],help="Groups to ignore in the column that you want to make a histogram from")
	parser.add_argument("-n","--numberbars",type=int,default="6",help="Of the most common values, how many of the top do you want to see")
	return parser.parse_args()

def read_file_to_panda(filename):
	dataframe = pd.read_csv(filename,sep=',')
	return dataframe

def subset_data_by_value(pdFile,columnSubsetValue,subsetRange):
	listDF = []
	listNames = []
	for step in subsetRange:
		under = pdFile.loc[pdFile[columnSubsetValue] <= step]
		listNames.append(step)
		listDF.append(under)
	final = subsetRange[-1]
	over = pdFile.loc[pdFile[columnSubsetValue] > final]
	listDF.append(over)
	listNames.append(final)
	return listDF,listNames

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

def graph_histogram(collectAgg,listNames,columnHistogram,subsetFinal,numBars):
	finalName = listNames[-1]
	finalDF = collectAgg[-1]
	
	del collectAgg[-1]
	del listNames[-1]
	
	sns.set_style('ticks')
	pp = PdfPages('Histogram.pdf')
	plt.figure(figsize=(5,5))
	sns.set_palette("husl",n_colors=numBars)
	for df,name in zip(collectAgg,listNames):
		sns.barplot(df['count'],df[columnHistogram],linewidth=0.3)
		plt.title('Top {0} Under {1} Months'.format(numBars,name),size=10)
		plt.tight_layout()
		sns.set_context(font_scale=.5)
		sns.despine()
		plt.savefig(pp, format='pdf')
	sns.barplot(finalDF['count'],finalDF[columnHistogram],linewidth=0.3)
	plt.title('Top {0} Over {1} Months'.format(numBars,finalName),size=10)
	sns.set_context(font_scale=.5)
	sns.despine()
	plt.tight_layout()
	plt.savefig(pp, format='pdf')
	pp.close()

def main():
	# Collect arguments
	args = get_args()
	file = args.file
	columnSubsetValue = args.columnsubset
	subsetFinal = args.subsetvalue
	stepSize = args.subsetstep
	subsetRange = np.arange(0,(subsetFinal+stepSize),stepSize).tolist()
	columnHistogram = args.columnhistogram
	numBars = args.numberbars
	ignoreCols = args.ignoregroups
	
	pdFile = read_file_to_panda(file)
	listDF,listNames = subset_data_by_value(pdFile,columnSubsetValue,subsetRange)
	
	collectAgg = []
	for df in listDF:
		aggDF = aggregate_most_common(df,numBars,columnHistogram,ignoreCols)
		collectAgg.append(aggDF)
	
	graph_histogram(collectAgg,listNames,columnHistogram,subsetFinal,numBars)

if __name__ == "__main__":
	main()