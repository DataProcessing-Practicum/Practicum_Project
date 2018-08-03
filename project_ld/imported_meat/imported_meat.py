########################################
#
# Authored and edited by
# Louis Discenza
#
########################################

#timer
import time
start = time.time() #gets the start time

#packages required for import
#library for handling PDF text extraction
import tabula as tb        #conda install tabula-py
#library for handling tabular data
import pandas as pd        #default
#library for handling numerical operations
import numpy as np         #default
#library for handling date and time objects
import datetime            #default
#library for handling warning messages
import warnings            #default
#library for handling Operating System commands
import os				   #default
#library for handling regular expressions
import re				   #default
#library for handling URL requests
import urllib.request as ur#default
#dateparser for identifying date objects
from dateutil.parser import parse
#library for handling system operations
import sys					#default

#this command suppresses warning messages related to patterns that
#are not matched when searching the tables
warnings.filterwarnings("ignore", 'This pattern has match groups')

#This option allows us to see up to 1000 rows and columns of a table at a time: 
#the default functionality is to cut out rows and columns in the display.
pd.set_option('display.max_rows', 1000)
pd.set_option('display.max_columns', 1000)

#this command suppresses pandas warning messages about dropping rows and 
#columns from the table index. 
#this may not even be necessary anymore #########################################
pd.options.mode.chained_assignment = None  # default='warn'

#Get the current date as of the time the file is ran
now = datetime.datetime.now()

print(" \n Universal Date-Time Format:\t", now)

#Convert to a month-day format
MMDD = now.strftime("%m%d")

print(" \n MonthMonthDayDay Format:\t", MMDD)

#variable to control how to save the data
#For testing purposes, to_SQL may be set to False
#so as to not send any incomplete data.
to_local   = True

#declare the URL and PATH variables for downloading
#and saving the document.
#Note - PATH2 will vary the filename based on the date
#format above.
URL = "https://www.ams.usda.gov/mnreports/lswimpe.pdf"
print("\n PDF URL:\t"+URL+"\n")
PATH1 = r".\PDFs\importedmeat.pdf"
print("\n Filepath 1:\t"+PATH1+"\n")
PATH2 = r".\PDFs\\"+MMDD+".pdf"
print("\n Filepath 2:\t"+PATH2+"\n")

#a function for saving documents
def save_imported_PDFs(URL, PATH1, PATH2):

	#save the PDF to the destination PATHs specified above.
	#the command opens the URL and initiates the download.
	ur.urlretrieve(URL, PATH1)
	ur.urlretrieve(URL, PATH2)

	#initialize a blank list
	download_succeed = []

	#check to see if files successfully saved to both locations
	if os.path.exists(PATH1):
		print("Downloaded File1 Found\n")
		download_succeed.append(True)
	else:
		print("File Not Found\n")
		download_succeed.append(False)
	if os.path.exists(PATH2):
		print("Downloaded File2 Found\n")
		download_succeed.append(True)
	else:
		print("File Not Found\n")
		download_succeed.append(False)

	#return a boolean based on the success of the downloads
	if all(download_succeed):
		return True
	else:
		return False
 
#call the function 
download_successful = save_imported_PDFs(URL, PATH1, PATH2)

print(" \n All downloads successfully completed:\t", download_successful)

#Reading from a saved file seems to be better than online, because if edits are made
#to that file by us or by them, it is already on our system when code runs
url = PATH2

print("\n Reading file from this directory:\t"+url)

#collect all relevant lists and declare in one spot

#these names are used to keep track of how many tables are being
#processed, and also as text strings for filenames.
names = ["freshbeef",
		 "processedbeef",
		 "freshpork",
		 "processedpork",
		 "lamb",
		 "mutton",
		 "veal",
		 "poultry"
		 ]
		 
print("\n The names of the tables:\t"+str(names)+"\n")

