import sys

import datetime

import psutil, time
from PyQt5.QtWidgets import (QWidget, QToolTip, 
    QPushButton,QVBoxLayout, QApplication, QLabel,QLineEdit, QSystemTrayIcon, QMenu)
from PyQt5.QtGui import QFont  
from PyQt5 import QtCore,QtGui

import pickledb

date_today = time.strftime("%d/%m/%Y")
blacklisted_processes = ["League of Legends.exe", "Activity Monitor"]
process_to_terminate = ["lol.exe"]

class SystemTrayIcon(QSystemTrayIcon):

    def __init__(self, icon, parent=None):
        super(SystemTrayIcon, self).__init__(icon, parent)
        menu = QMenu(parent)
        exitAction = menu.addAction("Exit")
        exitAction.triggered.connect(parent.close)
        self.setContextMenu(menu)

class Window(QWidget):
  limit_running_time = 3 * 60 * 60
  total_running_time = 0.0
  poll_time = 1.0
  db = pickledb.load('example.db', False)
    
  def __init__(self):
      super().__init__()
      self.initUI()

      if(self.db.get(date_today) != None):
        self.total_running_time = self.db.get(date_today)
      else:
        self.db.set(date_today, self.total_running_time)

  def initUI(self):
      
      QToolTip.setFont(QFont('SansSerif', 10))
      
      self.setToolTip('This is a <b>QWidget</b> widget')


      vbox = QVBoxLayout()

      self._timeLeftLabel = QLabel("Time Left: " + str(datetime.timedelta(seconds=self.limit_running_time - self.total_running_time)))

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


      self.tray_icon = SystemTrayIcon(QtGui.QIcon('icon.jpg'), self)
      self.tray_icon.show()
      self.show()
      # self.raise_()

  def updateUI(self):
    print("Update Called!")
    self._timeLeftLabel.setText("Time Left: " + str(datetime.timedelta(seconds=self.limit_running_time - self.total_running_time)))

  def handleButton(self):
    self._active = True
    self._timer = QtCore.QTimer(self)
    self._timer.setInterval(self.poll_time * 1000)
    self._timer.timeout.connect(self.pollProcesses)
    self._timer.start()


  def pollProcesses(self):
    print("Polling...")
    if self.total_running_time >= self.limit_running_time:
      print("Attempting to terminate")
      for proc in psutil.process_iter():
        try:
          if(proc.name() in process_to_terminate):
            print("Found Proc to Terminate")
            #proc.terminate()
            proc.kill()
        except psutil.NoSuchProcess:
          continue
    else:
      for proc in psutil.process_iter():
        try:
          if(proc.name() in blacklisted_processes):
            self.total_running_time += self.poll_time
            self.updateUI()
            self.db.set(date_today, self.total_running_time)
            self.db.dump()
            break
        except psutil.NoSuchProcess:
          continue


        
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Window()
    sys.exit(app.exec_())
