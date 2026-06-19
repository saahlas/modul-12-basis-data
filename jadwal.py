import tkinter as tk
from tkinter import ttk, messagebox
from koneksi import get_connection

BG = "#1e1e2e"
BG2 = "#181825"
BTN_BG = "#313244"
FG = "#cdd6f4"
ACCENT = "#89b4fa"
SUCCESS = "#a6e3a1"
DANGER = "#f38ba8"
WARNING = "#f9e2af"
TITLE_COLOR = "#cba6f7"

def apply_treeview_style():
    style = ttk.Style()
    style.theme_use("clam")
    style.configure("Treeview", background=BG2, foreground=FG,
                    fieldbackground=BG2, rowheight=28, font=("Segoe UI", 10))
    style.configure("Treeview.Heading", background=BTN_BG, foreground=ACCENT,
                    font=("Segoe UI", 10, "bold"))
    style.map("Treeview", background=[("selected", "#45475a")])


def get_list(table, id_col, nama_col):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(f"SELECT {id_col}, {nama_col} FROM {table}")
    data = cursor.fetchall()
    conn.close()
    return data


def open_jadwal():
    window = tk.Toplevel()
    window.title("Data Jadwal")
    window.geometry("800x420")
    window.configure(bg=BG)
    apply_treeview_style()

    tk.Label(window, text="DATA JADWAL", font=("Segoe UI", 14, "bold"),
             bg=BG, fg=TITLE_COLOR).pack(pady=(20, 5))
    tk.Frame(window, bg=ACCENT, height=1).pack(fill="x", padx=20, pady=(0, 10))

    columns = ('ID', 'Hari', 'Jam Mulai', 'Jam Selesai', 'Guru', 'Kelas', 'Mapel')
    tree = ttk.Treeview(window, columns=columns, show='headings')
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=100)
    tree.pack(fill='both', expand=True, padx=20)

    frame_btn = tk.Frame(window, bg=BG)
    frame_btn.pack(pady=15)
    btn_style = {"font": ("Segoe UI", 10), "relief": "flat",
                 "cursor": "hand2", "width": 12, "pady": 6}

    tk.Button(frame_btn, text="➕ Insert", bg=SUCCESS, fg=BG2,
              command=lambda: insert_jadwal(load_data), **btn_style).grid(row=0, column=0, padx=6)
    tk.Button(frame_btn, text="✏️ Update", bg=WARNING, fg=BG2,
              command=lambda: update_jadwal(tree, load_data), **btn_style).grid(row=0, column=1, padx=6)
    tk.Button(frame_btn, text="🗑️ Delete", bg=DANGER, fg=BG2,
              command=lambda: delete_jadwal(tree, load_data), **btn_style).grid(row=0, column=2, padx=6)
    tk.Button(frame_btn, text="🔄 Refresh", bg=BTN_BG, fg=FG,
              command=lambda: load_data(), **btn_style).grid(row=0, column=3, padx=6)

    def load_data():
        for row in tree.get_children():
            tree.delete(row)
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT j.id_jadwal, j.hari, j.jam_mulai, j.jam_selesai,
                   g.nama_guru, k.nama_kelas, m.nama_mapel
            FROM jadwal j
            JOIN guru g ON j.NIP = g.NIP
            JOIN kelas k ON j.id_kelas = k.id_kelas
            JOIN mata_pelajaran m ON j.id_mapel = m.id_mapel
        """)
        for row in cursor.fetchall():
            tree.insert('', 'end', values=row)
        conn.close()
    load_data()


def styled_form(title, height=520):
    form = tk.Toplevel()
    form.title(title)
    form.configure(bg=BG)
    form.geometry(f"380x{height}")
    form.resizable(True, True)
    tk.Label(form, text=title, font=("Segoe UI", 12, "bold"),
             bg=BG, fg=TITLE_COLOR).pack(pady=(15, 5))
    tk.Frame(form, bg=ACCENT, height=1).pack(fill="x", padx=20, pady=(0, 10))
    return form


def add_entry(form, label_text, default=""):
    tk.Label(form, text=label_text, font=("Segoe UI", 9),
             bg=BG, fg=FG).pack(anchor="w", padx=25)
    entry = tk.Entry(form, width=34, font=("Segoe UI", 10),
                      bg=BTN_BG, fg=FG, insertbackground=FG, relief="flat")
    entry.pack(padx=25, pady=(2, 8), ipady=5)
    if default:
        entry.insert(0, str(default))
    return entry


def add_hari_dropdown(form, default=None):
    tk.Label(form, text="Hari", font=("Segoe UI", 9),
             bg=BG, fg=FG).pack(anchor="w", padx=25)
    hari_list = ['Senin', 'Selasa', 'Rabu', 'Kamis', 'Jumat']
    combo = ttk.Combobox(form, values=hari_list, font=("Segoe UI", 10),
                          state="readonly", width=32)
    combo.pack(padx=25, pady=(2, 8), ipady=3)
    if default and default in hari_list:
        combo.current(hari_list.index(default))
    else:
        combo.current(0)
    return combo


def add_dropdown(form, label_text, data_list, default_id=None):
    """data_list: list of (id, nama). Returns combobox."""
    tk.Label(form, text=label_text, font=("Segoe UI", 9),
             bg=BG, fg=FG).pack(anchor="w", padx=25)
    display = [f"{i} - {n}" for i, n in data_list]
    combo = ttk.Combobox(form, values=display, font=("Segoe UI", 10),
                          state="readonly", width=32)
    combo.pack(padx=25, pady=(2, 8), ipady=3)

    if default_id is not None:
        for idx, (i, n) in enumerate(data_list):
            if i == default_id:
                combo.current(idx)
                break
    elif display:
        combo.current(0)
    return combo


def get_id(combo):
    return combo.get().split(" - ")[0]


def insert_jadwal(refresh):
    guru_list = get_list("guru", "NIP", "nama_guru")
    kelas_list = get_list("kelas", "id_kelas", "nama_kelas")
    mapel_list = get_list("mata_pelajaran", "id_mapel", "nama_mapel")

    form = styled_form("Insert Jadwal")

    combo_hari = add_hari_dropdown(form)
    e_mulai = add_entry(form, "Jam Mulai (HH:MM:SS)")
    e_selesai = add_entry(form, "Jam Selesai (HH:MM:SS)")
    combo_guru = add_dropdown(form, "Guru", guru_list)
    combo_kelas = add_dropdown(form, "Kelas", kelas_list)
    combo_mapel = add_dropdown(form, "Mata Pelajaran", mapel_list)

    def save():
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO jadwal (hari, jam_mulai, jam_selesai, NIP, id_kelas, id_mapel)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (
                combo_hari.get(), e_mulai.get(), e_selesai.get(),
                get_id(combo_guru), get_id(combo_kelas), get_id(combo_mapel)
            ))
            conn.commit()
            conn.close()
            messagebox.showinfo("Sukses", "Data jadwal berhasil ditambahkan!")
            refresh()
            form.destroy()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    tk.Button(form, text="Simpan", bg=SUCCESS, fg=BG,
              font=("Segoe UI", 10, "bold"), relief="flat",
              cursor="hand2", width=15, pady=6, command=save).pack(pady=10)


def delete_jadwal(tree, refresh):
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("Peringatan", "Pilih data jadwal dulu!")
        return
    id_jadwal = tree.item(selected[0])['values'][0]
    if messagebox.askyesno("Konfirmasi", f"Hapus jadwal ID {id_jadwal}?"):
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM jadwal WHERE id_jadwal = %s", (id_jadwal,))
            conn.commit()
            conn.close()
            messagebox.showinfo("Sukses", "Data jadwal berhasil dihapus!")
            refresh()
        except Exception as e:
            messagebox.showerror("Error", str(e))


def update_jadwal(tree, refresh):
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("Peringatan", "Pilih data jadwal dulu!")
        return

    values = tree.item(selected[0])['values']
    id_jadwal, hari, jam_mulai, jam_selesai, nama_guru, nama_kelas, nama_mapel = values

    guru_list = get_list("guru", "NIP", "nama_guru")
    kelas_list = get_list("kelas", "id_kelas", "nama_kelas")
    mapel_list = get_list("mata_pelajaran", "id_mapel", "nama_mapel")

    nip_default = next((i for i, n in guru_list if n == nama_guru), None)
    kelas_default = next((i for i, n in kelas_list if n == nama_kelas), None)
    mapel_default = next((i for i, n in mapel_list if n == nama_mapel), None)

    form = styled_form("Update Jadwal")

    combo_hari = add_hari_dropdown(form, hari)
    e_mulai = add_entry(form, "Jam Mulai (HH:MM:SS)", jam_mulai)
    e_selesai = add_entry(form, "Jam Selesai (HH:MM:SS)", jam_selesai)
    combo_guru = add_dropdown(form, "Guru", guru_list, nip_default)
    combo_kelas = add_dropdown(form, "Kelas", kelas_list, kelas_default)
    combo_mapel = add_dropdown(form, "Mata Pelajaran", mapel_list, mapel_default)

    def save():
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE jadwal SET hari=%s, jam_mulai=%s, jam_selesai=%s,
                NIP=%s, id_kelas=%s, id_mapel=%s
                WHERE id_jadwal=%s
            """, (
                combo_hari.get(), e_mulai.get(), e_selesai.get(),
                get_id(combo_guru), get_id(combo_kelas), get_id(combo_mapel),
                id_jadwal
            ))
            conn.commit()
            conn.close()
            messagebox.showinfo("Sukses", "Data jadwal berhasil diupdate!")
            refresh()
            form.destroy()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    tk.Button(form, text="Simpan", bg=WARNING, fg=BG,
              font=("Segoe UI", 10, "bold"), relief="flat",
              cursor="hand2", width=15, pady=6, command=save).pack(pady=10)