#NEW new areas as of February
#these represent the coordinate-areas used by tabula to find
#the table in the PDF. Currently, these areas accommodate as much white
#space as possible in an attempt to capture any future table expansions.
#However, if dramatic formatting changes are made (a whole new row/column/
#table gets added to the file) these areas may need to be updated.
#Please refer to the Docs on how to change the area coordinates.
area = [
#		#fresh beef
		[552.391,132.939,797.087,1071.548],
		
#		#processed beef
		[19.174,136.591,227.348,1078.852],
		
#		#fresh pork
		[227.348,136.591,481.174,934.592],
		
#		#processed pork
		[493.957,136.591,745.957,657.026],
		
#		#lamb
		[22.826,132.939,194.478,1082.505],
			
#		#mutton
		[187.174,132.939,289.435,662.505],
		
#		#veal
		[287.609,132.939,435.522,1002.157],
			
#		#poultry
		[470.218,131.113,596.218,872.505]
		
		]

print("\n Coordinate-Areas of tables:\t"+str(area)+"\n")

#the page number of each table by index value
page = [1,2,2,2,3,3,3,3]

print("\n Pages of Tables:\t"+str(page)+"\n")


#first column head
cols0 = [['AMR/','Boneless','Cheek/Heart','-','Edible','Head','Other','Primals &'],
		 ['Fully Cooked -','Heat Treated -','Heat Treated','Thermally'],
		 ['-','Boneless','-','Edible','Other','Primals &'],
		 ['Fully Cooked -','Heat Treated -','Heat Treated','Treated -','Second Inhib','Thermally'],
		 ['Boneless','-','-','Edible','Primals &'],
		 ['Boneless','-','-','Edible','Primals &'],
		 ['Boneless','-','-','Edible','Other','Primals &'],
		 ['Processed','Non-Intact','Non-Intact','Intact','(Ducks, Geese,','Intact','Fully Cooked','Thermally']
		]
#second column head
cols1 = [['Carcasses','Trimmings','Meat','Cuts','Offals','Meat','Intact','Subprimals'],
		 ['Not Shelf Stable','Not Shelf Stable','Shelf Stable','Processed'],
		 ['AMR','Trimmings','Cuts','Offals','Intact','Subprimals'],
		 ['Not Shelf Stable','Not Shelf Stable','Shelf Stable','Shelf Stable','Not Shelf Stable','Processed'],
		 ['Trimmings','Carcasses','Cuts','Offals','Subprimals'],
		 ['Trimmings','Carcasses','Cuts','Offal','Subprimals'],
		 ['Trimmings','Carcasses','Cuts','Offal','Intact','Subprimals'],
		 ['Poultry','Chicken','Turkey','Chicken','Squab)','Turkey','Poultry','Processed']
		]
#Rows (countries) to associate data with
rows = [['Australia','Brazil','Canada','Chile','Costa Rica','Honduras','Ireland','Japan','Mexico','New Zealand','Nicaragua','Uruguay','Total'],
		['Argentina','Australia','Brazil','Canada','Mexico','New Zealand','Uruguay','Total'],
		['Brazil','Canada','Chile','Denmark','Finland','Ireland','Mexico','Netherlands','North Ireland','Poland','Spain','United Kingdom','Total'],
		['Canada','Croatia','Denmark','Germany','Hungary','Italy','Mexico','Netherlands','Poland','Spain','Total'],
		['Australia','Canada','Chile','Iceland','New Zealand','Total'],
		['Australia','Chile','New Zealand','Total'],
		['Australia','Canada','New Zealand','Total'],
		['Canada','Chile','Israel','Mexico','South Korea','Total']
		]
