import sqlite3 as sq

"""
INITIALIZES FTS TABLES FOR SCHOOL NAME SEARCH
"""

init_db = sq.connect("data.db")

init_db.enable_load_extension(True)
init_db.load_extension("./fts5")

cur = init_db.cursor()
cur.execute("DROP TABLE IF EXISTS SCHOOL_NAMES_FTS")
cur.execute("CREATE VIRTUAL TABLE IF NOT EXISTS SCHOOL_NAMES_FTS USING FTS5(INSTITUTION_NAME, INSTITUTION_ID)")
cur.execute("INSERT INTO SCHOOL_NAMES_FTS(INSTITUTION_NAME, INSTITUTION_ID) SELECT INSTITUTION_NAME, INSTITUTION_ID FROM\
                ACCREDITATION_2015_6 GROUP BY INSTITUTION_NAME, INSTITUTION_ID")
cur.execute("INSERT INTO SCHOOL_NAMES_FTS(SCHOOL_NAMES_FTS) VALUES ('optimize')")

init_db.commit()
init_db.close()
