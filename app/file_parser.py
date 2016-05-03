import sys

sys.path.insert(2, '/usr/local/lib/python2.7/site-packages')
import timeit #test how long it takes
import xlrd #for reading .xlsx files
import csv #for readin .csv files
import sys  #getting sys arguments
import os #for getting cwd
import pymysql

CurrentDir= os.getcwd()+"/static/res/"

def buildOutputSQL(file_name, db_name):
   f = open(file_name, "wb")
   f.write("CREATE DATABASE "+db_name+";\n")
   f.write("DROP TABLE IF EXISTS "+db_name+".id;\n")
   f.write("CREATE TABLE "+db_name+'''.id (
	ID int not null,
	Year VARCHAR(8) not null,
	Department VARCHAR(128) not null,
	Major VARCHAR(128) not null,
	primary key (ID)
	);\n''')

   f.write("DROP TABLE IF EXISTS "+db_name+".Ethnicity;\n")
   f.write("CREATE TABLE "+db_name+'''.Ethnicity (
	ID int not null,
	White int not null,
	Asian int not null,
	AfAm int not null,
	Hisp int not null,
	NativeAmAl int not null,
	NativeHaw int not null,
	Multi int not null,
	Foreigner int not null,
	Other int not null,
	primary key (ID),
	FOREIGN KEY(ID) REFERENCES '''+ db_name+'''.id(ID) 
	ON DELETE CASCADE
	ON UPDATE CASCADE
	);\n''')
   f.write("DROP TABLE IF EXISTS "+db_name+".Gender;\n")
   f.write("CREATE TABLE "+db_name+'''.Gender (
	ID int not null,
	Male int not null,
	Female int not null,
	Other int not null,
	primary key (ID),
	FOREIGN KEY(ID) REFERENCES '''+ db_name+'''.id(ID) 
	ON DELETE CASCADE
	ON UPDATE CASCADE
	);\n''')
   f.write("DROP TABLE IF EXISTS "+db_name+".Residency;\n")
   f.write("CREATE TABLE "+db_name+'''.Residency (
	ID int not null,
	IL int not null,
	NonIL int not null,
	primary key (ID),
	FOREIGN KEY(ID) REFERENCES '''+ db_name+'''.id(ID) 
	ON DELETE CASCADE
	ON UPDATE CASCADE
	);\n''')
   f.close

def FilePar(fileloc, datb, term):
   
	Gender={}
	Ethnicity={}
	Residency = {}
	Department={}
	Departmentlist=[]
	wb=xlrd.open_workbook(fileloc)
	current_sheet=wb.sheet_by_index(0)

	dep = 0
	counter = 0
	db = pymysql.connect(host='162.243.195.102',user='root', passwd ='411Password', db = 'dummy')
	cursor = db.cursor()
	check="SHOW DATABASES LIKE '"+datb+"';"
	cursor.execute(check) # for ID
	exist = cursor.fetchall()
	if len(exist) > 0:
		check="SELECT COUNT(*) FROM "+datb+".id WHERE "+datb+".id.Year = '"+term+"';"
		cursor.execute(check) # for ID
		counter = cursor.fetchall()
		if counter == 0:
			return Department,Gender,Ethnicity,Residency

		check="SELECT max(ID) FROM "+datb+".id;"
		cursor.execute(check) # for ID
		counter = cursor.fetchall()
		counter = int(counter[0][0])
	
	for i in range(1, current_sheet.nrows):
		if(i>11):
			#print 'a'+current_sheet.cell(i,2).value+'a'
			#it was a double space for some reason....
			
			if(current_sheet.cell(i,2).value=='  ' and current_sheet.cell(i,3).value=='  ' and 
				current_sheet.cell(i,4).value=='  ' and current_sheet.cell(i,5).value!='  ' and 
				current_sheet.cell(i,9).value=='  ' and current_sheet.cell(i,10).value=='  '):
				thisdep = '"'+current_sheet.cell(i,5).value
				thisdep=thisdep[0:len(thisdep)-1]
				thisdep+='"'
				Departmentlist.append(thisdep)
				dep += 1
				Department[Departmentlist[dep-1]]={}
				continue

			elif(current_sheet.cell(i,4).value!='  ' and current_sheet.cell(i,5).value!='  ' and 
				type(current_sheet.cell(i,9).value) is float):
				maj='"'+current_sheet.cell(i,5).value
				maj= maj[0:len(maj)-1]
				maj+='"'
				if (maj not in Department[Departmentlist[dep-1]].keys()):
					Department[Departmentlist[dep-1]][maj]=counter
					counter += 1
				tempc = Department[Departmentlist[dep-1]][maj]
				if(tempc in Gender.keys()):
					j=tempc
					if(type(current_sheet.cell(i,9).value) is float):
						Gender[j][0]+=current_sheet.cell(i,9).value
					if(type(current_sheet.cell(i,10).value) is float):
						Gender[j][1]+=current_sheet.cell(i,10).value
					if(type(current_sheet.cell(i,9).value) is float):
						Gender[j][2]+=current_sheet.cell(i,11).value

					if(type(current_sheet.cell(i,12).value) is float):
						Ethnicity[j][0]+=current_sheet.cell(i,12).value
					if(type(current_sheet.cell(i,13).value) is float):
						Ethnicity[j][1]+=current_sheet.cell(i,13).value
					if(type(current_sheet.cell(i,14).value) is float):
						Ethnicity[j][2]+=current_sheet.cell(i,14).value
					if(type(current_sheet.cell(i,15).value) is float):
						Ethnicity[j][3]+=current_sheet.cell(i,15).value
					if(type(current_sheet.cell(i,16).value) is float):
						Ethnicity[j][4]+=current_sheet.cell(i,16).value
					if(type(current_sheet.cell(i,17).value) is float):
						Ethnicity[j][5]+=current_sheet.cell(i,17).value
					if(type(current_sheet.cell(i,18).value) is float):
						Ethnicity[j][6]+=current_sheet.cell(i,18).value
					if(type(current_sheet.cell(i,19).value) is float):
						Ethnicity[j][7]+=current_sheet.cell(i,19).value
					if(type(current_sheet.cell(i,20).value) is float):
						Ethnicity[j][8]+=current_sheet.cell(i,20).value

					if(type(current_sheet.cell(i,23).value) is float):
						Residency[j][0]+=current_sheet.cell(i,23).value
					if(type(current_sheet.cell(i,24).value) is float):
						Residency[j][1]+=current_sheet.cell(i,24).value
				else:
					Gender[tempc]=[0,0,0]
					Ethnicity[tempc]=[0,0,0,0,0,0,0,0,0]
					Residency[tempc]=[0,0]
					j=tempc
					if(type(current_sheet.cell(i,9).value) is float):
						Gender[j][0]+=current_sheet.cell(i,9).value
					if(type(current_sheet.cell(i,10).value) is float):
						Gender[j][1]+=current_sheet.cell(i,10).value
					if(type(current_sheet.cell(i,9).value) is float):
						Gender[j][2]+=current_sheet.cell(i,11).value

					if(type(current_sheet.cell(i,12).value) is float):
						Ethnicity[j][0]+=current_sheet.cell(i,12).value
					if(type(current_sheet.cell(i,13).value) is float):
						Ethnicity[j][1]+=current_sheet.cell(i,13).value
					if(type(current_sheet.cell(i,14).value) is float):
						Ethnicity[j][2]+=current_sheet.cell(i,14).value
					if(type(current_sheet.cell(i,15).value) is float):
						Ethnicity[j][3]+=current_sheet.cell(i,15).value
					if(type(current_sheet.cell(i,16).value) is float):
						Ethnicity[j][4]+=current_sheet.cell(i,16).value
					if(type(current_sheet.cell(i,17).value) is float):
						Ethnicity[j][5]+=current_sheet.cell(i,17).value
					if(type(current_sheet.cell(i,18).value) is float):
						Ethnicity[j][6]+=current_sheet.cell(i,18).value
					if(type(current_sheet.cell(i,19).value) is float):
						Ethnicity[j][7]+=current_sheet.cell(i,19).value
					if(type(current_sheet.cell(i,20).value) is float):
						Ethnicity[j][8]+=current_sheet.cell(i,20).value

					if(type(current_sheet.cell(i,23).value) is float):
						Residency[j][0]+=current_sheet.cell(i,23).value
					if(type(current_sheet.cell(i,24).value) is float):
						Residency[j][1]+=current_sheet.cell(i,24).value

	return Department,Gender,Ethnicity,Residency

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