#first column head
cols_to_check0 = [['-','AMR/','Beef Patty Prod/','Boneless','Cheek/Heart','-','Edible','Formed','Head','Non-Intact','Other','Other Non-','Primals &'],
		 ['-','Fully Cooked -','Heat Treated -','Heat Treated','Not Heat Treated -','Inhibitors','Thermally'],
		 ['-','-','Boneless','-','-','Edible','Ground Pork','Other','Other Non-','Primals &','-'],
		 ['-','Fully Cooked -','Heat Treated -','Heat Treated','Treated -','Second Inhib','Thermally'],
		 ['-','Boneless','-','-','Edible','Ground','Meals/Dinners/','Other','Other','Primals &'],
		 ['-','Boneless','-','Corned','-','Edible','Primals &'],
		 ['-','Boneless','-','Cheek','-','Edible','Heart','Meal/Dinners/','Non-Intact','Other','Other','Primals &'],
		 ['-','Processed','Non-Intact','Non-Intact','Intact','(Ducks, Geese,','Intact','Fully Cooked','Exposure to the','Thermally']
		]
#second column head
cols_to_check1 = [['-','Carcasses','Ground Beef','Trimmings','Meat','Cuts','Offals','Steaks','Meat','Cuts','Intact','Intact Cuts/Prod','Subprimals'],
		 ['-','Not Shelf Stable','Not Shelf Stable','Shelf Stable','Shelf Stable','Not Shelf Stable','Processed'],
		 ['-','AMR','Trimmings','Carcasses','Cuts','Offals','Products','Intact','Intact Cuts','Subprimals','Sausage'],
		 ['-','Not Shelf Stable','Not Shelf Stable','Shelf Stable','Shelf Stable','Not Shelf Stable','Processed'],
		 ['-','Trimmings','Carcasses','Cuts','Offals','Product','Entrees','Intact','Non-Intact','Subprimals'],
		 ['-','Trimmings','Carcasses','(Species)','Cuts','Offal','Subprimals'],
		 ['-','Trimmings','Carcasses','Meat','Cuts','Offal','Meat','Entrees','Cuts','Intact','Non-Intact','Subprimals'],
		 ['-','Poultry','Chicken','Turkey','Chicken','Squab)','Turkey','Poultry','Environment','Processed']
		]
#Rows 
rows_to_check = [['-','-','Australia','Brazil','Canada','Chile','Costa Rica','France','Honduras','Ireland','Japan','Mexico','Netherlands','New Zealand','Nicaragua','Spain','Uruguay','Total'],
		['-','-','Argentina','Australia','Brazil','Canada','Chile','Costa Rica','Denmark','Italy','Lithuania','Mexico','New Zealand','Uruguay','Total'],
		['-','-','Brazil','Canada','Chile','Costa Rica','Denmark','Finland','France','Ireland','Italy','Mexico','Netherlands','North Ireland','Poland','Spain','United Kingdom','Uruguay','Total'],
		['-','-','Austria','Brazil','Canada','Croatia','Denmark','France','Germany','Hungary','Italy','Lithuania','Mexico','Netherlands','Poland','San Marino','Spain','Uruguay','Total'],
		['-','-','Australia','Canada','Chile','Iceland','Mexico','New Zealand','Northern Ireland','Spain','Uruguay','Total'],
		['-','-','Australia','Chile','New Zealand','Total'],
		['-','-','Australia','Canada','France','Mexico','Netherlands','New Zealand','Uruguay','Total'],
		['-','-','Canada','Chile','Israel','Mexico','South Korea','Total']
		]

#errors
error_list = []

#this read is for obtaining the date
dfc = tb.read_pdf(url, pages=1, guess=False, area=[22.826,132.939,92.217,1327.2])#True

####			if needed, print												#####
print("\n First few lines of first page of document:\n", dfc.head())
####																			#####		


#the way the date is currently formatted, it appears in the top right and is read by
#tabula as a column header for the table that it makes out of the first page
def is_date(string):
	try: 
		parse(string)
		return True
	except ValueError:
		return False
