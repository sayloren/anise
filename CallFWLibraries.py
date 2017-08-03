"""
Script to analyze FrienshipsWorks data

Wren Saylor
July 23 2017
"""

import argparse
import ProcessInDataLibrary

def get_args():
	parser = argparse.ArgumentParser(description="Description")
	parser.add_argument("dfile", type=argparse.FileType('rU'), help='A file containing a list of paths to the element files with unique names separated by newlines')
	return parser.parse_args()

def main():
	# Collect arguments
	args = get_args()
	dFiles = [line.strip() for line in args.dfile]
	print 'Collecting the data files from {0}'.format(dfile)
	
	ProcessInDataLibrary.main(dFiles)

if __name__ == "__main__":
	main()