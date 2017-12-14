##########################################################################################################
#                                                                                                        #
# filename : server.py                                                                                   #
# authors : Rubanraj R(Digital), Aswini K(Digital)                                                       #
# language : Python3 (Flask Web Framework)                                                               #
# description : This file is responsible for spinning up the web server of the application and           #
#               takes care of the routes available in the server                                         #
#                                                                                                        #
##########################################################################################################

import os
from flask import Flask
from flask_restful import Api
# from employee import Employees  # imports Employees class from employee file
import pandas as pd
from flask_restful import Resource
from flask import request
from flask import make_response
import json

app = Flask(__name__)
api = Api(app)

@app.route('/')
def index():
    return '<h1>Deployed to Heroku</h1>'

@app.route('/employees', methods=['GET', 'POST'])
def employees_search():
    if request.method == 'POST':
        print('inside employees - >')
        req = request.get_json(silent=True, force=True)
        print('Request : ')
        print(req)
        print(json.dumps(req, indent=4))
        # reading the par report excel file
        try:
            df = pd.read_excel('./data/PAR WMG.xlsx')
            print('excel file has been read successfully!')
        except Exception as e:
            print('error in reading excel - > ', e)

        # passing parameters for filtering employees from par report
        skill_to_search = 'java'.upper()
        grade_to_search = 'b2'.upper()
        location_to_search = 'chennai'.upper()

        # converting the values to uppercase for particular columns in excel dataframe
        skill = df['PROJECT_ACQUIRED_SKILL'].str.upper()
        grade = df['GRADE'].str.upper()
        location = df['LOCATION'].str.upper()

        # performing dataframe operations to filter the employees
        try:
            filtered_employees = df[skill.str.contains(skill_to_search)
                                        & grade.str.contains(grade_to_search)
                                        & location.str.contains(location_to_search)]
            best_filtered_employees = filtered_employees[['EMPNO','NAME', 'EMP_EMAIL',
                                                          'GRADE', 'TOTAL_EXP', 'LOCATION',
                                                          'ONSITE_OFFSHORE', 'STATUS']].sort_values(['TOTAL_EXP'],
                                                        axis = 0, ascending = True, na_position = 'last').head(n=5)
        except Exception as e:
            print('Error in filtering - > ', e)

        # converting the dataframe to json
        try:
            data = filtered_employees.to_json(orient = 'records')
            data_obj = json.loads(data)
            print('Result JSON has been sent :-)')
            # return data_obj[0]
        except Exception as e:
            print('Error in converting dataframe to json - > ', e)

        res = {
            'speech' : 'Hello, Its response from webhook',
            'displayText' : 'Hello, Its response from webhook',
            'source' : 'Indent Creation'
        }

        response = json.dumps(res, indent = 4)
        r = make_response(res)
        r.headers['content-type'] = 'application/json'
        print('r - > ',r)
        return r



# try:
#     api.add_resource(Employees, '/employees', methods=['POST']) # Route_1
# except Exception as e:
#     print('Error in implementing route - > ', e)

if __name__ == '__main__':
    print('Inside main')
    app.run(debug=False, port=os.environ.get("PORT", 5002), host='0.0.0.0')  # server running on port 5002
