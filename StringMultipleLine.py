"""
Script to get number of each input string for column

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
	parser.add_argument("-colx","--columnxaxis",type=str,default="LengthofMatchMonths",help="Integer column to go along the x axis")
	parser.add_argument("-s","--ystring",type=str,nargs='+',default=["Volunteer too busy","Recipient deceased","Recipient too difficult"],help="Strings values to graph")
	parser.add_argument("-coly","--columnyaxis",type=str,default="ReasonEnded",help="String column to graph on y axis")
	return parser.parse_args()

def read_file_to_panda(filename):
	dataframe = pd.read_csv(filename,sep=',')
	return dataframe

def print_unique(pdFile,ColYAxis):
	unique = pdFile[ColYAxis].unique()
	print unique

def split_compound_string(subsetCols,ColXAxis,ColYAxis):
	toSplit = subsetCols[subsetCols[ColYAxis].str.contains(";")]
	noSplit = subsetCols[~subsetCols[ColYAxis].str.contains(";")]
	dfSplit = pd.DataFrame(toSplit[ColYAxis].str.split(';').tolist(), index=toSplit[ColXAxis]).stack()
	dfSplit = dfSplit.reset_index()[[0, ColXAxis]]
	dfSplit.columns = [ColYAxis,ColXAxis]
	frames = [dfSplit,noSplit]
	catSplit = pd.concat(frames,axis=0)
	return catSplit

def aggregate_by_y_col_count(subsetStr,ColXAxis,ColYAxis,strList):
	dfList = []
	for group in strList:
		groupStr = (subsetStr[subsetStr[ColYAxis] == group])
		agg = groupStr.groupby([ColXAxis])[ColXAxis].agg({"count": len})
		reset = agg.reindex(fill_value=0)
		dfList.append(reset)
	return dfList

def graph_lines(dfList,ColXAxis,strList):
	sns.set_style('ticks')
	pp = PdfPages('LineGraphs.pdf')
	plt.figure(figsize=(5,5))
	sns.set_palette("husl",n_colors=len(strList))

	gs = gridspec.GridSpec(1,2,height_ratios=[1])
	gs.update(hspace=.5) # setting the space between the graphs
	ax0 = plt.subplot(gs[0,0])
	ax1 = plt.subplot(gs[0,1],sharey=ax0)
	for df,name in zip(dfList,strList):
		ax0.plot(df[0:15],label=name)#x=ColXAxis,y='count',data=df
		ax1.plot(df[15:],label=name)
		plt.legend(loc=0,fontsize=5,labelspacing=0.1)
# 	plt.title('Top {0} Under {1} Months'.format(numBars,name),size=10)
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
	strList = args.ystring
	ColYAxis = args.columnyaxis
	
	# Read in the file
	pdFile = read_file_to_panda(file)
	
	# Select the columns we are looking for
	subsetCols = pdFile[[ColXAxis,ColYAxis]]
	
	# Remove rows with NA in the columns we are looking at
	subsetNA = remove_nan_values(subsetCols,ColXAxis,ColYAxis)
	
	# Print out the unique values for Y axis column
	print_unique(subsetNA,ColYAxis)
	
	# Split any ; into separate rows so as not to miss data
	catSplit = split_compound_string(subsetNA,ColXAxis,ColYAxis)
	
	# Find the particular strings to look at in the Y axis
	subsetStr = catSplit[catSplit[ColYAxis].isin(strList)]
	
	# Aggregate the selected strings in the Y axis by X axis
	dfList = aggregate_by_y_col_count(subsetStr,ColXAxis,ColYAxis,strList)
	
	# Graph
	graph_lines(dfList,ColXAxis,strList)

if __name__ == "__main__":
	main()