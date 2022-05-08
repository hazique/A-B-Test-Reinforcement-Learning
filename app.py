from cgi import test
from flask import Flask, request
from flask_cors import CORS
import time
import random

from init_db import init
from util.db_manager import *

app = Flask(__name__, static_url_path='', static_folder='ab-test-mab-ui/build')
CORS(app)

# Get db connection handle
init()

@app.route("/")
def get_time():
    return {'time': time.time()}

@app.route("/get-sub-id")
def get_sub_id():
    # request_data = request.get_json()
    # cookies = request.cookies

    # create a new user sid
    sub_id = random.randrange(1, 10**10)
    while db_has_sub_id(sub_id):
        sub_id = random.randrange(1, 10**10)

    return str(sub_id)

@app.route("/register-user", methods=['POST'])
def register_user():
    json = request.get_json()

    sub_id = int(json['sub_id'])
    fname = json['fname']
    lname = json['lname']
    
    # Allocate the variant and test name as decided by MAB
    test_name = json['test_name']
    # For testing only
    variant = 1

    test_done = int(json['test_done'])

    data = (sub_id, fname, lname, test_name, variant, test_done)
    
    try:
        add_subject_to_table(data)
        return "True"
    except Exception as e:
        print(e)
        return "False"

@app.route("/update-result", methods=['POST'])
def update_result():
    json = request.get_json()

    sub_id = int(json['sub_id'])

    result = int(json['result'])
    test_done = 1

    data = (result, test_done, sub_id)
    
    try:
        add_subject_to_table(data)
        return "True"
    except Exception as e:
        print(e)
        return "False"