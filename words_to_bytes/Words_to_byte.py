import sqlite3

# Step 1: Connect to the original database
source_db = "english_words.sqlite"
conn_src = sqlite3.connect(source_db)
cursor_src = conn_src.cursor()

# Step 2: Fetch all words
cursor_src.execute("SELECT word FROM words")
all_words = cursor_src.fetchall()
print(f"Total words fetched: {len(all_words)}")

# Step 3: Convert words to bytes using UTF-8
words_bytes = [(sqlite3.Binary(word[0].encode('utf-8')),) for word in all_words]

# Step 4: Create a new SQLite database (or overwrite existing)
target_db = "english_words_bytes.sqlite"
conn_tgt = sqlite3.connect(target_db)
cursor_tgt = conn_tgt.cursor()

# Step 5: Drop the table if it exists (ensures no old text is there)
cursor_tgt.execute("DROP TABLE IF EXISTS words")

# Step 6: Create table with column explicitly as BLOB
cursor_tgt.execute("""
CREATE TABLE words (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    word BLOB NOT NULL
)
""")
conn_tgt.commit()

# Step 7: Insert the byte data correctly as BLOBs
cursor_tgt.executemany("INSERT INTO words (word) VALUES (?)", words_bytes)
conn_tgt.commit()

print(f"Saved {len(words_bytes)} words as bytes to {target_db}")

# Step 8: Close connections
conn_src.close()
conn_tgt.close()
