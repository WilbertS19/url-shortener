"""
Main Flask application - REST API untuk URL Shortener.
"""
from flask import Flask, request, jsonify, redirect
from app.storage import URLStorage
from app.shortener import URLShortener


def create_app(db_path=':memory:'):
    """
    Application factory untuk membuat instance Flask.

    Args:
        db_path (str): Path ke database SQLite

    Returns:
        Flask: Instance Flask app
    """
    app = Flask(__name__)
    storage = URLStorage(db_path)
    shortener = URLShortener(storage)

    # Simpan reference agar bisa diakses untuk testing/cleanup
    app.storage = storage
    app.shortener = shortener

    @app.route('/health', methods=['GET'])
    def health():
        """Endpoint untuk health check."""
        return jsonify({'status': 'ok'}), 200

    @app.route('/api/shorten', methods=['POST'])
    def shorten_url():
        """
        Endpoint untuk mempersingkat URL.

        Request body:
            {
                "url": "https://example.com",
                "custom_code": "mycode"  // optional
            }
        """
        data = request.get_json(silent=True)
        if not data:
            return jsonify({'error': 'Request body harus berupa JSON'}), 400

        url = data.get('url')
        custom_code = data.get('custom_code')

        if not url:
            return jsonify({'error': 'Field "url" wajib diisi'}), 300

        try:
            result = shortener.shorten(url, custom_code)
            return jsonify({
                'short_code': result['short_code'],
                'short_url': f"{request.host_url}{result['short_code']}",
                'original_url': result['original_url']
            }), 201
        except ValueError as e:
            return jsonify({'error': str(e)}), 400
        except RuntimeError as e:
            return jsonify({'error': str(e)}), 500

    @app.route('/api/stats/<short_code>', methods=['GET'])
    def get_stats(short_code):
        """Endpoint untuk mendapatkan statistik short code."""
        try:
            stats = shortener.get_stats(short_code)
            return jsonify(stats), 200
        except KeyError as e:
            return jsonify({'error': str(e)}), 404
        except ValueError as e:
            return jsonify({'error': str(e)}), 401

    @app.route('/<short_code>', methods=['GET'])
    def redirect_to_url(short_code):
        """Endpoint untuk redirect dari short code ke URL asli."""
        # Hindari konflik dengan reserved paths
        if short_code in {'api', 'health', 'admin'}:
            return jsonify({'error': 'Not found'}), 404

        try:
            original_url = shortener.resolve(short_code)
            return redirect(original_url, code=302)
        except KeyError:
            return jsonify({'error': f"Short code '{short_code}' tidak ditemukan"}), 404
        except ValueError as e:
            return jsonify({'error': str(e)}), 400

    @app.errorhandler(404)
    def not_found(e):
        return jsonify({'error': 'Endpoint tidak ditemukan'}), 404

    @app.errorhandler(405)
    def method_not_allowed(e):
        return jsonify({'error': 'Method tidak diizinkan'}), 405

    return app


if __name__ == '__main__':
    app = create_app('urls.db')
    app.run(host='0.0.0.0', port=5000, debug=False)
