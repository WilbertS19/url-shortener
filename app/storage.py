"""
Storage module - Menangani persistensi data URL menggunakan SQLite.
"""
import sqlite3
from datetime import datetime


class URLStorage:
    """Kelas untuk menyimpan dan mengambil data URL."""

    def __init__(self, db_path=':memory:'):
        """
        Initialize storage dengan SQLite database.

        Args:
            db_path (str): Path ke file database, default in-memory
        """
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        self._create_table()

    def _create_table(self):
        """Membuat tabel urls jika belum ada."""
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS urls (
                short_code TEXT PRIMARY KEY,
                original_url TEXT NOT NULL,
                clicks INTEGER DEFAULT 0,
                created_at TEXT NOT NULL
            )
        ''')
        self.conn.commit()

    def save(self, short_code, original_url):
        """
        Menyimpan mapping short_code ke original_url.

        Args:
            short_code (str): Short code
            original_url (str): URL asli

        Raises:
            ValueError: Jika short_code sudah ada
        """
        if self.exists(short_code):
            raise ValueError(f"Short code '{short_code}' sudah ada")

        cursor = self.conn.cursor()
        cursor.execute(
            'INSERT INTO urls (short_code, original_url, clicks, created_at) VALUES (?, ?, 0, ?)',
            (short_code, original_url, datetime.utcnow().isoformat())
        )
        self.conn.commit()

    def exists(self, short_code):
        """
        Cek apakah short_code sudah ada.

        Args:
            short_code (str): Short code

        Returns:
            bool: True jika ada, False jika tidak
        """
        cursor = self.conn.cursor()
        cursor.execute('SELECT 1 FROM urls WHERE short_code = ?', (short_code,))
        return cursor.fetchone() is not None

    def get(self, short_code):
        """
        Mendapatkan URL asli dari short code.

        Args:
            short_code (str): Short code

        Returns:
            str | None: URL asli atau None jika tidak ditemukan
        """
        cursor = self.conn.cursor()
        cursor.execute('SELECT original_url FROM urls WHERE short_code = ?', (short_code,))
        row = cursor.fetchone()
        return row['original_url'] if row else None

    def increment_clicks(self, short_code):
        """
        Increment counter klik untuk short_code tertentu.

        Args:
            short_code (str): Short code
        """
        cursor = self.conn.cursor()
        cursor.execute(
            'UPDATE urls SET clicks = clicks + 1 WHERE short_code = ?',
            (short_code,)
        )
        self.conn.commit()

    def get_stats(self, short_code):
        """
        Mendapatkan statistik lengkap untuk short code.

        Args:
            short_code (str): Short code

        Returns:
            dict | None: Statistik atau None jika tidak ditemukan
        """
        cursor = self.conn.cursor()
        cursor.execute(
            'SELECT short_code, original_url, clicks, created_at FROM urls WHERE short_code = ?',
            (short_code,)
        )
        row = cursor.fetchone()
        if row is None:
            return None
        return {
            'short_code': row['short_code'],
            'original_url': row['original_url'],
            'clicks': row['clicks'],
            'created_at': row['created_at']
        }

    def get_all(self):
        """
        Mendapatkan semua URL yang tersimpan.

        Returns:
            list: List dictionary semua URL
        """
        cursor = self.conn.cursor()
        cursor.execute('SELECT short_code, original_url, clicks, created_at FROM urls')
        rows = cursor.fetchall()
        return [
            {
                'short_code': row['short_code'],
                'original_url': row['original_url'],
                'clicks': row['clicks'],
                'created_at': row['created_at']
            }
            for row in rows
        ]

    def delete(self, short_code):
        """
        Menghapus entry berdasarkan short_code.

        Args:
            short_code (str): Short code

        Returns:
            bool: True jika berhasil dihapus, False jika tidak ditemukan
        """
        if not self.exists(short_code):
            return False
        cursor = self.conn.cursor()
        cursor.execute('DELETE FROM urls WHERE short_code = ?', (short_code,))
        self.conn.commit()
        return True

    def close(self):
        """Menutup koneksi database."""
        if self.conn:
            self.conn.close()
