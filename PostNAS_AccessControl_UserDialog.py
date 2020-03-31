# -*- coding: utf-8 -*-

import os
from qgis.PyQt import QtGui,uic
from qgis.PyQt.QtWidgets import QDialog,QMessageBox
from .PostNAS_AccessControl import PostNAS_AccessControl
FORM_CLASS, _ = uic.loadUiType(os.path.join(os.path.dirname(__file__), 'PostNAS_AccessControl_UserDialog.ui'))

class PostNAS_AccessControl_UserDialog(QDialog, FORM_CLASS):
    def __init__(self, mode = "new",accessControl = None,iface = None, parent = None):
        super(PostNAS_AccessControl_UserDialog, self).__init__(parent)
        self.setupUi(self)
        if(accessControl == None):
            self.accessControl = PostNAS_AccessControl()
        else:
            self.accessControl = accessControl
        self.loadAccessModes()
        self.mode = mode

        if(self.mode == "update"):
            if(self.accessControl.getUsername() != None):
                self.lineEdit_username.setText(self.accessControl.getUsername())
            if(self.accessControl.getName() != None):
                self.lineEdit_name.setText(self.accessControl.getName())
            if(self.accessControl.getAccess() != None):
                self.comboBox.setCurrentIndex(self.accessControl.getAccess())

    def loadAccessModes(self):
        accessmodes = self.accessControl.getAccessModes()
        for mode in accessmodes:
            self.comboBox.insertItem(mode['id'], mode['bezeichnung'])

    def on_buttonBox_accepted(self):
        if(self.lineEdit_username.text() != ""):
            username_old=self.accessControl.getUsername()
            self.accessControl.setUsername(self.lineEdit_username.text())
            self.accessControl.setName(self.lineEdit_name.text())
            self.accessControl.setAccess(self.comboBox.currentIndex())
            if(self.mode == "new"):
                if(self.accessControl.checkUserExists() == False):
                    self.accessControl.insertUser()
                else:
                    QMessageBox.information(None,u"Benutzer hinzufügen",u"Der eingegebene Benutzername existiert bereits in der Datenbank.")
            elif(self.mode == "update"):
               self.accessControl.updateUser(username_old)
