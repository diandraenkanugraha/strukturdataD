# ============================================
# IMPLEMENTASI HASH TABLE DARI Nول (SCRATCH)
# ============================================

class HashTable:
    """Hash table dengan separate chaining"""
    
    def __init__(self, size=8):
        self.size = size
        self.buckets = [[] for _ in range(size)]
        self.count = 0
    
    def _hash(self, key):
        """Fungsi hash: sum(ord(char) * (i+1)) % size"""
        h = 0
        for i, ch in enumerate(str(key)):
            h += ord(ch) * (i + 1)
        return h % self.size
    
    def insert(self, key, value):
        """Masukkan key-value pair"""
        idx = self._hash(key)
        bucket = self.buckets[idx]
        
        # Cek apakah key sudah ada (update)
        for i, (k, v) in enumerate(bucket):
            if k == key:
                bucket[i] = (key, value)
                print(f"✓ Update '{key}' → '{value}' di bucket {idx}")
                return
        
        # Key baru, tambah ke bucket
        bucket.append((key, value))
        self.count += 1
        print(f"✓ Insert '{key}' → '{value}' di bucket {idx}")
        
        # Resize jika load factor > 0.7
        if self.load_factor() > 0.7:
            self._resize()
    
    def search(self, key):
        """Cari value berdasarkan key"""
        idx = self._hash(key)
        for k, v in self.buckets[idx]:
            if k == key:
                print(f"✓ Ditemukan '{key}' = '{v}' (bucket {idx})")
                return v
        print(f"✗ '{key}' tidak ditemukan")
        raise KeyError(key)
    
    def delete(self, key):
        """Hapus key-value pair"""
        idx = self._hash(key)
        original_len = len(self.buckets[idx])
        
        self.buckets[idx] = [
            (k, v) for k, v in self.buckets[idx]
            if k != key
        ]
        
        if len(self.buckets[idx]) < original_len:
            self.count -= 1
            print(f"✓ Hapus '{key}' dari bucket {idx}")
        else:
            print(f"✗ '{key}' tidak ada")
    
    def load_factor(self):
        """Menghitung beban tabel: count / size"""
        return self.count / self.size
    
    def _resize(self):
        """Resize tabel ke 2x lipat dan rehash semua elemen"""
        old_buckets = self.buckets
        self.size *= 2
        self.buckets = [[] for _ in range(self.size)]
        self.count = 0
        
        print(f"\n📊 Resize: dari {self.size//2} → {self.size} buckets")
        
        for bucket in old_buckets:
            for k, v in bucket:
                self.insert(k, v)
    
    def display(self):
        """Tampilkan isi hash table"""
        print(f"\n📋 Hash Table ({self.count}/{self.size})")
        print(f"Load Factor: {self.load_factor():.2f}")
        print("-" * 40)
        for i, bucket in enumerate(self.buckets):
            if bucket:
                items = ", ".join([f"({k}:{v})" for k, v in bucket])
                print(f"Bucket {i}: {items}")


# ============================================
# CONTOH PENGGUNAAN
# ============================================

print("=" * 50)
print("1. IMPLEMENTASI CUSTOM HASH TABLE")
print("=" * 50)

ht = HashTable(size=4)

print("\n--- Insert Data ---")
ht.insert("nama", "Alice")
ht.insert("umur", 25)
ht.insert("kota", "Jakarta")
ht.insert("negara", "Indonesia")

ht.display()

print("\n--- Search ---")
try:
    ht.search("nama")
    ht.search("umur")
    ht.search("hobi")  # Tidak ada
except KeyError:
    pass

print("\n--- Delete ---")
ht.delete("umur")
ht.delete("hobi")  # Tidak ada

ht.display()

# ============================================
# BUILT-IN: DICT (HASH TABLE PYTHON)
# ============================================

print("\n" + "=" * 50)
print("2. BUILT-IN: DICT (HASH TABLE)")
print("=" * 50)

# Dict adalah hash table yang dioptimasi
data = {"nama": "Bob", "umur": 30, "kota": "Bandung"}

