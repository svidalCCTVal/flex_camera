# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'test3.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1087, 837)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.Photo = QtWidgets.QLabel(self.centralwidget)
        self.Photo.setGeometry(QtCore.QRect(0, 0, 1080, 720))
        self.Photo.setText("")
        self.Photo.setPixmap(QtGui.QPixmap("C:\Users\CCTVAL\Desktop\Flexion Cam\UI Designs\cat.jpg"))
        self.Photo.setScaledContents(True)
        self.Photo.setObjectName("Photo")
        self.pushButton_Photo1 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_Photo1.setGeometry(QtCore.QRect(100, 720, 331, 71))
        self.pushButton_Photo1.setObjectName("pushButton_Photo1")
        self.pushButton_Photo2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_Photo2.setGeometry(QtCore.QRect(470, 720, 331, 71))
        self.pushButton_Photo2.setObjectName("pushButton_Photo2")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1087, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton_Photo1.setText(_translate("MainWindow", "Photo 1"))
        self.pushButton_Photo2.setText(_translate("MainWindow", "Photo 2"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