#searching for the date in the file header allows us to get away without specifying it directly
for i in range(len(dfc)):
	for j in range(len(dfc.columns)):
		returnValue = is_date(str(dfc.iloc[i,j]))
		if returnValue:
			print("\n Date found, in cell ", i, j)
			#as the location of the date has been subject to change, the script now identifies its position
			lswimpe_date = dfc.iloc[i,j]
		else:
			lswimpe_date = "Not found"


#the date is printed to compare its formatting.
print("\n Date on Report Reads: "+lswimpe_date+"\n")

#get prior friday
def get_prior_friday(date):

	date = date
	print(date)

	# Days to subtract based on date
	#####     0          1          2         3          4           5           6
	days=["Friday", "Saturday", "Sunday", "Monday", "Tuesday", "Wednesday", "Thursday"]

	# get the day of the week out of the date
	today_date = date.strftime("%A")
	print(today_date)

	# calculate how many days to subtract, print, and format date
	for i in range(len(days)):
		print(days[i])
		if today_date in days[i]:
			print(i)
			days_to_subtract = 7 + i
			break
	print("\n Subtracting " + str(days_to_subtract) + " days from today."+"\n")

	lswimpe_date_fixed = (date - datetime.timedelta(days=days_to_subtract)).strftime("%m/%d/%y")

	#the function returns the fixed date
	return lswimpe_date_fixed

#get today's date I realize this is redundant with some of the code written above
today = datetime.datetime.now()
today_date = today.strftime('%A, %B %d, %Y')
print(" Today's date is: "+today_date+"\n")
	
#if report is ran on a day other than Friday, it needs to report the correct day.
#for example, if a report has to be ran on Monday as opposed to Friday, it cannot
#just look back 7 days and use Monday's date from last week. It needs to get the 
#date of the previous Friday. Obviously, if a report is ran on Monday, then the
#last Friday is the date the report should have come out (3 days ago). The Friday 
#date needed is the Friday before then (10 days ago). A function that retrieves 
#that date is needed.
#adjust the date depending on when program is ran.
lswimpe_date_fixed = get_prior_friday(today)

#the finished date is printed to compare to the original
print(" The date to place in .hst will be formatted as: "+lswimpe_date_fixed+"\n")

#the date is saved just in case, as a template item.
with open(r'.\published_date.txt','w') as text_file:
	text_file.write(lswimpe_date_fixed)
#the date is also thrown into a log file, to monitor when and how often it is ran.
with open(r'.\published_date_log.txt','a') as text_file:
	text_file.write(" "+"\n")
	text_file.write(lswimpe_date_fixed)
	text_file.write(" "+"\n")

#initialize update
update = None

#get comcodes and description
PTH = os.path.dirname(os.path.abspath("imported_meat.csv"))
comcode = pd.read_csv(r''+PTH+r'\imported_meat.csv', index_col=False, usecols=[0,1])
cc_dict = {}

#if columns are not identified uniquely. find intersection.
def find_intersection(x,y):
	x0 = x.index
	y0 = y.index
	z = x0.intersection(y0).values
	return z

