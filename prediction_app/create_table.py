#!/usr/bin/python
import psycopg2
from config import config



def create_tables():
    """ create tables in the PostgreSQL database"""
    command = (
        """
         CREATE TABLE games2 (
             game_id INTEGER PRIMARY KEY,
             day DATE NOT NULL,
             home_team VARCHAR(30) NOT NULL,
             visit_team VARCHAR(30) NOT NULL,
             home_pct REAL NOT NULL,
             visit_pct REAL NOT NULL,
             home_ml VARCHAR(8) NOT NULL,
             visit_ml VARCHAR(8) NOT NULL,
             home_current_ml VARCHAR(8) NOT NULL,
             visit_current_ml VARCHAR(8) NOT NULL
         )
        -- ALTER TABLE games 
        --     ADD COLUMN day DATE NOT NULL;
        """)
    conn = None
    try:
        # read the connection parameters
        params = config()
        # connect to the PostgreSQL server
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        # create table one by one
        # for command in commands:
        cur.execute(command)
        # close communication with the PostgreSQL database server
        cur.close()
        # commit the changes
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


if __name__ == '__main__':
    create_tables()