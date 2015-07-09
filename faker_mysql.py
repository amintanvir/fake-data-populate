#!/usr/bin/python
# -*- coding: utf-8 -*-
from query_mysql import *
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


def constraint_finder(tables,cur):
	"""finding the constraints of all the tables in db"""
	for table in tables:
		cur.execute("truncate %s cascade;"%table)
		cur.execute(query_for_constraint % table)
		constraint_dic={}
		
		for i in cur.fetchall():
			constraint_dic[i[0]] = str(i[1])
		yield constraint_dic










constraint_list=constraint_finder(all_tables,cursor)
print "All contraint list from targeted database database"
print constraint_list

