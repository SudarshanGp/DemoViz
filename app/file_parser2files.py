import sys

sys.path.insert(2, '/usr/local/lib/python2.7/site-packages')
import timeit #test how long it takes
import xlrd #for reading .xlsx files
import csv #for readin .csv files
import sys  #getting sys arguments
import os #for getting cwd
import pymysql
import itertools
# db_name = 'Demo.db'
CurrentDir= os.getcwd()+"/static/res/"
cursor = ""
# /Users/Aadhya/GitHub
def dictfetchall(cursor):
	"""Returns all rows from a cursor as a list of dicts"""
	desc = cursor.description
	return [dict(itertools.izip([col[0] for col in desc], row))
			for row in cursor.fetchall()]

def buildOutputSQL(file_name, db_name):
   f = open(file_name, "wb")
   f.write("CREATE TABLE "+db_name+'''.Rank (
	ID int not null,
	Freshman int not null,
	Sophomore int not null,
	Junior int not null,
	Senior int not null,
	Graduate int not null,
	primary key(ID),
	FOREIGN KEY(ID) REFERENCES '''+ db_name+'''.id(ID) 
	ON DELETE CASCADE
	ON UPDATE CASCADE
	);\n''')
   f.close

def FilePar2(fileloc, datb, term):
   
   
	Rank={}
	wb=xlrd.open_workbook(fileloc)
	current_sheet=wb.sheet_by_index(0)

	db = pymysql.connect(host='162.243.195.102',user='root', passwd ='411Password', db = 'dummy')
	cursor = db.cursor()
	check="SHOW DATABASES LIKE '"+datb+"';"
	cursor.execute(check) # for ID
	exist = cursor.fetchall()
	if len(exist) > 0:
		check="SELECT * FROM "+datb+".id WHERE "+datb+".id.Year = '"+term+"';"
		cursor.execute(check)
		get_ids = dictfetchall(cursor)
	
	ids={}
	for key, val in enumerate(get_ids):
		ids[val['Major']]=val['ID']

	for i in range(1, current_sheet.nrows):
		if(i>11 and current_sheet.cell(i,4).value!='  ' and current_sheet.cell(i,5).value!='  ' and type(current_sheet.cell(i,8).value) is float):
			# maj='"'+current_sheet.cell(i,5).value
			maj=current_sheet.cell(i,5).value
			maj= maj[0:len(maj)-1]
			# maj+='"'
			if (maj not in ids.keys()):
				continue
			tempc = ids[maj]

			if(tempc in Rank.keys()):
				j=tempc
				if(type(current_sheet.cell(i,8).value) is float):
					Rank[j][0]+=current_sheet.cell(i,8).value
				if(type(current_sheet.cell(i,9).value) is float):
					Rank[j][1]+=current_sheet.cell(i,9).value
				if(type(current_sheet.cell(i,10).value) is float):
					Rank[j][2]+=current_sheet.cell(i,10).value
				if(type(current_sheet.cell(i,11).value) is float):
					Rank[j][3]+=current_sheet.cell(i,11).value	
				if(type(current_sheet.cell(i,17).value) is float):
					Rank[j][4]+=current_sheet.cell(i,17).value			
				
			else:
				
				Rank[tempc]=[0,0,0,0,0]
				
				j=tempc
			
				if(type(current_sheet.cell(i,8).value) is float):
					Rank[j][0]+=current_sheet.cell(i,8).value
				if(type(current_sheet.cell(i,9).value) is float):
					Rank[j][1]+=current_sheet.cell(i,9).value
				if(type(current_sheet.cell(i,10).value) is float):
					Rank[j][2]+=current_sheet.cell(i,10).value
				if(type(current_sheet.cell(i,11).value) is float):
					Rank[j][3]+=current_sheet.cell(i,11).value
				if(type(current_sheet.cell(i,17).value) is float):
					Rank[j][4]+=current_sheet.cell(i,17).value	

	return Rank  

def writeInsert(file_name, db_name, list, insType, first):
	if first == True:
		f = open(file_name, "w")
	else:
		f=open(file_name,"a")

	for i in list:
		f.write("INSERT IGNORE INTO ")
		f.write(db_name)
		f.write(".")
		f.write(insType)
		f.write(" VALUES(")
		f.write("'")
		f.write(str(i[0]))
		f.write("',")
		temp = i[1:]
		f.write(",".join(str(j) for j in temp))
		f.write(");\n")
	f.close()

def main():
	dbName = "db"

	fileloc=CurrentDir+str(sys.argv[1])
	file_name = str(sys.argv[1])[:-4]+".sql"
	term = (str(sys.argv[1])[3:])[:-4]
	
	createNew = ""
	if(len(sys.argv) == 3):
		createNew = str(sys.argv[2])
	
	first = True;

	if(createNew is 'n'):
		buildOutputSQL(file_name, dbName)
		first = False;

	Rank=FilePar2(fileloc,dbName,term)
	Ranklist=[]
	for key in Rank:
		temp=[]
		temp.append(key)
		temp.append(Rank[key][0])
		temp.append(Rank[key][1])
		temp.append(Rank[key][2])
		temp.append(Rank[key][3])
		temp.append(Rank[key][4])
	   
		Ranklist.append(temp)

	writeInsert(file_name, dbName, Ranklist, "Rank", first)       

if __name__ == '__main__':
	#main()
	#runs the main, and prints the time taken to run
	print timeit.timeit(main,number=1)