import sqlite3

# connection to database file
connection = sqlite3.connect('database.db')

#open schema file and execute its contents
with open('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

#execute sql statements to add posts to posts table
cur.execute("INSERT INTO posts (title, content) VALUES (?, ?)",
            ('First Post', 'Content for the first post')
            )

cur.execute("INSERT INTO posts (title, content) VALUES (?, ?)",
            ('Second Post', 'Content for the second post')
            )

# commit changes
connection.commit()
# close connection
connection.close()