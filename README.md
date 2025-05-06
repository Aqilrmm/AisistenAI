# AI Jualin Indonesia

Proyek ini adalah Sales AI berbahasa Indonesia yang menggunakan Ollama sebagai backend LLM (Large Language Model). AI Assistant ini dirancang untuk melakukan penjualan dalam bahasa Indonesia, termasuk menawarkan produk, memberikan link penjualan, dan melakukan percakapan dengan customer.

## 📋 Daftar Isi
- [Fitur Utama](#fitur-utama)
- [Persyaratan Sistem](#persyaratan-sistem)
- [Instalasi](#instalasi)
- [Penggunaan](#penggunaan)
- [Struktur Proyek](#struktur-proyek)
- [Panduan File](#panduan-file)
- [Konfigurasi](#konfigurasi)
- [Menambahkan Tool Baru](#menambahkan-tool-baru)
- [Troubleshooting](#troubleshooting)
- [Lisensi](#lisensi)

## 🚀 Fitur Utama

- **Bahasa Indonesia Natural**: Berinteraksi dengan pengguna dalam bahasa Indonesia yang alami dan ramah
- **Tool Pencarian Produk**: 
  - Mencari Produk yang sesuai dengan apa yang di inginkan customer
- **Tool Membuat transaki**: 
  - Membuat transaksi berdasarkan produk yang di inginkan customer

## 💻 Persyaratan Sistem

- Python 3.8 atau lebih baru
- Ollama terpasang dan berjalan di sistem lokal
- Model Ollama qwen3:0.6b atau model lain yang kompatibel
- Minimal 4GB RAM (direkomendasikan 8GB)
- 1GB ruang disk kosong

## 📥 Instalasi

1. **Kloning repositori ini**
   ```bash
   git clone https://github.com/Aqilrmm/AisistenAI.git
   cd AsistenAI/aiv2
   ```

2. **Buat virtual environment Python** (opsional tapi direkomendasikan)
   ```bash
   python -m venv venv
   # Pada Windows
   venv\Scripts\activate
   # Pada macOS/Linux
   source venv/bin/activate
   ```

3. **Pasang dependensi**
   ```bash
   pip install -r requirements.txt
   ```

4. **Pastikan Ollama terpasang**
   - Download dan pasang dari [ollama.com](https://ollama.com)
   - Jalankan Ollama: `ollama serve`

5. **Download model qwen3:0.6b**
   ```bash
   ollama pull qwen3:0.6b
   ```

## 🎮 Penggunaan

1. **Jalankan aplikasi**
   Pastikan kamu berada di root aplikasi yaitu "AisistenAI", bukan di dalam aiv2 karena akan menjalankan aplikasi ini di sebagai module
      ```bash
   cd ../
   ```
   ```bash
   python3 -m aiv2.main
   ```

2. **Mulai berinteraksi dengan asisten**
   ```
   ===================================================
              🤖 AI Assistant Indonesia 🤖            
   ===================================================
   Ketik 'keluar' atau 'quit' untuk keluar.
   Tips: Gunakan bahasa Indonesia yang jelas untuk hasil terbaik.
   ===================================================

   Pertanyaan Anda: Siapakah Soekarno?
   
   Sedang memikirkan jawaban...
   ```

## 📁 Struktur Proyek

```
ai_assistant/
├── main.py                   # File utama untuk menjalankan aplikasi
├── config.py                 # Konfigurasi aplikasi
├── requirements.txt          # Daftar dependensi Python
├── dokumen.txt               # File contoh untuk DokumenQA
├── utils/
│   ├── __init__.py           # Init untuk package utils
│   ├── logging_setup.py      # Setup logging
│   └── document_processor.py # Fungsi untuk memproses dokumen
├── tools/
│   ├── __init__.py           # Init untuk package tools
│   ├── joke_fetcher.py       # Tools untuk konversi satuan
│   ├── datetime_tools.py     # Tools untuk waktu dan tanggal
│   └── dynamic_tool_loader.py # Loader tools dinamis
└── agent/
    ├── __init__.py           # Init untuk package agent
    ├── agent_factory.py      # Factory untuk membuat agent
    └── prompt_templates.py   # Template prompt untuk agent
```

## 📖 Panduan File

### File Utama

#### `main.py`
File utama untuk menjalankan aplikasi. Bertanggung jawab untuk:
- Menginisialisasi logging
- Memuat tools dan membuat agent
- Menjalankan loop interaktif untuk memproses input pengguna
- Menampilkan output dalam format yang rapi

```python
# Contoh penggunaan main.py
python main.py
```

#### `config.py`
File konfigurasi aplikasi yang berisi:
- URL dan model untuk Ollama
- Path untuk dokumen yang akan diproses
- Konfigurasi chunk untuk pemrosesan dokumen
- Level logging
- Konfigurasi LLM (temperature, streaming)
- Daftar tools yang diaktifkan
- Konfigurasi spesifik untuk setiap tool

```python
# Contoh konfigurasi melalui environment variables
OLLAMA_MODEL=llama3 CHUNK_SIZE=2000 python main.py
```

### Package `utils`

#### `utils/logging_setup.py`
Setup logging untuk aplikasi dengan format yang konsisten. Menggunakan level logging dari config.py.

#### `utils/document_processor.py`
Memproses dokumen teks untuk digunakan dengan retrieval QA:
- Memuat dokumen dari path yang dikonfigurasi
- Membagi dokumen menjadi chunk dengan overlap
- Membuat embeddings dengan Ollama
- Menghasilkan retriever untuk pencarian dokumen

### Package `tools`

#### `tools/joke_fetcher.py`
- `fetch_random_jokes()`: Fungsi untuk memberikan jokes random yang di ambil dari API
#### `tools/datetime_tools.py`
Berisi tools terkait waktu:
- `get_datetime()`: Mendapatkan waktu dan tanggal saat ini dalam format Indonesia

#### `tools/dynamic_tool_loader.py`
Sistem untuk memuat dan mengelola tools secara dinamis:
- `ToolRegistry`: Class untuk mendaftarkan dan mengelola tools
- `load_default_tools()`: Memuat semua tools default
- `get_enabled_tools()`: Mendapatkan tools yang diaktifkan dari konfigurasi

### Package `agent`

#### `agent/prompt_templates.py`
Berisi template prompt untuk agent:
- `PREFIX_TEMPLATE`: Template awal untuk instruksi agent
- `SUFFIX_TEMPLATE`: Template akhir dengan instruksi penggunaan tools

#### `agent/agent_factory.py`
Factory untuk membuat agent LangChain:
- `create_agent()`: Membuat dan mengkonfigurasi agent dengan tools yang dipilih

## ⚙️ Konfigurasi

Anda dapat mengonfigurasi aplikasi melalui variabel lingkungan atau mengedit file `config.py`. Berikut adalah variabel konfigurasi utama:

| Variabel | Deskripsi | Default |
|----------|-----------|---------|
| `OLLAMA_BASE_URL` | URL untuk server Ollama | http://127.0.0.1:11434 |
| `OLLAMA_MODEL` | Model Ollama yang digunakan | qwen3:0.6b |
| `DOCUMENT_PATH` | Path ke dokumen untuk DokumenQA | dokumen.txt |
| `CHUNK_SIZE` | Ukuran chunk untuk pemrosesan dokumen | 1000 |
| `CHUNK_OVERLAP` | Overlap antara chunk dokumen | 100 |
| `LOG_LEVEL` | Level logging | INFO |
| `LLM_TEMPERATURE` | Temperature untuk LLM (kreativitas) | 0.7 |
| `LLM_STREAMING` | Mengaktifkan streaming output | True |
| `ENABLED_TOOLS` | Daftar tools yang diaktifkan | "DateTime,JokeFetcher,DokumenQA" |

## 🔧 Menambahkan Tool Baru

Untuk menambahkan tool baru ke aplikasi:

1. **Buat File atau Fungsi Tool**
   
   Buat file baru di direktori `tools/` atau tambahkan fungsi ke file yang sudah ada:

   ```python
   # tools/my_new_tool.py
   import logging
   
   logger = logging.getLogger(__name__)
   
   def my_new_function(query: str) -> str:
       """
       Deskripsi fungsi tool baru
       """
       try:
           # Implementasi tool
           result = "Hasil dari tool baru"
           return result
       except Exception as e:
           logger.error(f"Error in my_new_function: {e}")
           return f"Terjadi kesalahan: {str(e)}"
   ```

2. **Daftarkan Tool di ToolRegistry**

   Edit `tools/dynamic_tool_loader.py` untuk mendaftarkan tool baru:

   ```python
   # Di dalam function load_default_tools()
   from .my_new_tool import my_new_function
   
   # Tambahkan registrasi berikut
   tool_registry.register_tool(
       name="MyNewTool",
       func=my_new_function,
       description="Deskripsi tentang cara menggunakan tool baru ini."
   )
   ```

3. **Aktifkan Tool di Konfigurasi**

   Edit `config.py` untuk mengaktifkan tool baru:

   ```python
   # Tambahkan tool baru ke daftar ENABLED_TOOLS
   ENABLED_TOOLS = os.environ.get("ENABLED_TOOLS", "DateTime,JokeFetcher,DokumenQA").split(",")
   ```


## 🔍 Troubleshooting

### Error Koneksi ke Ollama
```
Error creating agent: Could not connect to Ollama service at http://127.0.0.1:11434
```
**Solusi**: Pastikan Ollama sedang berjalan dengan perintah `ollama serve`

### Model Tidak Ditemukan
```
Error: model 'qwen3:0.6b' not found
```
**Solusi**: Download model dengan perintah `ollama pull qwen3:0.6b`

### Memory Error
```
MemoryError: Unable to allocate array
```
**Solusi**: Kurangi `CHUNK_SIZE` di `config.py` atau melalui variabel lingkungan

### Package Tidak Ditemukan
```
ModuleNotFoundError: No module named 'langchain'
```
**Solusi**: Pasang semua dependensi dengan `pip install -r requirements.txt`

### File Dokumen Tidak Ditemukan
```
Error loading documents: [Errno 2] No such file or directory: 'dokumen.txt'
```
**Solusi**: Buat file dokumen atau sesuaikan `DOCUMENT_PATH` di `config.py`

## 📄 Lisensi

MIT License

Copyright (c) 2025 AI Assistant Indonesia

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.