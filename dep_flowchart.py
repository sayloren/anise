"""
Script to make flow chart

Wren Saylor
August 5 2017

https://github.com/pygraphviz/pygraphviz/blob/master/examples/star.py
"""

import argparse
import pygraphviz as pgv

def makeFlow():

	A=pgv.AGraph()

	A.add_edge('Input Data as .csv Files','Run Main Script with Options')
	A.add_edge('Run Main Script with Options','Return Graphs and Stats')
	
	print(A.string()) # print to screen
	print("Wrote simple.dot")
	A.write('flow.dot') # write to simple.dot

	B=pgv.AGraph('flow.dot') # create a new graph from file
	B.layout() # layout with default (neato)
	B.draw('flow.png') # draw png
	print("Wrote flow.png")

def main():
	makeFlow()
	
if __name__ == "__main__":
	main()