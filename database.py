import sqlite3
import pandas as pd
from datetime import datetime, date

DB_FILE = "notebooks.db"

def init_db():
    """Initialize the database and create/migrate the table."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    # Create base table if it doesn't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS notebooks (
            url TEXT PRIMARY KEY,
            title TEXT,
            date_added TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Migrate: add description column if missing
    existing_cols = [row[1] for row in cursor.execute("PRAGMA table_info(notebooks)")]
    if 'description' not in existing_cols:
        cursor.execute("ALTER TABLE notebooks ADD COLUMN description TEXT DEFAULT ''")
    if 'tags' not in existing_cols:
        cursor.execute("ALTER TABLE notebooks ADD COLUMN tags TEXT DEFAULT ''")

    conn.commit()
    conn.close()

def save_results(results):
    """
    Save search results to the database.
    results: list of dicts {'title': str, 'url': str, 'description': str (optional)}
    Returns count of newly inserted rows.
    """
    if not results:
        return 0

    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    new_count = 0
    for item in results:
        try:
            cursor.execute('''
                INSERT INTO notebooks (url, title, description)
                VALUES (?, ?, ?)
            ''', (item['url'], item.get('title', item['url']), item.get('description', '')))
            new_count += 1
        except sqlite3.IntegrityError:
            # URL already exists — skip to preserve original discovery date
            pass

    conn.commit()
    conn.close()
    return new_count

def get_all_notebooks():
    """Retrieve all notebooks from the database as a pandas DataFrame."""
    conn = sqlite3.connect(DB_FILE)
    df = pd.read_sql_query("SELECT * FROM notebooks ORDER BY date_added DESC", conn)
    conn.close()
    return df

def delete_notebook(url):
    """Delete a notebook entry by URL. Returns True if deleted."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM notebooks WHERE url = ?", (url,))
    deleted = cursor.rowcount > 0
    conn.commit()
    conn.close()
    return deleted

def update_tags(url, tags):
    """Update the tags for a notebook entry. tags is a comma-separated string."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("UPDATE notebooks SET tags = ? WHERE url = ?", (tags.strip(), url))
    conn.commit()
    conn.close()

def get_stats():
    """Return a dict with total count and count added today."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM notebooks")
    total = cursor.fetchone()[0]
    today = date.today().isoformat()
    cursor.execute("SELECT COUNT(*) FROM notebooks WHERE date(date_added) = ?", (today,))
    today_count = cursor.fetchone()[0]
    conn.close()
    return {"total": total, "today": today_count}
