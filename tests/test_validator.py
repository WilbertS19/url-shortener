"""
Unit tests untuk modul validator.
Total: 8 test cases
"""
import pytest
from app.validator import URLValidator


class TestURLValidation:
    """Test untuk validasi URL."""

    def test_valid_http_url(self):
        """Test 1: URL dengan skema http harus valid."""
        is_valid, error = URLValidator.validate_url("http://example.com")
        assert is_valid is True
        assert error == ""

    def test_valid_https_url_with_path(self):
        """Test 2: URL https dengan path harus valid."""
        is_valid, error = URLValidator.validate_url("https://example.com/path/to/page?q=1")
        assert is_valid is True
        assert error == ""

    def test_empty_url_is_invalid(self):
        """Test 3: URL kosong harus invalid."""
        is_valid, error = URLValidator.validate_url("")
        assert is_valid is False
        assert "kosong" in error.lower()

    def test_none_url_is_invalid(self):
        """Test 4: URL None harus invalid."""
        is_valid, error = URLValidator.validate_url(None)
        assert is_valid is False

    def test_url_without_scheme_is_invalid(self):
        """Test 5: URL tanpa skema http/https harus invalid."""
        is_valid, error = URLValidator.validate_url("example.com")
        assert is_valid is False
        assert "http" in error.lower()

    def test_url_with_invalid_scheme(self):
        """Test 6: URL dengan skema selain http/https harus invalid."""
        is_valid, error = URLValidator.validate_url("ftp://example.com")
        assert is_valid is False

    def test_url_too_long_is_invalid(self):
        """Test 7: URL melebihi batas maksimum harus invalid."""
        long_url = "https://example.com/" + ("a" * 3000)
        is_valid, error = URLValidator.validate_url(long_url)
        assert is_valid is False
        assert "panjang" in error.lower()

    def test_url_without_domain_is_invalid(self):
        """Test 8: URL tanpa domain valid harus invalid."""
        is_valid, error = URLValidator.validate_url("https://nodomain")
        assert is_valid is False


class TestCustomCodeValidation:
    """Test untuk validasi custom short code."""

    def test_valid_alphanumeric_code(self):
        """Test 9: Custom code alphanumeric harus valid."""
        is_valid, error = URLValidator.validate_custom_code("abc123")
        assert is_valid is True

    def test_valid_code_with_dash_and_underscore(self):
        """Test 10: Custom code dengan dash dan underscore harus valid."""
        is_valid, error = URLValidator.validate_custom_code("my-code_1")
        assert is_valid is True

    def test_code_too_short_is_invalid(self):
        """Test 11: Custom code kurang dari 3 karakter harus invalid."""
        is_valid, error = URLValidator.validate_custom_code("ab")
        assert is_valid is False
        assert "minimal" in error.lower()

    def test_code_too_long_is_invalid(self):
        """Test 12: Custom code melebihi 20 karakter harus invalid."""
        is_valid, error = URLValidator.validate_custom_code("a" * 25)
        assert is_valid is False
        assert "maksimal" in error.lower()

    def test_code_with_special_chars_is_invalid(self):
        """Test 13: Custom code dengan karakter spesial harus invalid."""
        is_valid, error = URLValidator.validate_custom_code("my@code!")
        assert is_valid is False

    def test_reserved_code_is_invalid(self):
        """Test 14: Reserved keyword tidak boleh digunakan."""
        is_valid, error = URLValidator.validate_custom_code("admin")
        assert is_valid is False
        assert "reserved" in error.lower()

    def test_none_code_is_invalid(self):
        """Test 15: Custom code None harus invalid."""
        is_valid, error = URLValidator.validate_custom_code(None)
        assert is_valid is False
