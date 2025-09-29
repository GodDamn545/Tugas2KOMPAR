#Muhammad Zaki Fadilla
#237006034
#A

import time, random, statistics
import threading, multiprocessing, concurrent.futures
import requests   # pip install requests

# ---------- IO-bound (Tugas 1) ----------
N_FILES = 10
MIN_SEC = 0.5
MAX_SEC = 2.0

def download_file(i: int, sec: float):
    time.sleep(sec)          # simulasi I/O

def jobs_io():
    return [(i, random.uniform(MIN_SEC, MAX_SEC)) for i in range(N_FILES)]

def io_serial():
    for i, sec in jobs_io(): download_file(i, sec)

def io_threads():
    jobs = jobs_io()
    threads = []
    for i, sec in jobs:
        t = threading.Thread(target=download_file, args=(i, sec))
        t.start(); threads.append(t)
    for t in threads: t.join()

def io_processes():
    # tiap proses kerjakan 1 job
    with multiprocessing.Pool(processes=N_FILES) as pool:
        pool.starmap(download_file, jobs_io())

# ---------- CPU-bound (Tugas 2) ----------
def heavy(n, iters=1_000_000):
    s = 0
    for i in range(iters):
        s += (i * n) % 7
    return s

DATA = list(range(1, 9))

def cpu_serial():
    for d in DATA: heavy(d)

def cpu_threads():
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as ex:
        ex.map(heavy, DATA)

def cpu_processes():
    with multiprocessing.Pool(processes=8) as pool:
        pool.map(heavy, DATA)

# ---------- timer ----------
def timed(func):
    t0 = time.perf_counter()
    func()
    return time.perf_counter() - t0

# ---------- main ----------
if __name__ == "__main__":
    random.seed(42)
    R = 5                                    # ulang 5 kali, ambil rata-rata
    print("Jenis Aplikasi | Serial (s) | Threads (s) | Processes (s) | Speedup Th | Speedup Pr")
    print("-" * 85)

    # IO-bound
    ts  = statistics.mean([timed(io_serial)   for _ in range(R)])
    tth = statistics.mean([timed(io_threads)  for _ in range(R)])
    tp  = statistics.mean([timed(io_processes) for _ in range(R)])
    print(f"IO-bound       | {ts:8.3f}   | {tth:9.3f}   | {tp:10.3f}  | {ts/tth:8.1f}x | {ts/tp:8.1f}x")

    # CPU-bound
    ts  = statistics.mean([timed(cpu_serial)   for _ in range(R)])
    tth = statistics.mean([timed(cpu_threads)  for _ in range(R)])
    tp  = statistics.mean([timed(cpu_processes) for _ in range(R)])
    print(f"CPU-bound      | {ts:8.3f}   | {tth:9.3f}   | {tp:10.3f}  | {ts/tth:8.1f}x | {ts/tp:8.1f}x")