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
            return r[0][0]
        else:
            return 0

    def add_headline(self, headline):
        """
        add_headline: add the headline to the headlines table, returns the id,
        if it already exists, just return the id
    
        Args:
            headline (string): the headline to add
        
        Returns:
            int - id of the headline (new or old)
        """
        h_id = self.get_id(headline)
        if not h_id:
            h_id = self.get_next_available_id()
            values = "%d, ?" % (h_id)
            q = self.insert_q % (c.headline_table, values)
            self.db.execute(q, (headline,))
        return h_id

    def get_id(self, headline):
        condition = "WHERE headline = ? LIMIT 1"
        q = self.select_q % ("id", c.headline_table, condition)
        r = self.db.execute(q, (headline,))
        if len(r) > 0:
            return r[0][0]
        else:
            return None

    def add_emotion(self, h_id, emotion_id):
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
    h_id = db.add_headline("blah blah blah")
    db.add_emotion(h_id, c.sentiment_lookup_reverse['anger'])
    print db.query_emotion_feedback("blah blah blah")
