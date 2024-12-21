from apscheduler.triggers.cron import CronTrigger
from os import environ
from psycopg2 import connect, OperationalError, DatabaseError

DATABASE_URL = environ['DATABASE_URL']

# conn = connect(DATABASE_URL)
# cur = conn.cursor()

def with_commit(func):
	def inner(*args, **kwargs):
		func(*args, **kwargs)
		commit()

	return inner

def commit():
  try:
    conn = connect(DATABASE_URL)

    conn.commit()
    
  except (Exception, DatabaseError) as error:
    print(error)

  finally:
    if conn is not None:
      conn.close()

@with_commit
def build():
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
    conn = connect(DATABASE_URL)
    cur = conn.cursor()

    for table in tables:
      cur.execute(table)

    conn.commit()
    
  except (Exception, DatabaseError) as error:
    print(error)

  finally:
    if conn is not None:
      conn.close()

  print('Build() execution end')

def script_execute(path):
  try:
    conn = connect(DATABASE_URL)
    cur = conn.cursor()

    cur.execute(open(path, "r", encoding="utf-8").read())
    conn.commit()

  except (Exception, DatabaseError) as error:
    print(error)

  finally:
    if conn is not None:
      conn.close()

def autosave(sched):
	sched.add_job(commit, CronTrigger(second=0))
   
def close(cur):
  if cur.closed is False:
    cur.close()
  else:
    print("Cursor is already closed!")

def field(command, *values):
  try:
    conn = connect(DATABASE_URL)
    cur = conn.cursor()

    cur.execute(command, tuple(values))

    if (fetch := cur.fetchone()) is not None:
      return fetch[0]
    
  except (Exception, DatabaseError) as error:
    print(error)

  finally:
    if conn is not None:
      conn.close()
  
def record(command, *values):
  try:
    conn = connect(DATABASE_URL)
    cur = conn.cursor()

    cur.execute(command, tuple(values))

    return cur.fetchone()
    
  except (Exception, DatabaseError) as error:
    print(error)

  finally:
    if conn is not None:
      conn.close()

def records(command, *values):
  try:
    conn = connect(DATABASE_URL)
    cur = conn.cursor()

    cur.execute(command, tuple(values))

    return cur.fetchall()

  except (Exception, DatabaseError) as error:
    print(error)

  finally:
    if conn is not None:
      conn.close()

def column(command, *values):
  try:
    conn = connect(DATABASE_URL)
    cur = conn.cursor()

    cur.execute(command, tuple(values))

    return [item[0] for item in cur.fetchall()]
    
  except (Exception, DatabaseError) as error:
    print(error)

  finally:
    if conn is not None:
      conn.close()

def execute(command, *values):
  try:
    conn = connect(DATABASE_URL)
    cur = conn.cursor()

    cur.execute(command, tuple(values))

    conn.commit()
    
  except (Exception, DatabaseError) as error:
    print(error)

  finally:
    if conn is not None:
      conn.close()

def multi_execute(command, valueset):
  try:
    conn = connect(DATABASE_URL)
    cur = conn.cursor()

    cur.executemany(command, valueset)

    conn.commit()
    
  except (Exception, DatabaseError) as error:
    print(error)

  finally:
    if conn is not None:
      conn.close()

def fetch_polls():
  try:    
    polls =  {}
    rows = records("SELECT * FROM polls;")
    for row in rows:
        polls[row[0]] = (row[1], row[2])
    return polls
  except OperationalError as e:
      print(e)