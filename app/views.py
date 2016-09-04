#!/usr/bin/python
# -*- coding: utf-8 -*-
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

app = Flask(__name__)
app.config.from_object(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
db = ""
cursor = ""
render_data = []
render_data1 = []
all_gender_predictions = {}
all_eth_predictions = {}
all_rank_predictions = {}
tree_data_rank = []
tree_data = []
tree_data_eth = []

rerenderRank = 0
rerenderEth = 0
rerenderGender = 0

def f(x, m, b):
    return m * x + b


def dictfetchall(cursor):
    """Returns all rows from a cursor as a list of dicts"""
    desc = cursor.description
    return [dict(itertools.izip([col[0] for col in desc], row))
            for row in cursor.fetchall()]


@app.route('/')
@app.route('/index', methods=['GET', 'POST'])
def index():
    """
    The index function is called when the a user makes a request to the ip address at which
    the website is hosted. It returns the base.html template and is rendered by jinja2
    :return: Return the base.html template when the root / or /index is requested
    """
    # print(render_data)

    return render_template('base.html', data=render_data)


@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if request.method == 'POST':
        file = request.files['file']
        if file:
            filename = file.filename
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    # get_departments_names = "SELECT DISTINCT Department from db.id;"
    # cursor.execute(get_departments_names)
    # get_department_names_json = dictfetchall(cursor)
    with open('department_names.json') as data_file:
        get_department_names_json = json.load(data_file)


    # get_gender_all_years = "SELECT db.id.Year, db.id.Department, db.id.Major, Male, Female, Other FROM db.Gender INNER JOIN db.id ON db.id.ID = db.Gender.ID ;"
    # cursor.execute(get_gender_all_years)
    # get_gender_all_years_json = dictfetchall(cursor)
    with open('gender_all_years.json') as data_file:
        get_gender_all_years_json = json.load(data_file)

    # get_gender_sum = "SELECT db.id.Year, db.id.Department, db.id.Major, (Male+ Female+Other) AS major_sum FROM db.Gender INNER JOIN db.id ON db.id.ID = db.Gender.ID ;"
    # cursor.execute(get_gender_sum)
    # get_gender_sum_json = dictfetchall(cursor)
    with open('gender_sum.json') as data_file:
        get_gender_sum_json = json.load(data_file)

    # all_department_gender_sum_year = "SELECT a.Department, a.Year, SUM(a.major_sum) as total\
    #         FROM (SELECT db.id.Year, db.id.Department, db.id.Major, (Male+ Female+Other) AS major_sum FROM db.Gender INNER JOIN db.id ON db.id.ID = db.Gender.ID ) a \
    #         GROUP BY a.Department, a.Year;"
    # cursor.execute(all_department_gender_sum_year)
    # all_department_gender_sum_year_json = dictfetchall(cursor)
    with open('all_department_gender_sum.json') as data_file:
        all_department_gender_sum_year_json = json.load(data_file)

    # get_ethinicity_all_years = "SELECT db.id.Year, db.id.Department, db.id.Major, db.Ethnicity.* FROM db.Ethnicity INNER JOIN db.id ON db.id.ID = db.Ethnicity.ID ;"
    # cursor.execute(get_ethinicity_all_years)
    # get_ethinicity_all_years_json = dictfetchall(cursor)

    with open('ethinicity_all_years.json') as data_file:
        get_ethinicity_all_years_json = json.load(data_file)

    ethinicity_dict = {}
    for key, value in enumerate(get_ethinicity_all_years_json):
        if value['Year'] in ethinicity_dict.keys():
            # if value['Department'] in ethinicity_dict[value['Year']]:
            temp_list = []
            temp_list.append({'label': 'African American', 'value': value['AfAm']})
            temp_list.append({'label': 'Asian', 'value': value['Asian']})
            temp_list.append({'label': 'Multi Racial', 'value': value['Multi']})

            temp_list.append({'label': 'Foreigner', 'value': value['Foreigner']})
            temp_list.append({'label': 'Hispanic', 'value': value['Hisp']})
            temp_list.append({'label': 'Native American', 'value': value['NativeAmAl']})
            temp_list.append({'label': 'White', 'value': value['White']})
            temp_list.append({'label': 'Native Hawaiian', 'value': value['NativeHaw']})

            temp_list.append({'label': 'Other', 'value': value['Other']})
            if value['Department'] in ethinicity_dict[value['Year']].keys():
                ethinicity_dict[value['Year']][value['Department']][value['Major']] = temp_list
            else:
                ethinicity_dict[value['Year']][value['Department']] = {}
                ethinicity_dict[value['Year']][value['Department']][value['Major']] = temp_list
        else:
            ethinicity_dict[value['Year']] = {}
            ethinicity_dict[value['Year']][value['Department']] = {}
            temp_list = []
            temp_list.append({'label': 'African American', 'value': value['AfAm']})
            temp_list.append({'label': 'Asian', 'value': value['Asian']})
            temp_list.append({'label': 'Multi Racial', 'value': value['Multi']})
            temp_list.append({'label': 'Foreigner', 'value': value['Foreigner']})
            temp_list.append({'label': 'Hispanic', 'value': value['Hisp']})
            temp_list.append({'label': 'Native American', 'value': value['NativeAmAl']})
            temp_list.append({'label': 'White', 'value': value['White']})
            temp_list.append({'label': 'Native Hawaiian', 'value': value['NativeHaw']})
            temp_list.append({'label': 'Other', 'value': value['Other']})
            ethinicity_dict[value['Year']][value['Department']][value['Major']] = temp_list

    gender_dict = {}
    for key, value in enumerate(get_gender_all_years_json):
        if value['Year'] in gender_dict.keys():
            # if value['Department'] in ethinicity_dict[value['Year']]:
            temp_list = []
            temp_list.append({'label': 'Male', 'value': value['Male']})
            temp_list.append({'label': 'Female', 'value': value['Female']})
            temp_list.append({'label': 'Other', 'value': value['Other']})

            if value['Department'] in gender_dict[value['Year']].keys():
                gender_dict[value['Year']][value['Department']][value['Major']] = temp_list
            else:
                gender_dict[value['Year']][value['Department']] = {}
                gender_dict[value['Year']][value['Department']][value['Major']] = temp_list
        else:
            gender_dict[value['Year']] = {}
            gender_dict[value['Year']][value['Department']] = {}
            temp_list = []
            temp_list.append({'label': 'Male', 'value': value['Male']})
            temp_list.append({'label': 'Female', 'value': value['Female']})
            temp_list.append({'label': 'Other', 'value': value['Other']})
            gender_dict[value['Year']][value['Department']][value['Major']] = temp_list

    major_dict = {}  # Enrollment by Major
    for key, value in enumerate(get_gender_sum_json):
        if value['Year'] in major_dict.keys():
            if value['Department'] in major_dict[value['Year']]:
                curr_list = major_dict[value['Year']][value['Department']]
                temp_dict = {}
                temp_dict['label'] = value['Major']
                temp_dict['value'] = value['major_sum']
                curr_list.append(temp_dict)
                major_dict[value['Year']][value['Department']] = curr_list
            else:
                temp_list = []
                temp_dict = {}
                temp_dict['label'] = value['Major']
                temp_dict['value'] = value['major_sum']
                temp_list.append(temp_dict)
                major_dict[value['Year']][value['Department']] = temp_list
        else:
            temp_list = []
            temp_dict = {}
            temp_dict['label'] = value['Major']
            temp_dict['value'] = value['major_sum']
            temp_list.append(temp_dict)
            major_dict[value['Year']] = {value['Department']: temp_list}
            # major_dict[value['Year']] = temp_list

    department_dict = {}  # Enrollment by department
    for key, value in enumerate(all_department_gender_sum_year_json):
        if value['Year'] in department_dict.keys():
            curr_list = department_dict[value['Year']]
            temp = {}
            temp['label'] = value['Department']
            temp['value'] = int(value['total'])
            curr_list.append(temp)
            department_dict[value['Year']] = curr_list
        else:
            temp_list = []
            temp = {}
            temp['label'] = value['Department']
            temp['value'] = int(value['total'])
            temp_list.append(temp)
            department_dict[value['Year']] = temp_list

    return render_template('dashboard.html', pie_department_data=department_dict, pie_major_data=major_dict,
                           ethinicity_data=ethinicity_dict, gender_data=gender_dict)


def regress(data, major, department, gender):
    CS = data[data['Major'].str.contains(major)]
    cs_eng = CS[CS['Department'].str.contains(department)]
    if cs_eng.empty:
        return []
    cs_eng = cs_eng.sort(columns=["Year"])

    X = np.array(cs_eng['Year'].tolist())
    Y = cs_eng[gender].tolist()
    year = np.array(X)
    val = np.array(Y)
    A = np.array([1 + 0 * year, year]).T
    Q, R = np.linalg.qr(A, "complete")
    m, n = A.shape

    if np.shape(Q.T.dot(val)[:n]) == (2,):
        x = linalg.solve_triangular(R[:n], Q.T.dot(val)[:n], lower=False)
        a_c, b_c = x
        pltgrid = np.array(range(2004, 2021))
        new_y = f(pltgrid, b_c, a_c)
        new_x = pltgrid

        return_json = []
        for i in range(len(X)):
            return_json.append({'symbol': 'Real', 'date': X[i], 'Enrollment': Y[i]})
        for i in range(len(new_x)):
            return_json.append({'symbol': 'Predicted', 'date': new_x[i], 'Enrollment': new_y[i]})
        # pprint.pprint(return_json)
        return return_json
    else:
        return []


@app.route('/trends/', methods=['GET', 'POST'])
def trends():
    global rerenderGender
    if rerenderGender == 1:
        preprocess()
        rerenderGender=0
    global all_gender_predictions
    global tree_data
    return render_template('trends.html', data=all_gender_predictions, tree_data=tree_data)


@app.route('/trendsEth/', methods=['GET', 'POST'])
def trendsEth():
    global rerenderEth
    if rerenderEth == 1:
        preprocessEth()
        rerenderEth=0
    global all_eth_predictions
    global tree_data_eth
    return render_template('trendsEth.html', data=all_eth_predictions, tree_data=tree_data_eth)


@app.route('/trendsStand/', methods=['GET', 'POST'])
def trendsStand():
    global rerenderRank
    if rerenderRank==1:
        preprocessRank()
        rerenderRank=0
    global all_rank_predictions
    global tree_data_rank
    return render_template('trendsStand.html', data=all_rank_predictions, tree_data=tree_data_rank)


# @app.route('/upload', methods=['GET', 'POST'])
# def upload():
#     if request.method == 'POST':
#         file = request.files['file']
#         if file:
#             filename = file.filename
#             file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
#             file_split = filename.split('.')
#             sql_file = file_split[0] + ".sql"

#             if "update" in filename.lower():
#                 python_command = "python " + "update_year.py" + " " + filename
#                 os.system(python_command)
#                 file_split = filename.split('.')
#                 sql_file = file_split[0] + ".sql"
#                 executeScriptsFromFile(sql_file)

#             elif "enr" in filename.lower():
#                 python_command = "python " + "standing_parser.py" + " " + filename
#                 os.system(python_command)
#                 file_split = filename.split('.')
#                 sql_file = file_split[0] + ".sql"
#                 executeScriptsFromFile(sql_file)

#             else:
#                 python_command = "python " + "file_parser.py" + " " + filename
#                 os.system(python_command)
#                 file_split = filename.split('.')
#                 sql_file = file_split[0] + ".sql"
#                 executeScriptsFromFile(sql_file)
#             return redirect(url_for('dashboard'))
#         elif request.form['filedel'] != '':
#             file_split = request.form['filedel'].split('.')
#             sql_file = "rm" + file_split[0] + ".sql"
#             if os.path.isfile(sql_file):
#                 executeScriptsFromFile(sql_file)
#             return redirect(url_for('dashboard'))
#         else:
#             return render_template('upload.html', message="Incorrect Input")
#     return render_template('upload.html', message="No file uploaded")


# @app.route('/uploads/<filename>')
# def uploaded_file(filename):
#     return send_from_directory(app.config['UPLOAD_FOLDER'],
#                                filename)


# def executeScriptsFromFile(filename):
#     # Open and read the file as a single buffer
#     global rerenderEth
#     global rerenderGender
#     global rerenderRank
#     fd = open(filename, "a")
#     fd.write("SELECT * FROM db.id WHERE db.id.Year = 'emptylol';")
#     fd.close()

#     fd = open(filename, 'r')
#     sqlFile = fd.read()
#     fd.close()
#     # cursor.execute(sqlFile)
#     db.commit()
#     rerenderGender=1
#     rerenderEth=1
#     rerenderRank=1


def preprocessRank():
    global all_rank_predictions
    global tree_data_rank
    # get_gender_all_years = "SELECT db.id.Year, db.id.Department, db.id.Major, Freshman, Sophomore, Junior, Senior, Graduate FROM db.Rank INNER JOIN db.id ON db.id.ID = db.Rank.ID ;"
    # cursor.execute(get_gender_all_years)
    # get_gender_all_years_json = dictfetchall(cursor)
    with open('ranking.json') as data_file:
        get_gender_all_years_json = json.load(data_file)
    regression_data = []
    for key, value in enumerate(get_gender_all_years_json):
        if value['Year'][:2] in "fa":
            # Fall
            year = int('20' + value['Year'][2:4])
            temp_dict = value
            temp_dict['Year'] = int(year)
            regression_data.append(temp_dict)
    data_gender = pd.DataFrame(regression_data)
    with open('department_names.json') as data_file:
        get_department_names_json = json_loads_byteified(data_file)
    # get_departments_names = "SELECT DISTINCT Department from db.id;"
    # cursor.execute(get_departments_names)
    # get_department_names_json = dictfetchall(cursor)
    for key, value in enumerate(get_department_names_json):
        tree_data_rank.append({'label': value['Department'], 'children': []})
    with open('major.json') as data_file:
        get_department_majors_json = json_loads_byteified(data_file)
    # get_department_majors = "SELECT DISTINCT Department, Major from db.id;"
    # cursor.execute(get_department_majors)
    # get_department_majors_json = dictfetchall(cursor)
    for key, value in enumerate(get_department_majors_json):
        match_index = next(index for (index, d) in enumerate(tree_data_rank) if d["label"] == value['Department'])
        tree_data_rank[match_index]['children'].append({'label': value['Major'],
                                                        'children': [{'label': 'Freshman'}, {'label': 'Sophomore'},
                                                                     {'label': 'Junior'}, {'label': 'Senior'},
                                                                     {'label': 'Graduate'}]})

    for key, value in enumerate(tree_data_rank):
        department = value['label']
        for key1, value1 in enumerate(value['children']):
            major = value1['label']
            temp_data_white = regress(data_gender, major, department, "Freshman")
            temp_data_asian = regress(data_gender, major, department, "Sophomore")
            temp_data_afam = regress(data_gender, major, department, "Junior")
            temp_data_hisp = regress(data_gender, major, department, "Senior")
            temp_data_amal = regress(data_gender, major, department, "Graduate")
            if len(temp_data_white) == 0 or len(temp_data_asian) == 0 or len(temp_data_afam) == 0 or len(
                    temp_data_hisp) == 0 or len(temp_data_amal) == 0:
                continue
            else:
                if department in all_rank_predictions.keys():
                    all_rank_predictions[department][major] = {'Freshman': temp_data_white,
                                                               'Sophomore': temp_data_asian, 'Junior': temp_data_afam,
                                                               'Senior': temp_data_hisp, 'Graduate': temp_data_amal}
                else:
                    all_rank_predictions[department] = {}
                    all_rank_predictions[department][major] = {'Freshman': temp_data_white,
                                                               'Sophomore': temp_data_asian, 'Junior': temp_data_afam,
                                                               'Senior': temp_data_hisp, 'Graduate': temp_data_amal}
    with open('all_rank_predictions.json', 'w') as outfile:
        json.dumps(all_rank_predictions, outfile)


def preprocessEth():
    global all_eth_predictions
    global tree_data_eth
    # get_gender_all_years = "SELECT db.id.Year, db.id.Department, db.id.Major, White, Asian, AfAm, Hisp, NativeAmAl, NativeHaw, Multi, Foreigner, Other FROM db.Ethnicity INNER JOIN db.id ON db.id.ID = db.Ethnicity.ID ;"
    # cursor.execute(get_gender_all_years)
    # get_gender_all_years_json = dictfetchall(cursor)
    with open('ethnicity.json') as data_file:
        get_gender_all_years_json = json.load(data_file)
    regression_data = []
    for key, value in enumerate(get_gender_all_years_json):
        if value['Year'][:2] in "fa":
            # Fall
            year = int('20' + value['Year'][2:4])
            temp_dict = value
            temp_dict['Year'] = int(year)
            regression_data.append(temp_dict)
    data_gender = pd.DataFrame(regression_data)
    with open('department_names.json') as data_file:
        get_department_names_json = json_loads_byteified(data_file)

    # get_departments_names = "SELECT DISTINCT Department from db.id;"
    # cursor.execute(get_departments_names)
    # get_department_names_json = dictfetchall(cursor)
    for key, value in enumerate(get_department_names_json):
        tree_data_eth.append({'label': value['Department'], 'children': []})
    with open('major.json') as data_file:
        get_department_majors_json = json_loads_byteified(data_file)
    # get_department_majors = "SELECT DISTINCT Department, Major from db.id;"
    # cursor.execute(get_department_majors)
    # get_department_majors_json = dictfetchall(cursor)
    for key, value in enumerate(get_department_majors_json):
        match_index = next(index for (index, d) in enumerate(tree_data_eth) if d["label"] == value['Department'])
        tree_data_eth[match_index]['children'].append({'label': value['Major'],
                                                       'children': [{'label': 'White'}, {'label': 'Asian'},
                                                                    {'label': 'African American'},
                                                                    {'label': 'Hispanic'}, {'label': 'Native American'},
                                                                    {'label': 'Foreigner'}]})

    for key, value in enumerate(tree_data_eth):
        department = value['label']
        for key1, value1 in enumerate(value['children']):
            major = value1['label']
            temp_data_white = regress(data_gender, major, department, "White")
            temp_data_asian = regress(data_gender, major, department, "Asian")
            temp_data_afam = regress(data_gender, major, department, "AfAm")
            temp_data_hisp = regress(data_gender, major, department, "Hisp")
            temp_data_amal = regress(data_gender, major, department, "NativeAmAl")
            temp_data_for = regress(data_gender, major, department, "Foreigner")
            if len(temp_data_white) == 0 or len(temp_data_asian) == 0 or len(temp_data_afam) == 0 or len(
                    temp_data_hisp) == 0 or len(temp_data_amal) == 0 or len(temp_data_for) == 0:
                continue
            else:
                if department in all_eth_predictions.keys():
                    all_eth_predictions[department][major] = {'White': temp_data_white, 'Asian': temp_data_asian,
                                                              'African American': temp_data_afam,
                                                              'Hispanic': temp_data_hisp,
                                                              'Native American': temp_data_amal,
                                                              'Foreigner': temp_data_for}
                else:
                    all_eth_predictions[department] = {}
                    all_eth_predictions[department][major] = {'White': temp_data_white, 'Asian': temp_data_asian,
                                                              'African American': temp_data_afam,
                                                              'Hispanic': temp_data_hisp,
                                                              'Native American': temp_data_amal,
                                                              'Foreigner': temp_data_for}
    with open('all_eth_predictions.json', 'w') as outfile:
        json.dumps(all_eth_predictions, outfile)


def preprocess():
    global all_gender_predictions
    global tree_data
    # get_gender_all_years = "SELECT db.id.Year, db.id.Department, db.id.Major, Male, Female, Other FROM db.Gender INNER JOIN db.id ON db.id.ID = db.Gender.ID ;"
    # cursor.execute(get_gender_all_years)
    # get_gender_all_years_json = dictfetchall(cursor)
    with open('gender.json') as data_file:
        get_gender_all_years_json = json.load(data_file)
    regression_data = []
    for key, value in enumerate(get_gender_all_years_json):
        if value['Year'][:2] in "fa":
            # Fall
            year = int('20' + value['Year'][2:4])
            temp_dict = value
            temp_dict['Year'] = int(year)
            regression_data.append(temp_dict)
    data_gender = pd.DataFrame(regression_data)
    with open('department_names.json') as data_file:
        get_department_names_json = json_loads_byteified(data_file)
    # get_departments_names = "SELECT DISTINCT Department from db.id;"
    # cursor.execute(get_departments_names)
    # get_department_names_json = dictfetchall(cursor)
    for key, value in enumerate(get_department_names_json):
        tree_data.append({'label': value['Department'], 'children': []})
    with open('major.json') as data_file:
        get_department_majors_json = json_loads_byteified(data_file)
    # get_department_majors = "SELECT DISTINCT Department, Major from db.id;"
    # cursor.execute(get_department_majors)
    # get_department_majors_json = dictfetchall(cursor)
    for key, value in enumerate(get_department_majors_json):
        match_index = next(index for (index, d) in enumerate(tree_data) if d["label"] == value['Department'])
        tree_data[match_index]['children'].append(
            {'label': value['Major'], 'children': [{'label': 'Male'}, {'label': 'Female'}]})

    for key, value in enumerate(tree_data):
        department = value['label']
        for key1, value1 in enumerate(value['children']):
            major = value1['label']
            temp_data_female = regress(data_gender, major, department, "Female")
            temp_data_male = regress(data_gender, major, department, "Male")
            if len(temp_data_female) == 0 or len(temp_data_male) == 0:
                continue
            else:
                if department in all_gender_predictions.keys():
                    all_gender_predictions[department][major] = {'Female': temp_data_female, 'Male': temp_data_male}
                else:
                    all_gender_predictions[department] = {}
                    all_gender_predictions[department][major] = {'Female': temp_data_female, 'Male': temp_data_male}

    with open('all_gender_predictions.json', 'w') as outfile:
        json.dumps(all_gender_predictions, outfile)

def json_loads_byteified(file_handle):
    return _byteify(
        json.load(file_handle, object_hook=_byteify),
        ignore_dicts=True
    )

def json_load_byteified(json_text):
    return _byteify(
        json.loads(json_text, object_hook=_byteify),
        ignore_dicts=True
    )

def _byteify(data, ignore_dicts = False):
    # if this is a unicode string, return its string representation
    if isinstance(data, unicode):
        return data.encode('utf-8')
    # if this is a list of values, return list of byteified values
    if isinstance(data, list):
        return [ _byteify(item, ignore_dicts=True) for item in data ]
    # if this is a dictionary, return dictionary of byteified keys and values
    # but only if we haven't already byteified it
    if isinstance(data, dict) and not ignore_dicts:
        return {
            _byteify(key, ignore_dicts=True): _byteify(value, ignore_dicts=True)
            for key, value in data.iteritems()
        }
    # if it's anything else, return it in its original form
    return data


if __name__ == '__main__':
    # db = pymysql.connect(host='162.243.195.102', user='root', passwd='411Password', db='db')
    # cursor = db.cursor()
    preprocess()
    print("Done preprocess")
    preprocessEth()
    print("Done preprocessEth")
    preprocessRank()
    print("Done preprocessRank")
    app.run(host='0.0.0.0')
