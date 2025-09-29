#Muhammad Zaki Fadilla
#237006034
#A

import threading, time, random, statistics

# ---------- konfigurasi ----------
N_FILES = 10
MIN_SEC = 0.5
MAX_SEC = 2.0

# ---------- fungsi ----------
def download_file(i: int, sec: float):
    """Simulasi unduh file ke-i selama sec detik."""
    time.sleep(sec)

# ---------- mode eksekusi ----------
def run_serial(jobs):
    """Menjalankan semua pekerjaan secara serial."""
    t0 = time.perf_counter()
    for i, sec in jobs:
        download_file(i, sec)
    return time.perf_counter() - t0

def run_threads(jobs):
    """Menjalankan semua pekerjaan secara threaded."""
    threads = []
    t0 = time.perf_counter()
    for i, sec in jobs:
        t = threading.Thread(target=download_file, args=(i, sec))
        threads.append(t)
        t.start()
    for t in threads:
        t.join()
    return time.perf_counter() - t0

# ---------- eksperimen ----------
def one_round() -> tuple[float, float]:
    """Satu putaran eksperimen, return (t_serial, t_threaded)."""
    jobs = [(i, random.uniform(MIN_SEC, MAX_SEC)) for i in range(N_FILES)]
    t_serial = run_serial(jobs)
    t_threaded = run_threads(jobs)
    return t_serial, t_threaded

# ---------- main ----------
if __name__ == "__main__":
    random.seed(42)                     # agar hasil bisa direproduksi
    rounds = 5                          # ulang 5 kali, ambil rata-rata
    serial_times, threaded_times = [], []

    for _ in range(rounds):
        ts, tt = one_round()
        serial_times.append(ts)
        threaded_times.append(tt)

    avg_serial = statistics.mean(serial_times)
    avg_threaded = statistics.mean(threaded_times)
    speedup = avg_serial / avg_threaded

    # ---------- tabel hasil ----------
    print("Tabel Hasil (rata-rata dari {} putaran)".format(rounds))
    print("--------------------------------------------------")
    print(f"{'Mode':<10} {'Jumlah File':<12} {'Waktu (s)':<10} {'Speedup':<8}")
    print("--------------------------------------------------")
    print(f"{'Serial':<10} {N_FILES:<12} {avg_serial:<10.2f} {'1.00':<8}")
    print(f"{'Threaded':<10} {N_FILES:<12} {avg_threaded:<10.2f} {speedup:<8.2f}")