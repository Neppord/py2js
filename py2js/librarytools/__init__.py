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

REQUIRES_ENTRY = 0
REQUIRES_FEATURE_ENTRY = 1
CONTAINS_ENTRY = 2
CONTAINS_FEATURE_ENTRY = 3
FILE_FOUND_ENTRY =4

DB_FILE = "library.db"
LIBRARY_DIRS = ["library"]

CREATE_TABLE = (
    "CREATE TABLE dependencies (" 
    "file text, "
    "argument text, "
    "type int)"
    )
INSERT = "INSERT INTO dependencies values (?, ?, ?)"

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
        cursor.execute(INSERT, (js_file, "", FILE_FOUND_ENTRY))
        # add information to DB_FILE
        for arg in re.findall(REQUIRES, contents, re.M):
            cursor.execute(
                    INSERT,
                    (js_file, arg.strip(), REQUIRES_ENTRY)
                    )
        for arg in re.findall(CONTAINS, contents, re.M):
            cursor.execute(
                    INSERT,
                    (js_file, arg.strip(), CONTAINS_ENTRY)
                    )
        for arg in re.findall(REQUIRES_FEATURE, contents, re.M):
            cursor.execute(
                    INSERT,
                    (js_file, arg.strip(), REQUIRES_FEATURE_ENTRY)
                    )
        for arg in re.findall(CONTAINS_FEATURE, contents, re.M):
            cursor.execute(
                    INSERT,
                    (js_file, arg.strip(), CONTAINS_FEATURE_ENTRY)
                    )

    db.commit()
    cursor.close()

def list_builtins():
    """
    Returns a list off all function that the librarytools have in its DB_FILE
    """
    db = sqlite3.connect(DB_FILE)
    cursor = db.cursor()

    cursor.execute(
            (
                "SELECT DISTINCT argument "
                "FROM dependencies "
                "WHERE type = ? "
                "AND argument LIKE '\\_\\_builtin\\_\\_.%' ESCAPE '\\'"
                ),
            (CONTAINS_ENTRY,)
            )

    ret = cursor.fetchall()
    db.commit()
    cursor.close()
    if ret:
        return map(lambda name: ".".join(name[0].split(".")[1:]), ret)
    else:
        return []

