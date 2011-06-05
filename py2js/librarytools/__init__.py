# copyright 2011 Samuel Ytterbrink <neppord@gmail.com>
"""
    This module contains functions to find and concatenate features and modules
    written in JavaScript located in the JavaScript library directory.
"""

# hopefully you could change this to something other then the sqlit3 library
# if you use this on the server side of a web application.
import sqlite3 as db_lib

import glob
import re
import os
import collections

REQUIRES = "^requires:(.*)$"
CONTAINS = "^contains:(.*)$"

DB_FILE = "library.db"
LIBRARY_DIRS = ["library"]

CREATE_REQUIRES = "CREATE TABLE requires (file text, argument text)"
CREATE_CONTAINS = "CREATE TABLE contains (file text, argument text)"
CREATE_FILES = "CREATE TABLE files (file text)"


INSERT_REQUIRES = "INSERT INTO requires VALUES (?, ?)"
INSERT_CONTAINS = "INSERT INTO contains VALUES (?, ?)"
INSERT_FILE = "INSERT INTO files VALUES (?)"

def open_db():
    """
        creates a connection and returns the connection and the cursor.
    """
    db = db_lib.connect(DB_FILE)
    cursor = db.cursor()
    return db, cursor

def close_db(db, cursor):
    """
        closes down the connection and cursor
    """
    db.commit()
    cursor.close()

def update_db():
    """
    Search the LIBRARY_DIRS for files with tags, and creating DB_FILE. This 
    function should only be called if you suspect that the DB_FILE is outdated.
    """
    os.remove(DB_FILE)
    db, cursor = open_db()
    cursor.execute(CREATE_REQUIRES)
    cursor.execute(CREATE_CONTAINS)
    cursor.execute(CREATE_FILES)

    # searching for all files that we should build our db from
    js_files = []
    for directory in LIBRARY_DIRS: 
        js_files += glob.glob(directory + "\*.js")

    # look for tags
    for js_file in js_files:
        contents = file(js_file, "rb").read()
        cursor.execute(INSERT_FILE, (js_file,))
        # add information to DB_FILE
        for arg in re.findall(REQUIRES, contents, re.M):
            cursor.execute(INSERT_REQUIRES,(js_file, arg.strip()))
        for arg in re.findall(CONTAINS, contents, re.M):
            cursor.execute(INSERT_CONTAINS,(js_file, arg.strip()))
    close_db(db, cursor)

def require(contains):
    """
        returns a list of all the "require" of the file related to the "contains".
    """
    db, cursor = open_db()

    cursor.execute("SELECT file FROM contains WHERE argument = ? ", (contains, ))
    file_name = cursor.fetchone() # returns a tuple
    if not file_name:
        raise ValueError("No file contains:" + contains)
    cursor.execute("SELECT DISTINCT argument FROM requires WHERE file = ?", file_name)
    requires = map(lambda item:item[0], cursor.fetchall())
    close_db(db, cursor)

    return requires + [contains]

def allrequire(contains):
    """
        returns a list of _all_ the "require" of a "contains", Using BSF.
    """
    queue = collections.deque(require(contains))
    visited = []
    while len(queue) > 0:
        contains = queue.pop()
        if contains in visited:
            continue
        visited.append(contains)
        queue.extendleft(require(contains))
    return visited


def create_runtime(requires):
    """
        Concatenates the files that contains the requirements and
        the required features into a string. You may want to call update_db
        before calling this function to be sure that the DB_FILE is up to
        date.
    """

    db, cursor = open_db()

    requires_list = sum((allrequire(req) for req in requires), [])
    command = (
                "SELECT DISTINCT file "
                "FROM contains "
                "WHERE argument IN (" 
                ) + ",".join("'"+s+"'" for s in requires_list) + ")"
    
    cursor.execute(command)
    contains_files = cursor.fetchall()

    db.commit()
    cursor.close()

    contents = []
    for file_name, in sorted(contains_files):
        contents.append(file(file_name, "rb").read())
    return "\n/*new file*/\n".join(contents)

def list_builtins():
    """
    Returns a list off all function that the librarytools have in its DB_FILE
    """

    db, cursor = open_db()

    cursor.execute(
            (
                "SELECT DISTINCT argument "
                "FROM contains "
                "WHERE argument LIKE '\\_\\_builtin\\_\\_.%' ESCAPE '\\'"
                )
            )

    ret = cursor.fetchall()
    db.commit()
    cursor.close()
    if ret:
        return map(lambda name: ".".join(name[0].split(".")[1:]), ret)
    else:
        return []
if __name__ == "__main__":
    update_db()
    req = "__builtin__.zip"
    import pprint
    print "list_bilitins():"
    pprint.pprint(list_builtins())
    print "require('" + req + "'):"
    pprint.pprint(require(req))
    print "allrequire(' + req + '):"
    pprint.pprint(allrequire(req))
    print "create_runtime([req]).count('\n') + 1:"
    print (create_runtime([req])).count('\n') + 1
