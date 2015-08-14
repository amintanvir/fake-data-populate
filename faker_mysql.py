#!/usr/bin/python
# -*- coding: utf-8 -*-
from query_mysql import *
import MySQLdb as mdb
from faker import Faker
import random

fake = Faker()


# Database connection
host = 'localhost'
user = 'root'
password = 'cloudly1'
database = 'fakertest'
connection = mdb.connect(host, user, password, database)
try:
    cursor = connection.cursor()
    print "Connected successfully"
except:
    print "Unable to connect"


# Fake data provider for mysql database datatype
def value_provider(limit=None):
    return {"character": fake.pystr(max_chars=5),
            "character varying": fake.pystr(max_chars=5),
            "varchar": fake.pystr(max_chars=5),
            "char": fake.random_letter(),
            "text": fake.pystr(max_chars=5),
            "bit": random.choice([True, False]),
            "varbit": random.choice([True, False]),
            "bit varying": random.choice([True, False]),
            "smallint": fake.random_digit(),
            "int": fake.random_number(),
            "bigint": fake.random_number(),
            "float": fake.random_number(),
            "integer": fake.random_digit(),
            "decimal": fake.random_number(),
            "smallserial": fake.random_number(),
            "serial": fake.random_number(),
            "bigserial": fake.random_number(),
            "double": fake.random_number(),
            "numeric": fake.random_digit(),
            "double precision": fake.random_number(),
            "real": fake.random_number(),
            "money": fake.random_number(),
            "bool": random.choice([True, False]),
            "boolean": random.choice([True, False]),
            "bytea": random.choice([0, 1, 10]),
            "date": fake.date(pattern="%Y-%m-%d"),
            "interval": fake.time(pattern="%H:%M:%S"),
            "time": fake.time(pattern="%H:%M:%S"),
            "datetime": fake.date_time_this_year(),
            "timestamp": fake.date_time_this_month(),
            "timestamp without time zone": fake.date_time(),
            "timestamp with time zone": fake.date_time(),
            "time without time zone": fake.time(pattern="%H:%M:%S"),
            "time with time zone": fake.time(pattern="%H:%M:%S"),
            "cidr": fake.ipv4(),
            "inet": fake.ipv6(),
            "ARRAY": '{{"jame","came"}}',
            "oid": fake.random_number(),
            "string": fake.random_letter(),
            "null": fake.random_digit_or_empty(),
            "tsvector": fake.random_letter(),
            "enum": fake.random_number(),
            "longtext": fake.pystr(max_chars=5),
            "longblob": fake.mime_type(category=None),
            "tinyint": fake.random_number(),
            "blob": fake.mime_type(category=None),
            "year": fake.year()

            }


# This function list down all tables from selected database
def find_table(cur):
    """Listing all the tables from the database """
    cur.execute("SHOW TABLES;")
    return [table[0] for table in cur.fetchall()]


# Assign all table in container
all_tables = find_table(cursor)
print "All tables from  %s Database" % database
print all_tables


# Before populate data this function turn off all triggers and truncate all tables
def disable_trigger(cur, tables, conn):
    """this function disable all the trigger and truncate all the tables"""
    # disabling trigger
    # try:
    #     pass
    #     cur.execute("SET session_replication_role = replica;")
    #     cur.execute("SET session_replication_role = DEFAULT;")
    # except:
    #     print "problem disable trigger"

    for table in tables:
        try:
            print " -------- tuncate ---------- table :{0}".format(table)
            cur.execute(query_for_disable_constarints)
            cur.execute(query_for_truncatetable % table)
            cur.execute(query_for_disabletrigger)
            print "trigger successfully turn off"
            # cur.execute("ALTER TABLE %s DISABLE TRIGGER %s"%(table,conn))
            # cur.execute("ALTER TABLE %s DISABLE ALL TRIGGERS")%table
            # truncating all the tables
            # cur.execute(query_for_disable_constarints)
            # cur.execute(query_for_truncatetable %table)
        except:
            pass


disable_trigger(cursor, all_tables, connection)


# This function list down all constraint from tables
def constraint_finder(tables, cur):
    """finding the constraints of all the tables in db and put them in a dictionary"""
    for table in tables:
        cur.execute(query_for_constraint % table)
        constraint_dic = {}
        # all_constraints is a list of tuple where each tuple contains (column_name,key_name) like (student_id,primary_key)
        all_constraints = cur.fetchall()
        for constraint in all_constraints:
            try:
                constraint_dic[constraint[0]].append(constraint[1])
            except:
                constraint_dic[constraint[0]] = [constraint[1]]

        yield constraint_dic


constraint_finder(all_tables, cursor)


def place_holder(columns):
    """creates tuple for inserting like if a table has 4 columns it returns('%s','%s','%s','%s')"""
    value_tuple = ()
    for i in range(columns):
        value_tuple += ('%s',)
    return str(tuple(value_tuple))


# Check constraint value provider
def check_constraint_value_provider(*args):
    return {
        "timestamp without time zone": timestamp_wo_timezone(*args)
    }


def date_provider(start='1900-01-01 00:00:00', end='2020-01-01 00:00:00'):
    time_format = '%Y-%m-%d %H:%M:%S'
    stime = time.mktime(time.strptime(start, time_format))
    etime = time.mktime(time.strptime(end, time_format))
    ptime = stime + random.random() * (etime - stime)
    return time.strftime(time_format, time.localtime(ptime))


def timestamp_wo_timezone(*args):
    times_list = re.findall(r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})', str(args))
    return date_provider(*times_list)

# print check_constraint_value_provider(*my_time).get("timestamp without time zone")


# This function populate fake data in tables
def insert_into_table(tables, cur, constraint, number, conn):
    for table in tables:
        cur.execute(query_for_datatypes % table)
        column_names = [value[0] for value in cur.fetchall()]
        print column_names
        cur.execute(query_for_datatypes % table)
        column_datatypes = [value[1] for value in cur.fetchall()]
        print column_datatypes
        constraint_dic = constraint.next()
        place_holder(len(column_names))
        value_holder_tuple = place_holder(len(column_names))
        print "table name %s" % table
        for i in range(number):
            value_list = []
            for column in column_names:
                if column in constraint_dic:
                    # column has constraints
                    if ('CHECK' in constraint_dic[str(column)]):
                        cur.execute(query_for_check % (table, column))
                        check_constraint = cur.fetchall()
                        value = check_constraint_value_provider(*check_constraint).get(
                            str(column_datatypes[column_names.index(column)]))
                        value_list.append(value)
                    if (('FOREIGN KEY' in constraint_dic[str(column)]) or ('UNIQUE' in constraint_dic[str(column)]) or (
                                'PRIMARY KEY' in constraint_dic[str(column)])):
                        value_list.append(i)

                else:
                    # column doesn't have constraints
                    val = value_provider().get(str(column_datatypes[column_names.index(column)]))
                    value_list.append(val)

            # If want to print each table at the time of data populates
            print table

            try:
                query = ("INSERT INTO %s VALUES " % (table) + value_holder_tuple)
                cur.execute(query % tuple(value_list))
                conn.commit()

            except:
                print "problem found %s" % table
                print column_datatypes
                print value_list


#constraint_list = constraint_finder(all_tables, cursor)
# print "All contraint list from targeted database database"
# print constraint_list


# Change the number to populate fake data in each table according to you requirements
insert_into_table(all_tables, cursor, constraint_finder(all_tables, cursor), 6, connection)
