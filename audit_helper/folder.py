import os
import re
import shutil
import logging
import json
from tkinter import Tk, Label, Entry, Button, messagebox
from tkinter.filedialog import askdirectory  # Импорт модуля для выбора папки
from apscheduler.schedulers.background import BackgroundScheduler
import tzlocal
from datetime import datetime

# Путь к файлу с настройками
from folder import create_folder_structure, move_files_to_folder, extract_audit_info_from_filename
from move_files_from_folder_to_arcive import move_file_to_archive_in_end_of_day
from move_files_to_i_dicect import sync_files

SETTINGS_FILE = 'settings.json'

# Настройки по умолчанию
DEFAULT_SETTINGS = {
    'PROJECT_PATH': 'C:/Users/aleksandrovva1/Desktop/spare_files_for_folder',
    'topath': 'C:/Users/aleksandrovva1/Desktop/spare_files_for_folder/folder',
    'archive_path': 'C:/Users/aleksandrovva1/Desktop/spare_files_for_folder/file_to_l_or_to_audit',
    'l_disk_path': 'L:/Analiz/01. МСФО/01. Рабочие файлы/',
    'audit_file': 'C:/Users/aleksandrovva1/Desktop/spare_files_for_folder/audit_files'
}

# Настройки логирования
logging.basicConfig(
    filename=os.path.join(DEFAULT_SETTINGS['PROJECT_PATH'], 'load_files_for_purpose.log'),
    filemode='a',
    format='%(levelname)s %(message)s, %(asctime)s',
    datefmt='%Y.%m.%d %H:%M:%S',
    level=logging.DEBUG
)

# Инициализация планировщика
sched = BackgroundScheduler(timezone=tzlocal.get_localzone_name())

def load_settings():
    """Загружает настройки из файла или использует значения по умолчанию"""
    if os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, 'r') as f:
            return json.load(f)
    return DEFAULT_SETTINGS

def save_settings(settings):
    """Сохраняет настройки в файл"""
    with open(SETTINGS_FILE, 'w') as f:
        json.dump(settings, f)

