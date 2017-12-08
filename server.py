##########################################################################################################
#                                                                                                        #
# filename : server.py                                                                                   #
# authors : Rubanraj R(Digital), Aswini K(Digital)                                                       #
# language : Python3 (Flask Web Framework)                                                               #
# description : This file is responsible for spinning up the web server of the application and           #
#               takes care of the routes available in the server                                         #
#                                                                                                        #
##########################################################################################################

from flask import Flask
from flask_restful import Api
from employee import Employees  # imports Employees class from employee file

app = Flask(__name__)
api = Api(app)

api.add_resource(Employees, '/employees') # Route_1

if __name__ == '__main__':
     app.run()  # server running on port 5002