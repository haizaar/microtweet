from functools import wraps

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import IntegrityError

from .. import exceptions
from ..base import ConnectorBase
from . import model as m

def to_dicts(fn):
	"""decorator that converts result model list to dict list"""
	@wraps(fn)
	def wrapper(*args, **kwargs):
		rv = list()
		objects =  fn(*args, **kwargs)
		for o in objects:
			rv.append( o.to_dict() )
		return rv
	return wrapper

class Connector(ConnectorBase):

	@classmethod
	def initialize(self, db_url):
		self.engine = create_engine(db_url, echo=True) #FIXME: Remove echo=True
		m.Base.metadata.create_all(self.engine)
		self.Session = sessionmaker(bind=self.engine)

	def get_user(self, user_id, session=None):
		session = session or self.Session()
		try:
			user = session.query(m.User).filter(m.User.id==user_id).one()
		except NoResultFound, e:
			raise exceptions.UnknownUser(unicode(e))
		return user

	def create_user(self, username):
		user = m.User(username=username)
		s = self.Session()
		s.add(user)
		s.commit()
		return user.id

	def post_tweet(self, user_id, tweet):
		s = self.Session()
		user = self.get_user(user_id, s)
		tweet = m.Tweet(user=user, text=tweet)
		s.add(tweet)
		s.commit()
		return tweet.id

	def follow(self, user_id, followed_user_id):
		s = self.Session()
		user = self.get_user(user_id, s)
		followed_user = self.get_user(followed_user_id, s)
		friendship = m.Friendship(following_user=user, followed_user=user)
		s.add(friendship)
		try:
			s.commit()
		except IntegrityError:
			pass

	def unfollow(self, user_id, unfollowed_user_id):
		s = self.Session()
		user = self.get_user(user_id, s)
		unfollowed_user = self.get_user(unfollowed_user_id, s)
		friendship = m.Friendship(following_user=user, followed_user=user)
		s.query(m.Friendship).filter(m.Friendship.following_user==user, m.Friendship.followed_user==unfollowed_user).delete()
		s.commit()
		
	@to_dicts
	def get_feed(self, user_id=None, tweet_id=None, start=0, amount=50):
		s = self.Session()
		q = s.query(m.Tweet)
		if user_id:
			user = self.get_user(user_id, s)
			q = q.filter(m.Tweet.user==user)
		if tweet_id:
			q = q.filter(m.Tweet.id==tweet_id)
		tweets = q.offset(start).limit(amount).all()
		return tweets

