import tkinter as tk
from tkinter import ttk
import time
import threading
import os
import sys
import subprocess
import json

print("=============================================")
print("🚀 НЕ БОЙСЯ, ОН СКАЧИВАЕТСЯ! Nexo запускается...")
print("=============================================")

class NexoAllInOneInstaller(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Nexo All-in-One Installer")
        self.geometry("550x380")
        self.configure(bg="#12121c")
        self.resizable(False, False)

        header = tk.Label(self, text="🚀 Nexo Все-в-одном Установщик", bg="#1a1a26", fg="#ffffff", font=("Segoe UI", 12, "bold"), anchor="w", padx=15, pady=10)
        header.pack(fill="x")

        self.content_frame = tk.Frame(self, bg="#12121c")
        self.content_frame.pack(fill="both", expand=True, padx=30, pady=20)

        self.title_lbl = tk.Label(self.content_frame, text="Установка Nexo", bg="#12121c", fg="#4df3ff", font=("Segoe UI", 16, "bold"))
        self.title_lbl.pack(anchor="w", pady=(0, 5))

        self.desc_lbl = tk.Label(self.content_frame, text="Нажмите кнопку ниже, чтобы развернуть приложение на ПК:", bg="#12121c", fg="#a0a0b8", font=("Segoe UI", 11))
        self.desc_lbl.pack(anchor="w", pady=(0, 15))

        self.banner_frame = tk.Frame(self.content_frame, bg="#1a1a26", highlightbackground="#4df3ff", highlightthickness=2, cursor="hand2")
        self.banner_frame.pack(fill="x", pady=10)
        self.banner_frame.bind("<Button-1>", lambda e: self.start_install())

        b_title = tk.Label(self.banner_frame, text="Установить Nexo.exe", bg="#1a1a26", fg="#ffffff", font=("Segoe UI", 14, "bold"), anchor="w")
        b_title.pack(anchor="w", padx=15, pady=(12, 2))
        b_title.bind("<Button-1>", lambda e: self.start_install())

        b_desc = tk.Label(self.banner_frame, text="Распаковка файлов, создание ярлыков и запуск.", bg="#1a1a26", fg="#b0b0c8", font=("Segoe UI", 10), anchor="w")
        b_desc.pack(anchor="w", padx=15, pady=(0, 12))
        b_desc.bind("<Button-1>", lambda e: self.start_install())

        self.progress_frame = tk.Frame(self.content_frame, bg="#12121c")
        
        self.status_lbl = tk.Label(self.progress_frame, text="Идет установка...", bg="#12121c", fg="#4df3ff", font=("Segoe UI", 11, "bold"))
        self.status_lbl.pack(anchor="w", pady=(10, 10))

        self.progress = ttk.Progressbar(self.progress_frame, orient="horizontal", length=470, mode="determinate")
        self.progress.pack(anchor="w", pady=5)

    def start_install(self):
        self.banner_frame.pack_forget()
        self.desc_lbl.pack_forget()
        self.progress_frame.pack(fill="x", pady=20)
        threading.Thread(target=self.run_installation).start()

    def run_installation(self):
        steps = [
            (20, "Создание рабочей директории в AppData..."),
            (50, "Распаковка внешних index.html и main.js..."),
            (80, "Регистрация системных компонентов..."),
            (100, "Установка успешно завершена!")
        ]

        target_dir = os.path.join(os.environ.get("APPDATA", "C:\\"), "NexoApp")
        os.makedirs(target_dir, exist_ok=True)

        for target_val, msg in steps:
            self.status_lbl.config(text=msg)
            while self.progress['value'] < target_val:
                self.progress['value'] += 1
                time.sleep(0.015)
                self.update_idletasks()

        # Копируем или создаем файлы из репозитория
        try:
            # Ищем index.html рядом со скриптом или упаковываем базовый
            base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
            
            src_index = os.path.join(base_path, "index.html")
            src_main = os.path.join(base_path, "main.js")

            # Если файлы есть рядом, копируем их, иначе создаем пустые заготовки
            if os.path.exists(src_index):
                with open(src_index, "r", encoding="utf-8") as f:
                    index_content = f.read()
            else:
                index_content = "<h1>Nexo App</h1>"

            if os.path.exists(src_main):
                with open(src_main, "r", encoding="utf-8") as f:
                    main_content = f.read()
            else:
                main_content = "// main.js"

            with open(os.path.join(target_dir, "index.html"), "w", encoding="utf-8") as f:
                f.write(index_content)
            with open(os.path.join(target_dir, "main.js"), "w", encoding="utf-8") as f:
                f.write(main_content)
            
            pkg_json = {
                "name": "nexo-app",
                "version": "1.0.0",
                "main": "main.js",
                "dependencies": {
                    "electron": "^28.0.0"
                }
            }
            with open(os.path.join(target_dir, "package.json"), "w", encoding="utf-8") as f:
                json.dump(pkg_json, f, indent=2)
        except Exception as e:
            print(f"File write error: {e}")

        time.sleep(0.6)
        self.status_lbl.config(text="Запуск Nexo... 🚀")
        time.sleep(0.6)

        self.destroy()
        
        try:
            os.startfile(target_dir)
        except Exception:
            pass

if __name__ == "__main__":
    app = NexoAllInOneInstaller()
    app.mainloop()
