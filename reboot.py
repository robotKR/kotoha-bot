import schedule
import time
import main

def reboot():

    main.main
    print("reboot")

def main1():

    schedule.every().days.at("06:30").do(reboot)

    while True:
        schedule.run_pending()
        time.sleep(1)