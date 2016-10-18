import psutil
import time

total_running_time = 0.0
limit_running_time = 2 * 60 * 60

poll_time = 1.0

blacklisted_processes = ["leagueoflegends.exe"]

process_to_terminate = ["lol.exe"]


def pollProcesses(self):
  while True:
    for proc in psutil.process_iter():
      try:
        if(proc.name() in blacklisted_processes):
          print("Processing : " + proc.name())
          total_running_time += poll_time
      except:
        continue


    if total_running_time > limit_running_time:
      for proc in psutil.process_iter():
        try:
          if(proc.name() in process_to_terminate):
            proc.terminate()
        except:
          continue
    time.sleep(1)