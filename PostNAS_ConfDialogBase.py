# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'PostNAS_ConfDialogBase.ui'
#
# Created: Thu Apr  7 17:34:35 2016
#      by: PyQt4 UI code generator 4.10.4
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

class Ui_PostNAS_ConfDialogBase(object):
    def setupUi(self, PostNAS_ConfDialogBase):
        PostNAS_ConfDialogBase.setObjectName(_fromUtf8("PostNAS_ConfDialogBase"))
        PostNAS_ConfDialogBase.setWindowModality(QtCore.Qt.NonModal)
        PostNAS_ConfDialogBase.resize(330, 291)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(PostNAS_ConfDialogBase.sizePolicy().hasHeightForWidth())
        PostNAS_ConfDialogBase.setSizePolicy(sizePolicy)
        PostNAS_ConfDialogBase.setMinimumSize(QtCore.QSize(330, 220))
        self.gridLayout_2 = QtGui.QGridLayout(PostNAS_ConfDialogBase)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.groupBox = QtGui.QGroupBox(PostNAS_ConfDialogBase)
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.gridLayout = QtGui.QGridLayout(self.groupBox)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.tabWidget = QtGui.QTabWidget(self.groupBox)
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
        self.auth = QtGui.QWidget()
        self.auth.setObjectName(_fromUtf8("auth"))
        self.gridLayout_5 = QtGui.QGridLayout(self.auth)
        self.gridLayout_5.setObjectName(_fromUtf8("gridLayout_5"))
        self.label_4 = QtGui.QLabel(self.auth)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.gridLayout_5.addWidget(self.label_4, 0, 0, 1, 1)
        self.leUID = QtGui.QLineEdit(self.auth)
        self.leUID.setText(_fromUtf8(""))
        self.leUID.setObjectName(_fromUtf8("leUID"))
        self.gridLayout_5.addWidget(self.leUID, 0, 1, 1, 1)
        self.label_5 = QtGui.QLabel(self.auth)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.gridLayout_5.addWidget(self.label_5, 1, 0, 1, 1)
        self.lePWD = QtGui.QLineEdit(self.auth)
        self.lePWD.setText(_fromUtf8(""))
        self.lePWD.setEchoMode(QtGui.QLineEdit.Password)
        self.lePWD.setObjectName(_fromUtf8("lePWD"))
        self.gridLayout_5.addWidget(self.lePWD, 1, 1, 1, 1)
        self.tabWidget.addTab(self.auth, _fromUtf8(""))
        self.gridLayout.addWidget(self.tabWidget, 3, 0, 1, 2)
        self.lePORT = QtGui.QLineEdit(self.groupBox)
        self.lePORT.setObjectName(_fromUtf8("lePORT"))
        self.gridLayout.addWidget(self.lePORT, 1, 1, 1, 1)
        self.leDBNAME = QtGui.QLineEdit(self.groupBox)
        self.leDBNAME.setObjectName(_fromUtf8("leDBNAME"))
        self.gridLayout.addWidget(self.leDBNAME, 2, 1, 1, 1)
        self.label = QtGui.QLabel(self.groupBox)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 2, 0, 1, 1)
        self.label_8 = QtGui.QLabel(self.groupBox)
        self.label_8.setObjectName(_fromUtf8("label_8"))
        self.gridLayout.addWidget(self.label_8, 1, 0, 1, 1)
        self.leHOST = QtGui.QLineEdit(self.groupBox)
        self.leHOST.setText(_fromUtf8(""))
        self.leHOST.setObjectName(_fromUtf8("leHOST"))
        self.gridLayout.addWidget(self.leHOST, 0, 1, 1, 1)
        self.label_7 = QtGui.QLabel(self.groupBox)
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.gridLayout.addWidget(self.label_7, 0, 0, 1, 1)
        self.gridLayout_2.addWidget(self.groupBox, 0, 0, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(PostNAS_ConfDialogBase)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.buttonBox.sizePolicy().hasHeightForWidth())
        self.buttonBox.setSizePolicy(sizePolicy)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout_2.addWidget(self.buttonBox, 1, 0, 1, 1)
        self.label_4.setBuddy(self.leUID)
        self.label_5.setBuddy(self.lePWD)
        self.label.setBuddy(self.leDBNAME)
        self.label_8.setBuddy(self.lePORT)
        self.label_7.setBuddy(self.leHOST)

        self.retranslateUi(PostNAS_ConfDialogBase)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(PostNAS_ConfDialogBase)
        PostNAS_ConfDialogBase.setTabOrder(self.leHOST, self.lePORT)
        PostNAS_ConfDialogBase.setTabOrder(self.lePORT, self.leDBNAME)
        PostNAS_ConfDialogBase.setTabOrder(self.leDBNAME, self.buttonBox)

    def retranslateUi(self, PostNAS_ConfDialogBase):
        PostNAS_ConfDialogBase.setWindowTitle(_translate("PostNAS_ConfDialogBase", "PostNAS-Suche", None))
        self.groupBox.setTitle(_translate("PostNAS_ConfDialogBase", "Datenbankeinstellungen", None))
        self.label_4.setText(_translate("PostNAS_ConfDialogBase", "Benutzername", None))
        self.label_5.setText(_translate("PostNAS_ConfDialogBase", "Paßwort", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.auth), _translate("PostNAS_ConfDialogBase", "Authentifizierung", None))
        self.lePORT.setInputMask(_translate("PostNAS_ConfDialogBase", "99999; ", None))
        self.lePORT.setText(_translate("PostNAS_ConfDialogBase", "5432", None))
        self.label.setText(_translate("PostNAS_ConfDialogBase", "Datenbankname", None))
        self.label_8.setText(_translate("PostNAS_ConfDialogBase", "Port", None))
        self.label_7.setText(_translate("PostNAS_ConfDialogBase", "Host", None))

