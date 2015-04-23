# -*- coding: utf-8 -*-
"""
/***************************************************************************
    PostNAS_Search
    -------------------
    Date                : April 2015
    copyright          : (C) 2015 by Marvin Brandt / Kreis-Unna
    email                : marvin.brandt@kreis-unna.de
 ***************************************************************************
 *                                                                                                                                    *
 *   This program is free software; you can redistribute it and/or modify                                       *
 *   it under the terms of the GNU General Public License as published by                                      *
 *   the Free Software Foundation; either version 2 of the License, or                                          *
 *   (at your option) any later version.                                                                                    *
 *                                                                                                                                    *
 ***************************************************************************/
"""

from PyQt4.QtGui import QDialog
from PyQt4.QtCore import pyqtSignature,  QSettings

from Ui_PostNAS_ConfDialogBase import Ui_Dialog

class PostNAS_ConfDialog(QDialog, Ui_Dialog):
    def __init__(self, parent = None,  iface = None):
        QDialog.__init__(self)
        self.setupUi(self)
        settings = QSettings("PostNAS", "PostNAS-Suche")
        self.leHOST.setText(settings.value("host", ""))
        self.lePORT.setText(settings.value("port", "5432"))
        self.leDBNAME.setText(settings.value("dbname", ""))
        self.leUID.setText(settings.value("user", ""))
        self.lePWD.setText(settings.value("password", ""))
        
    def on_buttonBox_accepted(self):
        settings = QSettings("PostNAS", "PostNAS-Suche")
        settings.setValue("host", self.leHOST.text())
        settings.setValue("port", self.lePORT.text())
        settings.setValue("dbname", self.leDBNAME.text())
        settings.setValue("user", self.leUID.text())
        settings.setValue("password", self.lePWD.text())
        QDialog.accept(self)
        
    def on_buttonBox_rejected(self):
        QDialog.reject(self)
