import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import sqlite3
import random
import string
from datetime import datetime
import os
import ctypes
import sys

# Enable High DPI awareness for Windows 11
try:
    ctypes.windll.shcore.SetProcessDpiAwareness(2)
except Exception:
    try:
        ctypes.windll.user32.SetProcessDPIAware()
    except Exception:
        pass

class SecurePassDatabase:
    def __init__(self, db_name="securepass.db"):
        self.db_name = db_name
        self.init_db()

    def init_db(self):
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS passwords (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    label TEXT NOT NULL,
                    password TEXT NOT NULL,
                    date_created TEXT NOT NULL
                )
            ''')
            conn.commit()
            conn.close()
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Failed to initialize database: {e}")

    def save_password(self, label, password):
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            date_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            cursor.execute('''
                INSERT INTO passwords (label, password, date_created)
                VALUES (?, ?, ?)
            ''', (label, password, date_now))
            conn.commit()
            conn.close()
            return True
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Failed to save record: {e}")
            return False

    def fetch_all(self):
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM passwords ORDER BY id DESC")
            rows = cursor.fetchall()
            conn.close()
            return rows
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Failed to fetch records: {e}")
            return []

    def delete_record(self, record_id):
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            cursor.execute("DELETE FROM passwords WHERE id = ?", (record_id,))
            conn.commit()
            conn.close()
            return True
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Failed to delete record: {e}")
            return False

class SecurePassApp:
    def __init__(self, root):
        self.root = root
        self.root.title("SecurePass Manager")
        self.root.geometry("900x620")
        self.root.configure(bg="#1e1e2e")
        self.root.minsize(850, 580)
        self.root.resizable(True, True)

        # Set App Icon (Resolves default tkinter feather icon)
        try:
            if getattr(sys, 'frozen', False):
                base_path = sys._MEIPASS
            else:
                base_path = os.path.dirname(os.path.abspath(__file__))
            icon_path = os.path.join(base_path, 'icon.ico')
            if os.path.exists(icon_path):
                self.root.iconbitmap(default=icon_path)
        except Exception:
            pass

        self.db = SecurePassDatabase()

        # UI Styling
        self.bg_color = "#1e1e2e"
        self.fg_color = "#f8f8f2"
        self.accent_blue = "#6272a4"
        self.accent_green = "#50fa7b"
        self.accent_red = "#ff5555"
        self.accent_purple = "#bd93f9"
        self.entry_bg = "#282a36"

        self.setup_ui()
        self.load_history()

    def setup_ui(self):
        # Header
        header_frame = tk.Frame(self.root, bg=self.bg_color)
        header_frame.pack(fill="x", pady=20)
        
        tk.Label(header_frame, text="SECUREPASS MANAGER", 
                 font=("Segoe UI", 24, "bold"), bg=self.bg_color, fg=self.accent_purple).pack()
        tk.Label(header_frame, text="Advanced Password Management & Generator", 
                 font=("Segoe UI", 10), bg=self.bg_color, fg="#6272a4").pack()

        # Generator Section
        gen_frame = tk.Frame(self.root, bg=self.bg_color)
        gen_frame.pack(fill="x", padx=40, pady=10)
        gen_frame.columnconfigure(1, weight=1) # Allow entry to expand

        # Label for password field
        tk.Label(gen_frame, text="Password:", font=("Segoe UI", 10, "bold"), 
                 bg=self.bg_color, fg=self.fg_color).grid(row=0, column=0, sticky="w", pady=5)
        
        self.pass_entry = tk.Entry(gen_frame, font=("Consolas", 14), bg=self.entry_bg, 
                                   fg=self.accent_green, insertbackground="white", borderwidth=0)
        self.pass_entry.grid(row=0, column=1, padx=10, pady=5, sticky="ew")
        self.pass_entry.bind("<KeyRelease>", lambda e: self.check_password_strength())

        btn_gen = tk.Button(gen_frame, text="Generate Password", font=("Segoe UI", 9, "bold"),
                           bg="#44475a", fg=self.fg_color, activebackground=self.accent_blue,
                           activeforeground="white", relief="flat", padx=10, command=self.generate_password)
        btn_gen.grid(row=0, column=2, padx=5)

        btn_copy = tk.Button(gen_frame, text="Copy", font=("Segoe UI", 9, "bold"),
                            bg="#44475a", fg=self.fg_color, activebackground=self.accent_green,
                            activeforeground="black", relief="flat", padx=10, command=self.copy_to_clipboard)
        btn_copy.grid(row=0, column=3, padx=5)

        # Password strength indicator
        self.strength_label = tk.Label(gen_frame, text="", font=("Segoe UI", 9), bg=self.bg_color)
        self.strength_label.grid(row=1, column=1, sticky="w", padx=10, pady=(0, 5))

        # Label / Description Section
        label_frame = tk.Frame(self.root, bg=self.bg_color)
        label_frame.pack(fill="x", padx=40, pady=10)
        label_frame.columnconfigure(1, weight=1) # Allow entry to expand

        tk.Label(label_frame, text="Nama / Keterangan:", font=("Segoe UI", 10, "bold"), 
                 bg=self.bg_color, fg=self.fg_color).grid(row=0, column=0, sticky="w", pady=5)
        
        self.label_entry = tk.Entry(label_frame, font=("Segoe UI", 12), bg=self.entry_bg, 
                                    fg=self.fg_color, insertbackground="white", borderwidth=0)
        self.label_entry.grid(row=0, column=1, padx=10, pady=5, sticky="ew")

        btn_save = tk.Button(label_frame, text="Simpan", font=("Segoe UI", 10, "bold"),
                            bg=self.accent_purple, fg="white", activebackground="#a277e3",
                            activeforeground="white", relief="flat", padx=20, pady=2, command=self.save_record)
        btn_save.grid(row=0, column=2, padx=10)

        # Table Section (Treeview)
        table_frame = tk.Frame(self.root, bg=self.bg_color)
        table_frame.pack(fill="both", expand=True, padx=40, pady=20)

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", 
                        background=self.entry_bg, 
                        foreground=self.fg_color, 
                        rowheight=25, 
                        fieldbackground=self.entry_bg,
                        borderwidth=0)
        style.map("Treeview", background=[('selected', self.accent_blue)])
        style.configure("Treeview.Heading", 
                        background="#44475a", 
                        foreground="white", 
                        font=("Segoe UI", 10, "bold"),
                        relief="flat")

        self.tree = ttk.Treeview(table_frame, columns=("No", "Label", "Password", "Date"), show="headings", height=8)
        self.tree.heading("No", text="No")
        self.tree.heading("Label", text="Nama/Keterangan")
        self.tree.heading("Password", text="Password")
        self.tree.heading("Date", text="Tanggal Dibuat")

        self.tree.column("No", width=40, anchor="center")
        self.tree.column("Label", width=180, anchor="w")
        self.tree.column("Password", width=180, anchor="w")
        self.tree.column("Date", width=180, anchor="center")

        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Action Buttons below table
        actions_frame = tk.Frame(self.root, bg=self.bg_color)
        actions_frame.pack(fill="x", padx=40, pady=(0, 20))

        btn_delete = tk.Button(actions_frame, text="Hapus Terpilih", font=("Segoe UI", 9, "bold"),
                              bg=self.accent_red, fg="white", activebackground="#ff6e6e",
                              activeforeground="white", relief="flat", padx=10, command=self.delete_record)
        btn_delete.pack(side="left")

        btn_export = tk.Button(actions_frame, text="Print / Export TXT", font=("Segoe UI", 9, "bold"),
                              bg=self.accent_green, fg="#282a36", activebackground="#69ff94",
                              activeforeground="#282a36", relief="flat", padx=10, command=self.export_txt)
        btn_export.pack(side="right")



    def generate_password(self):
        chars = string.ascii_uppercase + string.ascii_lowercase + string.digits + "!@#$%^&*"
        # Ensure at least one of each type
        password = [
            random.choice(string.ascii_uppercase),
            random.choice(string.ascii_lowercase),
            random.choice(string.digits),
            random.choice("!@#$%^&*")
        ]
        # Fill the rest to 12 characters (8 more to ensure strong password)
        password += [random.choice(chars) for _ in range(8)]
        random.shuffle(password)
        final_password = "".join(password)
        
        self.pass_entry.delete(0, tk.END)
        self.pass_entry.insert(0, final_password)
        self.check_password_strength()

    def check_password_strength(self):
        pwd = self.pass_entry.get()
        if len(pwd) < 10:
            self.strength_label.config(text=f"Password belum mencapai 10 karakter (sekarang: {len(pwd)})", fg=self.accent_red)
        elif len(pwd) >= 16:
            self.strength_label.config(text=f"Password sangat kuat ({len(pwd)} karakter)", fg=self.accent_green)
        else:
            self.strength_label.config(text=f"Password kuat ({len(pwd)} karakter)", fg=self.accent_green)

    def copy_to_clipboard(self):
        pwd = self.pass_entry.get()
        if pwd:
            self.root.clipboard_clear()
            self.root.clipboard_append(pwd)
            messagebox.showinfo("Success", "Password copied to clipboard!")
        else:
            messagebox.showwarning("Warning", "Generate a password first.")

    def save_record(self):
        label = self.label_entry.get().strip()
        pwd = self.pass_entry.get().strip()

        if not label or not pwd:
            messagebox.showwarning("Warning", "Mohon isi keterangan dan password.")
            return

        if self.db.save_password(label, pwd):
            messagebox.showinfo("Success", f"Password for '{label}' saved successfully!")
            self.label_entry.delete(0, tk.END)
            self.pass_entry.delete(0, tk.END)
            self.load_history()

    def load_history(self):
        # Clear current tree
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Load from DB
        rows = self.db.fetch_all()
        for idx, row in enumerate(rows, 1):
            # row is (id, label, password, date)
            self.tree.insert("", "end", values=(idx, row[1], row[2], row[3]), tags=(row[0],))

    def delete_record(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Pilih baris yang ingin dihapus.")
            return

        confirm = messagebox.askyesno("Confirm", "Hapus data ini dari riwayat?")
        if confirm:
            for item in selected_item:
                record_id = self.tree.item(item, "tags")[0]
                if self.db.delete_record(record_id):
                    self.tree.delete(item)
            self.load_history() # Refresh numbers

    def export_txt(self):
        rows = self.db.fetch_all()
        if not rows:
            messagebox.showwarning("Warning", "Tidak ada data untuk diexport.")
            return

        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt")],
            title="Simpan Riwayat Password",
            initialfile="SecurePass_Riwayat.txt"
        )

        if not file_path:
            return

        try:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write("====================================================\n")
                f.write("      SecurePass Manager - Riwayat Password         \n")
                f.write("====================================================\n")
                f.write(f"Tanggal Export: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                
                header = f"{'No':<5} | {'Nama/Keterangan':<20} | {'Password':<15} | {'Tanggal Dibuat'}\n"
                f.write(header)
                f.write("-" * len(header) + "\n")
                
                for idx, row in enumerate(rows, 1):
                    f.write(f"{idx:<5} | {row[1]:<20} | {row[2]:<15} | {row[3]}\n")
                
                f.write("\n====================================================\n")
                f.write("      RAHASIA - Jangan bagikan file ini             \n")
                f.write("====================================================\n")
            
            messagebox.showinfo("Success", "Export TXT berhasil!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = SecurePassApp(root)
    root.mainloop()
