# models/Article.py

import sqlite3
from database.connection import get_db_connection
from models.author import Author
from models.magazine import Magazine

class Article:
    def __init__(self, id, title, content, author_id, magazine_id):
        self.id = id
        self.title = title
        self.content = content
        self.author_id = author_id
        self.magazine_id = magazine_id

    def __str__(self):
        magazine = self.get_magazine()
        magazine_name = magazine.name if magazine else "Unknown Magazine"
        return f'< {magazine_name} {self.title} {self.content[:30]}...>'

    def save(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO articles (author_id, magazine_id, title, content) VALUES (?, ?, ?, ?)",
                       (self.author_id, self.magazine_id, self.title, self.content))
        self.id = cursor.lastrowid
        conn.commit()
        conn.close()

    def get_author(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM authors WHERE id = ?", (self.author_id,))
        author_data = cursor.fetchone()
        conn.close()
        if author_data:
            return Author(author_data["id"], author_data["name"])
        return None

    def get_magazine(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM magazines WHERE id = ?", (self.magazine_id,))
        magazine_data = cursor.fetchone()
        conn.close()
        if magazine_data:
            return Magazine(magazine_data["id"], magazine_data["name"], magazine_data["category"])
        return None
