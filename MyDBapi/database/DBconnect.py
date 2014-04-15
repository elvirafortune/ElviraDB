__author__ = 'Elvira'

import MySQLdb
import MySQLdb.cursors

def connect():
    db = MySQLdb.connect(host='localhost', port=3306, db='ElviraApiDb',
    user='root', passwd='390191',
    cursorclass=MySQLdb.cursors.SSDictCursor)
    return db