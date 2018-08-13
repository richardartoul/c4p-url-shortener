import logging
from flask import Flask
from flask import jsonify
from flask import redirect
from flask import request

# Setup a basic logger.
logging.basicConfig()
logger = logging.getLogger()
# Log at debug level by default.
logger.setLevel(logging.DEBUG)

def action_add_url(url,short_code,shortened_urls):
	if short_code in shortened_urls:
		logger.debug(
			"failed to create shortened URL, %s already exists",
			short_code,
		)
		return error(ERROR_ALREADY_EXISTS), 400
	
	logger.debug(
		"creating shortened URL, %s -> %s", url, short_code)
	shortened_urls[short_code] = url
	return jsonify({}), 200