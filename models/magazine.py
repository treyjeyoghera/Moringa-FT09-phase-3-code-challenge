# models/magazine.py

import sqlite3
from database.connection import get_db_connection

class Magazine:
    def __init__(self, id, name, category):
        self.id = id
        self.name = name
        self.category = category

    def __repr__(self):
        return f'<Magazine {self.name}>'

    def save_to_db(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO magazines (name, category) VALUES (?, ?)", (self.name, self.category))
        self.id = cursor.lastrowid
        conn.commit()
        conn.close()

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        if value is not None and not isinstance(value, int):
            raise ValueError("ID must be an integer")
        self._id = value

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if not isinstance(value, str) or not (2 <= len(value) <= 16):
            raise ValueError("Name must be a string between 2 and 16 characters")
        self._name = value

    @property
    def category(self):
        return self._category

    @category.setter
    def category(self, value):
        if not isinstance(value, str) or len(value) == 0:
            raise ValueError("Category must be a non-empty string")
        self._category = value

    def get_articles(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM articles WHERE magazine_id = ?", (self.id,))
        articles = cursor.fetchall()
        conn.close()
        return articles

    def get_contributors(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT DISTINCT authors.*
            FROM authors
            JOIN articles ON authors.id = articles.author_id
            WHERE articles.magazine_id = ?
        """, (self.id,))
        contributors = cursor.fetchall()
        conn.close()
        return contributors

    def get_article_titles(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT title FROM articles WHERE magazine_id = ?", (self.id,))
        titles = cursor.fetchall()
        conn.close()
        return [title[0] for title in titles] if titles else []

    def get_frequent_contributors(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT authors.*, COUNT(articles.id) as article_count
            FROM authors
            JOIN articles ON authors.id = articles.author_id
            WHERE articles.magazine_id = ?
            GROUP BY authors.id
            HAVING article_count > 2
        """, (self.id,))
        authors = cursor.fetchall()
        conn.close()
        return authors if authors else []
