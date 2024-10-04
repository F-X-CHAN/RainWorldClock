from PyQt5.QtWidgets import QMainWindow, QLabel, QVBoxLayout, QWidget, QSystemTrayIcon, qApp, QMenu, QAction, QApplication
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import QTimer, Qt

import ClockData
import Project

import time

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(400, 300)
        self.setWindowFlags(Qt.Tool | Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)  # 将窗口设为工具窗口，去掉窗口边框并保持置顶
        MainWindow.setAttribute(Qt.WA_TranslucentBackground)  # 设置背景透明

        centralWidget = QWidget(MainWindow)
        centralWidget.setObjectName("centralWidget")

        layout = QVBoxLayout(centralWidget)
        layout.setObjectName("layout")

        self.imageLabel = QLabel(centralWidget)
        self.imageLabel.setObjectName("imageLabel")
        layout.addWidget(self.imageLabel)

        MainWindow.setCentralWidget(centralWidget)

        self.createTrayIcon()


        clock_size = round(ClockData.CANVAS_SIZE * Project.SCALE)
        # put on top-right corner
        top_margin, right_margin = Project.POSITION

        screen_geometry = QApplication.desktop().screenGeometry()
        screen_width = screen_geometry.width()
        screen_height = screen_geometry.height()
        X = screen_width - right_margin - clock_size//2
        Y = top_margin - clock_size//2 
        self.setGeometry(X,Y,clock_size,clock_size)


    def createTrayIcon(self):
        # 创建托盘图标
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(QIcon('./resources/icon.png'))  # 替换为你的图标路径
        self.tray_icon.setVisible(True)

        # 创建菜单项
        self.toggle_action = QAction('隐藏', self)
        self.toggle_action.triggered.connect(self.toggleVisibility)
        exit_action = QAction('退出', self)
        self.toggle_timer_action = QAction('暂停', self)
        self.toggle_timer_action.triggered.connect(self.toggleTimer)
        self.is_paused = False
        exit_action.triggered.connect(self.quit)

        # 创建菜单
        menu = QMenu()
        menu.addAction(self.toggle_action)
        menu.addAction(self.toggle_timer_action)
        menu.addAction(exit_action)

        # 设置托盘图标的上下文菜单
        self.tray_icon.setContextMenu(menu)

    def toggleVisibility(self):
        if self.isHidden():
            self.show()
            self.toggle_action.setText('隐藏')
        else:
            self.hide()
            self.toggle_action.setText('显示')

    def toggleTimer(self):
        if self.is_paused: # restart
            self.timer.start()
            self.play_sound("boom")
            self.is_paused = False
            paused_time = time.time() - self.paused_moment
            self.intervalStart += paused_time
            self.lastFrame += paused_time
            self.toggle_timer_action.setText('暂停')
        else: # pause
            self.timer.stop() 
            self.play_sound("swoosh")
            self.paused_moment = time.time()
            self.is_paused = True
            self.toggle_timer_action.setText('继续')

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.offset = event.pos()

    def mouseMoveEvent(self, event):
        if self.offset is not None and event.buttons() == Qt.LeftButton:
            self.move(self.pos() + (event.pos() - self.offset))

    def mouseReleaseEvent(self, event):
        self.offset = None

    def quit(self):
         if self.is_paused:
            paused_time = time.time() - self.paused_moment
            self.intervalStart += paused_time
            self.lastFrame += paused_time
            self.timer.start()
         #self.tray_icon.hide()
         self.swoosh()

