import sqlite3

with sqlite3.connect('sample.db') as connection:
    # get a cursor object used to execute SQL commands
    c = connection.cursor()

    # drop the table first
    c.execute('DROP TABLE posts')
    # create the table
    c.execute('CREATE TABLE posts(title TEXT, description TEXT)')

    # insert dummy data into the table
    c.execute('INSERT INTO posts VALUES("Good", "I\'m good.")')
    c.execute('INSERT INTO posts VALUES("Well", "I\'m well.")')
    c.execute('INSERT INTO posts VALUES("Excellent", "I\'m excellent.")')
    c.execute('INSERT INTO posts VALUES("Okay", "I\'m okay.")')
