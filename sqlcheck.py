#! /usr/bin/python3
import sqlite3 
conn = sqlite3.connect('be_proj_check.db')
''' We need to use the Connection instance method cursor() to return a Cursor instance corresponding to the database we want to query.
'''
cursor = conn.cursor()
print(cursor)
cursor.execute('SELECT * FROM employee;')
#cursor.execute("insert into department(did, dname, hod) values (?, ?, ?)",(d, d_name, hod_t))
#cursor.execute("insert into employee(ename, dept_id) values (?,?)",(d_name,d))
results = cursor.fetchall()
print(results)
conn.commit()