#check the value by comparing description and comcode before adding to file
def find_value(ii,i,j,cc,tcc,bcc,template,match_count,mismatch_count):
	index_1 = ii
	print(index_1)
	index_2 = i
	print(index_2)
	index_3 = j
	print(index_3)
	cell = cc
	print(cell)
	total = tcc
	print(total)
	block = bcc
	print(block)
	mc = match_count
	print(mc)
	mmc = mismatch_count
	print(mmc)
	print(cols0[index_1][index_2], cols1[index_1][index_2], rows[index_1][index_3], '\t', cell)
	print('')
	print(comcode.iloc[total][0])
	print('')
	print(comcode.iloc[total][1])
	print('')
	print(template.loc[block][1])
	print('')
	print(template.loc[block][2])
	print('')
	
	#This section could present a problem if any comcodes are added or removed.
	#Without any way to know ahead of time how many or which ones, this code and 
	#the files it is based on would have to be altered for the code to continue to function.
	
	#successful match based on comcode and description match
	if (str(comcode.iloc[total][0]) in str(template.loc[block][1])) and \
		(str(comcode.iloc[total][1]) in str(template.loc[block][2])):
		print("Match Found")
		mc += 1
		
		#if space in value retrieved, remove space and just return the numbers
		#(\d+\s\d+)
		#for some reason, tabula has begun to add spaces in some of the two digit
		#numbers, and strangely its only a few and not all.
		if ' ' in cell and len(cell) == 3:
			cell = cell[0] + cell[-1]
		else:
			cell = cell
		#save value to template		
		template.iloc[block:,3] = cell
		cc_dict[str(comcode.iloc[total][0])] = cell
	else:
		print("---------- Mismatch -------------")
		mmc += 1
		#save "??" to template
		template.iloc[block:,3] = "-"
	print('')
	total += 1
	block += 1

	return mc, mmc, total, block

#check the date to make sure report is current before running results
if today_date in lswimpe_date:
	update = True
	print("-=-=-=-=-=-=-=-=-Ready to update-=-=-=-=-=-=-=-=-"+"\n")
else:
	update = False
	print("-=-=-=-=-=-=-=-=-Not ready to update-=-=-=-=-=-=-=-=-"+"\n")

#checker
def checker(table, rows, columns1, columns2, names):
    
	all_good = True
	print(table.head(3))

	#iterate across every column
	for i in range(len(table.columns)):
		print("\n", columns1[i], "\n")
		print("\n", table.iloc[0,i], "\n")
		if columns1[i] not in table.iloc[0,i]:
			all_good = False
		print("\n", columns2[i], "\n")
		print("\n", table.iloc[1,i], "\n")
		if columns2[i] not in table.iloc[1,i]:
			all_good = False
	#iterate down every row
	for i in range(len(table)):
		print("\n", rows[i], "\n")
		print("\n", table.iloc[i,0], "\n")
		if rows[i] not in table.iloc[i,0]:
			all_good = False
	  
	if all_good:
		return None
	else:
		return names
	
#check
def check_imported():   
	#main loop responsible for file handling and value extraction
	#loop over all blocks
	for ii in range(len(area)):
		#read in block

		## Because of some odd behavior present in the first table with detecting its boundaries
		## I have elected to manually declare its columns during the read, so that there is no
		## mistake where the lines for columns should be drawn.

		## However, being this explicit with it means that if anything changes (again) these
		## values will probably be obsolete or need to be updated. You can refer to the Docs
		## If you ever want to change them

		if ii == 0:

				#fresh beef
			m = tb.read_pdf(url, pages=page[ii], guess=False, area=area[ii]
			# columns = [152.21,  191.038, 245.448, 300.888, 361.886, 411.587, 458.182,
			# 		   510.989, 549.818, 599.519, 630.582, 686.496, 737.75]
					   ) #cols
			#replace NaN with "-"
			m.fillna(value="-", axis=1, inplace=True)

		else:

				#everything else
			m = tb.read_pdf(url, pages=page[ii], guess=False, area=area[ii]) #cols
			#replace NaN with "-"
			m.fillna(value="-", axis=1, inplace=True)

		## Print m to confirm the data read correctly

		#print("\n"+m+"\n")

		## Call the checker function - checks to see if the columns and rows are lined up
		## If not, it quits and throws an error, informing the user the tables are off.
		## Direct intervention is the quickest solution. Adjusting the table sizes in tabula should solve the issue.
		## The last step is to re-run the code with the adjustments made.

		error_list.append(checker(m, rows_to_check[ii], cols_to_check0[ii], cols_to_check1[ii], names[ii]))
		

	return None

