import time

import schedule

from handle.col_update import ColUpdate


def job():
    cu = ColUpdate()
    cu.content_length_handle()
    cu.word_cloud_handle()


schedule.every().day.at('00:30').do(job)

if __name__ == '__main__':
    while True:
        schedule.run_pending()
        time.sleep(1)
