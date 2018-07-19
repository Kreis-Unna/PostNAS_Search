# -*- coding: utf-8 -*-
"""
/***************************************************************************
    PostNAS_Search
    -------------------
    Date                : June 2016
    copyright          : (C) 2016 by Kreis-Unna
    email                : marvin.kinberger@kreis-unna.de
 ***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""

import os
from qgis.PyQt import QtGui,uic
from qgis.PyQt.QtWidgets import QDialog,QMessageBox,QTableWidget,QTableWidgetItem
from qgis.PyQt.QtCore import *
from .PostNAS_AccessControl import PostNAS_AccessControl
from .PostNAS_AccessControl_UserDialog import PostNAS_AccessControl_UserDialog
import qgis.gui
FORM_CLASS, _ = uic.loadUiType(os.path.join(os.path.dirname(__file__), 'PostNAS_ConfDialogBase.ui'))

class PostNAS_ConfDialog(QDialog, FORM_CLASS):
    def __init__(self, iface = None, parent = None):
        super(PostNAS_ConfDialog, self).__init__(parent)
        self.setupUi(self)
        self.accessControl = PostNAS_AccessControl()
        settings = QSettings("PostNAS", "PostNAS-Suche")
        self.leHOST.setText(settings.value("host", ""))
        self.lePORT.setText(settings.value("port", "5432"))
        self.leDBNAME.setText(settings.value("dbname", ""))
        self.leUID.setText(settings.value("user", ""))
        self.lePWD.setText(settings.value("password", ""))

        if hasattr(qgis.gui,'QgsAuthConfigSelect'):
            self.authCfgSelect = qgis.gui.QgsAuthConfigSelect( self, "postgres" )
            self.tabWidget.insertTab( 1, self.authCfgSelect, "Konfigurationen" )
            authcfg = settings.value( "authcfg", "" )
            if authcfg:
                self.tabWidget.setCurrentIndex( 1 )
                self.authCfgSelect.setConfigId( authcfg )

    def showEvent(self, QShowEvent):
        self.loadAccessTable()
        if(self.accessControl.checkAccessControlIsActive() == True and self.accessControl.checkUserIsAdmin() == True):
            self.enableAccessControl()
        elif(self.accessControl.checkAccessControlIsActive() == True and self.accessControl.checkUserIsAdmin() == False):
            self.disableAccessControl()
            self.checkBox.setEnabled(False)
            self.checkBox.setCheckState(Qt.Checked)

    def on_buttonBox_accepted(self):
        settings = QSettings("PostNAS", "PostNAS-Suche")
        settings.setValue("host", self.leHOST.text())
        settings.setValue("port", self.lePORT.text())
        settings.setValue("dbname", self.leDBNAME.text())
        settings.setValue("user", self.leUID.text())
        settings.setValue("password", self.lePWD.text())

        if hasattr(qgis.gui,'QgsAuthConfigSelect'):
            settings.setValue( "authcfg", self.authCfgSelect.configId() )

        if(self.checkBox.checkState() == Qt.Checked):
            settings.setValue("accessControl",1)
        else:
            settings.setValue("accessControl",0)

        QDialog.accept(self)

    def on_checkBox_stateChanged(self,state):
        if(self.accessControl.checkUserIsAdmin() == True or self.accessControl.checkAccessTable() == False):
            if(state == Qt.Unchecked):
                self.disableAccessControl()
            elif(state == Qt.Checked):
                self.enableAccessControl()
        elif(self.checkBox.checkState() == Qt.Checked and self.checkBox.isEnabled() == True):
            self.checkBox.setCheckState(Qt.Unchecked)
            message = QMessageBox()
            message.setWindowTitle("Zugriffskontrolle")
            message.setText(u"Sie besitzen keine Administrationsrechte für die Zugriffskontrolle.")
            message.setInformativeText(u"Bitte wenden Sie sich an Ihren Administrator.")
            message.setIcon(QMessageBox.Critical)
            message.exec_()

    def enableAccessControl(self):
        # Prüfen, ob die Access Tabelle in der Datenbank vorhanden ist.
        if(self.accessControl.checkAccessTable() == False):
            message = QMessageBox()
            message.setWindowTitle("Zugriffskontrolle")
            message.setText(u"Derzeit ist keine Tabelle für die Zugriffskontrolle in der Datenbank vorhanden.")
            message.setInformativeText(u"Möchten Sie die Tabelle in der Datenbank anlegen?")
            message.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            message.setIcon(QMessageBox.Information)
            if(message.exec_() == QMessageBox.Yes):
                if(self.accessControl.createAccessTable() == False):
                    self.disableAccessControl()
                else:
                    self.enableAccessControl()
            else:
                self.checkBox.setCheckState(Qt.Unchecked)
                self.disableAccessControl()
        # Prüfen, ob ein Administrator für die Zugriffskontrolle eingetragen ist
        elif(self.accessControl.checkAccessTableHasAdmin() == False):
            message = QMessageBox()
            message.setWindowTitle("Zugriffskontrolle")
            message.setText(u"Derzeit ist kein Administrator für die Zugriffskontrolle hinterlegt.")
            message.setInformativeText(u"Möchten Ihren Benutzernamen als Administrator hinterlegen?")
            message.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            message.setIcon(QMessageBox.Information)
            if(message.exec_() == QMessageBox.Yes):
                if(self.accessControl.insertAdminUser() == True):
                    self.enableAccessControl()
                    self.loadAccessTable()
                else:
                    QMessageBox.critical(None,"Fehler","Es ist ein Fehler aufgetreten.")
                    self.disableAccessControl()
        # Prüfen, ob angemeldeter Benutzer ein Admin ist
        elif(self.accessControl.checkUserIsAdmin() == True):
            self.checkBox.setCheckState(Qt.Checked)
            self.userTable.setEnabled(True)
            self.accessControlButtonAdd.setEnabled(True)
            self.accessControlButtonAdd.setEnabled(True)
            self.accessControlButtonEdit.setEnabled(False)
            self.accessControlButtonDelete.setEnabled(False)

    def disableAccessControl(self):
        self.checkBox.setCheckState(Qt.Unchecked)
        self.userTable.setEnabled(False)
        self.accessControlButtonAdd.setEnabled(False)
        self.accessControlButtonEdit.setEnabled(False)
        self.accessControlButtonDelete.setEnabled(False)

    def on_buttonBox_rejected(self):
        QDialog.reject(self)

    def loadAccessTable(self):
        self.userTable.setRowCount(0)
        self.userTable.setSortingEnabled(False)

        results = self.accessControl.loadUserAccessTable()
        for user in results:
            rowCount = self.userTable.rowCount()
            self.userTable.insertRow(rowCount)
            if(user['username'] != None):
                self.userTable.setItem(rowCount,0,QTableWidgetItem(user['username']))
            if(user['name'] != None):
                self.userTable.setItem(rowCount,1,QTableWidgetItem(user['name']))
            if(user['access'] != None):
                self.userTable.setItem(rowCount,2,QTableWidgetItem(user['access']))
        self.userTable.setSortingEnabled(True)
        self.userTable.sortByColumn(0,Qt.AscendingOrder)
        self.userTable.resizeColumnsToContents()

    def on_userTable_itemSelectionChanged(self):
        if(len(self.userTable.selectedItems()) > 0):
            self.accessControlButtonEdit.setEnabled(True)
            self.accessControlButtonDelete.setEnabled(True)
        else:
            self.accessControlButtonEdit.setEnabled(False)
            self.accessControlButtonDelete.setEnabled(False)

    def getSelectedUser(self):
        if(len(self.userTable.selectedItems()) > 0):
            return self.userTable.selectionModel().selectedRows()[0].data()

    def on_accessControlButtonAdd_released(self):
        userDialog = PostNAS_AccessControl_UserDialog("new")
        userDialog.exec_()
        self.loadAccessTable()

    def on_accessControlButtonEdit_released(self):
        updateAccessControl = PostNAS_AccessControl()
        updateAccessControl.setUsername(self.getSelectedUser())
        userDialog = PostNAS_AccessControl_UserDialog("update",updateAccessControl)
        userDialog.exec_()
        self.loadAccessTable()

    def on_accessControlButtonDelete_released(self):
        user = PostNAS_AccessControl(self.getSelectedUser())
        message = QMessageBox()
        message.setWindowTitle("Zugriffskontrolle")
        message.setText(u"Möchten Sie den Benutzer wirklich löschen?")
        message.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        message.setIcon(QMessageBox.Information)
        if(message.exec_() == QMessageBox.Yes):
            if(user.deleteUser() == True):
                self.loadAccessTable()
