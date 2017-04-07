import constants as c
import csv
import sqlite3
import os
from database import DBManager

def get_csv_from_feedback(csv_file_location):
    """
    get_csv_from_feedback: cleans the database, and dumps the result into a csv
    file

    Args:
        csv_file_location (string): location of the csv file to generate
    
    Returns: void
    """

    db_manager = DBManager(c.feedback_db)
    feedbacks = db_manager.get_all_emotion_feedbacks()
    db_manager.clear_tables()

    with open(csv_file_location, 'wb') as output:
        writer = csv.writer(output)
        writer.writerow(["headline"] + c.sentiment_lookup)

        for (headline, emotions) in feedbacks:
            writer.writerow([headline] + emotions)
