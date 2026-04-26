import random
import time

# ============================================
# IMPLEMENTASI ALGORITMA SORTING
# ============================================

def selection_sort(arr):
    """Selection Sort - O(n²)"""
    arr = arr.copy()
    n = len(arr)
    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            if arr[j] < arr[min_idx]:
                min_idx = j
        arr[i], arr[min_idx] = arr[min_idx], arr[i]
    return arr

def insertion_sort(arr):
    """Insertion Sort - O(n²)"""
    arr = arr.copy()
    n = len(arr)
    for i in range(1, n):
        key = arr[i]
        j = i - 1
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
    return arr

def merge_sort(arr):
    """Merge Sort - O(n log n)"""
    arr = arr.copy()
    
    if len(arr) <= 1:
        return arr
    
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    
    return merge(left, right)

def merge(left, right):
    """Fungsi helper untuk merge sort"""
    result = []
    i = j = 0
    
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    
    result.extend(left[i:])
    result.extend(right[j:])
    return result

# ============================================
# FUNGSI BENCHMARKING
# ============================================

def benchmark_sorting(algorithm, data, num_runs=5):
    """
    Menjalankan benchmark untuk satu algoritma
    Mengembalikan waktu rata-rata dalam detik
    """
    times = []
    
    for run in range(num_runs):
        # Copy data agar setiap run menggunakan data yang sama
        test_data = data.copy()
        
        start_time = time.perf_counter()
        algorithm(test_data)
        end_time = time.perf_counter()
        
        elapsed = end_time - start_time
        times.append(elapsed)
        print(f"    Run {run + 1}: {elapsed:.6f} detik")
    
    avg_time = sum(times) / len(times)
    return avg_time, times

def run_benchmark():
    """Fungsi utama untuk menjalankan semua benchmark"""
    
    # Konfigurasi
    data_sizes = [100, 1000, 10000, 50000]
    num_runs = 5  # Jumlah pengulangan untuk rata-rata
    
    algorithms = [
        ("Selection Sort", selection_sort),
        ("Insertion Sort", insertion_sort),
        ("Merge Sort", merge_sort)
    ]
    
    # Storage untuk hasil
    results = {}
    
    print("=" * 70)
    print("SORTING BENCHMARKING")
    print("=" * 70)
    print(f"Jumlah pengulangan per test: {num_runs}")
    print(f"Ukuran data: {data_sizes}")
    print("=" * 70)
    
    for size in data_sizes:
        print(f"\n{'=' * 70}")
        print(f"DATA SIZE: {size:,} elemen")
        print(f"{'=' * 70}")
        
        # Generate random data
        random.seed(42)  # Untuk reproducibility
        data = [random.randint(0, 1000000) for _ in range(size)]
        
        results[size] = {}
        
        for algo_name, algo_func in algorithms:
            print(f"\n  [{algo_name}]")
            avg_time, times = benchmark_sorting(algo_func, data, num_runs)
            
            results[size][algo_name] = {
                'avg': avg_time,
                'times': times,
                'min': min(times),
                'max': max(times)
            }
            
            print(f"    >>> RATA-RATA: {avg_time:.6f} detik")
    
    return results

def print_summary(results):
    """Mencetak ringkasan hasil benchmark"""
    
    print("\n" + "=" * 80)
    print("RINGKASAN HASIL BENCHMARKING (WAKTU RATA-RATA DALAM DETIK)")
    print("=" * 80)
    
    algorithms = ["Selection Sort", "Insertion Sort", "Merge Sort"]
    data_sizes = [100, 1000, 10000, 50000]
    
    # Header
    header = f"{'Algoritma':<20}"
    for size in data_sizes:
        header += f"{size:>15,}"
    print(header)
    print("-" * 80)
    
    # Data
    for algo in algorithms:
        row = f"{algo:<20}"
        for size in data_sizes:
            avg = results[size][algo]['avg']
            row += f"{avg:>15.6f}"
        print(row)
    
    print("=" * 80)

def print_detailed_analysis(results):
    """Mencetak analisis detail per ukuran data"""
    
    print("\n" + "=" * 80)
    print("ANALISIS DETAIL PER UKURAN DATA")
    print("=" * 80)
    
    algorithms = ["Selection Sort", "Insertion Sort", "Merge Sort"]
    
    for size in [100, 1000, 10000, 50000]:
        print(f"\n--- Ukuran Data: {size:,} ---")
        
        times_dict = {}
        for algo in algorithms:
            times_dict[algo] = results[size][algo]['avg']
        
        # Urutkan dari tercepat
        sorted_times = sorted(times_dict.items(), key=lambda x: x[1])
        
        fastest = sorted_times[0]
        slowest = sorted_times[-1]
        ratio = slowest[1] / fastest[1] if fastest[1] > 0 else 0
        
        print(f"  Tercepat : {fastest[0]} ({fastest[1]:.6f} detik)")
        print(f"  Terlambat: {slowest[0]} ({slowest[1]:.6f} detik)")
        print(f"  Rasio kecepatan: {ratio:.1f}x lebih lambat")
        
        for algo, time_val in sorted_times:
            print(f"    - {algo}: {time_val:.6f} detik")

def calculate_speedup(results):
    """Menghitung speedup saat data size meningkat 10x"""
    
    print("\n" + "=" * 80)
    print("ANALISIS SPEEDUP (KETIKA DATA SIZE NAIK 10x)")
    print("=" * 80)
    
    comparisons = [(100, 1000), (1000, 10000), (10000, 50000)]
    algorithms = ["Selection Sort", "Insertion Sort", "Merge Sort"]
    
    for algo in algorithms:
        print(f"\n[{algo}]")
        for small, large in comparisons:
            small_time = results[small][algo]['avg']
            large_time = results[large][algo]['avg']
            
            if small_time > 0:
                ratio = large_time / small_time
                size_ratio = large / small
                print(f"  {small:,} -> {large:,}: {ratio:.1f}x lebih lama (size {size_ratio:.0f}x)")

# ============================================
# MAIN PROGRAM
# ============================================

if __name__ == "__main__":
    # Jalankan benchmark
    results = run_benchmark()
    
    # Cetak ringkasan
    print_summary(results)
    
    # Cetak analisis detail
    print_detailed_analysis(results)
    
    # Cetak analisis speedup
    calculate_speedup(results)