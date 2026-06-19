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


def open_mapel():
    window = tk.Toplevel()
    window.title("Data Mata Pelajaran")
    window.geometry("500x400")
    window.configure(bg=BG)
    apply_treeview_style()

    tk.Label(window, text="DATA MATA PELAJARAN", font=("Segoe UI", 14, "bold"),
             bg=BG, fg=TITLE_COLOR).pack(pady=(20, 5))
    tk.Frame(window, bg=ACCENT, height=1).pack(fill="x", padx=20, pady=(0, 10))

    columns = ('ID Mapel', 'Nama Mapel', 'Jumlah Jam')
    tree = ttk.Treeview(window, columns=columns, show='headings')
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=140)
    tree.pack(fill='both', expand=True, padx=20)

    frame_btn = tk.Frame(window, bg=BG)
    frame_btn.pack(pady=15)
    btn_style = {"font": ("Segoe UI", 10), "relief": "flat",
                 "cursor": "hand2", "width": 12, "pady": 6}

    tk.Button(frame_btn, text="➕ Insert", bg=SUCCESS, fg=BG2,
              command=lambda: insert_mapel(load_data), **btn_style).grid(row=0, column=0, padx=6)
    tk.Button(frame_btn, text="✏️ Update", bg=WARNING, fg=BG2,
              command=lambda: update_mapel(tree, load_data), **btn_style).grid(row=0, column=1, padx=6)
    tk.Button(frame_btn, text="🗑️ Delete", bg=DANGER, fg=BG2,
              command=lambda: delete_mapel(tree, load_data), **btn_style).grid(row=0, column=2, padx=6)
    tk.Button(frame_btn, text="🔄 Refresh", bg=BTN_BG, fg=FG,
              command=lambda: load_data(), **btn_style).grid(row=0, column=3, padx=6)

    def load_data():
        for row in tree.get_children():
            tree.delete(row)
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM mata_pelajaran")
        for row in cursor.fetchall():
            tree.insert('', 'end', values=row)
        conn.close()

    load_data()


def styled_form(title, height=350):
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
                      bg=BTN_BG, fg=FG, insertbackground=FG, relief="flat")
    entry.pack(padx=25, pady=(2, 8), ipady=5)
    if default:
        entry.insert(0, str(default))
    return entry


def insert_mapel(refresh):
    form = styled_form("Insert Mata Pelajaran")

    e_nama = add_entry(form, "Nama Mapel")
    e_jam = add_entry(form, "Jumlah Jam")

    def save():
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO mata_pelajaran (nama_mapel, jumlah_jam)
                VALUES (%s, %s)
            """, (e_nama.get(), e_jam.get()))
            conn.commit()
            conn.close()
            messagebox.showinfo("Sukses", "Data mapel berhasil ditambahkan!")
            refresh()
            form.destroy()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    tk.Button(form, text="Simpan", bg=SUCCESS, fg=BG,
              font=("Segoe UI", 10, "bold"), relief="flat",
              cursor="hand2", width=15, pady=6, command=save).pack(pady=10)


def delete_mapel(tree, refresh):
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("Peringatan", "Pilih data mapel dulu!")
        return
    id_mapel = tree.item(selected[0])['values'][0]
    if messagebox.askyesno("Konfirmasi", f"Hapus mapel ID {id_mapel}?"):
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM mata_pelajaran WHERE id_mapel = %s", (id_mapel,))
            conn.commit()
            conn.close()
            messagebox.showinfo("Sukses", "Data mapel berhasil dihapus!")
            refresh()
        except Exception as e:
            messagebox.showerror("Error", str(e))


def update_mapel(tree, refresh):
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("Peringatan", "Pilih data mapel dulu!")
        return

    values = tree.item(selected[0])['values']
    id_mapel, nama, jam = values

    form = styled_form("Update Mata Pelajaran")

    e_nama = add_entry(form, "Nama Mapel", nama)
    e_jam = add_entry(form, "Jumlah Jam", jam)

    def save():
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE mata_pelajaran SET nama_mapel=%s, jumlah_jam=%s
                WHERE id_mapel=%s
            """, (e_nama.get(), e_jam.get(), id_mapel))
            conn.commit()
            conn.close()
            messagebox.showinfo("Sukses", "Data mapel berhasil diupdate!")
            refresh()
            form.destroy()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    tk.Button(form, text="Simpan", bg=WARNING, fg=BG,
              font=("Segoe UI", 10, "bold"), relief="flat",
              cursor="hand2", width=15, pady=6, command=save).pack(pady=10)