import sqlite3
import requests

# Step 1: Download English word list
WORDLIST_URL = "https://raw.githubusercontent.com/dwyl/english-words/master/words.txt"
response = requests.get(WORDLIST_URL)
words = response.text.splitlines()

print(f"Total words downloaded: {len(words)}")

# Step 2: Create SQLite database
db_file = "english_words.sqlite"
conn = sqlite3.connect(db_file)
cursor = conn.cursor()

# Step 3: Create table with UNIQUE word
cursor.execute("""
CREATE TABLE IF NOT EXISTS words (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    word TEXT UNIQUE NOT NULL
)
""")
conn.commit()

# Step 4: Insert words, ignoring duplicates
cursor.executemany("INSERT OR IGNORE INTO words (word) VALUES (?)", [(word,) for word in words])
conn.commit()

print(f"Saved words to {db_file} (duplicates automatically ignored)")

# Step 5: Close connection
conn.close()
