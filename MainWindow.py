from MainWindowUI import MainWindowUI
from Field import *
from PyQt5.QtWidgets import QMainWindow, QMessageBox, QAction
from PyQt5.QtCore import Qt, QBasicTimer, pyqtSignal, pyqtSlot
from PyQt5 import QtCore, QtWidgets
from Painter import *
from Settings import *

class MainWindow(QMainWindow, MainWindowUI):
    Difficulty = 3
    BlockWidth = 10
    BlockHeight = 17
    Speed = 5000
    msgStatusbar = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.Dialog = WindowConfig()
        self.bag = self.Dialog
        self.my_field = Field(self, self.BlockHeight, self.BlockWidth, self.Difficulty)
        self.timer = QBasicTimer()
        self.count_deleted_blocks = 0
        self.painter = Painter(self, self.BlockHeight, self.BlockWidth)
        self.is_paused = False
        self.is_started = False
        self.setFocusPolicy(Qt.StrongFocus)
        self.setCentralWidget(self.painter)
        self.msgStatusbar[str].connect(self.statusbar.showMessage)
        self.bag.punched.connect(self.env_punched)
        self.create_menu()

    def create_menu(self):
        self.menubar = QtWidgets.QMenuBar(self)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1200, 20))
        self.menubar.setObjectName("menubar")

        self.menu = QtWidgets.QMenu(self.menubar)
        self.menu.setObjectName("menu")

        self.act_new = QtWidgets.QAction(self)
        self.act_new.setObjectName("new")
        self.act_settings = QtWidgets.QAction(self)
        self.act_settings.setObjectName("settings")
        self.act_info = QtWidgets.QAction(self)
        self.act_info.setObjectName("info")

        self.menu.addActions([self.act_new, self.act_info, self.act_settings])
        self.menubar.addAction(self.menu.menuAction())

        self.setMenuBar(self.menubar)

        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.menu.setTitle(_translate("MainWindow", "Game"))
        self.act_new.setText(_translate("MainWindow", "&New"))
        self.act_settings.setText(_translate("MainWindow", "&Settings"))
        self.act_info.setText(_translate("MainWindow", "&Help"))

        self.act_new.triggered.connect(self.start)
        self.act_info.triggered.connect(self.help)
        self.act_settings.triggered.connect(self.show_dialog_for_settings)

    @pyqtSlot()
    def show_dialog_for_settings(self):
        self.Dialog.showDialog()

    @pyqtSlot(int, int)
    def env_punched(self, color_num, dif_num):
        colors = [ColorTables.Bright, ColorTables.Soft, ColorTables.Mono, ColorTables.Neon, ColorTables.Dark]
        self.painter.ColorScheme = colors[color_num]
        self.Difficulty = dif_num + 1
        self.my_field.Difficulty = self.Difficulty
        self.painter.update()

    def help(self):
        text = "    Тетрис наоборот - это игра, в которой нужно не " \
               "дать опуститься блокам до низа поля, управляя платформой.\n\n" \
               "    Во время игры через равные промежутки времени будут появляться " \
               "новые блоки, опуская старые на ряд ниже.\n\n" \
               "    Чтобы переместить платформу нажимайте стрелки вправо и влево на клавиатуре. " \
               "Чтобы уронить блоки на платформу или подкинуть их вверх к остальным нажмите пробел."
        QMessageBox.information(self, 'Help', text)

    def start(self):
        self.is_paused = False
        self.is_started = True
        self.count_deleted_blocks = 0
        self.my_field.start()

        self.timer.start(self.Speed, self)

        self.painter.refresh(self.my_field.field)

        self.msgStatusbar.emit(str(self.count_deleted_blocks * 1000))

    def timerEvent(self, event):
        if event.timerId() == self.timer.timerId():
            self.my_field.one_line_down()
            self.painter.refresh(self.my_field.field)
            self.game_over()

        else:
            super(MainWindow, self).timerEvent(event)

    def game_over(self):
        if self.my_field.check_for_game_over():
            self.is_paused = not self.is_paused
            self.timer.stop()
            self.msgStatusbar.emit("game over")
            score = self.count_deleted_blocks * 1000
            QMessageBox.information(self, 'GAME OVER', "Your score: " + str(score))
            #tkinter.messagebox.showinfo("GAME OVER", )

    def pause(self):

        if not self.is_started:
            return

        self.is_paused = not self.is_paused

        if self.is_paused:
            self.timer.stop()
            self.msgStatusbar.emit("pause")
        else:
            self.timer.start(Field.Speed, self)
            self.msgStatusbar.emit(str(self.count_deleted_blocks * 1000))

        self.painter.refresh(self.my_field.field)

    def keyPressEvent(self, event):

        #if not self.is_started:
        #    super(MainWindow, self).keyPressEvent(event)
        #    return

        key = event.key()

        if key == Qt.Key_P:

            self.pause()
            return
        elif key == Qt.Key_1:
            self.painter.ColorScheme = ColorTables.Bright
            self.update()

        elif key == Qt.Key_2:
            self.painter.ColorScheme = ColorTables.Soft
            self.update()

        elif key == Qt.Key_3:
            self.painter.ColorScheme = ColorTables.Mono
            self.update()

        elif key == Qt.Key_4:
            self.painter.ColorScheme = ColorTables.Dark
            self.update()

        elif key == Qt.Key_5:
            self.painter.ColorScheme = ColorTables.Neon
            self.update()

        elif key == Qt.Key_Plus:
            self.Difficulty += 1

        elif key == Qt.Key_Minus:
            self.Difficulty -= 1

        elif key == Qt.Key_N:
            self.start()

        elif self.is_paused:
            return

        elif key == Qt.Key_Left:
            self.my_field.move(-1)
            self.painter.refresh(self.my_field.field)

        elif key == Qt.Key_Right:
            self.my_field.move(1)
            self.painter.refresh(self.my_field.field)

        elif key == Qt.Key_Space:
            self.count_deleted_blocks += self.my_field.action()
            self.msgStatusbar.emit(str(self.count_deleted_blocks * 1000))
            self.game_over()
            self.painter.refresh(self.my_field.field)

        else:
            super(MainWindow, self).keyPressEvent(event)
