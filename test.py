import schedule
import time

def ss():
	print 'ok'
schedule.every(1).minutes.do(ss)
while True:
    schedule.run_pending()
    time.sleep(1)