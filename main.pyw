import sys
from PyQt5.QtCore import QTimer, Qt, QUrl, QObject, QThread, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtWidgets import QApplication, QMainWindow
from ui import Ui_MainWindow  # 导入上面定义的 Ui_MainWindow 类
from PyQt5.QtMultimedia import QSoundEffect, QSound

import Project
from Project import Interval
import ClockData

import time
 

class MyMainWindow(QMainWindow, Ui_MainWindow):

    def __init__(self):
        super(MyMainWindow, self).__init__()
        self.setupUi(self)
        
        self.start = time.time()
        self.intervalStart = self.start
        self.lastFrame = self.start
        self.fadingPower = 0
        self.currentInterval = Interval()
        self.intervals = []
        self.fnDown = False
        self.gonnaQuit = False
        self.isTick = True  # tick or tock?
        self.lastTick = 0  # integer count
        self.prepared = False  # play a file silently to reduce lag

        self.intervals = Project.loadData()
        self.currentInterval = Interval(totalTime=0)

        # 创建定时器
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.logic)
        self.timer.start(int(1000 / 60))  # 每秒触发 60 次

        # 音效
        self.sound_effects = {}
        prefix = "./resources/"
        for name, file in zip(["tick","tock","swoosh","boom"],
                            ["tick.wav","tock.wav","Pre.wav","Hit.wav"]):
            self.sound_effects[name] = prefix+file

    def logic(self):
        current = time.time()
        if self.fadingPower <= 0.01:
            # should quit?
            #print(self.audio_thread.worker.sound_effects["swoosh"].isPlaying())
            if (self.gonnaQuit):
                self.quit_timer = QTimer(self)
                self.quit_timer.setSingleShot(True)
                self.quit_timer.start(1000)
                self.quit_timer.timeout.connect(QApplication.quit)


        # next interval?
        # if you peek, we never switch to the next :)
        if (not self.gonnaQuit 
            and current - self.intervalStart + 0.02 > self.currentInterval.totalTime):
            #self.audio_signal.emit("boom")
            self.play_sound("boom")
            self.intervalStart = current
            self.lastTick = 0
            if self.intervals:
                self.currentInterval = self.intervals.pop(0)
            else:
                self.currentInterval = Interval()        

        # half-time forced show
        # half-time -0.7 to +1.5 (maybe slightly more)
        halftime = self.currentInterval.totalTime/2
        # but if it is too short, then no half time (but it still flashes)
        inHalftime = halftime > 10 and \
            halftime - 2.75 <= current - self.intervalStart <= halftime + 2.55
        # end-time forced show
        # when last pip starts to disappear
        endtime = self.currentInterval.totalTime * (1 - 1/self.currentInterval.totalPip) \
            if self.currentInterval.totalPip > 0 else float("inf")
        inEndtime = endtime - 5.15 <= current - self.intervalStart <= \
            min(endtime + 1.2, self.currentInterval.totalTime - 0.65)
        # also appear at the start to not be too quiet
        shouldDisplay = not self.gonnaQuit and \
            (Project.settings["alwaysdisplay"] or
             self.fnDown or inHalftime or inEndtime or current - self.intervalStart <= 10 
             or self.currentInterval.totalTime == float("inf"))

        # tick-tock noise
        #if current - self.intervalStart \
        #    >= (self.lastTick + 0.5) * Project.settings["ticktock"] and \
        #    not self.prepared:
        #    if self.isTick:
        #        self.play_sound("tick")
        #    else:
        #        self.play_sound("tock")
        #    self.prepared = True
        # In Huang's version, a silent tick-tock is played to reduced the lag
        # here seems we don't need to
        if current - self.intervalStart \
            >= (self.lastTick + 1) * Project.settings["ticktock"]:
            if self.fadingPower >= 0.86 and \
                not inHalftime and not inEndtime and \
                self.currentInterval.totalPip > 0 and current - self.intervalStart <= endtime:
                if self.isTick:
                    self.play_sound("tick")
                else:
                    self.play_sound("tock")
                self.isTick = not self.isTick
                self.prepared = False
            self.lastTick += 1

        dt = min(current - self.lastFrame, 1/20)
        if shouldDisplay:
            self.fadingPower += dt
            self.fadingPower = min(self.fadingPower, 1)
        else:
            self.fadingPower -= dt/0.7
            self.fadingPower = max(self.fadingPower, 0)

        clock = ClockData.computeClock(
            self.currentInterval.totalTime,
            current - self.intervalStart,
            self.currentInterval.totalPip,
            self.currentInterval.karmaSymbol,
            self.currentInterval.karmaReinforced,
            self.currentInterval.maxKarma,
            # mystic parameter space change
            self.fadingPower if shouldDisplay else (self.fadingPower - 1) * 0.7
        )

        if clock.alpha > 0:
            buffer_img = clock.render()
            img = QImage.fromData(buffer_img)
            pixmap = QPixmap.fromImage(img)
            self.imageLabel.setPixmap(pixmap)
        self.setWindowOpacity(clock.alpha)
        self.lastFrame = current 

    def swoosh(self):
        self.gonnaQuit = True
        self.play_sound("swoosh")
        

    def play_sound(self,name):
        QSound.play(self.sound_effects[name])
        


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyMainWindow()
    window.show()
    sys.exit(app.exec_())