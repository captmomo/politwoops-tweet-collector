#!/usr/bin/env python
# encoding: utf-8
"""
beanstalk.py

Created by Breyten Ernsting on 2010-08-08.
Copyright (c) 2010 __MyCompanyName__. All rights reserved.
"""

import sys
import os
import unittest
import ConfigParser
import MySQLdb

import anyjson
import beanstalkc

import tweetsclient

class MySQLTrackPlugin(tweetsclient.TrackPlugin):
    def _get_database(self):
        self._debug("Making DB connection")
        conn = MySQLdb.connect(
            host=self.config.get('database', 'host'),
            port=int(self.config.get('database', 'port')),
            db=self.config.get('database', 'database'),
            user=self.config.get('database', 'username'),
            passwd=self.config.get('database', 'password'),
            charset="utf8",
            use_unicode=True
        )
        conn.cursor().execute('SET NAMES UTF8')
        return conn

    def _query(self, connection, table_name, field_name, conditions = None):
        cursor = connection.cursor()
        q = "SELECT `%s` FROM `%s`" % (field_name, table_name)
        if conditions:
            q = q + " WHERE %s" % (conditions)
        self._debug("Executing query " + q)
        cursor.execute(q)
        return [str(t[0]) for t in cursor.fetchall()]
    
    def _get_trackings(self):
        tbl = self.config.get('database', 'table')
        fld = self.config.get('database', 'field')
        cnd = self.config.get('database', 'conditions')
        conn = self._get_database()
        return self._query(conn, tbl, fld, cnd)
    
    def get_type(self):
        return self.config.get('tweets-client', 'type')
    
    def get_items(self):
        stream_type = self.get_type()
        if stream_type == 'users':
            return self._get_trackings()
        elif stream_type == 'words':
            return self._get_trackings()
        else:
            return []