#the primary function of the code
def update_imported():    
	#Declare relevant tracking variables outside main loop
	#total_cell_count
	total_cell_count = 0
	#count matches
	match_count = 0
	#count mismatches
	mismatch_count = 0

	#main loop responsible for file handling and value extraction
	#loop over all blocks
	for ii in range(len(area)):
		#read in block
		
		## Because of some odd behavior present in the first table with detecting its boundaries
		## I have elected to manually declare its columns during the read, so that there is no
		##mistake where the lines for columns should be drawn.
		
		## However, being this explicit with it means that if anything changes (again) these
		## values will probably be obsolete or need to be updated. You can refer to the Docs
		## If you ever want to change them
		
		if ii == 0:
		
				#fresh beef
			m = tb.read_pdf(url, pages=page[ii], guess=False, area=area[ii]
			# columns = [152.21,  191.038, 245.448, 300.888, 361.886, 411.587, 458.182,
			# 		   510.989, 549.818, 599.519, 630.582, 686.496, 737.75]
					   ) #cols
			#replace NaN with "-"
			m.fillna(value="-", axis=1, inplace=True)
			
		else:
			
				#everything else
			m = tb.read_pdf(url, pages=page[ii], guess=False, area=area[ii]) #cols
			#replace NaN with "-"
			m.fillna(value="-", axis=1, inplace=True)
		
		## Print m to confirm the data read correctly
		
		print("\n"+m+"\n")
		
		## Call some kind of checker function - checks to see if the columns and rows are lined up
		## If not, it quits and throws an error, informing the user the tables are off.
		## Direct intervention is the quickest solution. Adjusting the table sizes in tabula should solve the issue.
		## The last step is to re-run the code with the adjustments made.

		#import template document using names
		PTH = os.path.dirname(os.path.abspath('importedmeat_'+names[ii]+'_template.txt'))
		temp_path = r''+PTH+r'\importedmeat_'+\
					names[ii]+r'_template.txt'
		template = pd.read_csv(temp_path, sep='\t')
		#the date value that was obtained earlier can be filled in to the template
		#this should fill in the "Date" column with the current date.
		template.iloc[1:,0] = lswimpe_date_fixed

		#look for values on first and second row match strings
		block_cell_count = 1
		#iterate over all rows in table
		for j in range(len(rows[ii])):
			#iterate over all cols in table
			for i in range(len(cols0[ii])):
			
				#x represents the columns that match keywords from row 0
				x = m.iloc[0,:] == cols0[ii][i]
				x = x.to_frame()
				x = x.loc[x.groupby(x.index.values)[0].transform(all)]
				
				print("\n X: "+str(x)+"\n")
				
				#y represents the columns that match keywords from row 1
				y = m.iloc[1,:] == cols1[ii][i]
				y = y.to_frame()
				y = y.loc[y.groupby(y.index.values)[1].transform(all)]
				
				print("\n Y: "+str(y)+"\n")
				
				#c represents the intersection of matches between x and y
				c = find_intersection(x,y)
				
				print("\n C: "+str(c)+"\n")
				
				#r represents the row that matches keyword from column 0
				r = m.iloc[:,0] == rows[ii][j]
				
				print("\n R: "+str(r)+"\n")
				
				#cc is the cell value at the intersection or row r and column c
				cc = m.loc[r, c].values[0][0]
				
				print("\n CC: "+str(cc)+"\n")
				
				#count variables are updated by the function call find_value
				match_count, mismatch_count, total_cell_count, block_cell_count = \
				find_value(ii,i,j,cc,total_cell_count,block_cell_count,template,
				match_count,mismatch_count)
				
		#Set conditional statements to update filepaths
		if to_local == True:		
			#write template to file
			PTH = os.path.dirname(os.path.abspath('importedmeat_'+str(names[ii])+'_test.hst'))
			template.to_csv(r''+PTH+r'\importedmeat_'
							+str(names[ii])+r'_test.hst',sep="\t", index=False)

	print("Made ", match_count, " matches"+"\n")
	print("Made ", mismatch_count, " mismatches"+"\n")

	#pretty print out using pprint in the future
	#print(cc_dict)
	print(len(cc_dict))
	return None


