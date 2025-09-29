#Muhammad Zaki Fadilla
#237006034
#A

"""
Tugas Praktikum 4 – Hybrid Pipeline (Threads + Processes)
--------------------------------------------------------
Stage-1: threads loader (I/O-bound)  – baca path → queue
Stage-2: process pool (CPU-bound)    – proses isi file
Stage-3: agregasi                    – hitung kata total
Usage:
  python 4_Hybrid.py <jumlah_thread_loader> <jumlah_process_worker>
Contoh:
  python 4_Hybrid.py 4 4
"""

import statistics, os, time, random, string, multiprocessing, threading, queue, sys

# ---------- konfigurasi ----------
N_FILES      = 100        # total file dummy yang akan dibuat & diproses
FILE_SIZE    = 500_000    # bytes per file (±500 KB teks random)
DATA_DIR     = "dummy_files"
RESULT_QUEUE = multiprocessing.Queue()   # hasil dari process pool
BACKPRESSURE = 50                        # maxsize queue antara stage-1 & 2

# ---------- utilitas ----------
def generate_dummy_files():
    os.makedirs(DATA_DIR, exist_ok=True)
    for i in range(N_FILES):
        path = os.path.join(DATA_DIR, f"file_{i:03d}.txt")
        with open(path, "w", encoding="utf-8") as f:
            f.write(''.join(random.choices(string.ascii_letters + " \n", k=FILE_SIZE)))
    print(f"[INFO] {N_FILES} file dummy siap di {DATA_DIR}")

def count_words(text: str) -> int:
    """Dummy CPU work: hitung kata + sleep kecil agar CPU-bound terasa."""
    time.sleep(0.005)          # simulasi komputasi
    return len(text.split())

# ---------- stage-2 (CPU-bound) ----------
def worker_cpu(file_queue: multiprocessing.JoinableQueue):
    while True:
        item = file_queue.get()
        if item is None:                 # sentinel -> shutdown
            file_queue.task_done()
            break
        path, start_time = item
        with open(path, encoding="utf-8") as f:
            text = f.read()
        n_words = count_words(text)
        latency = time.perf_counter() - start_time
        RESULT_QUEUE.put((path, n_words, latency))
        file_queue.task_done()

# ---------- stage-1 (I/O-bound) ----------
def loader_thread(file_queue: multiprocessing.JoinableQueue, paths, tid):
    for path in paths:
        file_queue.put((path, time.perf_counter()))
    print(f"[LOADER-{tid}] selesai mengirim {len(paths)} path")

# ---------- pipeline hybrid ----------
def hybrid_pipeline(n_loader_threads, n_workers):
    generate_dummy_files()
    all_paths = [os.path.join(DATA_DIR, f) for f in sorted(os.listdir(DATA_DIR))]
    file_queue = multiprocessing.JoinableQueue(maxsize=BACKPRESSURE)

    # start process pool (stage-2)
    processes = [multiprocessing.Process(target=worker_cpu, args=(file_queue,)) for _ in range(n_workers)]
    for p in processes:
        p.start()

    # start loader threads (stage-1)
    chunk_size = (len(all_paths) + n_loader_threads - 1) // n_loader_threads
    loaders = []
    t0 = time.time()
    for i in range(n_loader_threads):
        chunk = all_paths[i*chunk_size : (i+1)*chunk_size]
        t = threading.Thread(target=loader_thread, args=(file_queue, chunk, i))
        t.start()
        loaders.append(t)

    # tunggu loader selesai
    for t in loaders: t.join()
    # tunggu queue kosong, lalu kirim sentinel
    file_queue.join()
    for _ in range(n_workers):
        file_queue.put(None)
    for p in processes:
        p.join()

    total_time = time.time() - t0

    # agregasi hasil
    total_words = 0
    latencies = []
    while not RESULT_QUEUE.empty():
        _, words, lat = RESULT_QUEUE.get()
        total_words += words
        latencies.append(lat)

    throughput = N_FILES / total_time
    avg_latency = statistics.mean(latencies)

    return total_time, throughput, avg_latency

# ---------- baseline single-process ----------
def baseline_single():
    generate_dummy_files()
    paths = [os.path.join(DATA_DIR, f) for f in sorted(os.listdir(DATA_DIR))]
    t0 = time.time()
    total_words = 0
    for path in paths:
        with open(path, encoding="utf-8") as f:
            total_words += count_words(f.read())
    total_time = time.time() - t0
    throughput = N_FILES / total_time
    return total_time, throughput

# ---------- main ----------
if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python 4_Hybrid.py <n_loader_threads> <n_cpu_workers>")
        sys.exit(1)

    n_loaders = int(sys.argv[1])
    n_workers = int(sys.argv[2])

    print("\n========== HYBRID PIPELINE ==========")
    t_pipe, thru_pipe, lat_pipe = hybrid_pipeline(n_loaders, n_workers)
    print(f"Threads Loader : {n_loaders}")
    print(f"CPU Workers    : {n_workers}")
    print(f"Total Waktu    : {t_pipe:.2f} s")
    print(f"Throughput     : {thru_pipe:.2f} file/s")
    print(f"Avg Latency    : {lat_pipe:.3f} s")

    print("\n========== BASELINE SINGLE ==========")
    t_base, thru_base = baseline_single()
    print(f"Total Waktu    : {t_base:.2f} s")
    print(f"Throughput     : {thru_base:.2f} file/s")
    print(f"Speed-up pipe  : {t_base/t_pipe:.2f}x")

    # ---------- tabel cepat ----------
    print("\nTabel Hasil")
    print(f"{'Threads Loader':<15} {'CPU Workers':<12} {'File':<6} {'Waktu (s)':<10} {'Throughput':<12} {'Avg Latency (s)':<15}")
    print("-" * 80)
    print(f"{n_loaders:<15} {n_workers:<12} {N_FILES:<6} {t_pipe:<10.2f} {thru_pipe:<12.2f} {lat_pipe:<15.3f}")