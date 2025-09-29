#Muhammad Zaki Fadilla
#237006034
#A

import time
from concurrent.futures import ProcessPoolExecutor

def heavy(n, iters=10**6):
    s = 0
    for i in range(iters):
        s += (i * n) % 7
    return s

def run_serial():
    start = time.time()
    results = [heavy(n) for n in range(1, 9)]
    end = time.time()
    return end - start

def run_parallel(max_workers):
    start = time.time()
    with ProcessPoolExecutor(max_workers=max_workers) as ex:
        results = list(ex.map(heavy, range(1, 9)))
    end = time.time()
    return end - start

if __name__ == "__main__":
    # Jalankan serial
    t_serial = run_serial()

    # Jalankan paralel dengan 2, 4, 8 proses
    t_2 = run_parallel(2)
    t_4 = run_parallel(4)
    t_8 = run_parallel(8)

    # Hitung speedup dan efisiensi
    speedup_2 = t_serial / t_2
    speedup_4 = t_serial / t_4
    speedup_8 = t_serial / t_8

    eff_2 = speedup_2 / 2
    eff_4 = speedup_4 / 4
    eff_8 = speedup_8 / 8

    # Tampilkan hasil
    print(f"{'Proses':<6} {'Waktu (s)':<10} {'Speedup':<8} {'Efisiensi':<10}")
    print("-" * 40)
    print(f"{'1':<6} {t_serial:<10.4f} {'1.00':<8} {'1.00':<10}")
    print(f"{'2':<6} {t_2:<10.4f} {speedup_2:<8.2f} {eff_2:<10.2f}")
    print(f"{'4':<6} {t_4:<10.4f} {speedup_4:<8.2f} {eff_4:<10.2f}")
    print(f"{'8':<6} {t_8:<10.4f} {speedup_8:<8.2f} {eff_8:<10.2f}")