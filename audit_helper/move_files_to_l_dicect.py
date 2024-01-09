from apscheduler.schedulers.blocking import BlockingScheduler
import tzlocal
import shutil
from datetime import datetime
import os

archive = 'C:/Users/aleksandrovva1/Desktop/spare_files_for_folder/file_to_l_or_to_audit'
dir_l = 'L:/Analiz/01. МСФО/01. Рабочие файлы/'
sched = BlockingScheduler(misfire_grace_time=100,timezone=tzlocal.get_localzone_name())

year = ''.join(os.listdir('audit_files')[0].split('_')[2][3:7])
period = 'Audit ' + ''.join(os.listdir('audit_files')[0].split('_')[2][3:7] + 'm' + os.listdir('audit_files')[0].split('_')[2][:2])


@sched.scheduled_job('cron', day_of_week='5', hour='17', minute='25-50')
def create_folder_for_files_in_l_disk():
    for i in os.listdir(os.path.join(archive)):
        if os.path.isdir(os.path.join(dir_l, year, period, '01. Орг/Запросы/Планирование/', i)):
            continue
        else:
            os.chdir(os.path.join(dir_l, year, period, '01. Орг/Запросы/Планирование/'))
            os.mkdir(i)
        for j in os.listdir(os.path.join(archive, i)):
            if os.path.isdir(os.path.join(dir_l, year, period, '01. Орг/Запросы/Планирование/', i, j)):
                continue
            else:
                os.chdir(os.path.join(dir_l, year, period, '01. Орг/Запросы/Планирование/', i))
                os.mkdir(j)


@sched.scheduled_job('cron', day_of_week='5', hour='17-20')
def move_file_to_l_disk():
    for i in os.listdir(os.path.join(archive)):
        for j in os.listdir(os.path.join(archive, i)):
            for u in os.listdir(os.path.join(archive, i, j)):
                if os.path.isdir(os.path.join(dir_l, year, period, '01. Орг/Запросы/Планирование/', i, j, u)):
                    continue
                else:
                    shutil.copy(os.path.join(archive, i, j, u),
                                os.path.join(dir_l, year, period, '01. Орг/Запросы/Планирование/', i, j, u))


if __name__ == '__main__':
    sched.start()
