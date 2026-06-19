import tkinter as tk
from tkinter import ttk, messagebox
from koneksi import get_connection

# Tema
BG = "#1e1e2e"
BG2 = "#181825"
BTN_BG = "#313244"
BTN_HOVER = "#45475a"
FG = "#cdd6f4"
ACCENT = "#89b4fa"
SUCCESS = "#a6e3a1"
DANGER = "#f38ba8"
WARNING = "#f9e2af"
TITLE_COLOR = "#cba6f7"

def apply_treeview_style():
    style = ttk.Style()
    style.theme_use("clam")
    style.configure("Treeview",
                    background=BG2,
                    foreground=FG,
                    fieldbackground=BG2,
                    rowheight=28,
                    font=("Segoe UI", 10))
    style.configure("Treeview.Heading",
                    background=BTN_BG,
                    foreground=ACCENT,
                    font=("Segoe UI", 10, "bold"))
    style.map("Treeview", background=[("selected", "#45475a")])


def get_kelas_list():
    """Return list of (id_kelas, nama_kelas) for dropdown"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id_kelas, nama_kelas FROM kelas")
    data = cursor.fetchall()
    conn.close()
    return data


def open_siswa():
    window = tk.Toplevel()
    window.title("Data Siswa")
    window.geometry("750x480")
    window.configure(bg=BG)
    apply_treeview_style()

    tk.Label(window, text="DATA SISWA",
             font=("Segoe UI", 14, "bold"),
             bg=BG, fg=TITLE_COLOR).pack(pady=(20, 5))
    tk.Frame(window, bg=ACCENT, height=1).pack(fill="x", padx=20, pady=(0, 10))

    columns = ('NIS', 'Nama', 'JK', 'Tgl Lahir', 'Alamat', 'ID Kelas', 'Kelas')
    tree = ttk.Treeview(window, columns=columns, show='headings')

    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=95)

    tree.pack(fill='both', expand=True, padx=20)

    frame_btn = tk.Frame(window, bg=BG)
    frame_btn.pack(pady=15)

    btn_style = {"font": ("Segoe UI", 10), "relief": "flat",
                 "cursor": "hand2", "width": 12, "pady": 6}

    tk.Button(frame_btn, text="➕ Insert", bg=SUCCESS, fg=BG2,
              command=lambda: insert_siswa(load_data), **btn_style).grid(row=0, column=0, padx=6)
    tk.Button(frame_btn, text="✏️ Update", bg=WARNING, fg=BG2,
              command=lambda: update_siswa(tree, load_data), **btn_style).grid(row=0, column=1, padx=6)
    tk.Button(frame_btn, text="🗑️ Delete", bg=DANGER, fg=BG2,
              command=lambda: delete_siswa(tree, load_data), **btn_style).grid(row=0, column=2, padx=6)
    tk.Button(frame_btn, text="🔄 Refresh", bg=BTN_BG, fg=FG,
              command=lambda: load_data(), **btn_style).grid(row=0, column=3, padx=6)

    def load_data():
        for row in tree.get_children():
            tree.delete(row)
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT s.NIS, s.nama_siswa, s.jenis_kelamin,
                   s.tanggal_lahir, s.alamat, s.id_kelas, k.nama_kelas
            FROM siswa s
            JOIN kelas k ON s.id_kelas = k.id_kelas
        """)
        for row in cursor.fetchall():
            tree.insert('', 'end', values=row)
        conn.close()

    load_data()


def styled_form(title, height=450):
    form = tk.Toplevel()
    form.title(title)
    form.configure(bg=BG)
    form.geometry(f"360x{height}")
    form.resizable(True, True)

    tk.Label(form, text=title, font=("Segoe UI", 12, "bold"),
             bg=BG, fg=TITLE_COLOR).pack(pady=(15, 5))
    tk.Frame(form, bg=ACCENT, height=1).pack(fill="x", padx=20, pady=(0, 10))

    return form


def add_entry(form, label_text, default=""):
    tk.Label(form, text=label_text, font=("Segoe UI", 9),
             bg=BG, fg=FG).pack(anchor="w", padx=25)
    entry = tk.Entry(form, width=32, font=("Segoe UI", 10),
                      bg=BTN_BG, fg=FG, insertbackground=FG,
                      relief="flat")
    entry.pack(padx=25, pady=(2, 8), ipady=5)
    if default:
        entry.insert(0, str(default))
    return entry


