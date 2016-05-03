import sys
from sqlite3 import OperationalError

sys.path.insert(2, '/usr/local/lib/python2.7/site-packages')
from flask import Flask, render_template, request, jsonify, send_from_directory, redirect, url_for
import pymysql, json
import itertools
import pprint
import numpy as np
import pandas as pd
import os
import scipy
from scipy import linalg


def dictfetchall(cursor):
    """Returns all rows from a cursor as a list of dicts"""
    desc = cursor.description
    return [dict(itertools.izip([col[0] for col in desc], row))
            for row in cursor.fetchall()]


db = pymysql.connect(host='162.243.195.102', user='root', passwd='411Password', db='db')
cursor = db.cursor()

preprocess = "SELECT db.id.Year, db.id.Department, db.id.Major, Male, Female, Other FROM db.Gender INNER JOIN db.id ON db.id.ID = db.Gender.ID ;"
cursor.execute(preprocess)
get_gender_all_years_json = dictfetchall(cursor)
with open('app/gender.json', 'w') as f:
    json.dump(get_gender_all_years_json, f, ensure_ascii=False)

preprocessEth = "SELECT db.id.Year, db.id.Department, db.id.Major, White, Asian, AfAm, Hisp, NativeAmAl, NativeHaw, Multi, Foreigner, Other FROM db.Ethnicity INNER JOIN db.id ON db.id.ID = db.Ethnicity.ID ;"
cursor.execute(preprocessEth)
get_gender_all_years_json = dictfetchall(cursor)
with open('app/ethnicity.json', 'w') as f:
    json.dump(get_gender_all_years_json, f, ensure_ascii=False)

preprocessRank = "SELECT db.id.Year, db.id.Department, db.id.Major, Freshman, Sophomore, Junior, Senior, Graduate FROM db.Rank INNER JOIN db.id ON db.id.ID = db.Rank.ID ;"
cursor.execute(preprocessRank)
get_gender_all_years_json = dictfetchall(cursor)
with open('app/ranking.json', 'w') as f:
    json.dump(get_gender_all_years_json, f, ensure_ascii=False)

get_departments_names = "SELECT DISTINCT Department from db.id;"
cursor.execute(get_departments_names)
department_names = dictfetchall(cursor)
with open('app/department_names.json', 'w') as f:
    json.dump(department_names, f, ensure_ascii=False)

get_gender_all_years = "SELECT db.id.Year, db.id.Department, db.id.Major, Male, Female, Other FROM db.Gender INNER JOIN db.id ON db.id.ID = db.Gender.ID ;"
cursor.execute(get_gender_all_years)
department_names = dictfetchall(cursor)
with open('app/gender_all_years.json', 'w') as f:
    json.dump(department_names, f, ensure_ascii=False)

get_gender_sum = "SELECT db.id.Year, db.id.Department, db.id.Major, (Male+ Female+Other) AS major_sum FROM db.Gender INNER JOIN db.id ON db.id.ID = db.Gender.ID ;"
cursor.execute(get_gender_sum)
department_names = dictfetchall(cursor)
with open('app/gender_sum.json', 'w') as f:
    json.dump(department_names, f, ensure_ascii=False)

all_department_gender_sum_year = "SELECT a.Department, a.Year, SUM(a.major_sum) as total\
    FROM (SELECT db.id.Year, db.id.Department, db.id.Major, (Male+ Female+Other) AS major_sum FROM db.Gender INNER JOIN db.id ON db.id.ID = db.Gender.ID ) a \
    GROUP BY a.Department, a.Year;"
cursor.execute(all_department_gender_sum_year)
department_names = dictfetchall(cursor)
for key, value in enumerate(department_names):
    value['total'] = int(value['total'])
with open('app/all_department_gender_sum.json', 'w') as f:
    json.dump(department_names, f, ensure_ascii=False)

get_ethinicity_all_years = "SELECT db.id.Year, db.id.Department, db.id.Major, db.Ethnicity.* FROM db.Ethnicity INNER JOIN db.id ON db.id.ID = db.Ethnicity.ID ;"
cursor.execute(get_ethinicity_all_years)
department_names = dictfetchall(cursor)
with open('app/ethinicity_all_years.json', 'w') as f:
    json.dump(department_names, f, ensure_ascii=False)
