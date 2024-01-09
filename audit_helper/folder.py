import os
import pandas as pd
import re
import geopandas
import shutil
import logging

path = os.environ.get('PROJECT_PATH', 'C:/Users/aleksandrovva1/Desktop/spare_files_for_folder')
topath = 'C:/Users/aleksandrovva1/Desktop/spare_files_for_folder/folder'
df = os.listdir('C:/Users/aleksandrovva1/Desktop/spare_files_for_folder/download_from_pyrus')
scole = []
task_file = pd.ExcelFile(f'{path}/audit_files/' + os.listdir(f'{path}/audit_files')[0])
list_of_files = os.listdir(r'C:\Users\aleksandrovva1\Desktop\spare_files_for_folder\download_from_pyrus')
number_of_request = input('Введи номер запроса')
request_number = input('Введи пункт запроса')



def find_request_number():
    for file in list_of_files:
        shutil.move(f'C:/Users/aleksandrovva1/Desktop/spare_files_for_folder/download_from_pyrus/{file}',
                    f'C:/Users/aleksandrovva1/Desktop/spare_files_for_folder/prepared_files/{number_of_request + "_" + request_number + "_" + file}')


def make_dir():
    list_of_tasks = task_file.sheet_names
    prep_names = []
    for i in range(0, len(list_of_tasks)):
        if list_of_tasks[i][0] not in '012345678910':
            pass
        else:
            prep_names.append(list_of_tasks[i].replace('.', ' '))
    for file in os.listdir(f"{path}/audit_files"):
        for task in prep_names:
            if task not in os.listdir(f'{path}/folder') and task.split(' ')[0] not in [i.split(' ')[0] for i in os.listdir(f'{path}/folder')] \
                    and task.split('.')[0] not in [i[0] for i in os.listdir(f'{path}/folder')]:
                os.chdir(f'{path}/folder')
                os.mkdir(task.split(' ')[0] + ' Запрос '
                         + file.split('_')[2][:7]
                         + ' '
                         + task.split(' ')[-1])
            else:
                pass


def make_unndo_dir():
    derf = os.listdir('C:/Users/aleksandrovva1/Desktop/spare_files_for_folder/prepared_files')
    for file in derf:
        os.chdir(
            f"{path}/folder/{[i for i in os.listdir('C:/Users/aleksandrovva1/Desktop/spare_files_for_folder/folder') if i.split(' ')[0] == file.split('_')[0]][0]}")
        if os.path.isdir('Пункт ' + file.split('_')[0] + '_' + file.split('_')[1]):
            continue
        else:
            os.mkdir('Пункт ' + file.split('_')[0] + '_' + file.split('_')[1])


def find_dir():
    derf = os.listdir('C:/Users/aleksandrovva1/Desktop/spare_files_for_folder/prepared_files')
    scole = []
    for i in derf:
        if i.split('_')[0] in [j.split(' ')[0] for j in os.listdir(topath)]:
            file = i
            filed = file.split('_')
            scole.append(filed)
            for word in scole:
                if word[0] in [j.split(' ')[0] for j in os.listdir(topath)]:
                    shutil.move(f'C:/Users/aleksandrovva1/Desktop/spare_files_for_folder/prepared_files/{file}',
                                f'C:/Users/aleksandrovva1/Desktop/spare_files_for_folder/folder/{[i for i in os.listdir(topath) if i.split(" ")[0] == word[0]][0]}/{"Пункт " + str(number_of_request) + "_" + str(request_number)}/{file}')
                    scole.remove(word)
                    logging.basicConfig(filename='C:/Users/aleksandrovva1/Desktop/spare_files_for_folder/load_files_for_purpose',
                                        filemode='a',
                                        format='%(levelname)s %(message)s, %(asctime)s,',
                                        datefmt='%Y.%m.%d %H:%M:%S',
                                        level=logging.DEBUG)

                    logging.info(f'{file} send to disc L by {os.getenv("username")} by')

if __name__ == '__main__':
    find_request_number()
    make_dir()
    make_unndo_dir()
    find_dir()