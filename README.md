# URL Shortener — Final Project Software Testing

[![CI Pipeline](https://github.com/WilbertS19/url-shortener/actions/workflows/ci.yml/badge.svg)](https://github.com/WilbertS19/url-shortener/actions/workflows/ci.yml)
[![codecov](https://codecov.io/gh/WilbertS19/url-shortener/branch/main/graph/badge.svg)](https://codecov.io/gh/WilbertS19/url-shortener)
[![Python](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/)
[![Tests](https://img.shields.io/badge/tests-46%20passing-brightgreen.svg)]()
[![Coverage](https://img.shields.io/badge/coverage-90%25%2B-brightgreen.svg)]()

> Final Project untuk mata kuliah **Software Testing**. Aplikasi URL Shortener sederhana dengan REST API yang dilengkapi unit testing, integration testing, dan CI pipeline menggunakan GitHub Actions.

## Daftar Isi

1. [Deskripsi Aplikasi](#deskripsi-aplikasi)
2. [Fitur](#fitur)
3. [Arsitektur](#arsitektur)
4. [Teknologi](#teknologi)
5. [Cara Menjalankan Aplikasi](#cara-menjalankan-aplikasi)
6. [Cara Menjalankan Test](#cara-menjalankan-test)
7. [Strategi Pengujian](#strategi-pengujian)
8. [Test Coverage](#test-coverage)
9. [API Documentation](#api-documentation)
10. [CI/CD Pipeline](#cicd-pipeline)

## Deskripsi Aplikasi

URL Shortener adalah aplikasi web sederhana berbasis REST API yang berfungsi untuk mempersingkat URL panjang menjadi URL pendek. Aplikasi ini dibangun menggunakan Python + Flask dan menyimpan data ke dalam database SQLite.

Tujuan utama proyek ini adalah mendemonstrasikan praktik **software testing modern** yang mencakup:

- Unit testing untuk logika bisnis dan validasi.
- Integration testing untuk endpoint REST API.
- Test coverage measurement dengan target minimal 60%.
- Continuous Integration menggunakan GitHub Actions.

## Fitur

Aplikasi memiliki **3 fitur utama**:

1. **Mempersingkat URL** — Menerima URL panjang dan menghasilkan short code unik (random atau custom).
2. **Redirect** — Mengakses short URL akan otomatis redirect ke URL asli serta meng-increment counter klik.
3. **Statistik** — Menampilkan jumlah klik, URL asli, dan tanggal pembuatan untuk setiap short code.

Validasi input mencakup:

- Format URL (skema http/https, panjang maksimum, domain valid).
- Custom short code (panjang 3-20 karakter, alphanumeric + dash/underscore, tidak menggunakan reserved keyword).

## Arsitektur

Aplikasi mengikuti **layered architecture** dengan pemisahan tanggung jawab yang jelas:

```
┌─────────────────────────────────────────────────┐
│            Layer 1: API (Flask)                  │
│  app/main.py — endpoint, request/response        │
└─────────────────┬───────────────────────────────┘
                  │
┌─────────────────▼───────────────────────────────┐
│        Layer 2: Business Logic                   │
│  app/shortener.py — URLShortener,CodeGenerator   │
│  app/validator.py — URLValidator                 │
└─────────────────┬───────────────────────────────┘
                  │
┌─────────────────▼───────────────────────────────┐
│         Layer 3: Storage (SQLite)                │
│  app/storage.py — URLStorage                     │
└──────────────────────────────────────────────────┘
```

### Struktur Repository

```
url-shortener/
├── app/                          # Source code aplikasi
│   ├── __init__.py
│   ├── main.py                   # Flask app & API endpoints
│   ├── shortener.py              # Business logic (shortener, generator)
│   ├── validator.py              # Input validation
│   └── storage.py                # SQLite persistence layer
├── tests/                        # Test suite
│   ├── __init__.py
│   ├── test_validator.py         # 15 unit tests
│   ├── test_shortener.py         # 17 unit tests
│   ├── test_storage.py           # 6 unit tests
│   └── test_integration.py       # 8 integration tests
├── .github/
│   └── workflows/
│       └── ci.yml                # GitHub Actions CI pipeline
├── requirements.txt              # Python dependencies
├── pytest.ini                    # Pytest & coverage config
├── .gitignore
└── README.md
```

## Teknologi

| Komponen | Teknologi |
|----------|-----------|
| Bahasa | Python 3.10+ |
| Web Framework | Flask 3.0 |
| Database | SQLite (built-in) |
| Testing Framework | pytest 8.x |
| Coverage Tool | pytest-cov 5.x |
| CI/CD | GitHub Actions |

## Cara Menjalankan Aplikasi

### 1. Clone Repository

```bash
git clone https://github.com/WilbertS19/url-shortener.git
cd url-shortener
```

### 2. Setup Virtual Environment (opsional tapi disarankan)

```bash
python -m venv venv
# Linux/Mac
source venv/bin/activate
# Windows
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Jalankan Aplikasi

```bash
python -m app.main
```

Aplikasi akan berjalan di `http://localhost:5000`.

### 5. Mencoba Aplikasi

```bash
# Health check
curl http://localhost:5000/health

# Mempersingkat URL
curl -X POST http://localhost:5000/api/shorten \
  -H "Content-Type: application/json" \
  -d '{"url": "https://www.example.com/very/long/path"}'

# Mempersingkat dengan custom code
curl -X POST http://localhost:5000/api/shorten \
  -H "Content-Type: application/json" \
  -d '{"url": "https://google.com", "custom_code": "gogl"}'

# Akses short URL (akan redirect)
curl -L http://localhost:5000/gogl

# Lihat statistik
curl http://localhost:5000/api/stats/gogl
```

## Cara Menjalankan Test

### Menjalankan Seluruh Test Suite

```bash
pytest
```

### Menjalankan Test Tertentu

```bash
# Hanya unit test validator
pytest tests/test_validator.py

# Hanya integration test
pytest tests/test_integration.py

# Test tertentu berdasarkan nama
pytest -k "test_shorten_valid_url"
```

### Generate Coverage Report

```bash
# Laporan teks di terminal
pytest --cov=app --cov-report=term-missing

# Laporan HTML (buka htmlcov/index.html di browser)
pytest --cov=app --cov-report=html

# Laporan XML (untuk Codecov / CI tools)
pytest --cov=app --cov-report=xml
```

### Mode Verbose

```bash
pytest -v
```

## Strategi Pengujian

Strategi pengujian aplikasi ini menggunakan pendekatan **testing pyramid** dengan dua level utama:

### 1. Unit Testing (38 test cases)

Unit test berfokus pada pengujian individu **fungsi/method** secara terisolasi tanpa ketergantungan eksternal. Setiap modul diuji dengan dependency yang di-mock atau menggunakan in-memory database (`:memory:`).

| File | Jumlah Test | Yang Diuji |
|------|-------------|-----------|
| `test_validator.py` | 15 | Validasi URL & custom code (valid, invalid, edge cases) |
| `test_shortener.py` | 17 | CodeGenerator (random, hash) & URLShortener (shorten, resolve, stats) |
| `test_storage.py` | 6 | CRUD storage (save, get, exists, increment, delete) |

**Kategori pengujian** yang dicakup:
- **Happy path** — input valid, hasil sukses.
- **Edge cases** — input kosong, None, panjang ekstrem, karakter spesial.
- **Error handling** — exception harus di-raise dengan benar (ValueError, KeyError).
- **State transitions** — counter klik harus bertambah setelah resolve.

### 2. Integration Testing (8 test cases)

Integration test memverifikasi **interaksi end-to-end** antara endpoint API, layer business logic, dan layer storage. Test menggunakan Flask test client dengan in-memory SQLite database.

Skenario yang diuji:

| # | Skenario |
|---|----------|
| 1 | Health check endpoint tersedia |
| 2 | Full flow: POST `/api/shorten` → simpan ke DB → response valid |
| 3 | Custom code → akses short URL → redirect 302 ke URL asli |
| 4 | Error handling: URL invalid → response 400 |
| 5 | Click counter ter-update setelah multiple redirect |
| 6 | Short code tidak ditemukan → response 404 |
| 7 | Duplicate custom code → response 400 |
| 8 | Missing field `url` → response 400 |

## Test Coverage

Target coverage: **minimal 60%** (sesuai requirement proyek).
Coverage aktual: **>90%** untuk seluruh modul `app/`.

Coverage report dapat dilihat di:
- Terminal output saat menjalankan `pytest`.
- HTML report di folder `htmlcov/`.
- Codecov badge di atas README.

Konfigurasi coverage ada di file `pytest.ini` dengan opsi `--cov-fail-under=60` yang akan **menggagalkan CI** jika coverage di bawah 60%.

## API Documentation

### `GET /health`

Health check endpoint.

**Response:**
```json
{ "status": "ok" }
```

### `POST /api/shorten`

Mempersingkat URL.

**Request body:**
```json
{
  "url": "https://example.com/long/path",
  "custom_code": "mycode"
}
```

`custom_code` bersifat opsional. Jika tidak diberikan, sistem akan men-generate kode random 6 karakter.

**Response (201):**
```json
{
  "short_code": "mycode",
  "short_url": "http://localhost:5000/mycode",
  "original_url": "https://example.com/long/path"
}
```

**Response error (400):** body validasi gagal.

### `GET /<short_code>`

Redirect 302 ke URL asli dan meng-increment counter klik.

### `GET /api/stats/<short_code>`

Mendapatkan statistik short code.

**Response (200):**
```json
{
  "short_code": "mycode",
  "original_url": "https://example.com/long/path",
  "clicks": 5,
  "created_at": "2026-05-01T10:00:00"
}
```

## CI/CD Pipeline

CI dijalankan otomatis di GitHub Actions pada event:
- `push` ke branch `main`, `master`, atau `develop`.
- `pull_request` ke branch tersebut.

**Tahapan pipeline (file `.github/workflows/ci.yml`):**

1. **Checkout repository** — clone source code.
2. **Setup Python** — matrix testing pada Python 3.10, 3.11, 3.12.
3. **Install dependencies** — `pip install -r requirements.txt`.
4. **Build (compile check)** — `python -m compileall app/` untuk memastikan tidak ada syntax error.
5. **Run tests with coverage** — menjalankan `pytest` dengan coverage report.
6. **Upload coverage report** — sebagai artifact GitHub & ke Codecov.

Pipeline akan **gagal** jika:
- Ada test yang gagal.
- Coverage di bawah 60%.
- Ada syntax error di source code.

## Lisensi

Proyek ini dibuat untuk keperluan akademik mata kuliah Software Testing.

---

**Catatan**: Ganti `WilbertS19` pada link badge di bagian atas README dengan WilbertS19 GitHub Anda yang sebenarnya.