print(f"\nDict: {data}")
print(f"Akses data['nama']: {data['nama']}")
print(f"'umur' in data: {'umur' in data}")

data["hobi"] = "Coding"  # Insert O(1)
del data["umur"]        # Delete O(1)

print(f"Setelah update: {data}")

# ============================================
# BUILT-IN: SET (HASH SET)
# ============================================

print("\n" + "=" * 50)
print("3. BUILT-IN: SET (HASH SET)")
print("=" * 50)

numbers = {1, 2, 3, 2, 1, 3}  # Duplikat otomatis dihapus
print(f"Set dari [1,2,3,2,1,3]: {numbers}")

numbers.add(4)
numbers.discard(2)
print(f"Setelah add(4) dan discard(2): {numbers}")

# Operasi set
a = {1, 2, 3}
b = {2, 3, 4}
print(f"\nUnion {a} ∪ {b}: {a | b}")
print(f"Intersection {a} ∩ {b}: {a & b}")
print(f"Difference {a} − {b}: {a - b}")

# ============================================
# KRIPTOGRAFI: HASHLIB
# ============================================

print("\n" + "=" * 50)
print("4. HASHLIB (CRYPTOGRAPHIC HASHING)")
print("=" * 50)

import hashlib

password = "rahasia123"

# MD5 (DEPRECATED untuk password!)
md5_hash = hashlib.md5(password.encode()).hexdigest()
print(f"\nPassword: {password}")
print(f"MD5:    {md5_hash}")

# SHA-256 (lebih aman)
sha256_hash = hashlib.sha256(password.encode()).hexdigest()
print(f"SHA256: {sha256_hash}")

# SHA-512 (lebih panjang)
sha512_hash = hashlib.sha512(password.encode()).hexdigest()
print(f"SHA512: {sha512_hash[:64]}...")  # Potong karena terlalu panjang

# Hashing file
print("\n--- Hashing File ---")
# Buat file dummy
with open("test.txt", "w") as f:
    f.write("Hello World!\nIni file contoh.")

# Hash file dengan streaming (efficient untuk file besar)
sha256_file = hashlib.sha256()
with open("test.txt", "rb") as f:
    for chunk in iter(lambda: f.read(4096), b""):
        sha256_file.update(chunk)

print(f"SHA256 of test.txt: {sha256_file.hexdigest()}")

# ============================================
# CUSTOM HASH: __hash__ & __eq__
# ============================================

print("\n" + "=" * 50)
print("5. CUSTOM HASH UNTUK CLASS")
print("=" * 50)

class Point:
    """Class point dengan custom hash"""
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def __hash__(self):
        return hash((self.x, self.y))
    
    def __eq__(self, other):
        return (self.x, self.y) == (other.x, other.y)
    
    def __repr__(self):
        return f"Point({self.x}, {self.y})"

# Sekarang Point bisa digunakan sebagai dict key
points = {
    Point(0, 0): "origin",
    Point(1, 1): "diagonal",
    Point(2, 3): "koordinat"
}

print(f"\nDict dengan Point sebagai key:")
for point, label in points.items():
    print(f"  {point} → {label}")

# Set of points
unique_points = {Point(0, 0), Point(1, 1), Point(0, 0)}
print(f"\nSet of Points: {unique_points}")

# ============================================
# PERBANDINGAN: HASH vs LINEAR SEARCH
# ============================================

print("\n" + "=" * 50)
print("6. PERBANDINGAN PERFORMA")
print("=" * 50)

import time

n = 10000
data_list = list(range(n))
data_dict = {i: i for i in range(n)}

# Linear search di list
start = time.perf_counter()
result = 9999 in data_list
linear_time = time.perf_counter() - start

# Hash search di dict
start = time.perf_counter()
result = 9999 in data_dict
hash_time = time.perf_counter() - start

print(f"\nCari elemen 9999 dari {n} data:")
print(f"  List (linear search):  {linear_time*1e6:.2f} μs")
print(f"  Dict (hash search):    {hash_time*1e6:.2f} μs")
print(f"  Speedup: {linear_time/hash_time:.0f}x lebih cepat!")

print("\n" + "=" * 50)