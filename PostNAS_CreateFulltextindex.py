# -*- coding: utf-8 -*-
"""
/***************************************************************************
    PostNAS_Search
    -------------------
    Date                : June 2016
    copyright          : (C) 2016 by Kreis-Unna
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

import os, locale
from PyQt4 import QtGui, uic
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtSql import *
import time

FORM_CLASS, _ = uic.loadUiType(os.path.join(os.path.dirname(__file__), 'PostNAS_FulltextindexInProgress.ui'))

class PostNAS_CreateFulltextindex(QtGui.QDialog, FORM_CLASS):
    def __init__(self, iface, parent=None):
        super(PostNAS_CreateFulltextindex, self).__init__(parent)
        self.setupUi(self)
        self.setWindowTitle(u'Volltextindex')
        locale.setlocale(locale.LC_ALL, 'german')

    def exec_(self):
        self.open()
        self.createFulltextindex()
        self.close()

    def createFulltextindex(self):
        if(self.checkPostnasSeachTable() == False):
            if(self.createIndexTable() == False):
                QMessageBox.critical(None,"Fehler",u"Indextabelle wurde nicht angelegt.\r\nPrüfen Sie die Schreibrechte des Datenbankbenutzers.")
                return False
        self.updateIndex()

    def createIndexTable(self):
        self.sqlCreateTable = "CREATE TABLE postnas_search(gml_id character(16), vector tsvector) WITH (OIDS=FALSE);"

        if(hasattr(self,"db") == False):
            self.loadDbSettings()
            self.db.open()
        self.queryCreate = QSqlQuery(self.db)
        self.queryCreate.exec_(self.sqlCreateTable)
        self.db.close()

        if(self.checkPostnasSeachTable() == True):
            return True
        else:
            return False


    def updateIndex(self):
        self.sqlBegin = "BEGIN;"
        self.sqlDelete = "DELETE FROM postnas_search;"
        self.sqlAktuell = "INSERT INTO postnas_search ( \
            SELECT ax_flurstueck.gml_id, \
                to_tsvector('german'::regconfig, \
                    CASE WHEN ax_flurstueck.gemarkungsnummer IS NULL THEN '0000' ELSE ax_flurstueck.gemarkungsnummer END || ' ' || \
                    CASE WHEN ax_flurstueck.flurnummer IS NULL THEN '000' ELSE ax_flurstueck.flurnummer END || ' ' || \
                    CASE WHEN ax_flurstueck.zaehler IS NULL THEN 0 ELSE ax_flurstueck.zaehler END || ' ' || \
                    CASE WHEN ax_flurstueck.nenner IS NULL THEN '' ELSE ax_flurstueck.nenner END || ' ' || \
                    CASE WHEN ax_flurstueck.gemarkungsnummer IS NULL THEN '0000' ELSE ax_flurstueck.gemarkungsnummer END || \
                    CASE WHEN ax_flurstueck.flurnummer IS NULL THEN '000' ELSE ax_flurstueck.flurnummer END || \
                    CASE WHEN ax_flurstueck.zaehler IS NULL THEN 0 ELSE ax_flurstueck.zaehler END || \
                    CASE WHEN ax_flurstueck.nenner IS NULL THEN '' ELSE ax_flurstueck.nenner END || ' ' || \
                    CASE WHEN ax_flurstueck.gemarkungsnummer IS NULL THEN '0000' ELSE lpad(ax_flurstueck.gemarkungsnummer::text, 4, '0'::text) END || \
                    CASE WHEN ax_flurstueck.flurnummer IS NULL THEN '000' ELSE lpad(ax_flurstueck.flurnummer::text, 3, '0'::text) END || \
                    CASE WHEN ax_flurstueck.zaehler IS NULL THEN '' ELSE lpad(ax_flurstueck.zaehler::text, 5, '0'::text) END || \
                    CASE WHEN ax_flurstueck.nenner IS NULL THEN '' ELSE lpad(ax_flurstueck.nenner::text, 3, '0'::text) END || ' ' || \
                    CASE WHEN ax_flurstueck.gemarkungsnummer IS NULL THEN '0000' ELSE ax_flurstueck.gemarkungsnummer END || '-' || \
                    CASE WHEN ax_flurstueck.flurnummer IS NULL THEN '000' ELSE ax_flurstueck.flurnummer END || '-' || \
                    CASE WHEN ax_flurstueck.zaehler IS NULL THEN 0 ELSE ax_flurstueck.zaehler END || '-' || \
                    CASE WHEN ax_flurstueck.nenner IS NULL THEN '' ELSE '/' || ax_flurstueck.nenner END || ' ' || \
                    CASE WHEN ax_flurstueck.gemarkungsnummer IS NULL THEN '0000' ELSE lpad(ax_flurstueck.gemarkungsnummer::text, 4, '0'::text) END || '-' || \
                    CASE WHEN ax_flurstueck.flurnummer IS NULL THEN '000' ELSE lpad(ax_flurstueck.flurnummer::text, 3, '0'::text) END || '-' || \
                    CASE WHEN ax_flurstueck.zaehler IS NULL THEN '' ELSE lpad(ax_flurstueck.zaehler::text, 5, '0'::text) END || '-' || \
                    CASE WHEN ax_flurstueck.nenner IS NULL THEN '' ELSE '/' || lpad(ax_flurstueck.nenner::text, 3, '0'::text) END || ' ' || \
                    CASE WHEN ax_gemarkung.bezeichnung IS NOT NULL THEN ax_gemarkung.bezeichnung END) \
            FROM ax_flurstueck \
            JOIN ax_gemarkung ON ax_flurstueck.land::text = ax_gemarkung.land::text AND ax_flurstueck.gemarkungsnummer::text = ax_gemarkung.gemarkungsnummer::text AND ax_gemarkung.endet IS NULL \
            WHERE ax_flurstueck.endet IS NULL);"
        self.sqlHistorisch = "INSERT INTO postnas_search ( \
                SELECT ax_historischesflurstueck.gml_id, \
                    to_tsvector('german'::regconfig, \
                        CASE WHEN ax_historischesflurstueck.gemarkungsnummer IS NULL THEN '0000' ELSE ax_historischesflurstueck.gemarkungsnummer END || ' ' || \
                        CASE WHEN ax_historischesflurstueck.flurnummer IS NULL THEN '000' ELSE ax_historischesflurstueck.flurnummer END || ' ' || \
                        CASE WHEN ax_historischesflurstueck.zaehler IS NULL THEN '' ELSE ax_historischesflurstueck.zaehler END || ' ' || \
                        CASE WHEN ax_historischesflurstueck.nenner IS NULL THEN '' ELSE ax_historischesflurstueck.nenner END || ' ' || \
                        CASE WHEN ax_historischesflurstueck.gemarkungsnummer IS NULL THEN '0000' ELSE ax_historischesflurstueck.gemarkungsnummer END || \
                        CASE WHEN ax_historischesflurstueck.flurnummer IS NULL THEN '000' ELSE ax_historischesflurstueck.flurnummer END || \
                        CASE WHEN ax_historischesflurstueck.zaehler IS NULL THEN '' ELSE ax_historischesflurstueck.zaehler END || \
                        CASE WHEN ax_historischesflurstueck.nenner IS NULL THEN '' ELSE ax_historischesflurstueck.nenner END || ' ' || \
                        CASE WHEN ax_historischesflurstueck.gemarkungsnummer IS NULL THEN '0000' ELSE lpad(ax_historischesflurstueck.gemarkungsnummer::text, 4, '0'::text) END || \
                        CASE WHEN ax_historischesflurstueck.flurnummer IS NULL THEN '000' ELSE lpad(ax_historischesflurstueck.flurnummer::text, 3, '0'::text) END || \
                        CASE WHEN ax_historischesflurstueck.zaehler IS NULL THEN '' ELSE lpad(ax_historischesflurstueck.zaehler::text, 5, '0'::text) END || \
                        CASE WHEN ax_historischesflurstueck.nenner IS NULL THEN '' ELSE lpad(ax_historischesflurstueck.nenner::text, 3, '0'::text) END || ' ' || \
                        CASE WHEN ax_historischesflurstueck.gemarkungsnummer IS NULL THEN '0000' ELSE ax_historischesflurstueck.gemarkungsnummer END || '-' || \
                        CASE WHEN ax_historischesflurstueck.flurnummer IS NULL THEN '000' ELSE ax_historischesflurstueck.flurnummer END || '-' || \
                        CASE WHEN ax_historischesflurstueck.zaehler IS NULL THEN '' ELSE ax_historischesflurstueck.zaehler END || '-' || \
                        CASE WHEN ax_historischesflurstueck.nenner IS NULL THEN '' ELSE '/' || ax_historischesflurstueck.nenner END || ' ' || \
                        CASE WHEN ax_historischesflurstueck.gemarkungsnummer IS NULL THEN '0000' ELSE lpad(ax_historischesflurstueck.gemarkungsnummer::text, 4, '0'::text) END || '-' || \
                        CASE WHEN ax_historischesflurstueck.flurnummer IS NULL THEN '000' ELSE lpad(ax_historischesflurstueck.flurnummer::text, 3, '0'::text) END || '-' || \
                        CASE WHEN ax_historischesflurstueck.zaehler IS NULL THEN '' ELSE lpad(ax_historischesflurstueck.zaehler::text, 5, '0'::text) END || '-' || \
                        CASE WHEN ax_historischesflurstueck.nenner IS NULL THEN '' ELSE '/' || lpad(ax_historischesflurstueck.nenner::text, 3, '0'::text) END || ' ' || \
                        CASE WHEN ax_gemarkung.bezeichnung IS NOT NULL THEN ax_gemarkung.bezeichnung END \
                    ) \
                FROM ax_historischesflurstueck \
            JOIN ax_gemarkung ON ax_historischesflurstueck.land::text = ax_gemarkung.land::text AND ax_historischesflurstueck.gemarkungsnummer::text = ax_gemarkung.gemarkungsnummer::text AND ax_gemarkung.endet IS NULL \
            WHERE ax_historischesflurstueck.endet IS NULL);"
        self.sqlAdresse = "INSERT INTO postnas_search ( \
            SELECT ax_lagebezeichnungmithausnummer.gml_id, to_tsvector('german', ax_lagebezeichnungkatalogeintrag.bezeichnung || ' ' || ax_lagebezeichnungmithausnummer.hausnummer) \
		    FROM ax_lagebezeichnungkatalogeintrag \
		    JOIN ax_gemeinde ON ax_lagebezeichnungkatalogeintrag.land = ax_gemeinde.land AND ax_lagebezeichnungkatalogeintrag.regierungsbezirk = ax_gemeinde.regierungsbezirk AND ax_lagebezeichnungkatalogeintrag.kreis = ax_gemeinde.kreis AND ax_lagebezeichnungkatalogeintrag.gemeinde = ax_gemeinde.gemeinde AND ax_gemeinde.endet IS NULL \
		    JOIN ax_lagebezeichnungmithausnummer ON ax_lagebezeichnungkatalogeintrag.land = ax_lagebezeichnungmithausnummer.land AND ax_lagebezeichnungkatalogeintrag.regierungsbezirk = ax_lagebezeichnungmithausnummer.regierungsbezirk AND ax_lagebezeichnungkatalogeintrag.kreis = ax_lagebezeichnungmithausnummer.kreis AND ax_lagebezeichnungkatalogeintrag.gemeinde = ax_lagebezeichnungmithausnummer.gemeinde AND ax_lagebezeichnungkatalogeintrag.lage = ax_lagebezeichnungmithausnummer.lage AND ax_lagebezeichnungmithausnummer.endet IS NULL \
		    WHERE ax_lagebezeichnungkatalogeintrag.endet IS NULL);";

        self.sqlCommit = "COMMIT;"

        self.loadDbSettings()
        self.db.open()
        self.queryBegin = QSqlQuery(self.db)
        self.queryBegin.exec_(self.sqlBegin)
        self.queryDelete = QSqlQuery(self.db)
        self.queryDelete.exec_(self.sqlDelete)
        self.queryAktuell = QSqlQuery(self.db)
        self.queryAktuell.exec_(self.sqlAktuell)
        self.queryHistorisch = QSqlQuery(self.db)
        self.queryHistorisch.exec_(self.sqlHistorisch)
        self.queryAdresse = QSqlQuery(self.db)
        self.queryAdresse.exec_(self.sqlAdresse)

        self.queryCommit = QSqlQuery(self.db)
        self.queryCommit.exec_(self.sqlCommit)
        self.db.close()

    def checkPostnasSeachTable(self):
        sql = "SELECT table_name FROM information_schema.tables WHERE table_name = 'postnas_search'";

        if(hasattr(self,"db") == False):
            self.loadDbSettings()
            self.db.open()
        query = QSqlQuery(self.db)
        query.exec_(sql)

        if(query.size() > 0):
            return True
        else:
            return False

    def loadDbSettings(self):
        settings = QSettings("PostNAS", "PostNAS-Suche")

        self.dbHost = settings.value("host", "")
        self.dbDatabasename = settings.value("dbname", "")
        self.dbPort = settings.value("port", "5432")
        self.dbUsername = settings.value("user", "")
        self.dbPassword = settings.value("password", "")

        authcfg = settings.value( "authcfg", "" )

        if authcfg != "" and hasattr(qgis.core,'QgsAuthManager'):
            amc = qgis.core.QgsAuthMethodConfig()
            qgis.core.QgsAuthManager.instance().loadAuthenticationConfig( authcfg, amc, True)
            self.dbUsername = amc.config( "username", self.dbUsername )
            self.dbPassword = amc.config( "password", self.dbPassword )

        self.db = QSqlDatabase.addDatabase("QPSQL")
        self.db.setHostName(self.dbHost)
        self.db.setPort(int(self.dbPort))
        self.db.setDatabaseName(self.dbDatabasename)
        self.db.setUserName(self.dbUsername)
        self.db.setPassword(self.dbPassword)