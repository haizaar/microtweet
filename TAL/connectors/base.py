

class ConnectorBase(object):
	"""TAL Connector interface class"""

	@classmethod
	def initialize(cls, conf):
		"""module-wide initializion code goes here"""
		raise NotImplementedError

	def create_user(self, username):
		"""Creates user with given username. Returns user_id"""
		raise NotImplementedError

	def post_tweet(self, user_id, tweet):
		"""Creates tweet for given user. Returns new tweet_id"""
		raise NotImplementedError

	def follow(self, user_id, followed_user_id):
		raise NotImplementedError

	def unfollow(self, user_id, unfollowed_user_id):
		raise NotImplementedError

	def get_feed(self, user_id=None, tweet_id=None, start=0, amount=50):
		raise NotImplementedError
