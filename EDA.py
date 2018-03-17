from __future__ import division
import sys, os
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import collections
import html_content
import argparse
sns.set(rc={'axes.facecolor':'#f2f2f2', 'figure.facecolor':'#f2f2f2'})

def indexpage(data):
	index_file = open('index.html','w')
	## writting the header in the file
	index_file.write(html_content.index_header)

	## data quality overview
	data = pd.read_csv(data)
	data_desc = {}
	data_desc['No of Variables'] = data.shape[1]
	data_desc['No of Observations'] = data.shape[1]*data.shape[0]
	totalMissingValues = data.isnull().sum().sum()
	data_desc['Total Missing (%)'] = str(round(totalMissingValues/(data.shape[1]*data.shape[0]), 3)*100) + '%'
	df_test = pd.DataFrame.from_dict(data=data_desc,orient='index', dtype=None)

	index_file.write(df_test.to_html(header=False))

	## collecting data types of the variables and storing it in a barplot fig
	dt = data.dtypes.value_counts()
	dt_df = pd.DataFrame({'datatype':dt.index, '#vars':dt.values})
	plt.figure()
	barplot_dtype = sns.barplot(x='datatype',y='#vars', data=dt_df, palette='Spectral')
	dir_path = os.path.abspath(os.path.dirname(__file__))
	fig_path = str(dir_path+'/images/'+"barplot_datatypes.png")
	plt.savefig(fig_path)

	## displaying the datatype fig
	index_file.write(html_content.barplot_datatype_fig)
	index_file.close()

	


def variable_exploration(data):
	var_page = open('variable_exploration.html','w')

	## writting the header in the file
	var_page.write(html_content.variable_header)
	# getting only numeric columns
	data = pd.read_csv(data)
	num_cols = data._get_numeric_data().columns
	# iterating each variable and 
	for column in num_cols:
		try:

			series = data[column]

			### variable info writing as table
			variableInfoDict = {}
			variableInfoDict['Distinct Values'] = len(series.unique())
			variableInfoDict['Distinct(%)'] = str(round((float(variableInfoDict['Distinct Values'])/(series.shape[0])*100),2))+"%"
			df_dict = pd.DataFrame.from_dict(data=variableInfoDict,orient='index', dtype=None)
			var_page.write(html_content.card_header)
			## left content-- variable name and table 
			var_page.write(html_content.card_left_header)
			var_page.write("<h2><b>%s</b></h2>"%(column))
			var_page.write(df_dict.to_html(header=False))
			

			# 5 sample values
			var_page.write(html_content.pad_div)
			var_page.write("<h3><b>Most frequently occuring values</b></h3>")
			var_page.write(series.value_counts().to_frame().head(5).to_html(header=False))
			var_page.write(html_content.close_div)


			var_page.write(html_content.close_div)

			
			# right content - dist plots of variables
			var_page.write(html_content.card_right_header)
			dir_path = os.path.abspath(os.path.dirname(__file__))
			hist_series = series.dropna()
			plt.figure()
			dist_plot = sns.distplot(hist_series)
			dist_plot.autoscale()
			dist_file = str("hist_%s.png"%(series.name))
			fig_path = str(dir_path+'/images/'+dist_file)
			plt.savefig(fig_path)
			plt.close()


			# image tags
			var_page.write("""
			<img src="
			""".rstrip('\n'))
			var_page.write("images/%s"%(dist_file).rstrip('\n'))
			var_page.write("""
			" alt="Avatar" style="width:80% ; height:80%">
			""")


			var_page.write(html_content.close_div)
			var_page.write(html_content.card_footer)


		except Exception as e:
			print (column,e)



def main(file_name):

	'''
	Create the image folders
	'''
	dir_path = os.path.abspath(os.path.dirname(__file__))
	image_path = os.path.join(dir_path,'images')
	
	os.mkdir(image_path)

	### Create index page -- containing overall description of variables

	indexpage(file_name)

	variable_exploration(file_name)



if __name__ == '__main__':

	parser = argparse.ArgumentParser(description='Pass CSV for EDA')
	parser.add_argument('-a','--file_name', help='file in proper csv format', required=True)

	args = parser.parse_args()
	main(args.file_name)