import customtkinter as ctk
import json
import os

DATA_FILE = "audit_data.json"

# --- Модуль Domain (Логика аудита) ---
DEFAULT_CHECKLIST = [
    {"id": 1, "question": "Проверка питания", "status": "OK", "comment": ""},
    {"id": 2, "question": "Проверка охлаждения", "status": "OK", "comment": ""},
    {"id": 3, "question": "Целостность корпуса", "status": "OK", "comment": ""},
    {"id": 4, "question": "Тест сетевых интерфейсов", "status": "OK", "comment": ""},
]

def load_data():
    if not os.path.exists(DATA_FILE):
        return DEFAULT_CHECKLIST
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        # Защита от сбоя: если файл битый, загружаем дефолт
        return DEFAULT_CHECKLIST

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

# --- UI ---
class AuditorApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Офлайн-аудитор")
        self.geometry("600x700")
        
        self.data = load_data()
        
        # Заголовок
        ctk.CTkLabel(self, text="Чек-лист аудита", font=("Arial", 20, "bold")).pack(pady=10)
        
        self.scroll_frame = ctk.CTkScrollableFrame(self, width=550, height=500)
        self.scroll_frame.pack(pady=10, fill="both", expand=True)
        
        self.render_checklist()
        
        # Кнопка сохранения и экспорта
        frame_btns = ctk.CTkFrame(self)
        frame_btns.pack(pady=10)
        
        ctk.CTkButton(frame_btns, text="Сохранить черновик", command=self.save_draft).pack(side="left", padx=10)
        ctk.CTkButton(frame_btns, text="Экспорт отчета", command=self.export_report, fg_color="green").pack(side="left", padx=10)

    def render_checklist(self):
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()
            
        for item in self.data:
            frame = ctk.CTkFrame(self.scroll_frame)
            frame.pack(fill="x", pady=5, padx=5)
            
            lbl = ctk.CTkLabel(frame, text=item["question"], width=200, anchor="w")
            lbl.pack(side="left", padx=5)
            
            # Переключатель ОК / Не ОК
            switch_var = ctk.StringVar(value=item["status"])
            switch = ctk.CTkSegmentedButton(frame, values=["OK", "Не ОК"], variable=switch_var,
                                            command=lambda val, i=item["id"]: self.update_status(i, val))
            switch.pack(side="left", padx=5)
            
            # Поле для комментария
            comment_entry = ctk.CTkEntry(frame, placeholder_text="Комментарий", width=150)
            comment_entry.insert(0, item["comment"])
            comment_entry.pack(side="left", padx=5)
            # Сохраняем комментарий при потере фокуса
            comment_entry.bind("<FocusOut>", lambda e, i=item["id"], entry=comment_entry: self.update_comment(i, entry.get()))

    def update_status(self, item_id, status):
        for item in self.data:
            if item["id"] == item_id:
                item["status"] = status
                break
        save_data(self.data) # Автосохранение

    def update_comment(self, item_id, comment):
        for item in self.data:
            if item["id"] == item_id:
                item["comment"] = comment
                break
        save_data(self.data) # Автосохранение

    def save_draft(self):
        save_data(self.data)
        ctk.CTkLabel(self, text="Черновик сохранен!", text_color="green").pack()

    def export_report(self):
        report = {"status": "Провален" if any(i["status"] == "Не ОК" for i in self.data) else "Пройден", "items": self.data}
        with open("final_report.json", "w", encoding="utf-8") as f:
            json.dump(report, f, ensure_ascii=False, indent=4)
        ctk.CTkLabel(self, text="Отчет экспортирован (final_report.json)!", text_color="blue").pack()

if __name__ == "__main__":
    ctk.set_appearance_mode("Dark")
    app = AuditorApp()
    app.mainloop()