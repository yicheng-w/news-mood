import sqlite3
import constants as c
import os

def is_initialized():
    assert c.feedback_db in os.listdir('.')
    db = Connection(c.feedback_db)
    tables = db.execute("SELECT sql FROM sqlite_master WHERE type='table'")
    assert len(tables) == 2

class Connection:
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()

    def execute(self, *args):
        self.cursor.execute(*args)
        retVal = list(self.cursor.fetchall())
        self.conn.commit()
        return retVal

    def __del__(self):
        self.conn.close()
        del self.cursor
        del self.conn

class DBManager:
    def __init__(self):
        self.db = Connection(c.feedback_db)
        self.insert_q = "INSERT INTO %s VALUES (%s)"
        self.select_q = "SELECT %s FROM %s %s"

    def get_next_available_id(self):
        condition = "ORDER BY id DESC LIMIT 1"
        q = self.select_q % ("id", c.headline_table, condition)
        r =  self.db.execute(q)
        if r:
            return r
        else:
            return 0

    def add_headline(self, headline):
        values = "%d, ?" % (self.get_next_available_id())
        q = self.insert_q % (c.headline_table, values)
        self.db.execute(q, (headline,))

    def get_id(self, headline):
        condition = "WHERE headline = ? LIMIT 1"
        q = self.select_q % ("id", c.headline_table, condition)
        r = self.db.execute(q, (headline,))
        return r[0][0]

    def add_emotion(self, headline, emotion_id):
        h_id = self.get_id(headline)
        values = "?, ?"
        q = self.insert_q % (c.feeback_table, values)
        self.db.execute(q, (h_id, emotion_id))

    def query_emotion_feedback(self, headline):
        h_id = self.get_id(headline)
        condition = "WHERE id = ?"
        q = self.select_q % ("emotion", c.feeback_table, condition)
        result = self.db.execute(q, (h_id,))
        emotions = [0 for i in xrange(6)] # all possible emotions
        for (a, ) in result:
            emotions[a] += 1

        return emotions


if __name__ == "__main__":
    import os
    os.system("rm feedback.db")
    import init
    is_initialized()
    db = DBManager()
    db.add_headline("blah blah blah")
    db.add_emotion("blah blah blah", c.sentiment_lookup_reverse['anger'])
    print db.query_emotion_feedback("blah blah blah")
