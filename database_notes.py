import sqlite3

def connect():
    return sqlite3.connect("data/database_notes.db")

def add_note(user_id, date, content, status="active"):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO notes (user_id, note, date, status) VALUES (?, ?, ?, ?)",
        (user_id, content, date, status)
    )
    conn.commit()
    note_id = cursor.lastrowid
    conn.close()
    return note_id 

def get_notes_by_user(user_id):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, note, date, status FROM notes 
        WHERE user_id = ? AND status = 'active'
        ORDER BY date DESC
    """, (user_id,))
    notes = cursor.fetchall()
    conn.close()
    return notes

def delete_note(note_id):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM notes WHERE id = ?", (note_id,))
    conn.commit()
    conn.close()

def update_note(note_id, new_text):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("UPDATE notes SET note = ? WHERE id = ?", (new_text, note_id))
    conn.commit()
    conn.close()

def update_note_status(note_id, new_status):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("UPDATE notes SET status = ? WHERE id = ?", (new_status, note_id))
    conn.commit()
    conn.close()