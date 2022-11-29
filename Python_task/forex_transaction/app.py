from flask import Flask
from flask import jsonify, make_response

import os
from transaction import Transaction
basedir = os.path.abspath(os.path.dirname(__file__))

#print(basedir)
app = Flask(__name__)


@app.route("/")
def home():
    ret_val = f"""Welcome to Forex Transaction!
                Please run the URL with valid folder name"""
    print(ret_val)
    return ret_val


@app.route("/<folder>")
def process_start(folder):
    print(f"Executing files in {folder} directory")
    obj = Transaction()
    obj.process_file(folder)
    resp = obj.display()
    return make_response(jsonify(resp), 200)


if __name__ == '__main__':
    # run() method of Flask class runs the application
    # on the local development server.
    app.run()

