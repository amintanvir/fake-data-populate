from query import *
import psycopg2
from faker import Faker
import random

fake = Faker()
 
 #This will give database connection credentials
user_credentials = {'host':'localhost',
               'database':'db_fakertest',
               'user':'postgres',
               'password':'cloudly1'}

#Fake data provider for postgresql datatype
value_provider={"character":fake.pystr(max_chars=5) ,
		"character varying":fake.pystr(max_chars=5) ,
		"varchar":fake.pystr(max_chars=5),
		"char":fake.pystr(max_chars=5),
		"text":fake.random_letter() ,
		"bit":random.choice([True, False]),
		"varbit":random.choice([True, False]),
		"bit varying":random.choice([True, False]),
		"smallint":fake.random_digit() ,
		"int":fake.random_number(),
		"bigint":fake.random_number(),
		"integer":fake.random_number() ,
		"smallserial":fake.random_number(),
		"serial":fake.random_number(),
		"bigserial":fake.random_number(),
		"numeric":fake.random_digit(),
		"double precision":fake.random_number(),
		"real":fake.random_number(),
		"money":fake.random_number(),
		"bool":random.choice([True, False]),
		"boolean":random.choice([True, False]),
		"bytea":random.choice([0,1,10]),
		"date":fake.date(pattern="%Y-%m-%d") ,
		"interval":fake.time(pattern="%H:%M:%S"),
		"timestamp without time zone":fake.date_time_ad()
		
		}


#Build connection with database
try:
	conn=psycopg2.connect(**user_credentials)
	cursor = conn.cursor()
	print "connected successfully"
except:
	print "unable to connect"


#This function retrieve all table from targeted database
def find_table(cur):
	"""Listing all the tables from the database """
	
	cur.execute("select relname from pg_class where relkind='r' and relname !~ '^(pg_|sql_)';")
	return  [table[0] for table in  cur.fetchall()]

#Assign all table in container
all_tables=find_table(cursor)
print "All tables from  targated Database"
print all_tables

#This function find out constraint from all tables
def constraint_finder(tables,cur):
	"""finding the constraints of all the tables in db"""
	for table in tables:
		cur.execute("truncate %s cascade;"%table)
		cur.execute(query_for_constraint % table)
		constraint_dic={}
		
		for i in cur.fetchall():
			constraint_dic[i[0]] = str(i[1])
		yield constraint_dic
		




#This function populate fake data in tables
def insert_tupel(tables,cur,conn,constraint,value_dic,n):
	#to disable all triggers;
	try:
		cur.execute("SET session_replication_role = replica;")
		cur.execute("SET session_replication_role = DEFAULT;")
	except:
		print "problem disable trigger"
	
	for table in tables:#go through each table
		try:
			cur.execute("ALTER TABLE %s DISABLE TRIGGER %s"%(table,user))
			
			
			
			print "trigger successfully turn off"
		except:
			pass
		

		cur.execute(query_for_datatypes % table)
		column_names= [value[0] for value in cur.fetchall()]
		print "Table columns name"
		print column_names
		
		cur.execute(query_for_datatypes % table)
		column_datatypes=[value[1] for value in cur.fetchall()]
		print "Table data type"
		print column_datatypes
		
		constraint_dic=constraint.next()
		
		def place_holder(num_col):
			value_tuple=()
			for i in range (num_col):
				value_tuple += ('%s',)
			return str(tuple(value_tuple))


		value_holder_tuple=place_holder(len(column_names))
		for i in range (n):
			value_list=[]
			for column in column_names:
			
				if column in constraint_dic:
					if (constraint_dic[str(column)] == 'FOREIGN KEY') or (constraint_dic[str(column)] == 'PRIMARY KEY') or (constraint_dic[str(column)] == 'UNIQUE') or (constraint_dic=='CHECK'):
						value_list.append(i)
						
					elif (constraint_dic[str(column)] == 'CHECK'):
						
						cur.execute("ALTER TABLE %s DROP CHECK CONSTRAINT %s")% (table,constraint_dic[str(column)])
						value_list.append(i)
				else :
					
					try:
						value_list.append(value_provider[column_datatypes[column_names.index(column)]])
					except:

						value_list.append('NULL')
			query = ("INSERT INTO %s VALUES " % (table) + value_holder_tuple)
			cur.execute(query % tuple(value_list))
			conn.commit()
		#conn.close()		 	
			  			
constraint_list=constraint_finder(all_tables,cursor)
print "All contraint list from targeted database database"
print constraint_list
insert_tupel(all_tables,cursor,conn,constraint_finder(all_tables,cursor),value_provider,10)
