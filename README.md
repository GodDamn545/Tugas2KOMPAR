# Tugas2KOMPAR

# Tugas Praktikum Komputasi Paralel (KOMPAR)

Repo ini berisi solusi untuk Tugas Praktikum 1 hingga 4 mata kuliah Komputasi Paralel. Setiap tugas berfokus pada teknik paralelisme yang berbeda, baik itu *Threads*, *Processes*, maupun implementasi *Hybrid Pipeline*.

## 🚀 Panduan Eksekusi (Cara Run)

Pastikan Anda berada di direktori yang sama dengan semua berkas `.py` dan menggunakan **Python 3.8+**.

### 📊 Tugas 1: Thread Parallelism (I/O-Bound)

Tugas ini membandingkan eksekusi **Serial** vs. **Threaded** untuk pekerjaan I/O-Bound yang disimulasikan (`time.sleep`).

| File | Perintah Eksekusi | Keterangan |
| :--- | :--- | :--- |
| `1_ThreadParallelism.py` | `python 1_ThreadParallelism.py` | Menjalankan 5 putaran dan menampilkan perbandingan waktu dan *speedup*. |

### 🚀 Tugas 2: Task Parallelism (CPU-Bound)

Tugas ini menggunakan `ProcessPoolExecutor` untuk pekerjaan **CPU-Bound** (`heavy()`) dan membandingkan hasilnya pada berbagai jumlah *workers* (proses).

| Jumlah Worker (p) | Perintah Eksekusi (Implisit di dalam kode) |
| :--- | :--- |
| **p=1 (Serial)** | Dilakukan oleh fungsi `run_serial()` |
| **p=2** | Dilakukan oleh `run_parallel(2)` |
| **p=4** | Dilakukan oleh `run_parallel(4)` |
| **p=8** | Dilakukan oleh `run_parallel(8)` |

**Perintah Run:**

```bash
python 2_TaskParallelism_Bound.py
```

### 📊 Tugas 3: Perbandingan Threads vs. Processes

Tugas ini membandingkan secara langsung performa threads dan processes pada kedua jenis beban kerja (I/O dan CPU).

*Perintah Run**

```bash
python 3_TaskParallelism_IO.py
```

### 🚀 Tugas 4: Pipeline Hibrid

Tugas ini mengimplementasikan pipeline multi-tahap yang menggabungkan threads untuk I/O dan processes untuk pekerjaan CPU. Skrip ini menerima argumen dari command line.

*Cara Menjalankan:*

Jalankan dari terminal dengan format: python 4_Hybrid.py <jumlah_threads> <jumlah_proses>.

**Contoh Perintah Run 4 Thread 4 Proses**

```bash
python 4_Hybrid.py 4 4
```
```bash
python 4_Hybrid.py 1 1
```
