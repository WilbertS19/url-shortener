"""
Validator module - Menangani validasi input untuk aplikasi URL Shortener.
"""
import re
from urllib.parse import urlparse


class URLValidator:
    """Kelas untuk memvalidasi URL dan custom short code."""

    # Maximum panjang URL yang diizinkan
    MAX_URL_LENGTH = 2048
    # Minimum dan maximum panjang custom code
    MIN_CODE_LENGTH = 3
    MAX_CODE_LENGTH = 20
    # Pattern untuk custom code (huruf, angka, dash, underscore)
    CODE_PATTERN = re.compile(r'^[a-zA-Z0-9_-]+$')
    # Skema URL yang diizinkan
    ALLOWED_SCHEMES = {'http', 'https'}

    @staticmethod
    def validate_url(url):
        """
        Memvalidasi format URL.

        Args:
            url (str): URL yang akan divalidasi

        Returns:
            tuple: (is_valid: bool, error_message: str)
        """
        if not url:
            return False, "URL tidak boleh kosong"

        if not isinstance(url, str):
            return False, "URL harus berupa string"

        url = url.strip()

        if len(url) == 0:
            return False, "URL tidak boleh kosong"

        if len(url) > URLValidator.MAX_URL_LENGTH:
            return False, f"URL terlalu panjang (max {URLValidator.MAX_URL_LENGTH} karakter)"

        try:
            parsed = urlparse(url)
        except Exception:
            return False, "Format URL tidak valid"

        if parsed.scheme not in URLValidator.ALLOWED_SCHEMES:
            return False, "URL harus menggunakan http atau https"

        if not parsed.netloc:
            return False, "URL harus memiliki domain yang valid"

        # Validasi domain memiliki minimal satu titik
        if '.' not in parsed.netloc:
            return False, "Domain tidak valid"

        return True, ""

    @staticmethod
    def validate_custom_code(code):
        """
        Memvalidasi custom short code yang diberikan user.

        Args:
            code (str): Custom code yang akan divalidasi

        Returns:
            tuple: (is_valid: bool, error_message: str)
        """
        if code is None:
            return False, "Custom code tidak boleh None"

        if not isinstance(code, str):
            return False, "Custom code harus berupa string"

        if len(code) < URLValidator.MIN_CODE_LENGTH:
            return False, f"Custom code minimal {URLValidator.MIN_CODE_LENGTH} karakter"

        if len(code) > URLValidator.MAX_CODE_LENGTH:
            return False, f"Custom code maksimal {URLValidator.MAX_CODE_LENGTH} karakter"

        if not URLValidator.CODE_PATTERN.match(code):
            return False, "Custom code hanya boleh berisi huruf, angka, dash (-) dan underscore (_)"

        # Reserved keywords yang tidak boleh digunakan
        reserved = {'api', 'admin', 'shorten', 'stats', 'health'}
        if code.lower() in reserved:
            return False, f"Custom code '{code}' adalah reserved keyword"

        return True, ""
