"""
Unit tests untuk modul shortener (CodeGenerator dan URLShortener).
Total: 12 test cases
"""
import pytest
from app.shortener import CodeGenerator, URLShortener
from app.storage import URLStorage


class TestCodeGenerator:
    """Test untuk class CodeGenerator."""

    def test_generate_random_code_default_length(self):
        """Test 16: Random code default harus berlength 6."""
        code = CodeGenerator.generate_random_code()
        assert len(code) == 6

    def test_generate_random_code_custom_length(self):
        """Test 17: Random code dengan custom length."""
        code = CodeGenerator.generate_random_code(length=10)
        assert len(code) == 10

    def test_generate_random_code_uses_valid_charset(self):
        """Test 18: Random code hanya boleh berisi huruf dan angka."""
        code = CodeGenerator.generate_random_code(length=15)
        for char in code:
            assert char.isalnum()

    def test_generate_random_code_invalid_length_raises(self):
        """Test 19: Length kurang dari 3 harus raise ValueError."""
        with pytest.raises(ValueError):
            CodeGenerator.generate_random_code(length=2)

    def test_generate_random_code_too_long_raises(self):
        """Test 20: Length lebih dari 20 harus raise ValueError."""
        with pytest.raises(ValueError):
            CodeGenerator.generate_random_code(length=25)

    def test_generate_hash_code_deterministic(self):
        """Test 21: Hash code untuk URL yang sama harus identik."""
        url = "https://example.com"
        code1 = CodeGenerator.generate_hash_code(url)
        code2 = CodeGenerator.generate_hash_code(url)
        assert code1 == code2

    def test_generate_hash_code_different_urls(self):
        """Test 22: URL berbeda menghasilkan hash code berbeda."""
        code1 = CodeGenerator.generate_hash_code("https://example.com")
        code2 = CodeGenerator.generate_hash_code("https://different.com")
        assert code1 != code2

    def test_generate_hash_code_empty_url_raises(self):
        """Test 23: Hash code dengan URL kosong harus raise error."""
        with pytest.raises(ValueError):
            CodeGenerator.generate_hash_code("")


class TestURLShortener:
    """Test untuk class URLShortener (logika bisnis utama)."""

    @pytest.fixture
    def shortener(self):
        """Fixture untuk membuat shortener dengan in-memory storage."""
        storage = URLStorage(':memory:')
        return URLShortener(storage)

    def test_shorten_valid_url(self, shortener):
        """Test 24: Mempersingkat URL valid harus berhasil."""
        result = shortener.shorten("https://example.com")
        assert 'short_code' in result
        assert result['original_url'] == "https://example.com"
        assert result['clicks'] == 0

    def test_shorten_with_custom_code(self, shortener):
        """Test 25: Shorten dengan custom code harus pakai code tersebut."""
        result = shortener.shorten("https://example.com", custom_code="mycode")
        assert result['short_code'] == "mycode"

    def test_shorten_duplicate_custom_code_raises(self, shortener):
        """Test 26: Custom code yang sudah ada harus raise ValueError."""
        shortener.shorten("https://example.com", custom_code="dupcode")
        with pytest.raises(ValueError, match="sudah digunakan"):
            shortener.shorten("https://other.com", custom_code="dupcode")

    def test_shorten_invalid_url_raises(self, shortener):
        """Test 27: Shorten dengan URL invalid harus raise ValueError."""
        with pytest.raises(ValueError):
            shortener.shorten("not-a-valid-url")

    def test_resolve_existing_code(self, shortener):
        """Test 28: Resolve code yang ada mengembalikan URL asli."""
        shortener.shorten("https://example.com", custom_code="test01")
        result = shortener.resolve("test01")
        assert result == "https://example.com"

    def test_resolve_nonexistent_code_raises(self, shortener):
        """Test 29: Resolve code yang tidak ada harus raise KeyError."""
        with pytest.raises(KeyError):
            shortener.resolve("notexist")

    def test_resolve_increments_click_counter(self, shortener):
        """Test 30: Resolve harus menambah counter klik."""
        shortener.shorten("https://example.com", custom_code="track1")
        shortener.resolve("track1")
        shortener.resolve("track1")
        stats = shortener.get_stats("track1")
        assert stats['clicks'] == 2

    def test_get_stats_returns_correct_data(self, shortener):
        """Test 31: get_stats mengembalikan data yang benar."""
        shortener.shorten("https://example.com", custom_code="stats1")
        stats = shortener.get_stats("stats1")
        assert stats['short_code'] == "stats1"
        assert stats['original_url'] == "https://example.com"
        assert stats['clicks'] == 0

    def test_shortener_requires_storage(self):
        """Test 32: URLShortener tanpa storage harus raise ValueError."""
        with pytest.raises(ValueError):
            URLShortener(None)
