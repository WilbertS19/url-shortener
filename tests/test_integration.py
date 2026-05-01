"""
Integration tests untuk REST API URL Shortener.
Menguji interaksi end-to-end antara endpoint, service, dan storage.
Total: 7 integration test cases
"""
import pytest
import json
from app.main import create_app


@pytest.fixture
def client():
    """Fixture untuk membuat Flask test client dengan in-memory database."""
    app = create_app(':memory:')
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


class TestAPIIntegration:
    """Integration tests untuk REST API endpoints."""

    def test_health_endpoint(self, client):
        """
        Integration Test 1: Health check endpoint harus mengembalikan 200.
        Menguji: routing -> response.
        """
        response = client.get('/health')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['status'] == 'ok'

    def test_shorten_url_full_flow(self, client):
        """
        Integration Test 2: Full flow shorten URL -> save ke DB -> response.
        Menguji: endpoint -> validator -> shortener -> storage -> response.
        """
        response = client.post(
            '/api/shorten',
            data=json.dumps({'url': 'https://www.example.com/page'}),
            content_type='application/json'
        )
        assert response.status_code == 201
        data = json.loads(response.data)
        assert 'short_code' in data
        assert 'short_url' in data
        assert data['original_url'] == 'https://www.example.com/page'
        # Verifikasi short_code memiliki panjang yang benar
        assert len(data['short_code']) == 6

    def test_shorten_with_custom_code_then_resolve(self, client):
        """
        Integration Test 3: Shorten dengan custom code lalu redirect.
        Menguji: shorten endpoint -> redirect endpoint -> storage interaction.
        """
        # Step 1: Shorten dengan custom code
        response = client.post(
            '/api/shorten',
            data=json.dumps({
                'url': 'https://www.google.com',
                'custom_code': 'gogl1'
            }),
            content_type='application/json'
        )
        assert response.status_code == 201
        data = json.loads(response.data)
        assert data['short_code'] == 'gogl1'

        # Step 2: Akses short URL untuk redirect
        response = client.get('/gogl1', follow_redirects=False)
        assert response.status_code == 302
        assert 'https://www.google.com' in response.headers['Location']

    def test_shorten_invalid_url_returns_400(self, client):
        """
        Integration Test 4: Shorten dengan URL invalid harus return 400.
        Menguji: error handling pipeline dari endpoint -> validator.
        """
        response = client.post(
            '/api/shorten',
            data=json.dumps({'url': 'not-a-url'}),
            content_type='application/json'
        )
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data

    def test_stats_endpoint_after_redirects(self, client):
        """
        Integration Test 5: Stats endpoint mengembalikan click count yang benar
        setelah beberapa kali redirect.
        Menguji: integrasi antara redirect handler dan click counter di storage.
        """
        # Buat short URL
        client.post(
            '/api/shorten',
            data=json.dumps({
                'url': 'https://example.com',
                'custom_code': 'stat1x'
            }),
            content_type='application/json'
        )

        # Lakukan 3x redirect
        for _ in range(3):
            client.get('/stat1x', follow_redirects=False)

        # Cek stats
        response = client.get('/api/stats/stat1x')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['clicks'] == 3
        assert data['original_url'] == 'https://example.com'

    def test_resolve_nonexistent_short_code(self, client):
        """
        Integration Test 6: Akses short code yang tidak ada harus return 404.
        Menguji: error handling untuk resource yang tidak ditemukan.
        """
        response = client.get('/notexists')
        assert response.status_code == 404
        data = json.loads(response.data)
        assert 'error' in data

    def test_duplicate_custom_code_returns_400(self, client):
        """
        Integration Test 7: Mendaftarkan custom code yang sama 2x harus gagal.
        Menguji: integrasi storage uniqueness constraint dengan API.
        """
        # Pertama kali - berhasil
        response1 = client.post(
            '/api/shorten',
            data=json.dumps({
                'url': 'https://first.com',
                'custom_code': 'dupcd1'
            }),
            content_type='application/json'
        )
        assert response1.status_code == 201

        # Kedua kali dengan code sama - harus gagal
        response2 = client.post(
            '/api/shorten',
            data=json.dumps({
                'url': 'https://second.com',
                'custom_code': 'dupcd1'
            }),
            content_type='application/json'
        )
        assert response2.status_code == 400
        data = json.loads(response2.data)
        assert 'sudah digunakan' in data['error']

    def test_shorten_without_url_field_returns_400(self, client):
        """
        Integration Test 8: Request tanpa field 'url' harus return 400.
        Menguji: validasi request body di level endpoint.
        """
        response = client.post(
            '/api/shorten',
            data=json.dumps({}),
            content_type='application/json'
        )
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data
