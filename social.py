#!/usr/bin/env python3

import click
import sqlite3
import os
import sys
import time
SCHEMA_FILE = 'schema.sql'
DB_NAME = 'database.db'

def read_schema():
    with open(SCHEMA_FILE, 'r') as f:
        return f.read()

@click.group()
def cli():
    pass

@click.command()
def create():
    # Connect to the SQLite database (this will create it if it doesn't exist)
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    print('Connected to the SQLite database')
    
    # Read the schema file's content
    schema = read_schema()

    # Execute the schema file's commands
    try:
        cursor.executescript(schema)
        click.echo("Database created successfully.")
    except sqlite3.Error as e:
        click.echo(f"An error occurred: {e}")
    finally:
        conn.close()

def getdb(create=False):
    if not os.path.exists(DB_NAME):
        if not create:
            print('No database found. Please create the database first.')
            sys.exit(1)
        else:
            create()
    conn = sqlite3.connect(DB_NAME)
    conn.execute('PRAGMA foreign_keys = ON')
    return conn

@click.command()
@click.argument('name')
@click.argument('email')
def addUser(name, email):
    print('Creating user with name and email address:', name," and ",email)
    with getdb() as con:
        cursor = con.cursor()
        cursor.execute('INSERT INTO Users (name,email) VALUES (?,?)', (name,email))
        id = cursor.lastrowid
        print(f'Inserted with id={id}')

@click.command()
@click.argument('email')
@click.argument('username')
def addAccount(email, username):
    print('Creating account with username:', username, 'for email:', email)
    with getdb() as con:
        cursor = con.cursor()
        cursor.execute('''INSERT INTO Accounts (user_id, username)
                          VALUES ((SELECT id FROM Users WHERE email = ?), ?)''', (email, username))
        id = cursor.lastrowid
        print(f'Inserted with id={id}')

@click.command()
@click.argument('userName')
@click.argument('title')
@click.argument('content')
def createPost(userName, title, content):
    print('Creating post with title:', title, 'for user:', userName)
    cursor.execute('''SELECT id FROM Users WHERE username = ?''', (userName,))
    user_id = cursor.fetchone()
    if user_id is None:
        print('User does not exist.')
        return
    with getdb() as con:
        cursor = con.cursor()
        cursor.execute('''INSERT INTO Posts (user_id, title, content)
                          VALUES ((SELECT id FROM users WHERE username = ?), ?, ?)''', (userName, title, content))
        id = cursor.lastrowid
        print(f'Inserted with id={id}')

@click.command()
@click.argument('userName')
def feed(userName):
    print('Listing posts for user:', userName)

    with getdb() as con:
        cursor = con.cursor()
        cursor.execute('''SELECT title, content FROM Posts WHERE user_id = (SELECT id FROM users WHERE username = ?)''', (userName,))
        rows = cursor.fetchall()
        for row in rows:
            print(row)
@click.command()
@click.argument('userName')
@click.argument('followUserName')
def follow(userName, followUserName):
    cursor.execute('''SELECT id FROM users WHERE username = ?''', (userName,))
    user_id = cursor.fetchone()
    followId=cursor.execute('''SELECT followee_id FROM Follows WHERE follower_id = ?''', (followUserName,))
    if user_id is None or followId is None:
        print('User does not exist.')
        return
    print('Following user:', userName, 'with id:', followUserName)
    with getdb() as con:
        cursor = con.cursor()
        cursor.execute('''INSERT INTO Follows (follower_id, followee_id)
                          VALUES ((SELECT id FROM users WHERE username = ?), ?)''', (userName, followUserName))
        id = cursor.lastrowid
        print(f'Inserted with id={id}')

@click.command() 
@click.argument('userName')
@click.argument('searchUser')
def searchUser(username,searchUser):
    print('Searching for user:', searchUser)
    with getdb() as con:
        cursor = con.cursor()
        cursor.execute('''SELECT username FROM users WHERE username = %?%''', (searchUser,))
        rows = cursor.fetchall()
        for row in rows:
            print(row)
# Adding commands to the click group
cli.add_command(feed)
cli.add_command(create)
cli.add_command(createPost)
cli.add_command(addUser)
cli.add_command(addAccount)
cli.add_command(follow)
cli.add_command(searchUser)

cli()
