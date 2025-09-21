import sqlite3

conn = sqlite3.connect("english_words_bytes.sqlite")
cursor = conn.cursor()
cursor.execute("SELECT word FROM words LIMIT 5")
rows = cursor.fetchall()

for row in rows:
    print(row[0], type(row[0]))  # type(row[0]) should show <class 'bytes'>
conn.close()