class Application(Tk):
    def __init__(self):
        super().__init__()
        self.title("Управление задачами")
        self.geometry("750x500")  # Увеличиваем размер окна для удобства

        self.settings = load_settings()

        # Поля ввода с увеличенной шириной
        self.project_path_entry = Entry(self, width=60)
        self.topath_entry = Entry(self, width=60)
        self.archive_path_entry = Entry(self, width=60)
        self.l_disk_path_entry = Entry(self, width=60)
        self.audit_files_folder_entry = Entry(self, width=60)

        self.number_of_request_entry = Entry(self)
        self.request_number_entry = Entry(self)

        self.initialize_ui()

    def initialize_ui(self):
        """Инициализация интерфейса"""
        Label(self, text="Путь к проекту:").grid(row=0, column=0, padx=10, pady=10)
        self.project_path_entry.grid(row=0, column=1, padx=10, pady=10)
        self.project_path_entry.insert(0, self.settings['PROJECT_PATH'])
        Button(self, text="Выбрать", command=lambda: self.select_path(self.project_path_entry)).grid(row=0, column=2, padx=10, pady=10)

        Label(self, text="Путь к папке:").grid(row=1, column=0, padx=10, pady=10)
        self.topath_entry.grid(row=1, column=1, padx=10, pady=10)
        self.topath_entry.insert(0, self.settings['topath'])
        Button(self, text="Выбрать", command=lambda: self.select_path(self.topath_entry)).grid(row=1, column=2, padx=10, pady=10)

        Label(self, text="Путь к архиву:").grid(row=2, column=0, padx=10, pady=10)
        self.archive_path_entry.grid(row=2, column=1, padx=10, pady=10)
        self.archive_path_entry.insert(0, self.settings['archive_path'])
        Button(self, text="Выбрать", command=lambda: self.select_path(self.archive_path_entry)).grid(row=2, column=2, padx=10, pady=10)

        Label(self, text="Путь к L диску:").grid(row=3, column=0, padx=10, pady=10)
        self.l_disk_path_entry.grid(row=3, column=1, padx=10, pady=10)
        self.l_disk_path_entry.insert(0, self.settings['l_disk_path'])
        Button(self, text="Выбрать", command=lambda: self.select_path(self.l_disk_path_entry)).grid(row=3, column=2, padx=10, pady=10)

        Label(self, text="Путь к папке с аудит файлами:").grid(row=4, column=0, padx=10, pady=10)
        self.audit_files_folder_entry.grid(row=4, column=1, padx=10, pady=10)
        self.audit_files_folder_entry.insert(0, self.settings['audit_file'])
        Button(self, text="Выбрать", command=lambda: self.select_path(self.audit_files_folder_entry)).grid(row=4,column=2,padx=10,pady=10)

        Button(self, text="Сохранить настройки", command=self.save_settings).grid(row=5, column=0, columnspan=3, padx=10, pady=10)
        Label(self, text="Номер запроса:").grid(row=6, column=0, padx=10, pady=10)
        self.number_of_request_entry.grid(row=6, column=1, padx=10, pady=10, sticky="w")

        Label(self, text="Пункт запроса:").grid(row=7, column=0, padx=10, pady=10)
        self.request_number_entry.grid(row=7, column=1, padx=10, pady=10, sticky="w")

        Button(self, text="Старт", command=self.start_process).grid(row=8, column=0, columnspan=3, pady=10)

        Button(self, text="Запустить процесс отправки документов в конце рабочего дня", command=self.start_tasks).grid(
            row=9, column=0, columnspan=3, pady=10)
        Button(self, text="Остановить процесс отправки документов в конце рабочего дня", command=self.stop_tasks).grid(
            row=10, column=0, columnspan=3, pady=10)

    def select_path(self, entry_widget):
        """Открывает диалоговое окно для выбора папки и вставляет путь в указанный Entry"""
        selected_path = askdirectory()  # Открываем диалоговое окно для выбора папки
        if selected_path:  # Если папка выбрана
            entry_widget.delete(0, 'end')  # Очищаем поле ввода
            entry_widget.insert(0, selected_path)  # Вставляем выбранный путь

    def save_settings(self):
        """Сохраняет настройки в файл"""
        self.settings['PROJECT_PATH'] = self.project_path_entry.get()
        self.settings['topath'] = self.topath_entry.get()
        self.settings['archive_path'] = self.archive_path_entry.get()
        self.settings['l_disk_path'] = self.l_disk_path_entry.get()
        self.settings['audit_file'] = self.audit_files_folder_entry.get()
        save_settings(self.settings)
        messagebox.showinfo("Успех", "Настройки сохранены")

    def start_tasks(self):
        """Запуск задач"""
        try:
            sched.add_job(sync_files, 'cron', day_of_week='0-5', hour='17', minute='25-50')
            sched.add_job(move_file_to_archive_in_end_of_day, 'cron', day_of_week='0-5', hour='17', minute='28-32')
            sched.start()
            messagebox.showinfo("Успех", "Задачи запущены")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка при запуске задач: {str(e)}")

    def stop_tasks(self):
        """Остановка задач"""
        try:
            sched.shutdown(wait=False)
            messagebox.showinfo("Успех", "Задачи остановлены")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка при остановке задач: {str(e)}")

    def start_process(self):
        """Обработка нажатия кнопки Старт"""
        number_of_request = self.number_of_request_entry.get()
        request_number = self.request_number_entry.get()

        if not number_of_request or not request_number:
            messagebox.showerror("Ошибка", "Пожалуйста, заполните все поля")
            return

        # Путь к аудит файлам
        audit_files_folder = self.audit_files_folder_entry.get()
        audit_file_path = os.path.join(audit_files_folder, os.listdir(audit_files_folder)[0])

        # Извлекаем информацию о периоде аудита из имени файла
        audit_period = extract_audit_info_from_filename(audit_file_path)

        if audit_period:
            # Создаем структуру папок
            main_folder = create_folder_structure(audit_period, number_of_request, request_number)

            if main_folder:
                # Перемещаем файлы
                source_folder = os.path.join(self.settings['PROJECT_PATH'], 'download_from_pyrus')
                move_files_to_folder(source_folder, main_folder, number_of_request, request_number)
                messagebox.showinfo("Успех", "Файлы успешно организованы")
                self.return_to_start()
        else:
            messagebox.showerror("Ошибка", "Не удалось извлечь период аудита из имени файла")

    def return_to_start(self):
        """Возврат в начальное состояние"""
        self.number_of_request_entry.delete(0, 'end')
        self.request_number_entry.delete(0, 'end')

if __name__ == '__main__':
    app = Application()
    app.mainloop()
