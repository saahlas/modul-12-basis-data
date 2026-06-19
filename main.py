import tkinter as tk
from siswa import open_siswa
from guru import open_guru
from jadwal import open_jadwal
from kelas import open_kelas
from mata_pelajaran import open_mapel


BG = "#1e1e2e"
BTN_BG = "#313244"
BTN_HOVER = "#45475a"
BTN_TEXT = "#cdd6f4"
TITLE_COLOR = "#cba6f7"
ACCENT = "#89b4fa"

def styled_button(parent, text, command):
    btn = tk.Button(
        parent, text=text, command=command,
        bg=BTN_BG, fg=BTN_TEXT,
        font=("Segoe UI", 11),
        width=28, height=2,
        relief="flat", cursor="hand2",
        activebackground=BTN_HOVER,
        activeforeground=BTN_TEXT,
        bd=0
    )
    return btn

def main():
    root = tk.Tk()
    root.title("Aplikasi Database Sekolah")
    root.geometry("420x480")
    root.resizable(False, False)
    root.configure(bg=BG)


    tk.Label(root, text="DATABASE SEKOLAH",
             font=("Segoe UI", 16, "bold"),
             bg=BG, fg=TITLE_COLOR).pack(pady=(30, 5))

    tk.Label(root, text="Sistem Manajemen Data Sekolah",
             font=("Segoe UI", 9),
             bg=BG, fg="#6c7086").pack(pady=(0, 20))

    # Divider
    tk.Frame(root, bg=ACCENT, height=1, width=300).pack(pady=(0, 20))


    buttons = [
        ("👤  Data Siswa", open_siswa),
        ("🧑‍🏫  Data Guru", open_guru),
        ("📅  Data Jadwal", open_jadwal),
        ("🏫  Data Kelas", open_kelas),
        ("📚  Data Mata Pelajaran", open_mapel),
    ]

    for text, cmd in buttons:
        btn = styled_button(root, text, cmd)
        btn.pack(pady=4)

    # Tombol keluar
    tk.Button(root, text="✕  Keluar",
              command=root.destroy,
              bg="#f38ba8", fg="#1e1e2e",
              font=("Segoe UI", 10, "bold"),
              width=28, height=1,
              relief="flat", cursor="hand2",
              activebackground="#eb6c8a",
              activeforeground="#1e1e2e",
              bd=0).pack(pady=(15, 0))

    root.mainloop()

if __name__ == "__main__":
    main()