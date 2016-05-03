__author__ = 'Nathan'
#!/usr/bin/env python
import pymysql
import itertools
import numpy as np
import matplotlib.pyplot as plt
import scipy.linalg
from matplotlib.pyplot import *
from numpy.random import normal
#from scipy.optimize import curve_fit


def f(x, m, b):
    return m*x+b

def dictfetchall(cursor):
    """Returns all rows from a cursor as a list of dicts"""
    desc = cursor.description
    return [dict(itertools.izip([col[0] for col in desc], row))
            for row in cursor.fetchall()]

def main():
    get_gender_all_years = "SELECT db.id.Year, db.id.Department, db.id.Major, Male, Female, Other FROM db.Gender INNER JOIN db.id ON db.id.ID = db.Gender.ID ;"
    cursor.execute(get_gender_all_years)
    get_gender_all_years_json = dictfetchall(cursor)
    
    major={}
    females=[]
    years=[]
    termdict={}
    for i in get_gender_all_years_json:
        term = 0
        if "fa" in i['Year']:
            term = int(i['Year'][2:]+"00")
        else:
            term = int(i['Year'][2:]+"00")+50
        if term in termdict.keys():
            termdict[term][i['Major']]=int(i['Female'])
            
        else:
            termdict[term]={}
            termdict[term][i['Major']]=int(i['Female'])
        
        
    templist=[]
    
    #for i in termdict.keys():
    #    for j in termdict[i]:
    #        if j == "Computer Science":
    #            print (str(i)+"\t"+str(j)+"\t"+str(termdict[i][j]))
    
    for i in termdict.keys():
        for j in termdict[i]:
            major[j]=[]
    for i in termdict.keys():
        for j in termdict[i]:
            major[j].append([int(i),int(termdict[i][j])])
    
    newdict={}
    
    majInf=[]
    for i in major.keys():

        majInf=np.array(major[i])
        year = majInf[:,0] #x
        val = majInf[:,1] #y
        A = np.array([1+0*year, year]).T
        Q,R = np.linalg.qr(A,"complete")
        m,n=A.shape
        print i+"\t"+str(np.shape(Q.T.dot(val)[:n]))
            # sleep(2)
        if np.shape(Q.T.dot(val)[:n]) == (2,):
            x = scipy.linalg.solve_triangular(R[:n], Q.T.dot(val)[:n],lower = False)
            a_c,b_c = x
            # plt.plot(year,val,'o')
            pltgrid = np.linspace(400,2000,50)
            new_y=f(pltgrid, b_c, a_c)
            new_x=pltgrid
            
            newdict[i]=[]
            newdict[i].append(new_x)
            newdict[i].append(new_y)
        
        # plt.plot(pltgrid, f(pltgrid, b_c, a_c),'b-', label='fit')
        # plt.show()  
    print newdict
        
   


if __name__ == '__main__':
    db = pymysql.connect(host='162.243.195.102',user='root', passwd ='411Password', db = 'db')
    cursor = db.cursor()
    #runs the main, and prints the time taken to run
    main()