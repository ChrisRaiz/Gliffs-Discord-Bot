from apscheduler.triggers.cron import CronTrigger
from os import environ
from os.path import isfile
from psycopg2 import connect, OperationalError

BUILD_PATH = "./data/db/build.sql"

conn = connect(database = environ["DB_DATABASE"],
               user = environ["DB_USER"],
               host = environ["DB_HOST"],
               password = environ["DB_PASS"],
               port = environ["DB_PORT"])

cur = conn.cursor()

def with_commit(func):
	def inner(*args, **kwargs):
		func(*args, **kwargs)
		commit()

	return inner

def commit():
  conn.commit()

@with_commit
def build():
  print('Build() execution start')
  if isfile(BUILD_PATH):
    script_execute(BUILD_PATH)
  print('Build() execution end')

def script_execute(path):
  cur.execute(open(path, "r", encoding="utf-8").read())

def autosave(sched):
	sched.add_job(commit, CronTrigger(second=0))
   
def close():
  cur.close()

def field(command, *values):
  cur.execute(command, tuple(values))

  if (fetch := cur.fetchone()) is not None:
    return fetch[0]
  
def record(command, *values):
  cur.execute(command, tuple(values))

  return cur.fetchone()

def records(command, *values):
  cur.execute(command, tuple(values))

  return cur.fetchall()

def column(command, *values):
  cur.execute(command, tuple(values))

  return [item[0] for item in cur.fetchall()]

def execute(command, *values):
  cur.execute(command, tuple(values))

def multi_execute(command, valueset):
  cur.executemany(command, valueset)

def fetch_polls():
  try:
    polls =  {}
    rows = records("SELECT * FROM polls;")
    for row in rows:
        polls[row[0]] = (row[1], row[2])
    return polls
  except OperationalError as e:
      print(e)