def writeDel(file_name, db_name, insType):
	yearVal = file_name[2:]
	yearVal = yearVal[:-4]

	f = open(file_name, "w")
	f.write("DELETE FROM ")
	f.write(db_name)
	f.write(".")
	f.write(insType)
	f.write(" WHERE Year = '")
	f.write(yearVal)
	f.write("';\n")
	f.close()

def main():
	dbName = "db"

	fileloc=CurrentDir+str(sys.argv[1])
	file_name = str(sys.argv[1])[:-4]+".sql"
	rm_file = "rm"+file_name
	createNew = ""
	term = str(sys.argv[1])[:-4]
	if(len(sys.argv) == 3):
		createNew = str(sys.argv[2])
	
	first = True;

	if(createNew is 'n'):
		buildOutputSQL(file_name, dbName)
		first = False;

	Department, Gender, Ethnicity, Residency = FilePar(fileloc, dbName, term)
	ids = []
	gen = []
	eth = []
	res = []

	for key in Department:
		for val in Department[key]:
			temp=[]
			temp.append(str(Department[key][val]))
			temp.append('"'+str(sys.argv[1])[:-4]+'"')
			temp.append(key)
			temp.append(val)
			ids.append(temp)

	for key in Gender:
		temp=[]
		temp.append(key)
		temp.append(Gender[key][0])
		temp.append(Gender[key][1])
		temp.append(Gender[key][2])
		gen.append(temp)
   
	for key in Ethnicity:
		temp=[]
		temp.append(key)
		temp.append(Ethnicity[key][0])
		temp.append(Ethnicity[key][1])
		temp.append(Ethnicity[key][2])
		temp.append(Ethnicity[key][3])
		temp.append(Ethnicity[key][4])
		temp.append(Ethnicity[key][5])
		temp.append(Ethnicity[key][6])
		temp.append(Ethnicity[key][7])
		temp.append(Ethnicity[key][8])
		eth.append(temp)
	
	for key in Residency:
		temp=[]
		temp.append(key)
		temp.append(Residency[key][0])
		temp.append(Residency[key][1])
		res.append(temp)

	writeInsert(file_name, dbName, ids, "id", first)
	writeDel(rm_file, dbName, "id")
	first = False;
	writeInsert(file_name, dbName, gen, "Gender", first)
	writeInsert(file_name, dbName, eth, "Ethnicity", first)
	writeInsert(file_name, dbName, res, "Residency", first)


if __name__ == '__main__':
	#main()
	#runs the main, and prints the time taken to run
	print timeit.timeit(main,number=1)