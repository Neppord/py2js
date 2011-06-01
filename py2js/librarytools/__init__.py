# copyright 2011 Samuel Ytterbrink <neppord@gmail.com>
"""
    This module contains functions to find and concatenate features and modules
    written in JavaScript located in the JavaScript library directory.
"""
import sqlite3
import glob
import re
import os

REQUIRES = "^requires:(.*)$"
CONTAINS = "^contains:(.*)$"
CONTAINS_FEATURE = "^contains_feature:(.*)$"
REQUIRES_FEATURE = "^requires_feature:(.*)$"

DB_FILE = "library.db"
LIBRARY_DIRS = ["library"]

CREATE_TABLE = (
    "CREATE TABLE dependencies (" 
    "file text, "
    "requires text, "
    "contains text, "
    "requires_feature text,"
    "contains_feature text)"
    )
INSERT = "INSERT INTO dependencies values (?, ?, ?, ?, ?)"

def update_db():
    """
    Search the LIBRARY_DIRS for files with tags, and creating DB_FILE. This 
    function should only be called if you suspect that the DB_FILE is outdated.
    """
    os.remove(DB_FILE)
    db = sqlite3.connect(DB_FILE)
    cursor = db.cursor()
    cursor.execute(CREATE_TABLE)

    # searching for all files that we should build our db from
    js_files = []
    for directory in LIBRARY_DIRS: 
        js_files += glob.glob(directory + "\*.js")

    # look for tags
    for js_file in js_files:
        contents = file(js_file, "rb").read()
        requires = ",".join(re.findall(REQUIRES, contents))
        contains = ",".join(re.findall(CONTAINS, contents))
        requires_feature = ",".join(re.findall(REQUIRES_FEATURE, contents))
        contains_feature = ",".join(re.findall(CONTAINS_FEATURE, contents))
        # add information to DB_FILE
        cursor.execute(
                INSERT,
                (
                    js_file,
                    requires,
                    contains,
                    requires_feature,
                    contains_feature
                )
                )
    db.commit()
    cursor.close()




update_db()
