from flask import Flask, request
from flask_cors import CORS
import time

app = Flask(__name__, static_url_path='', static_folder='ab-test-mab-ui/build')
CORS(app)

@app.route("/")
def get_time():
    return {'time': time.time()}

@app.route("/register-participant")
def register_participant():
    request_data = request.get_json()
    cookies = request.cookies

    # get the generated user id stored on the browser and process further