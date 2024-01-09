import os
import shutil

list_of_files = os.listdir(r'C:\Users\aleksandrovva1\Desktop\spare_files_for_folder\download_from_pyrus')
number_of_request = input('Введи номер запроса')
request_number = input('Введи пункт запроса')

for file in list_of_files:
    i = file
    shutil.move(f'C:/Users/aleksandrovva1/Desktop/spare_files_for_folder/download_from_pyrus/{file}',
                f'C:/Users/aleksandrovva1/Desktop/spare_files_for_folder/prepared_files/{number_of_request + "_" + request_number + "_" + file}')