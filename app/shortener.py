"""
Shortener module - Logika bisnis untuk men-generate dan mengelola short code.
"""
import random
import string
import hashlib


class CodeGenerator:
    """Kelas untuk men-generate short code unik."""

    DEFAULT_LENGTH = 6
    CHARSET = string.ascii_letters + string.digits

    @staticmethod
    def generate_random_code(length=DEFAULT_LENGTH):
        """
        Generate short code random.

        Args:
            length (int): Panjang code yang akan di-generate

        Returns:
            str: Random short code

        Raises:
            ValueError: Jika length tidak valid
        """
        if not isinstance(length, int):
            raise ValueError("Length harus berupa integer")

        if length < 3:
            raise ValueError("Length minimal 3 karakter")

        if length > 20:
            raise ValueError("Length maksimal 20 karakter")

        return ''.join(random.choices(CodeGenerator.CHARSET, k=length))

    @staticmethod
    def generate_hash_code(url, length=DEFAULT_LENGTH):
        """
        Generate code berbasis hash dari URL (deterministik).

        Args:
            url (str): URL yang akan di-hash
            length (int): Panjang code

        Returns:
            str: Hash-based short code
        """
        if not url:
            raise ValueError("URL tidak boleh kosong")

        if length < 3 or length > 20:
            raise ValueError("Length harus antara 3 dan 20")

        hash_obj = hashlib.md5(url.encode('utf-8'))
        # Ambil hex digest dan potong sesuai length
        return hash_obj.hexdigest()[:length]


class URLShortener:
    """Kelas utama untuk service URL shortener."""

    def __init__(self, storage):
        """
        Initialize URL shortener dengan storage.

        Args:
            storage: Instance storage (database/file)
        """
        if storage is None:
            raise ValueError("Storage tidak boleh None")
        self.storage = storage
        self.max_attempts = 10

    def shorten(self, url, custom_code=None):
        """
        Mempersingkat URL.

        Args:
            url (str): URL yang akan dipersingkat
            custom_code (str, optional): Custom short code

        Returns:
            dict: Informasi short URL

        Raises:
            ValueError: Jika input tidak valid atau code sudah ada
        """
        from app.validator import URLValidator

        # Validasi URL
        is_valid, error = URLValidator.validate_url(url)
        if not is_valid:
            raise ValueError(error)

        url = url.strip()

        # Jika custom code diberikan, validasi dan gunakan
        if custom_code is not None:
            is_valid, error = URLValidator.validate_custom_code(custom_code)
            if not is_valid:
                raise ValueError(error)

            if self.storage.exists(custom_code):
                raise ValueError(f"Short code '{custom_code}' sudah digunakan")

            short_code = custom_code
        else:
            # Generate random code, coba beberapa kali jika collision
            short_code = self._generate_unique_code()

        # Simpan ke storage
        self.storage.save(short_code, url)

        return {
            'short_code': short_code,
            'original_url': url,
            'clicks': 0
        }

    def _generate_unique_code(self):
        """Generate code unik yang belum ada di storage."""
        for _ in range(self.max_attempts):
            code = CodeGenerator.generate_random_code()
            if not self.storage.exists(code):
                return code
        raise RuntimeError("Tidak dapat men-generate short code unik")

    def resolve(self, short_code):
        """
        Mendapatkan URL asli dari short code dan increment counter.

        Args:
            short_code (str): Short code

        Returns:
            str: URL asli

        Raises:
            KeyError: Jika short code tidak ditemukan
        """
        if not short_code:
            raise ValueError("Short code tidak boleh kosong")

        url = self.storage.get(short_code)
        if url is None:
            raise KeyError(f"Short code '{short_code}' tidak ditemukan")

        # Increment click counter
        self.storage.increment_clicks(short_code)

        return url

    def get_stats(self, short_code):
        """
        Mendapatkan statistik dari short code.

        Args:
            short_code (str): Short code

        Returns:
            dict: Statistik short code
        """
        if not short_code:
            raise ValueError("Short code tidak boleh kosong")

        stats = self.storage.get_stats(short_code)
        if stats is None:
            raise KeyError(f"Short code '{short_code}' tidak ditemukan")

        return stats
