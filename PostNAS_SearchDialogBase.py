# -*- coding: utf-8 -*-

from qgis.PyQt import QtCore, QtGui
from qgis.PyQt.QtWidgets import QGridLayout, QTreeWidget, QLineEdit, QToolButton, QAbstractItemView, QApplication
from qgis.PyQt.QtGui import QPixmap, QIcon

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QApplication.translate(context, text, disambig)

class Ui_PostNAS_SearchDialogBase(object):
    def setupUi(self, PostNAS_SearchDialogBase):
        PostNAS_SearchDialogBase.setObjectName(_fromUtf8("PostNAS_SearchDialogBase"))
        PostNAS_SearchDialogBase.resize(501, 337)
        self.gridLayout = QGridLayout(PostNAS_SearchDialogBase)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.treeWidget = QTreeWidget(PostNAS_SearchDialogBase)
        self.treeWidget.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.treeWidget.setHeaderHidden(True)
        self.treeWidget.setObjectName(_fromUtf8("treeWidget"))
        self.treeWidget.headerItem().setText(0, _fromUtf8("1"))
        self.gridLayout.addWidget(self.treeWidget, 1, 0, 1, 3)
        self.lineEdit = QLineEdit(PostNAS_SearchDialogBase)
        self.lineEdit.setObjectName(_fromUtf8("lineEdit"))
        self.gridLayout.addWidget(self.lineEdit, 0, 0, 1, 3)
        self.showButton = QToolButton(PostNAS_SearchDialogBase)
        self.showButton.setEnabled(False)
        icon = QtGui.QIcon()
        icon.addPixmap(QPixmap(_fromUtf8(":/plugins/PostNAS_Search/search_16x16.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.showButton.setIcon(icon)
        self.showButton.setObjectName(_fromUtf8("showButton"))
        self.gridLayout.addWidget(self.showButton, 2, 2, 1, 1)
        self.resetButton = QToolButton(PostNAS_SearchDialogBase)
        self.resetButton.setEnabled(False)
        icon1 = QIcon()
        icon1.addPixmap(QtGui.QPixmap(_fromUtf8(":/plugins/PostNAS_Search/marker-delete.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.resetButton.setIcon(icon1)
        self.resetButton.setObjectName(_fromUtf8("resetButton"))
        self.gridLayout.addWidget(self.resetButton, 2, 1, 1, 1)

        self.retranslateUi(PostNAS_SearchDialogBase)
        QtCore.QMetaObject.connectSlotsByName(PostNAS_SearchDialogBase)

    def retranslateUi(self, PostNAS_SearchDialogBase):
        PostNAS_SearchDialogBase.setWindowTitle(_translate("PostNAS_SearchDialogBase", "KU_Search", None))
        self.showButton.setToolTip(_translate("PostNAS_SearchDialogBase", "Auswahl anzeigen", None))
        self.showButton.setText(_translate("PostNAS_SearchDialogBase", "Anzeigen", None))
        self.resetButton.setToolTip(_translate("PostNAS_SearchDialogBase", "Ergebnis löschen", None))
        self.resetButton.setText(_translate("PostNAS_SearchDialogBase", "Reset", None))