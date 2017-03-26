import update_records
import time

WAIT_MINUTES = 10
while True:
    print("RECORD-SERVER running UPDATE_RECORDS @ {}...".format(time.ctime()))
    update_records.main()
    time.sleep(WAIT_MINUTES*60)


