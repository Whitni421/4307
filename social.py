#!/usr/bin/env python3

import click
import os
import sqlite3
import sys

DB_FILE = 'network.db'

def getdb(create=False):
    if os.path.exists(DB_FILE):
        if create:
            os.remove(DB_FILE)
    else:
        if not create:
            print('no database found')
            sys.exit(1)
    con = sqlite3.connect(DB_FILE)
    con.execute('PRAGMA foreign_keys = ON')
    return con

@click.group()
def cli():
    pass

@click.command()
def create():
    with getdb(create=True) as con:
        con.execute(
'''CREATE TABLE users (
    id          INTEGER PRIMARY KEY,
    email       TEXT NOT NULL
)''')
        con.execute(
'''CREATE UNIQUE INDEX users_email ON users (email)''')

        con.execute(
'''CREATE TABLE accounts (
    id          INTEGER PRIMARY KEY,
    user_id     INTEGER NOT NULL,
    username    TEXT NOT NULL,

    FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE ON UPDATE CASCADE
)''')
    print('database created')

@click.command()
@click.argument('email')
def adduser(email):
    print('creating user with email address', email)
    with getdb() as con:
        cursor = con.cursor()
        cursor.execute('''INSERT INTO users (email) VALUES (?)''', (email,))
        id = cursor.lastrowid
        print(f'inserted with id={id}')

@click.command()
@click.argument('email')
@click.argument('username')
def addaccount(email, username):
    print('creating account with username', username, 'for email', email)
    with getdb() as con:
        cursor = con.cursor()
        cursor.execute('''INSERT INTO accounts (user_id, username)
VALUES ((SELECT id FROM users WHERE email = ?), ?)''', (email, username))
        id = cursor.lastrowid
        print(f'inserted with id={id}')

cli.add_command(create)
cli.add_command(adduser)
cli.add_command(addaccount)
cli()
