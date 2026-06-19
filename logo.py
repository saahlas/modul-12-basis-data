import matplotlib.pyplot as plt

# Data harga
points = [12300, 16250]
labels = ['Harga Awal', 'Harga Terbaru']

# Membuat area grafik
plt.figure(figsize=(6, 5))

# Membuat grafik garis berwarna merah dengan titik lingkaran
plt.plot(labels, points, marker='o', color='red', linewidth=2, markersize=8)

# Menambahkan judul dan keterangan dokumen
plt.title('Grafik Kenaikan Harga Pertamax', fontsize=14, pad=15)
plt.ylabel('Harga (Rp per Liter)', fontsize=12)
plt.grid(axis='y', linestyle='--', alpha=0.7)

# Menampilkan angka nominal di atas setiap titik
for i, txt in enumerate(points):
    plt.annotate(f"Rp {txt:,}", (labels[i], points[i]), textcoords="offset points", 
                 xytext=(0,10), ha='center', weight='bold')

# Mengatur batas bawah dan atas sumbu Y agar grafik proporsional
plt.ylim(11000, 17500)
plt.tight_layout()

# MENAMPILKAN GRAFIK DI LAYAR HP/LAPTOP
plt.show()