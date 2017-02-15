import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()


class Users(Base):
	
	__tablename__ = 'users'
	
	id = Column(Integer, primary_key=True)
	username = Column(String(250), nullable=False)
	password = Column(String(250), nullable=False)
	email = Column(String(250), nullable=False)
	department = Column(String(250), nullable=False)
	designation = Column(String(250))
	
class Issues(Base):
	
	__tablename__ = 'issues'
	
	id = Column(Integer, primary_key=True)
	name = Column(String(80), nullable=False)
	description = Column(String(250), nullable = True)
	priority = Column(String(20), nullable= True)
	department = Column(String(250), nullable= True)
	assignned = Column(String(250), nullable= True)
	opened = Column(String(250), nullable= True)
	resolved = Column(String(250), nullable= True)
	remarks = Column(String(250), nullable= True)
	user_id = Column(Integer, ForeignKey('users.id'))
	users = relationship(Users)
	
engine = create_engine('sqlite:///issue_tracker.db')
Base.metadata.create_all(engine)