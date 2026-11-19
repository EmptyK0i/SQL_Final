import sqlite3

def get_nested_text_value(
    db_path: str, parent_key: str, nested_key: str
) -> str | None:
  query = """
        SELECT tv.text_value
        FROM parent_dictionaries pd
        INNER JOIN nested_dictionaries nd ON nd.parent_key = pd.key
        INNER JOIN dictionary_text_values tv ON tv.parent_key = nd.key
        WHERE pd.key = ? AND nd.key = ?
        LIMIT 1;
    """
  with sqlite3.connect(db_path) as conn:
    cursor = conn.cursor()
    cursor.execute(query, (parent_key, nested_key))
    row = cursor.fetchone()
    return row[0] if row else None
  
connection = sqlite3.connect("tables.db")
connection.execute("PRAGMA foreign_keys = ON")

try:
    cursor = connection.cursor()

    cursor.execute("DROP TABLE IF EXISTS parent_dictionaries;")
    cursor.execute("DROP TABLE IF EXISTS nested_dictionaries;")
    cursor.execute("DROP TABLE IF EXISTS dictionary_text_values;")
    cursor.execute("DROP TABLE IF EXISTS dictionary_int_values;")
    cursor.execute("DROP TABLE IF EXISTS dictionary_list_values;")

    # parent_dictionaries
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS parent_dictionaries (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        key TEXT NOT NULL UNIQUE
        )
        """
        )
    
    # nested_dictionaries
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS nested_dictionaries (
        parent_key TEXT NOT NULL,
        key TEXT NOT NULL,
        FOREIGN KEY (parent_key) REFERENCES parent_dictionaries (key) ON DELETE CASCADE
        )
        """
        )

    # dictionary_text_values
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS dictionary_text_values (
        parent_key TEXT NOT NULL,
        text_value TEXT
        )
        """
        )

    # dictionary_int_values
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS dictionary_int_values (
        parent_key TEXT NOT NULL,
        int_value INTEGER
        )
        """
        )

    # dictionary_list_values
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS dictionary_list_values (
        parent_key TEXT NOT NULL,
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        int_value INTEGER,
        text_value TEXT
        )
        """
        )

    connection.commit()

    # inserting data:
    
    # Creating parent_dictionary 'character'
    cursor.execute("INSERT INTO parent_dictionaries (key) VALUES (?)",
                   ('character',))    

    # Creating nested_dictionary 'name'
    cursor.execute("INSERT INTO nested_dictionaries (parent_key, key) VALUES (?, ?)",
                   ('character','name'))

    # Creating dictionary_text_value 'Aeloria Nightwhisper'
    cursor.execute("INSERT INTO dictionary_text_values (parent_key, text_value) VALUES (?, ?)",
                   ('name','Aeloria Nightwhisper'))

    connection.commit()
        
finally:
    connection.close()

# Usage
character_name = get_nested_text_value("tables.db", "character", "name")
print(character_name)  # Output: Aeloria Nightwhisper