##################################################
#Prompt user for input on how to proceed

#print tips:
print("Tip:  To make a selection, press either y, yes, n, or no. \n \
The reader is not case-sensitive. \n Press the Enter key to confirm \
your selection. \n You will be prompted again if you make an invalid selection. \n")

while update==False:
	try:
		proceed = input('Imported Meat is not ready to update. Do you want to update anyway? (y/n)'+"\n\n")
		print('\nThe current date of the report is ' + str(lswimpe_date)+"\n")
		if proceed.lower() == 'y' or proceed.lower() == 'yes':
			print('You have chosen to update Comtell. Sending Data to SQL...'+"\n")
			check_imported()
			if all(x==error_list[0] for x in error_list):
				proceed = input("\nNo issues detected in tables. Press any key to continue . . . ")
			else:
				print("\nThe following tables have issues that may inhibit data retrieval:")
				for i in range(len(error_list)):
					if error_list[i] != None:
						print("\n\t*\t"+error_list[i])
				print("\nProceed to check tabula for the current coordinate areas for these tables.")
				print(r"\nDocs can be found at - U:\IMN_temporaryfiles\_Documentation\_Imported_Documentation_WIP.docx")
				print("\nCancelling out ...")
				sys.exit()
			update_imported()
			update = None
			#inform user to post story
			print('\n #################################################################')
			print('\n ####  Reminder: Imported PDF has been saved to the library ! ####')
			print('\n ####         Don\'t forget to Post the Story online !         ####')
			print('\n #################################################################\n\n\n\n\n\n')
		elif proceed.lower() == 'n' or proceed.lower() == 'no':
			print('\nYou have chosen not to update Comtell. No data will be sent to SQL.'+"\n")
			update = None
		else:
			print('\nInvalid Entry  -  Pleae Try Again.'+"\n")
			update=False
	except ValueError:
		print('\nInvalid Entry  -  Pleae Try Again.'+"\n")
		update=False
		
while update==True:
	try:
		proceed = input('Imported Meat is ready to update. Do you want to run the data to Comtell? (y/n): '+"\n\n")
		print('\nThe current date of the report is ' + str(lswimpe_date)+"\n")
		if proceed.lower() == 'y' or proceed.lower() == 'yes':
			print('You have chosen to update Comtell. Sending Data to SQL...'+"\n")
			check_imported()
			if all(x==error_list[0] for x in error_list):
				proceed = input("\nNo issues detected in tables. Press any key to continue . . . ")
			else:
				print("\nThe following tables have issues that may inhibit data retrieval:")
				for i in range(len(error_list)):
					if error_list[i] != None:
						print("\n\t*\t"+error_list[i])
				print("\nProceed to check tabula for the current coordinate areas for these tables.")
				print(r"\nDocs can be found at - U:\IMN_temporaryfiles\_Documentation\_Imported_Documentation_WIP.docx")
				print("\nCancelling out ...")
				sys.exit()
			update_imported()
			update = None
			#inform user to post story
			print('\n #################################################################')
			print('\n ####  Reminder: Imported PDF has been saved to the library ! ####')
			print('\n ####         Don\'t forget to Post the Story online !         ####')
			print('\n #################################################################\n\n\n\n\n\n')
		elif proceed.lower() == 'n' or proceed.lower() == 'no':
			print('You have chosen not to update Comtell. No data will be sent to SQL.'+"\n")
			update = None
		else:
			print('Invalid Entry  -  Pleae Try Again.'+"\n")
			update=True
	except ValueError:
		print('Invalid Entry  -  Pleae Try Again.'+"\n")
		update=True

##################################################
print('The script took {0} seconds to run! '.format(time.time()-start))
#27.17
#23.02
#22.34