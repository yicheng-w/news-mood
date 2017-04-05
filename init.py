import sqlite3
import constants as c

conn = sqlite3.connect(c.feedback_db)

cur = conn.cursor()

creation = "CREATE TABLE %s (%s)"

cur.execute(creation % (c.headline_table, "id INTEGER, headline TEXT"))
cur.execute(creation % (c.feeback_table, "id INTEGER, emotion INTEGER"))

conn.commit()
