from apscheduler.schedulers.blocking import BlockingScheduler
import tzlocal
import shutil
from datetime import datetime
import os

sched = BlockingScheduler(timezone=tzlocal.get_localzone_name())
path = os.environ.get('PROJECT_PATH', 'C:/Users/aleksandrovva1/Desktop/spare_files_for_folder')
topath = 'C:/Users/aleksandrovva1/Desktop/spare_files_for_folder/folder'
to_archive = 'C:/Users/aleksandrovva1/Desktop/spare_files_for_folder/file_to_l_or_to_audit'


@sched.scheduled_job('cron', day_of_week='0-5', hour='17', minute ='28-32')
def move_file_to_archive_in_end_of_day():
    for i in os.listdir(topath):
        if os.path.isdir(to_archive + '/' + i):
            pass
        else:
            os.chdir(to_archive)
            os.mkdir(i)
        for j in os.listdir(topath + '/' + i):
            if os.path.isdir(to_archive + '/' + i + '/' + j):
                pass
            else:
                os.chdir(to_archive + '/' + i)
                os.mkdir(j)
    for dir in os.listdir(topath):
        for secondir in os.listdir(topath + '/' + dir):
            if len(os.listdir(topath + '/' + dir + '/' + secondir)) > 0:
                for file in os.listdir(topath + '/' + dir + '/' + secondir):
                    shutil.move(
                        f'C:/Users/aleksandrovva1/Desktop/spare_files_for_folder/folder/{dir}/{secondir}/{file}',
                        f'C:/Users/aleksandrovva1/Desktop/spare_files_for_folder/file_to_l_or_to_audit/'
                        f'{dir}/{secondir}/{file}')
            else:
                continue
    for g in os.listdir(topath):
        shutil.rmtree(topath + '/' + g)


if __name__ == '__main__':
    sched.start()
