import psutil
import time

total_running_time = 0.0
limit_running_time = 2 * 60 * 60

poll_time = 1.0

blacklisted_processes = ["leagueoflegends.exe","python3.5ltsdKit.WebContenterionServicervicey","AppleIDAuthAgent"]


def pollProcesses(self):
  while True:
    for proc in psutil.process_iter():
      try:
        if(proc.name() in blacklisted_processes):
          print("Processing : " + proc.name())
          total_running_time += poll_time
      except:
        i = 0

    time.sleep(1)