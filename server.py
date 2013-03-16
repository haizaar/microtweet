from functools import wraps

from flask import Flask, request, abort, jsonify

# Register app
app = Flask(__name__)

# FIXME: user JSONBadRequest instead of plain abort
# FIXME: respond with 201/Created and new dLocation when creating objects
# FIXME: Bind index dispetcher on "/"

# Decorators
################################################################################
def enforce_json(fn):
	"""Verify that JSON is specified as content type"""
	@wraps(fn)
	def wrapped(*args, **kwargs):
		required_ct = "application/json"
		request_ct = request.headers["Content-Type"]
		if request_ct != required_ct:
			abort(400, "Unsupported content type: %s. Use: %s" % (request_ct, required_ct)
		if request.method in ["POST", "DELETE"] and request.json is None:
			abort(400, "Empty json data")
		return fn(*args, **kwargs)
	return wrapped

# Classes
################################################################################
class MicroTweet(object):
	"""High level wrapper around TAL"""

	tal = None # FIXME: get TAL here
	def __init__(self, tal):
		self.tal = tal

	def create_user(self, username):
		return 1
	
	def create_tweet(self, text):
		pass

	def get_tweets(self, user_id=None, tweet_id=None):
		pass

	def follow(self, following_user_id, followed_user_id):
		pass

	def unfollow(self, following_user_id, unfollowed_user_id):
		pass


# helpers
################################################################################
def require(d, *keys):
	"""Verify that the given dictionary has required keys"""
	for k in keys:
		if not d.get(k, None):
			abort(400, "The data is missing %s key" % k)

# Routing
################################################################################
@app.route("/user", methods = ["POST"])
@enforce_json
def api_user():
	require(request.json, "username")
	username = request.json["username"]
	app.logger.debug("username is: %s", userdata["username"])
	user_id = app.mt.create_user(username)

	return jsonify( **dict(user_idr=user_id )


@app.route("/tweet", methods = ["GET", "POST"])
@enforce_json
def api_tweets():
	if request.method == "GET":
		user_id = request.args.get("user_id", None)
		if user_id is not None:
			try:
				user_id = int(user_id)
			except ValueError:
				abort(400, "Non-integer user_id passed")
		tweets = app.mt.get_tweets(user_id=user_id)
		return jsonify( **dict(tweets=tweets) )

	elif request.method == "POST":
		require(request.json, "text")
		text = request.json["text"]
		tweet_id = app.mt.create_tweet(text)
		return jsonify( **dict(tweet_id=tweet_id) )
		
	abort(400, "BUG! unsupported HTTP method")

@app.route("/tweet/<int:tweet_id>", methods = ["GET"])
def api_tweet(tweet_id):
	try:
		tweet = app.mt.get_tweets(tweet_id)
	except app.mt.NotFound:
		abort(404)
	return jsonify( **tweet )

@app.route("/friendship", methods = ["POST", "DELETE"])
@enforce_json
def api_friendship():
	# FIXME: Handle errors: not found users, etc...
	require(request.json, "user_id", "followed_user_id")
	if request.method == "POST":
		app.mt.follow(request.json["user_id"], request.json["followed_user_id"])
	
	elif request.method == "DELETE":
		app.mt.unfollow(request.json["user_id"], request.json["followed_user_id"])


# Setup
################################################################################
def setup():
	# Application setup goes here
	tal = None # FIXME
	mt = MicroTweet(tal)
	app.mt = mt


# Main
################################################################################

if __name__ == "__main__":
	app.debug = True
	setup()
	app.run(host="0.0.0.0", port=8890)
else:
	setup()
