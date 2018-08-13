import logging

from flask import Flask
from flask import jsonify
from flask import redirect
from flask import request
from action_utils import *

app = Flask(__name__)

ERROR_ALREADY_EXISTS = "short_code_already_in_use"
ERROR_SHORT_CODE_DOES_NOT_EXIST = "short_code_does_not_exist"

# Our "database". Note that accessing this dictionary requires no
# synchronization because flask doesn't do any multithreading / concurrency.
# TODO: We should probably wrap this up in some kind of singleton / class,
# but this works for demo purposes.
shortened_urls = dict()
def reset_shortened_urls():
	global shortened_urls
	shortened_urls = dict()



@app.route("/", methods=["GET"])
def create_short_url():
	if request.method == "GET":
		return get_short_url()
	raise Exception("unsupported method type")

#this method used to ADD shortende urls
@app.route("/add", methods=["POST"])
def add_short_url():
	req = request.get_json()
	url = req["url"]
	short_code = req["short_code"]
	return action_add_url(url,short_code,shortened_urls)

#this method used to MODIFY shortende urls
# @app.route("/modify", methods=["POST"])
# def add_short_url():
# 	req = request.get_json()
# 	url = req["url"]
# 	short_code = req["short_code"]
# 	return action_modify_url(url,short_code,shortened_urls)

def get_short_url():
	short_code = request.args["short_code"]
	url = shortened_urls.get(short_code)
	if not url:
		return error(ERROR_SHORT_CODE_DOES_NOT_EXIST)
	return redirect(url, code=302)

def error(code):
	return jsonify({"error_code": code})

if __name__ == "__main__":
	app.run(debug=True, use_reloader=True)

