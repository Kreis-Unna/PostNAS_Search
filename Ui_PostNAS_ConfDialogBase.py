# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\u200584\.qgis2\python\plugins\PostNAS_Search\PostNAS_ConfDialogBase.ui'
#
# Created: Thu Apr 23 11:08:27 2015
#      by: PyQt4 UI code generator 4.10.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.setWindowModality(QtCore.Qt.NonModal)
        Dialog.resize(330, 220)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Dialog.sizePolicy().hasHeightForWidth())
        Dialog.setSizePolicy(sizePolicy)
        Dialog.setMinimumSize(QtCore.QSize(330, 220))
        Dialog.setMaximumSize(QtCore.QSize(330, 220))
        self.gridLayout = QtGui.QGridLayout(Dialog)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.groupBox = QtGui.QGroupBox(Dialog)
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.gridLayout_2 = QtGui.QGridLayout(self.groupBox)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.label_8 = QtGui.QLabel(self.groupBox)
        self.label_8.setObjectName(_fromUtf8("label_8"))
        self.gridLayout_2.addWidget(self.label_8, 2, 0, 1, 1)
        self.lePORT = QtGui.QLineEdit(self.groupBox)
        self.lePORT.setObjectName(_fromUtf8("lePORT"))
        self.gridLayout_2.addWidget(self.lePORT, 2, 1, 1, 1)
        self.label_7 = QtGui.QLabel(self.groupBox)
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.gridLayout_2.addWidget(self.label_7, 1, 0, 1, 1)
        self.leHOST = QtGui.QLineEdit(self.groupBox)
        self.leHOST.setText(_fromUtf8(""))
        self.leHOST.setObjectName(_fromUtf8("leHOST"))
        self.gridLayout_2.addWidget(self.leHOST, 1, 1, 1, 1)
        self.leDBNAME = QtGui.QLineEdit(self.groupBox)
        self.leDBNAME.setObjectName(_fromUtf8("leDBNAME"))
        self.gridLayout_2.addWidget(self.leDBNAME, 3, 1, 1, 1)
        self.label_2 = QtGui.QLabel(self.groupBox)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout_2.addWidget(self.label_2, 4, 0, 1, 1)
        self.label_3 = QtGui.QLabel(self.groupBox)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridLayout_2.addWidget(self.label_3, 8, 0, 1, 1)
        self.leUID = QtGui.QLineEdit(self.groupBox)
        self.leUID.setText(_fromUtf8(""))
        self.leUID.setObjectName(_fromUtf8("leUID"))
        self.gridLayout_2.addWidget(self.leUID, 4, 1, 1, 1)
        self.label = QtGui.QLabel(self.groupBox)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout_2.addWidget(self.label, 3, 0, 1, 1)
        self.lePWD = QtGui.QLineEdit(self.groupBox)
        self.lePWD.setText(_fromUtf8(""))
        self.lePWD.setEchoMode(QtGui.QLineEdit.Password)
        self.lePWD.setObjectName(_fromUtf8("lePWD"))
        self.gridLayout_2.addWidget(self.lePWD, 8, 1, 1, 1)
        self.gridLayout.addWidget(self.groupBox, 0, 0, 2, 1)
        self.buttonBox = QtGui.QDialogButtonBox(Dialog)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 4, 0, 1, 2)
        self.label_8.setBuddy(self.lePORT)
        self.label_7.setBuddy(self.leHOST)
        self.label_2.setBuddy(self.leUID)
        self.label_3.setBuddy(self.lePWD)
        self.label.setBuddy(self.leDBNAME)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
        Dialog.setTabOrder(self.leHOST, self.lePORT)
        Dialog.setTabOrder(self.lePORT, self.leDBNAME)
        Dialog.setTabOrder(self.leDBNAME, self.leUID)
        Dialog.setTabOrder(self.leUID, self.lePWD)
        Dialog.setTabOrder(self.lePWD, self.buttonBox)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "ALKIS-Import", None))
        self.groupBox.setTitle(_translate("Dialog", "Datenbankeinstellungen", None))
        self.label_8.setText(_translate("Dialog", "Port", None))
        self.lePORT.setInputMask(_translate("Dialog", "99999; ", None))
        self.lePORT.setText(_translate("Dialog", "5432", None))
        self.label_7.setText(_translate("Dialog", "Host", None))
        self.label_2.setText(_translate("Dialog", "Benutzername", None))
        self.label_3.setText(_translate("Dialog", "Paßwort", None))
        self.label.setText(_translate("Dialog", "Datenbankname", None))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    Dialog = QtGui.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())

