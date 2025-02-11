import os
import shutil
import logging
from apscheduler.schedulers.blocking import BlockingScheduler
import tzlocal
from datetime import datetime

# Настройки логирования
logging.basicConfig(
    filename='C:/Users/aleksandrovva1/Desktop/spare_files_for_folder/sync_files.log',
    filemode='a',
    format='%(levelname)s %(message)s, %(asctime)s',
    datefmt='%Y.%m.%d %H:%M:%S',
    level=logging.DEBUG
)

# Пути
archive_path = 'C:/Users/aleksandrovva1/Desktop/spare_files_for_folder/file_to_l_or_to_audit'
l_disk_path = 'L:/Analiz/01. МСФО/01. Рабочие файлы/'


def get_request_info():
    """
    Извлекает информацию о года и месяце из имен папок в архиве
    """
    try:
        requests = []
        for folder in os.listdir(archive_path):
            # Проверяем, является ли папка запросом
            if folder.startswith(' ') or 'Запрос' in folder:
                parts = folder.split()
                for part in parts:
                    if 'м' in part:
                        period = part
                        # Преобразуем формат с "12м2023" на "2023m12"
                        year = period[-4:]
                        month = period[:-4]
                        # Устраняем возможное обозначение месяца (например, "12м" становится "12")
                        if 'м' in month:
                            month = month.replace('м', '')
                        formatted_period = f"{year}m{month}"
                        requests.append({
                            'folder_name': folder,
                            'year': year,
                            'month': month,
                            'period': formatted_period
                        })
                        break
        return requests
    except Exception as e:
        logging.error(f"Ошибка при извлечении информации о запросах: {str(e)}")
        return []


def create_directory_structure(request):
    """
    Создает структуру папок на диске L для одного запроса
    """
    try:
        # Формируем путь на диске L с исправленным форматом периода
        target_path = os.path.join(l_disk_path, request['year'], f"Audit {request['period']}", '01. Орг', 'запросы',
                                   request['folder_name'])

        # Создаем промежуточные папки
        os.makedirs(target_path, exist_ok=True)

        # Логирование
        logging.info(f"Создана структура папок: {target_path}")
        return target_path
    except Exception as e:
        logging.error(f"Ошибка при создании папок для запроса {request['folder_name']}: {str(e)}")
        return None


def copy_files_to_l_disk(source_path, target_path):
    """
    Копирует файлы из архива на диск L
    """
    try:
        # Сравниваем содержимое архива и целей
        source_files = os.listdir(source_path)
        target_files = os.listdir(target_path) if os.path.exists(target_path) else []

        # Копируем новые файлы
        for file in source_files:
            if file not in target_files:
                shutil.copy2(os.path.join(source_path, file), target_path)
                logging.info(f"Скопирован файл: {file}")
        return True
    except Exception as e:
        logging.error(f"Ошибка при копировании файлов: {str(e)}")
        return False


def sync_files():
    """
    Синхронизирует файлы между архивом и диском L
    """
    try:
        requests = get_request_info()
        if not requests:
            logging.warning("Нет запросов для синхронизации")
            return

        for request in requests:
            # Создаем структуру папок на диске L
            target_path = create_directory_structure(request)
            if target_path:
                # Копируем файлы для каждого пункта запроса
                base_request_path = os.path.join(archive_path, request['folder_name'])
                for point_folder in os.listdir(base_request_path):
                    point_path = os.path.join(base_request_path, point_folder)
                    if os.path.isdir(point_path):
                        final_target = os.path.join(target_path, point_folder)
                        if not os.path.exists(final_target):
                            os.makedirs(final_target, exist_ok=True)
                        copy_files_to_l_disk(point_path, final_target)
        logging.info("Синхронизация завершена успешно")
    except Exception as e:
        logging.error(f"Ошибка при синхронизации файлов: {str(e)}")


sched = BlockingScheduler(timezone=tzlocal.get_localzone_name())

# Планируем задание
sched.add_job(sync_files, 'cron', day_of_week='0-5', hour='17', minute='25-50')

if __name__ == '__main__':
    sched.start()
