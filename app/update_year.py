import sys

sys.path.insert(2, '/usr/local/lib/python2.7/site-packages')
import timeit #test how long it takes
import xlrd #for reading .xlsx files
import csv #for readin .csv files
import sys  #getting sys arguments
import os #for getting cwd
import pymysql

CurrentDir= os.getcwd()+"/static/res/"

def FilePar(fileloc, datb):

	Gender={}
	Ethnicity={}
	Residency = {}
	Department={}
	Departmentlist=[]
	wb=xlrd.open_workbook(fileloc)
	current_sheet=wb.sheet_by_index(0)

	counter=0
	dep = 0
	db = pymysql.connect(host='162.243.195.102',user='root', passwd ='411Password', db = 'db')
	cursor = db.cursor()
	check="SHOW DATABASES LIKE '"+datb+"';"
	cursor.execute(check) # for ID
	exist = cursor.fetchall()
	if len(exist) > 0:
		term = str(sys.argv[1])[6:]
		check="SELECT min(ID) FROM "+datb+".id WHERE "+datb+".id.Year = '"+term[:-4]+"';"
		cursor.execute(check) # for ID
		counter = cursor.fetchall()
		if counter[0][0] is None:
			return Department,Gender,Ethnicity,Residency
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

def writeUpdate(file_name, db_name, list, insType, defList, first):
	if first == True:
		f = open(file_name, "w")
	else:
		f=open(file_name,"a")

	for i in list:
		f.write("UPDATE ")
		f.write(db_name)
		f.write(".")
		f.write(insType)
		f.write(" SET ")
		f.write(defList[0])
		f.write("= '"+str(i[0])+"'")
		for j in range(1,len(i)):
			f.write(", ")
			f.write(defList[j])
			f.write("= ")
			f.write(str(i[j]))
		f.write(" WHERE ")
		f.write(db_name)
		f.write(".")
		f.write(insType)
		f.write(".ID = ")
		f.write("'")
		f.write(str(i[0]))
		f.write("'")
		f.write(";\n")
	f.close()

def main():
	dbName = "db"

	idTable = [dbName+".id.ID", dbName+".id.Year", dbName+".id.Department", dbName+".id.Major"]
	ethTable = [dbName+".Ethnicity.ID", dbName+".Ethnicity.White", dbName+".Ethnicity.Asian", dbName+".Ethnicity.AfAm", dbName+".Ethnicity.Hisp", dbName+".Ethnicity.NativeAmAl", dbName+".Ethnicity.NativeHaw", dbName+".Ethnicity.Multi", dbName+".Ethnicity.Foreigner", dbName+".Ethnicity.Other"]
	genTable = [dbName+".Gender.ID", dbName+".Gender.Male", dbName+".Gender.Female", dbName+".Gender.Other"]
	resTable = [dbName+".Residency.ID", dbName+".Residency.IL", dbName+".Residency.NonIL"]

	fileloc=CurrentDir+str(sys.argv[1])
	file_name = str(sys.argv[1])[:-4]+".sql"

	first = True;

	Department, Gender, Ethnicity, Residency = FilePar(fileloc, dbName)
	ids = []
	gen = []
	eth = []
	res = []

	for key in Department:
		for val in Department[key]:
			temp=[]
			temp.append(Department[key][val])
			term = str(sys.argv[1])[6:]
			temp.append('"'+term[:-4]+'"')
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

	writeUpdate(file_name, dbName, ids, "id", idTable, first)
	first = False;
	writeUpdate(file_name, dbName, gen, "Gender", genTable, first)

	writeUpdate(file_name, dbName, eth, "Ethnicity", ethTable, first)

	writeUpdate(file_name, dbName, res, "Residency", resTable, first)

if __name__ == '__main__':
	#main()
	#runs the main, and prints the time taken to run
	print timeit.timeit(main,number=1)