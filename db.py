#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
##Copyright 2018 Robin "riisen" Riis
#
#Redistribution and use in source and binary forms, with or without modification,
#are permitted provided that the following conditions are met:
#
##1. Redistributions of source code must retain the above copyright notice,
#this list of conditions and the following disclaimer.
#
##2. Redistributions in binary form must reproduce the above copyright notice,
#this list of conditions and the following disclaimer in the documentation and/or
#other materials provided with the distribution.
#
#THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY
#EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO,
#THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.
#IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
#INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
#PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS;
#OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT,
#STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
#ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE,
#EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import sqlite3
import uuid
import re

class GotNoTableError(Exception):
    pass

def is_sql_valid(the_argument):
    return re.match(r"^[0-9a-zA-Z_\-\*]+$", '', the_argument)

def is_valid_swedish_mobilenumber(the_number):
    return re.match(r"^(\+?46|0)7(0|2|3|6|9)\d{7}$", the_number)

def is_valid_swedish_homenumber(the_number):
    return re.match(r"^(\+?46|0)\d{8}$", the_number)

def is_valid_email(the_mail):
    return re.match(r"^\w+@\w+[\.]\w{2,6}$", the_mail)

def is_valid_regnummer(regnummer):
    return re.match(r"^(\w{3} ?\d{3})$", regnummer)

def remove_non_numeric(the_string):
    return re.sub("[^0-9]", "", the_string)

def random_idx():
    return uuid.uuid4().int & (1<<32)-1

class Columns():
    def __init__(self, name, kind, primary_key=None):
        self.Name = name
        self.Kind = kind
        self.Primary_key = primary_key

    def get(self):
        ret = str(self.Name)+" "+str(self.Kind)
        if self.Primary_key:
            ret += " PRIMARY KEY"
        return str(ret)

    def __str__(self):
        return self.get()

class Databas():
    """This is a Parent-class
    for classes that needs sqlite3
    the constructor takes 1 optional argument named db.
    that defaults to 'Database.db' if not specified
    """

    def __init__(self, table, db="Database.db"):
        """Constructor function

        Parameters:
        -----------
        db : str
            The name of the database
        table : str
            The name of the table the child class will use

        Returns:
        -----------
        Nothing
        """

        _connect = None
        _cursor = None
        self.database = db
        self.Table = table
        self.Columns = []

    def add_column(self, name, kind, primary_key=None):
        """Add a sql column to your database class/table

        Parameters:
        -----------
        name : str
            the name of the database table
        kind : str
            the type of the database table (like TEXT, INTEGER, REAL, BLOB)
        primary_key : int
            defaults to None.. else it is a primary key

        Returns:
        -----------
        None
        """
        self.Columns.append(Columns(name, kind, primary_key))

    def get_primary_key(self):
        """Search and find the primary key column

        Parameters:
        -----------
        None

        Returns:
        -----------
        str
            the name of the primary key column or "NotFound" if not found
        """

        for x in self.Columns:
            if x.Primary_key:
                return x.Name
        return "NotFound"

    def get_columns(self):
        """Get all columns in table

        Parameters:
        -----------
        None

        Returns:
        ----------
        str
            of all columns in table separated by ', '
        """
        ret = ''
        for col in self.Columns:
            ret += col.Name+', '
        return ret[:-2]

    def select(self, cols=None, table=None, where=None, fetchone=None):
        """select query

        Parameters:
        -----------
        cols : str
            string of columns in db table separated by ', '

        table : str
            the table name

        where : str
            the column value of the primary_key in db table

        fetchone : int
            if None return all if not return just one

        Returns:
        -----------
        list
            of results from db table
        """
        query = 'SELECT '
        values = []
        if cols == None:
            query += self.get_columns()
        else:
            query += str(cols)
        query += ' FROM '
        if table == None:
            query += self.Table
        else:
            query += str(table)
        if not where == None:
            query += ' WHERE '+self.get_primary_key()+' = ?'
            values.append(where)
        self.open_database()
        self._cursor.execute(query, tuple(values))
        if fetchone != None:
            result = self._cursor.fetchone()
        else:
            result = self._cursor.fetchall()
        self.close_database()
        return result

    def query_this(self, q, v=None, ret=False):
        """Make a sql-query!

        Parameters:
        -----------
        q : str
            Query to send
        v : tuple
            Values in wildcards of query string
        ret : bool
            if it should return the result

        Returns:
        -----------
        None or list of result
        """
        self.open_database()
        if v:
            self._cursor.execute(q, v)
        else:
            self._cursor.execute(q)
        if not ret:
            self.close_database()
            return
        else:
            ret = self._cursor.fetchall()
            self.close_database()
        return ret

    def insert_into_query(self):
        """get the sql query to insert in all columns in table

        Parameters:
        -----------
        None

        Returns:
        -----------
        str
            a sql statement
        """

        val = '('
        i = 0
        while i < len(self.Columns):
            val += '?, '
            i += 1
        val = val[:-2]+');'
        return 'INSERT INTO '+self.Table+'('+self.get_columns()+') VALUES'+val

    def remove_by_id(self, idx):
        """Remove an item from the database

        Parameters:
        -----------
        idx : int
            The ID number

        Returns:
        ----------
        None
        """
        query = "DELETE FROM "+self.Table+" WHERE "+self.get_primary_key()+" = ?"
        self.query_this(query (idx,))

    def open_database(self):
        """Open the database connection

        Parameters:
        -----------
        Empty

        Returns:
        -----------
        None or Error
        """
        try:
            self._connect = sqlite3.connect(self.database)
            self._cursor = self._connect.cursor()
        except Error as fel:
            print('Kunde inte öppna databasen: '+self.database)
            print('Fel medelande: '+fel)
        return

    def close_database(self):
        """Close the database connection

        Parameters:
        -----------
        None

        Returns:
        -----------
        None
        """
        if self._connect:
            self._connect.commit()
            self._cursor.close()
            self._connect.close()

    def create_database_table(self):
        """Create the table if not exists

        Parameters:
        -----------
        None

        Returns:
        -----------
        None
        """

        query = "CREATE TABLE IF NOT EXISTS "+self.Table+"("
        for x in self.Columns:
            query += x.get()+','
        query = query[:-1]+');'
        self.query_this(query)

    def __str__(self):
        return 'this is a database class, dont print it :D'
