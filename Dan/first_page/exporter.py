import schedule
from datetime import datetime
import time

print('hani wselt')

def do_nothing():
    print('kol dkika'+str(datetime.now()))

schedule.every(5).seconds.do(do_nothing)
while 1:

    schedule.run_pending()
    time.sleep(1)