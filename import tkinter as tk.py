import tkinter as tk
from tkinter import messagebox, ttk
import random
import json
import os

# Имя твоего файла истории (Пункт 5)
HISTORY_FILE = "history.json"

class QuoteApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Random Quote Generator")
        self.root.geometry("600x650")

        # 1. Список цитат (Пункт 1)
        self.quotes = [
            {"text": "Жизнь — это то, что происходит, пока вы строите планы.", "author": "Джон Леннон", "theme": "Жизнь"},
            {"text": "Успех — это идти от ошибки к ошибке без потери энтузиазма.", "author": "Уинстон Черчилль", "theme": "Успех"},
            {"text": "Сделай шаг, и дорога появится сама собой.", "author": "Стив Джобс", "theme": "Мотивация"},
            {"text": "Сложнее всего начать действовать.", "author": "Амелия Эрхарт", "theme": "Мотивация"},
            {"text": "Код работает быстрее, чем ты думаешь, если он чист.", "author": "Роберт Мартин", "theme": "IT"}
        ]

        # Загружаем историю из файла при старте
        self.history = self.load_history()

        self.setup_ui()

    def setup_ui(self):
        """Интерфейс приложения"""
        # Блок вывода цитаты
        self.quote_display = tk.Label(self.root, text="Нажмите кнопку для получения цитаты", 
                                      wraplength=500, font=("Arial", 14, "italic"), pady=30)
        self.quote_display.pack()

        self.author_display = tk.Label(self.root, text="", font=("Arial", 12, "bold"), fg="gray")
        self.author_display.pack()

        # Кнопка генерации (Пункт 2)
        self.gen_btn = tk.Button(self.root, text="СГЕНЕРИРОВАТЬ ЦИТАТУ", command=self.generate_quote,
                                 bg="#2196F3", fg="white", font=("Arial", 10, "bold"), padx=20, pady=10)
        self.gen_btn.pack(pady=20)

        # Блок фильтрации (Пункт 4)
        filter_frame = tk.LabelFrame(self.root, text=" Фильтры поиска ", padx=10, pady=10)
        filter_frame.pack(fill="x", padx=20, pady=10)

        tk.Label(filter_frame, text="Автор:").grid(row=0, column=0, sticky="w")
        self.auth_entry = tk.Entry(filter_frame)
        self.auth_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(filter_frame, text="Тема:").grid(row=0, column=2, sticky="w")
        self.theme_entry = tk.Entry(filter_frame)
        self.theme_entry.grid(row=0, column=3, padx=5, pady=5)

        # Блок истории (Пункт 3)
        tk.Label(self.root, text="История просмотров:").pack()
        self.history_list = tk.Listbox(self.root, width=70, height=10)
        self.history_list.pack(padx=20, pady=10)
        
        self.update_history_ui()

    def generate_quote(self):
        """Выбор цитаты с учетом фильтров и сохранение"""
        auth_f = self.auth_entry.get().strip().lower()
        theme_f = self.theme_entry.get().strip().lower()

        # Фильтрация
        filtered = [
            q for q in self.quotes 
            if (not auth_f or auth_f in q['author'].lower()) and 
               (not theme_f or theme_f in q['theme'].lower())
        ]

        if not filtered:
            messagebox.showwarning("Ничего не найдено", "Цитат с такими параметрами нет.")
            return

        selected = random.choice(filtered)

        # Показываем на экране
        self.quote_display.config(text=f"«{selected['text']}»")
        self.author_display.config(text=f"— {selected['author']} ({selected['theme']})")

        # Добавляем в историю (в начало списка)
        self.history.insert(0, selected)
        
        # Ограничим историю 50 записями, чтобы файл не рос бесконечно
        self.history = self.history[:50]
        
        self.save_history() # Пункт 5
        self.update_history_ui()

    def update_history_ui(self):
        """Обновление списка на экране"""
        self.history_list.delete(0, tk.END)
        for item in self.history:
            self.history_list.insert(tk.END, f" {item['author']}: {item['text'][:40]}...")

    def save_history(self):
        """Сохранение в JSON (Пункт 5)"""
        try:
            with open(HISTORY_FILE, "w", encoding="utf-8") as f:
                json.dump(self.history, f, ensure_ascii=False, indent=4)
        except Exception as e:
            print(f"Ошибка при сохранении: {e}")

    def load_history(self):
        """Загрузка из JSON (Пункт 5)"""
        if os.path.exists(HISTORY_FILE):
            try:
                with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                    return json.load(f)
            except:
                return [] # Если файл поврежден, возвращаем пустой список
        return []

if __name__ == "__main__":
    root = tk.Tk()
    app = QuoteApp(root)
    root.mainloop()
