from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import QRadioButton, QSizePolicy, QDialog, QBoxLayout, QGroupBox, QPushButton
from Painter import ColorTables


class WindowConfig(QDialog):
    color_num = 0
    dif_num = 0
    dif_name = ["Easy", "Middle", "Hard"]
    color_names = ["Bright", "Soft", "Mono", "Neon", "Dark"]
    punched = pyqtSignal(int, int)


    def __init__(self):
        QDialog.__init__(self)
        self.initUI()

    def initUI(self):
        self.setObjectName("Dialog")
        self.resize(500, 300)
        self.grp_1 = QGroupBox("Color")
        self.grp_2 = QGroupBox("Difficulty")
        self.rbs_c = []
        self.rbs_d = []
        for i in range(5):
            c = self.color_names[i]
            self.rbs_c.append(QRadioButton(str(c)))
        for i in range(3):
            d = self.dif_name[i]
            self.rbs_d.append(QRadioButton(str(d)))
        self.btn = QPushButton("Apply", self)
        self.btn.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.btn.move(400, 300)
        self.btn.clicked.connect(self.punch)
        # ???? ?? ? Form Widget? ??
        self.base_layout = QBoxLayout(QBoxLayout.TopToBottom, self)
        self.grp_1_layout = QBoxLayout(QBoxLayout.TopToBottom)
        self.grp_2_layout = QBoxLayout(QBoxLayout.TopToBottom)

        #self.btn_layout = QBoxLayout(QBoxLayout.TopToBottom)

        self.grp_1.setLayout(self.grp_1_layout)
        self.grp_2.setLayout(self.grp_2_layout)
        #self.btn.setLayout(self.btn_layout)



        for i in range(5):
            self.grp_1_layout.addWidget(self.rbs_c[i])
        for i in range(3):
            self.grp_2_layout.addWidget(self.rbs_d[i])

        #self.rbs_c[0].toggled.connect(lambda: self.punched.emit())

        self.rbs_c[self.color_num].setChecked(True)
        self.rbs_d[self.dif_num].setChecked(True)
        self.base_layout.addWidget(self.grp_1)
        self.base_layout.addWidget(self.grp_2)
        self.base_layout.addWidget(self.btn)

        self.setLayout(self.base_layout)

    def punch(self):
        for i in range(5):
            if self.rbs_c[i].isChecked():
                self.color_num = i
        for i in range(3):
            if self.rbs_c[i].isChecked():
                self.dif_num = i
        self.punched.emit(self.color_num, self.dif_num)

    def showDialog(self):
        self.show()
