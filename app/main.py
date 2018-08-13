import logging
import os

from flask import Flask
from flask import jsonify
from flask import redirect
from flask import request

from datadog import initialize
from datadog import ThreadStats

#i wanted to add something for the pull request

DATADOG_API_KEY_ENVIRON = "DATADOG_API_KEY"
DATADOG_APP_KEY_ENVIRON = "DATADOG_APP_KEY"

if not os.environ.get(DATADOG_API_KEY_ENVIRON):
	print("did not find datadog API key")
if not os.environ.get(DATADOG_APP_KEY_ENVIRON):
	print("did not find datadog App key")

datadog_options = {
	"api_key": os.environ.get(DATADOG_API_KEY_ENVIRON),
	"app_key": os.environ.get(DATADOG_APP_KEY_ENVIRON)
}
initialize(**datadog_options)
stats = ThreadStats()
stats.start()

app = Flask(__name__)

ERROR_ALREADY_EXISTS = "short_code_already_in_use"
ERROR_SHORT_CODE_DOES_NOT_EXIST = "short_code_does_not_exist"
ERROR_SHORT_CODE_MUST_BE_PROVIDED = "short_code_must_be_provided"

# Our "database". Note that accessing this dictionary requires no
# synchronization because flask doesn't do any multithreading / concurrency.
# TODO: We should probably wrap this up in some kind of singleton / class,
# but this works for demo purposes.
shortened_urls = dict()
def reset_shortened_urls():
	global shortened_urls
	shortened_urls = dict()

# Setup a basic logger.
logging.basicConfig()
logger = logging.getLogger()
# Log at debug level by default.
logger.setLevel(logging.DEBUG)

@app.route("/", methods=["GET", "POST"])
def create_short_url():
	if request.method == "POST":
		return post_short_url()
	if request.method == "GET":
		return get_short_url()
	raise Exception("unsupported method type")

@stats.timed("post-url-timer")
def post_short_url():
	req = request.get_json()
	url = req["url"]
	short_code = req["short_code"]
	if short_code in shortened_urls:
		logger.debug(
			"failed to create shortened URL, %s already exists",
			short_code,
		)
		stats.increment("post-short-code-already-exists")
		return error(ERROR_ALREADY_EXISTS), 400
	
	logger.debug(
		"creating shortened URL, %s -> %s", url, short_code)
	shortened_urls[short_code] = url
	stats.increment("post-short-code-success")
	return jsonify({}), 200

@stats.timed("get-url-timer")
def get_short_url():
	short_code = request.args.get("short_code")
	if not short_code:
		stats.increment("redirect-error-short-code-must-be-provided")
		return error(ERROR_SHORT_CODE_MUST_BE_PROVIDED)
	url = shortened_urls.get(short_code)
	if not url:
		stats.increment("redirect-error-short-code-not-exist")
		return error(ERROR_SHORT_CODE_DOES_NOT_EXIST)
	stats.increment("redirect-success")
	return redirect(url, code=302)

def error(code):
	return jsonify({"error_code": code})

if __name__ == "__main__":
	app.run(debug=True, use_reloader=True)

