#!/usr/bin/python
# -*- coding: utf-8 -*-
from query_psql import *
import MySQLdb as mdb
from faker import Faker
import random
fake = Faker()


#Database connection 
user_credentials = mdb.connect('localhost', 'root', 'cloudly1', 'db_test')

try:
	cursor = user_credentials.cursor()
	print "connected successfully"
except:
	print "unable to connect"

def find_table(cur):
	"""Listing all the tables from the database """
	
	cur.execute("SHOW TABLES;")
	return  [table[0] for table in  cur.fetchall()]

#Assign all table in container
all_tables=find_table(cursor)
print "All tables from  targated Database"
print all_tables