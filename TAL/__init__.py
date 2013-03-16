

class TALAPI(object):
	"""Implement generic microtweeter accesss API"""

	class UknownUser(Exception):
		"""Given user ID does not exist"""
		pass

	def __init__(self):
		pass

	def create_user(self, username):
		"""creates user with given username. Returns user_id"""
		pass

	def post_tweet(self, user_id, tweet):
		pass

	def follow(self, following_user_id, followed_user_id):
		pass

	def unfollow(self, following_user_id, unfollowed_user_id):
		pass
		
	def get_feed(self, user_id, start=0, amount=50):
		pass

	def get_global_feed(self, start=0, amount=50):
		pass
		
