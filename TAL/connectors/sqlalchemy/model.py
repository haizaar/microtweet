import datetime

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.sql import func

from sqlalchemy.ext.declarative import declared_attr


class MyBase(object):
	@declared_attr
	def __tablename__(cls):
		return cls.__name__.lower()

	__table_args__ = {"mysql_engine": "InnoDB"}
	#__mapper_args__ = {"always_refresh": True}

	id =  Column(Integer, primary_key=True)
	created_at = Column(DateTime, default=func.utc_timestamp(), index=True)

	def to_dict(self):
		d = dict()
		for c in self.__table__.columns:
			v = getattr(self, c.name)
			if isinstance(v, datetime.datetime):
				v = v.isoformat()
			d[c.name] = v
		return d

Base = declarative_base(cls=MyBase)


class User(Base):
	username = Column(String(50), unique=True)

	def __repr__(self):
		return u"<User(%s)>" % self.username


class Tweet(Base):
	text = Column(String(140))

	user_id = Column(Integer, ForeignKey("user.id"))
	user = relationship("User", order_by=User.created_at, lazy="joined")

	def __repr__(self):
		return u"<Tweet(%s, %s)>" % (self.user.username, self.text)


class Friendship(Base):
	following_user_id = Column(Integer, ForeignKey("user.id"), index=True)
	following_user = relationship("User", foreign_keys=[following_user_id])

	followed_user_id = Column(Integer, ForeignKey("user.id"), index=True)
	followed_user = relationship("User", foreign_keys=[followed_user_id])

	__table_args__ = (UniqueConstraint("following_user_id", "followed_user_id"), Base.__table_args__)


