# Program Antrean Bengkel Supercar

antrean_bengkel = []

# Fungsi buat masukin mobil ke antrean (Enqueue)
def mobil_masuk(pelat, merek):
    mobil = f"{merek} (Pelat: {pelat})"
    antrean_bengkel.append(mobil)
    print(f"🏎️  {mobil} baru saja masuk antrean servis.")
    print("Status Antrean saat ini:", antrean_bengkel)
    print("-" * 40)

# (Dequeue)
def kerjakan_servis():
    if len(antrean_bengkel) == 0:
        print("🛠️  Bengkel lagi sepi, mekanik bisa istirahat sebentar!")
    else:
        mobil_diservis = antrean_bengkel.pop(0)
        print(f"🔧 Sedang mengerjakan servis untuk: {mobil_diservis}")
        print("Sisa Antrean:", antrean_bengkel)
    print("-" * 40)

# Cara Pakainya (Simulasi) 
print("=== SISTEM ANTREAN BENGKEL SUPERCAR ===")

mobil_masuk("B 1234 XYZ", "Ferrari 458 Italia")
mobil_masuk("D 999 PRO", "Porsche 911 GT3")
mobil_masuk("E 777 FAF", "Ferrari LaFerrari")

kerjakan_servis() 
kerjakan_servis() 
mobil_masuk("B 888 KUL", "Porsche Taycan") 
kerjakan_servis()