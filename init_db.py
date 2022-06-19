import sqlite3

connection = sqlite3.connect('database.db')


with open('shop.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()
cur.execute("INSERT INTO producer (id, producer_country) VALUES (?,?)",
            (1, 'Russia')
            )
cur.execute("INSERT INTO producer (id, producer_country) VALUES (?,?)",
            (2, 'USA',)
            )

cur.execute("INSERT INTO posts (title, content,producer_id) VALUES (?, ?, ?)",
            ('First Post', 'Content for the first post', 1)
            )

cur.execute("INSERT INTO posts (title, content,producer_id) VALUES (?, ?, ?)",
            ('Second Post', 'Content for the second post', 2)
            )

connection.commit()
connection.close()