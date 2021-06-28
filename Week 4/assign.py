import json
import sqlite3

conn=sqlite3.connect('rosterdb.sqlite')
cur=conn.cursor()

cur.executescript('''
DROP TABLE IF EXISTS User;
DROP TABLE IF EXISTS Member;
DROP TABLE IF EXISTS Course;

create table User (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE
);

create table Course (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT UNIQUE
);

create table Member (
    user_id INTEGER,
    course_id INTEGER,
    role INTEGER,
    PRIMARY KEY (user_id, course_id)
);
''')

fname = 'roster_data.json'
data = json.loads(open(fname).read())

for entry in data:
    name = entry[0]
    title = entry[1]
    role = entry[2]

    cur.execute('insert or ignore into User(name) values (?)', (name,))
    cur.execute('Select id from user where name = ?',(name,))
    user_id=cur.fetchone()[0]

    cur.execute('insert or ignore into Course(title) values (?)', (title,))
    cur.execute('Select id from Course where title = ?',(title,))
    course_id=cur.fetchone()[0]

    cur.execute('insert or replace into Member values (?,?,?)', (user_id,course_id,role))

    conn.commit()