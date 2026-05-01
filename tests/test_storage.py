"""
Unit tests untuk modul storage.
Total: 5 test cases
"""
import pytest
from app.storage import URLStorage


class TestURLStorage:
    """Test untuk class URLStorage."""

    @pytest.fixture
    def storage(self):
        """Fixture untuk in-memory storage."""
        s = URLStorage(':memory:')
        yield s
        s.close()

    def test_save_and_get_url(self, storage):
        """Test 33: Save dan get URL harus mengembalikan URL yang benar."""
        storage.save("abc123", "https://example.com")
        assert storage.get("abc123") == "https://example.com"

    def test_save_duplicate_raises(self, storage):
        """Test 34: Save short_code yang sudah ada harus raise ValueError."""
        storage.save("dup", "https://example.com")
        with pytest.raises(ValueError):
            storage.save("dup", "https://other.com")

    def test_exists_returns_correct_value(self, storage):
        """Test 35: Method exists harus mengembalikan True/False yang benar."""
        assert storage.exists("notexist") is False
        storage.save("exist1", "https://example.com")
        assert storage.exists("exist1") is True

    def test_increment_clicks(self, storage):
        """Test 36: increment_clicks harus menambah counter."""
        storage.save("clk1", "https://example.com")
        storage.increment_clicks("clk1")
        storage.increment_clicks("clk1")
        storage.increment_clicks("clk1")
        stats = storage.get_stats("clk1")
        assert stats['clicks'] == 3

    def test_delete_existing_entry(self, storage):
        """Test 37: Delete entry yang ada harus berhasil."""
        storage.save("del1", "https://example.com")
        result = storage.delete("del1")
        assert result is True
        assert storage.exists("del1") is False

    def test_delete_nonexistent_returns_false(self, storage):
        """Test 38: Delete entry yang tidak ada harus mengembalikan False."""
        result = storage.delete("notexist")
        assert result is False