def add_kelas_dropdown(form, default_id=None):
    """Returns (combobox, list_of_(id,nama))"""
    tk.Label(form, text="Kelas", font=("Segoe UI", 9),
             bg=BG, fg=FG).pack(anchor="w", padx=25)

    kelas_list = get_kelas_list()
    display_values = [f"{k_id} - {nama}" for k_id, nama in kelas_list]

    combo = ttk.Combobox(form, values=display_values,
                          font=("Segoe UI", 10), state="readonly", width=30)
    combo.pack(padx=25, pady=(2, 8), ipady=3)

    if default_id is not None:
        for i, (k_id, nama) in enumerate(kelas_list):
            if k_id == default_id:
                combo.current(i)
                break
    elif display_values:
        combo.current(0)

    return combo, kelas_list


def get_selected_id_kelas(combo):
    """Extract id_kelas from 'ID - Nama' format"""
    selected = combo.get()
    return int(selected.split(" - ")[0])


def insert_siswa(refresh):
    form = styled_form("Insert Siswa", height=560)

    e_nis = add_entry(form, "NIS")
    e_nama = add_entry(form, "Nama Siswa")
    e_jk = add_entry(form, "Jenis Kelamin (L/P)")
    e_tgl = add_entry(form, "Tanggal Lahir (YYYY-MM-DD)")
    e_alamat = add_entry(form, "Alamat")
    combo_kelas, _ = add_kelas_dropdown(form)

    def save():
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO siswa (NIS, nama_siswa, jenis_kelamin,
                                   tanggal_lahir, alamat, id_kelas)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (
                e_nis.get(), e_nama.get(), e_jk.get(),
                e_tgl.get(), e_alamat.get(),
                get_selected_id_kelas(combo_kelas)
            ))
            conn.commit()
            conn.close()
            messagebox.showinfo("Sukses", "Data siswa berhasil ditambahkan!")
            refresh()
            form.destroy()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    tk.Button(form, text="Simpan", bg=SUCCESS, fg=BG,
              font=("Segoe UI", 10, "bold"), relief="flat",
              cursor="hand2", width=15, pady=6,
              command=save).pack(pady=10)


def delete_siswa(tree, refresh):
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("Peringatan", "Pilih data siswa dulu!")
        return
    NIS = tree.item(selected[0])['values'][0]
    if messagebox.askyesno("Konfirmasi", f"Hapus siswa dengan NIS {NIS}?"):
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM siswa WHERE NIS = %s", (NIS,))
            conn.commit()
            conn.close()
            messagebox.showinfo("Sukses", "Data siswa berhasil dihapus!")
            refresh()
        except Exception as e:
            messagebox.showerror("Error", str(e))


def update_siswa(tree, refresh):
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("Peringatan", "Pilih data siswa dulu!")
        return

    values = tree.item(selected[0])['values']
    # values: NIS, Nama, JK, Tgl Lahir, Alamat, ID Kelas, Nama Kelas
    NIS, nama, jk, tgl, alamat, id_kelas, nama_kelas = values

    form = styled_form("Update Siswa", height=560)

    e_nama = add_entry(form, "Nama Siswa", nama)
    e_jk = add_entry(form, "Jenis Kelamin (L/P)", jk)
    e_tgl = add_entry(form, "Tanggal Lahir (YYYY-MM-DD)", tgl)
    e_alamat = add_entry(form, "Alamat", alamat)
    combo_kelas, _ = add_kelas_dropdown(form, default_id=id_kelas)

    def save():
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE siswa SET nama_siswa=%s, jenis_kelamin=%s,
                tanggal_lahir=%s, alamat=%s, id_kelas=%s
                WHERE NIS=%s
            """, (
                e_nama.get(), e_jk.get(), e_tgl.get(),
                e_alamat.get(), get_selected_id_kelas(combo_kelas),
                NIS
            ))
            conn.commit()
            conn.close()
            messagebox.showinfo("Sukses", "Data siswa berhasil diupdate!")
            refresh()
            form.destroy()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    tk.Button(form, text="Simpan", bg=WARNING, fg=BG,
              font=("Segoe UI", 10, "bold"), relief="flat",
              cursor="hand2", width=15, pady=6,
              command=save).pack(pady=10)