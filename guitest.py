import sys

import datetime

import psutil, time
from PyQt5.QtWidgets import (QWidget, QToolTip, 
    QPushButton,QVBoxLayout, QApplication, QLabel)
from PyQt5.QtGui import QFont    
from PyQt5 import QtCore



total_running_time = 0.0
limit_running_time = 2 * 60 * 60

poll_time = 1.0

blacklisted_processes = ["leagueoflegends.exe","python3.5ltsdKit.WebContenterionServicervicey","AppleIDAuthAgent"]

class Window(QWidget):
    
  def __init__(self):
      super().__init__()
      self.initUI()

  def initUI(self):
      
      QToolTip.setFont(QFont('SansSerif', 10))
      
      self.setToolTip('This is a <b>QWidget</b> widget')


      vbox = QVBoxLayout()

      self._timeLeftLabel = QLabel("Time Left: " + str(datetime.timedelta(seconds=limit_running_time - total_running_time)))
      vbox.addWidget(self._timeLeftLabel)
      
      btn = QPushButton('Start Polling', self)
      btn.setToolTip('This is a <b>QPushButton</b> widget')
      btn.resize(btn.sizeHint())
      btn.move(50, 50)
      btn.clicked.connect(self.handleButton)
      vbox.addWidget(btn)



      self.setLayout(vbox)    
      
      self.setGeometry(300, 300, 300, 200)
      self.setWindowTitle('Process Tracker')
      self._active = False
      self.show()
      self.raise_()

  def updateUI(self):
    print("Update Called!")
    self._timeLeftLabel.setText("Time Left: " + str(datetime.timedelta(seconds=limit_running_time - total_running_time)))

  def handleButton(self):
    self._active = True
    self._timer = QtCore.QTimer(self)
    self._timer.setInterval(poll_time * 1000)
    self._timer.timeout.connect(self.pollProcesses)
    self._timer.start()
  def pollProcesses(self):
    print("Polling...")
    for proc in psutil.process_iter():
      try:
        # print("Processing : " + proc.name() + "\r", end=" ")
        if(proc.name() in blacklisted_processes):
          global total_running_time, poll_time
          total_running_time += poll_time
          print(total_running_time)
          self.updateUI()
      except psutil.NoSuchProcess:
        continue
        
        
if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    ex = Window()
    sys.exit(app.exec_())