from scrapy.cmdline import execute
import os
import sys
import schedule
import time

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
execute(['scrapy', 'crawl', 'singers'])

# def job():
#     sys.path.append(os.path.dirname(os.path.abspath(__file__)))
#     execute(['scrapy', 'crawl', 'singers'])
#
#
# schedule.every().day.at('01:00').do(job)
#
# if __name__ == '__main__':
#     while True:
#         schedule.run_pending()
#         time.sleep(1)
