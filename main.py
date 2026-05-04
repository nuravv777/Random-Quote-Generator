import tkinter as tk
from tkinter import ttk, messagebox
import random
import string
import json
import os
from datetime import datetime

class PasswordGeneratorApp:
    MIN_LEN = 4
    MAX_LEN = 32

    def __init__(self, root):
        self.root = root
        self.root.title("Random Password Generator")
        self.root.geometry("650x550")
        self.root.resizable(False, False)

        self.history_file = "password_history.json"
        self.history = self.load_history()

        self.setup_ui()

    def setup_ui(self):
        # --- Настройки ---
        settings_frame = ttk.Frame(self.root, padding="10")
        settings_frame.pack(fill=tk.X)

        # Ползунок длины
        ttk.Label(settings_frame, text="Длина пароля:").grid(row=0, column=0, sticky=tk.W, padx=5)
        self.length_var = tk.IntVar(value=12)
        self.length_slider = ttk.Scale(settings_frame, from_=self.MIN_LEN, to=self.MAX_LEN,
                                       variable=self.length_var, orient=tk.HORIZONTAL)
        self.length_slider.grid(row=0, column=1, padx=5, sticky=tk.EW)
        self.length_label = ttk.Label(settings_frame, textvariable=self.length_var)
        self.length_label.grid(row=0, column=2, padx=5)

        # Чекбоксы
        self.use_digits = tk.BooleanVar(value=True)
        self.use_letters = tk.BooleanVar(value=True)
        self.use_special = tk.BooleanVar(value=True)

        ttk.Checkbutton(settings_frame, text="Цифры (0-9)", variable=self.use_digits).grid(row=1, column=0, sticky=tk.W, pady=5)
        ttk.Checkbutton(settings_frame, text="Буквы (A-Z, a-z)", variable=self.use_letters).grid(row=1, column=1, sticky=tk.W, pady=5)
        ttk.Checkbutton(settings_frame, text="Спецсимволы (!@#$%)", variable=self.use_special).grid(row=1, column=2, sticky=tk.W, pady=5)

        # Кнопка генерации
        self.gen_btn = ttk.Button(settings_frame, text="Сгенерировать", command=self.generate_password)
        self.gen_btn.grid(row=2, column=0, columnspan=3, pady=10, sticky=tk.EW)

        # Поле результата
        self.result_var = tk.StringVar()
        self.result_entry = ttk.Entry(self.root, textvariable=self.result_var, font=("Courier", 14), justify=tk.CENTER)
        self.result_entry.pack(fill=tk.X, padx=15, pady=5)
        self.result_entry.config(state="readonly")

        # Копирование
        self.copy_btn = ttk.Button(self.root, text="📋 Копировать в буфер", command=self.copy_to_clipboard)
        self.copy_btn.pack(pady=5)

        # --- Таблица истории ---
        history_frame = ttk.LabelFrame(self.root, text="История генераций", padding="5")
        history_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        cols = ("time", "length", "password")
        self.tree = ttk.Treeview(history_frame, columns=cols, show="headings")
        self.tree.heading("time", text="Время")
        self.tree.heading("length", text="Длина")
        self.tree.heading("password", text="Пароль")
        self.tree.column("time", width=140)
        self.tree.column("length", width=50, anchor=tk.CENTER)
        self.tree.column("password", width=250)

        scrollbar = ttk.Scrollbar(history_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.update_history_table()

    def generate_password(self):
        length = self.length_var.get()

        # Валидация длины
        if length < self.MIN_LEN or length > self.MAX_LEN:
            messagebox.showwarning("Ошибка ввода", f"Длина пароля должна быть от {self.MIN_LEN} до {self.MAX_LEN}!")
            return

        # Формирование пула символов
        chars = ""
        if self.use_digits.get(): chars += string.digits
        if self.use_letters.get(): chars += string.ascii_letters
        if self.use_special.get(): chars += string.punctuation

        if not chars:
            messagebox.showwarning("Ошибка", "Выберите хотя бы один тип символов!")
            return

        # Генерация через random
        password = ''.join(random.choice(chars) for _ in range(length))
        self.result_var.set(password)
        self.result_entry.config(state="normal")
        self.result_entry.delete(0, tk.END)
        self.result_entry.insert(0, password)
        self.result_entry.config(state="readonly")

        # Сохранение в историю
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        entry = {"time": timestamp, "length": length, "password": password}
        self.history.append(entry)
        self.save_history()
        self.update_history_table()

    def load_history(self):
        if os.path.exists(self.history_file):
            try:
                with open(self.history_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            except (json.JSONDecodeError, Exception):
                return []
        return []

    def save_history(self):
        with open(self.history_file, "w", encoding="utf-8") as f:
            json.dump(self.history, f, ensure_ascii=False, indent=2)

    def update_history_table(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        # Новые записи сверху
        for entry in reversed(self.history):
            self.tree.insert("", tk.END, values=(entry["time"], entry["length"], entry["password"]))

    def copy_to_clipboard(self):
        pwd = self.result_var.get()
        if pwd:
            self.root.clipboard_clear()
            self.root.clipboard_append(pwd)
            self.root.update()
            messagebox.showinfo("Успех", "Пароль скопирован в буфер обмена!")

if __name__ == "__main__":
    root = tk.Tk()
    app = PasswordGeneratorApp(root)
    root.mainloop()
