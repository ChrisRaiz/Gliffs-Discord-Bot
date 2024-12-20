from apscheduler.triggers.cron import CronTrigger
from os import environ
from psycopg2 import connect, OperationalError, DatabaseError

DATABASE_URL = environ['DATABASE_URL']

conn = connect(DATABASE_URL)

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

  tables = (
          """CREATE TABLE IF NOT EXISTS guilds(
            guild_id BIGINT UNIQUE PRIMARY KEY,
            prefix VARCHAR (5) DEFAULT '!');""",
          """CREATE TABLE IF NOT EXISTS exp(
            user_id BIGINT UNIQUE PRIMARY KEY,
            xp INTEGER DEFAULT 0,
            level SMALLINT DEFAULT 0,
            xp_lock TIMESTAMP DEFAULT CURRENT_TIMESTAMP);""",
          """CREATE TABLE IF NOT EXISTS mutes(
            user_id BIGINT UNIQUE PRIMARY KEY,
            role_ids TEXT NOT NULL,
            end_time TIMESTAMP);""",
          """CREATE TABLE IF NOT EXISTS starboard(
            root_message_id BIGINT UNIQUE PRIMARY KEY,
            star_message_id BIGINT UNIQUE NOT NULL,
            stars INTEGER DEFAULT 1);""",
          """CREATE TABLE IF NOT EXISTS polls(
            poll_message_id BIGINT UNIQUE PRIMARY KEY,
            channel_id BIGINT NOT NULL,
            question TEXT NOT NULL);"""
  )    

  try:
    for table in tables:
        cur.execute(table)
    conn.commit()
  except (Exception, DatabaseError) as error:
      print(error)

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