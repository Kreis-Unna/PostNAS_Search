# -*- coding: utf-8 -*-
"""
/***************************************************************************
    PostNAS_Search
    -------------------
    Date                : June 2016
    copyright          : (C) 2016 by Kreis-Unna
    email                : marvin.brandt@kreis-unna.de
 ***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtSql import *
from PyQt4 import QtGui, uic, QtCore
from qgis.core import *
import qgis.core
from PostNAS_SearchDialogBase import Ui_PostNAS_SearchDialogBase
from PostNAS_AccessControl import PostNAS_AccessControl

class PostNAS_SearchDialog(QtGui.QDialog, Ui_PostNAS_SearchDialogBase):
    def __init__(self, parent=None,  iface=None):
        super(PostNAS_SearchDialog, self).__init__(parent)
        self.setupUi(self)
        self.iface = iface

        self.map = QgsMapLayerRegistry.instance()
        self.treeWidget.setColumnCount(1)

        self.indexWarning = True

        self.accessControl = PostNAS_AccessControl()

    def on_lineEdit_returnPressed(self):
        searchString = self.lineEdit.text()
        QApplication.setOverrideCursor(Qt.WaitCursor)
        if(len(searchString) > 0):
            self.loadDbSettings()
            self.db.open()
            query = QSqlQuery(self.db)
            self.treeWidget.clear()

            if(self.checkPostnasSeachTable() == False):
                if(self.indexWarning == True):
                    QMessageBox.warning(None,"Suche beschleunigen",u"Auf der ALKIS-Datenbank ist kein Volltextindex für die Suche vorhanden. Dieser kann die Suchperformance deutlich erhöhen. .\r\nDer Volltextindes unter\r\n    \"Datenbank -> PostNAS-Suche -> Volltextindex erstellen\"\r\nerstellen werden.")
                    self.indexWarning = False
            else:
                self.indexWarning = False

            #------------------------- Flurstück suchen
            if(self.checkPostnasSeachTable() == True):
                sqlFlurstueck = "SELECT gml_id FROM postnas_search WHERE vector @@ to_tsquery('german', '" + unicode(self.getSearchStringFlurstueck()) + "') AND typ LIKE 'flurstueck%'"
            else:
                sqlFlurstueck = "SELECT ax_flurstueck.gml_id \
                FROM ax_flurstueck \
                LEFT JOIN ax_gemarkung ON ax_flurstueck.land::text = ax_gemarkung.land::text AND ax_flurstueck.gemarkungsnummer::text = ax_gemarkung.gemarkungsnummer::text AND ax_gemarkung.endet IS NULL \
                WHERE to_tsvector('german'::regconfig, CASE WHEN ax_flurstueck.gemarkungsnummer IS NULL THEN '0000' ELSE ax_flurstueck.gemarkungsnummer END || ' ' || CASE WHEN ax_flurstueck.flurnummer IS NULL THEN '000' ELSE ax_flurstueck.flurnummer END || ' ' || CASE WHEN ax_flurstueck.zaehler IS NULL THEN 0 ELSE ax_flurstueck.zaehler END || ' ' || CASE WHEN ax_flurstueck.nenner IS NULL THEN '' ELSE ax_flurstueck.nenner END || ' ' || CASE WHEN ax_flurstueck.gemarkungsnummer IS NULL THEN '0000' ELSE ax_flurstueck.gemarkungsnummer END || CASE WHEN ax_flurstueck.flurnummer IS NULL THEN '000' ELSE ax_flurstueck.flurnummer END || CASE WHEN ax_flurstueck.zaehler IS NULL THEN 0 ELSE ax_flurstueck.zaehler END || CASE WHEN ax_flurstueck.nenner IS NULL THEN '' ELSE ax_flurstueck.nenner END || ' ' || CASE WHEN ax_flurstueck.gemarkungsnummer IS NULL THEN '0000' ELSE lpad(ax_flurstueck.gemarkungsnummer::text, 4, '0'::text) END || CASE WHEN ax_flurstueck.flurnummer IS NULL THEN '000' ELSE lpad(ax_flurstueck.flurnummer::text, 3, '0'::text) END || CASE WHEN ax_flurstueck.zaehler IS NULL THEN '' ELSE lpad(ax_flurstueck.zaehler::text, 5, '0'::text) END || CASE WHEN ax_flurstueck.nenner IS NULL THEN '' ELSE lpad(ax_flurstueck.nenner::text, 3, '0'::text) END || ' ' || CASE WHEN ax_flurstueck.gemarkungsnummer IS NULL THEN '0000' ELSE ax_flurstueck.gemarkungsnummer END || '-' || CASE WHEN ax_flurstueck.flurnummer IS NULL THEN '000' ELSE ax_flurstueck.flurnummer END || '-' || CASE WHEN ax_flurstueck.zaehler IS NULL THEN 0 ELSE ax_flurstueck.zaehler END || '-' || CASE WHEN ax_flurstueck.nenner IS NULL THEN '' ELSE '/' || ax_flurstueck.nenner END || ' ' || CASE WHEN ax_flurstueck.gemarkungsnummer IS NULL THEN '0000' ELSE lpad(ax_flurstueck.gemarkungsnummer::text, 4, '0'::text) END || '-' || CASE WHEN ax_flurstueck.flurnummer IS NULL THEN '000' ELSE lpad(ax_flurstueck.flurnummer::text, 3, '0'::text) END || '-' || CASE WHEN ax_flurstueck.zaehler IS NULL THEN '' ELSE lpad(ax_flurstueck.zaehler::text, 5, '0'::text) END || '-' || CASE WHEN ax_flurstueck.nenner IS NULL THEN '' ELSE '/' || lpad(ax_flurstueck.nenner::text, 3, '0'::text) END || ' ' || CASE WHEN ax_gemarkung.bezeichnung IS NOT NULL THEN ax_gemarkung.bezeichnung ELSE '' END) @@ to_tsquery('german', '" + unicode(self.getSearchStringFlurstueck()) + "') \
                UNION \
                SELECT ax_historischesflurstueck.gml_id \
                FROM ax_historischesflurstueck \
                LEFT JOIN ax_gemarkung ON ax_historischesflurstueck.land::text = ax_gemarkung.land::text AND ax_historischesflurstueck.gemarkungsnummer::text = ax_gemarkung.gemarkungsnummer::text AND ax_gemarkung.endet IS NULL \
                WHERE to_tsvector('german'::regconfig, CASE WHEN ax_historischesflurstueck.gemarkungsnummer IS NULL THEN '0000' ELSE ax_historischesflurstueck.gemarkungsnummer END || ' ' || CASE WHEN ax_historischesflurstueck.flurnummer IS NULL THEN '000' ELSE ax_historischesflurstueck.flurnummer END || ' ' || CASE WHEN ax_historischesflurstueck.zaehler IS NULL THEN '0' ELSE ax_historischesflurstueck.zaehler END || ' ' || CASE WHEN ax_historischesflurstueck.nenner IS NULL THEN '' ELSE ax_historischesflurstueck.nenner END || ' ' || CASE WHEN ax_historischesflurstueck.gemarkungsnummer IS NULL THEN '0000' ELSE ax_historischesflurstueck.gemarkungsnummer END || CASE WHEN ax_historischesflurstueck.flurnummer IS NULL THEN '000' ELSE ax_historischesflurstueck.flurnummer END || CASE WHEN ax_historischesflurstueck.zaehler IS NULL THEN '0' ELSE ax_historischesflurstueck.zaehler END || CASE WHEN ax_historischesflurstueck.nenner IS NULL THEN '' ELSE ax_historischesflurstueck.nenner END || ' ' || CASE WHEN ax_historischesflurstueck.gemarkungsnummer IS NULL THEN '0000' ELSE lpad(ax_historischesflurstueck.gemarkungsnummer::text, 4, '0'::text) END || CASE WHEN ax_historischesflurstueck.flurnummer IS NULL THEN '000' ELSE lpad(ax_historischesflurstueck.flurnummer::text, 3, '0'::text) END || CASE WHEN ax_historischesflurstueck.zaehler IS NULL THEN '' ELSE lpad(ax_historischesflurstueck.zaehler::text, 5, '0'::text) END || CASE WHEN ax_historischesflurstueck.nenner IS NULL THEN '' ELSE lpad(ax_historischesflurstueck.nenner::text, 3, '0'::text) END || ' ' || CASE WHEN ax_historischesflurstueck.gemarkungsnummer IS NULL THEN '0000' ELSE ax_historischesflurstueck.gemarkungsnummer END || '-' || CASE WHEN ax_historischesflurstueck.flurnummer IS NULL THEN '000' ELSE ax_historischesflurstueck.flurnummer END || '-' || CASE WHEN ax_historischesflurstueck.zaehler IS NULL THEN '0' ELSE ax_historischesflurstueck.zaehler END || '-' || CASE WHEN ax_historischesflurstueck.nenner IS NULL THEN '' ELSE '/' || ax_historischesflurstueck.nenner END || ' ' || CASE WHEN ax_historischesflurstueck.gemarkungsnummer IS NULL THEN '0000' ELSE lpad(ax_historischesflurstueck.gemarkungsnummer::text, 4, '0'::text) END || '-' || CASE WHEN ax_historischesflurstueck.flurnummer IS NULL THEN '000' ELSE lpad(ax_historischesflurstueck.flurnummer::text, 3, '0'::text) END || '-' || CASE WHEN ax_historischesflurstueck.zaehler IS NULL THEN '' ELSE lpad(ax_historischesflurstueck.zaehler::text, 5, '0'::text) END || '-' || CASE WHEN ax_historischesflurstueck.nenner IS NULL THEN '' ELSE '/' || lpad(ax_historischesflurstueck.nenner::text, 3, '0'::text) END || ' ' || CASE WHEN ax_gemarkung.bezeichnung IS NOT NULL THEN ax_gemarkung.bezeichnung ELSE '' END) @@ to_tsquery('german', '" + unicode(self.getSearchStringFlurstueck()) + "') \
                UNION \
                SELECT ax_historischesflurstueckohneraumbezug.gml_id \
                FROM ax_historischesflurstueckohneraumbezug \
                LEFT JOIN ax_gemarkung ON ax_historischesflurstueckohneraumbezug.land::text = ax_gemarkung.land::text AND ax_historischesflurstueckohneraumbezug.gemarkungsnummer::text = ax_gemarkung.gemarkungsnummer::text AND ax_gemarkung.endet IS NULL \
                WHERE to_tsvector('german'::regconfig, CASE WHEN ax_historischesflurstueckohneraumbezug.gemarkungsnummer IS NULL THEN '0000' ELSE ax_historischesflurstueckohneraumbezug.gemarkungsnummer END || ' ' || CASE WHEN ax_historischesflurstueckohneraumbezug.flurnummer IS NULL THEN '000' ELSE ax_historischesflurstueckohneraumbezug.flurnummer END || ' ' || CASE WHEN ax_historischesflurstueckohneraumbezug.zaehler IS NULL THEN '0' ELSE ax_historischesflurstueckohneraumbezug.zaehler END || ' ' || CASE WHEN ax_historischesflurstueckohneraumbezug.nenner IS NULL THEN '' ELSE ax_historischesflurstueckohneraumbezug.nenner END || ' ' || CASE WHEN ax_historischesflurstueckohneraumbezug.gemarkungsnummer IS NULL THEN '0000' ELSE ax_historischesflurstueckohneraumbezug.gemarkungsnummer END || CASE WHEN ax_historischesflurstueckohneraumbezug.flurnummer IS NULL THEN '000' ELSE ax_historischesflurstueckohneraumbezug.flurnummer END || CASE WHEN ax_historischesflurstueckohneraumbezug.zaehler IS NULL THEN '0' ELSE ax_historischesflurstueckohneraumbezug.zaehler END || CASE WHEN ax_historischesflurstueckohneraumbezug.nenner IS NULL THEN '' ELSE ax_historischesflurstueckohneraumbezug.nenner END || ' ' || CASE WHEN ax_historischesflurstueckohneraumbezug.gemarkungsnummer IS NULL THEN '0000' ELSE lpad(ax_historischesflurstueckohneraumbezug.gemarkungsnummer::text, 4, '0'::text) END || CASE WHEN ax_historischesflurstueckohneraumbezug.flurnummer IS NULL THEN '000' ELSE lpad(ax_historischesflurstueckohneraumbezug.flurnummer::text, 3, '0'::text) END || CASE WHEN ax_historischesflurstueckohneraumbezug.zaehler IS NULL THEN '' ELSE lpad(ax_historischesflurstueckohneraumbezug.zaehler::text, 5, '0'::text) END || CASE WHEN ax_historischesflurstueckohneraumbezug.nenner IS NULL THEN '' ELSE lpad(ax_historischesflurstueckohneraumbezug.nenner::text, 3, '0'::text) END || ' ' || CASE WHEN ax_historischesflurstueckohneraumbezug.gemarkungsnummer IS NULL THEN '0000' ELSE ax_historischesflurstueckohneraumbezug.gemarkungsnummer END || '-' || CASE WHEN ax_historischesflurstueckohneraumbezug.flurnummer IS NULL THEN '000' ELSE ax_historischesflurstueckohneraumbezug.flurnummer END || '-' || CASE WHEN ax_historischesflurstueckohneraumbezug.zaehler IS NULL THEN '0' ELSE ax_historischesflurstueckohneraumbezug.zaehler END || '-' || CASE WHEN ax_historischesflurstueckohneraumbezug.nenner IS NULL THEN '' ELSE '/' || ax_historischesflurstueckohneraumbezug.nenner END || ' ' || CASE WHEN ax_historischesflurstueckohneraumbezug.gemarkungsnummer IS NULL THEN '0000' ELSE lpad(ax_historischesflurstueckohneraumbezug.gemarkungsnummer::text, 4, '0'::text) END || '-' || CASE WHEN ax_historischesflurstueckohneraumbezug.flurnummer IS NULL THEN '000' ELSE lpad(ax_historischesflurstueckohneraumbezug.flurnummer::text, 3, '0'::text) END || '-' || CASE WHEN ax_historischesflurstueckohneraumbezug.zaehler IS NULL THEN '' ELSE lpad(ax_historischesflurstueckohneraumbezug.zaehler::text, 5, '0'::text) END || '-' || CASE WHEN ax_historischesflurstueckohneraumbezug.nenner IS NULL THEN '' ELSE '/' || lpad(ax_historischesflurstueckohneraumbezug.nenner::text, 3, '0'::text) END || ' ' || CASE WHEN ax_gemarkung.bezeichnung IS NOT NULL THEN ax_gemarkung.bezeichnung ELSE '' END) @@ to_tsquery('german', '" + unicode(self.getSearchStringFlurstueck()) + "')"
            query.exec_(sqlFlurstueck)
            if(query.size() > 0):
                item_titleFlurstuecke = QTreeWidgetItem(self.treeWidget)
                item_titleFlurstuecke.setText(0,u"Flurstücke")
                item_titleFlurstuecke.setChildIndicatorPolicy(QTreeWidgetItem.ShowIndicator)

            #------------------------------------------ Adresse suchen
            if(self.checkPostnasSeachTable() == True):
                sqlAdresse = "SELECT gml_id FROM postnas_search WHERE vector @@ to_tsquery('german', '" + unicode(self.getSearchStringAdresse()) + "') AND typ = 'adresse'"
            else:
                sqlAdresse = "SELECT ax_lagebezeichnungkatalogeintrag.gml_id FROM ax_lagebezeichnungkatalogeintrag LEFT JOIN ax_gemeinde ON ax_lagebezeichnungkatalogeintrag.land = ax_gemeinde.land AND ax_lagebezeichnungkatalogeintrag.regierungsbezirk = ax_gemeinde.regierungsbezirk AND ax_lagebezeichnungkatalogeintrag.kreis = ax_gemeinde.kreis AND ax_lagebezeichnungkatalogeintrag.gemeinde = ax_gemeinde.gemeinde AND ax_gemeinde.endet IS NULL JOIN ax_lagebezeichnungmithausnummer ON ax_lagebezeichnungkatalogeintrag.land = ax_lagebezeichnungmithausnummer.land AND ax_lagebezeichnungkatalogeintrag.regierungsbezirk = ax_lagebezeichnungmithausnummer.regierungsbezirk AND ax_lagebezeichnungkatalogeintrag.kreis = ax_lagebezeichnungmithausnummer.kreis AND ax_lagebezeichnungkatalogeintrag.gemeinde = ax_lagebezeichnungmithausnummer.gemeinde AND ax_lagebezeichnungkatalogeintrag.lage = ax_lagebezeichnungmithausnummer.lage AND ax_lagebezeichnungmithausnummer.endet IS NULL WHERE to_tsvector('german', ax_lagebezeichnungkatalogeintrag.bezeichnung || ' ' || reverse(ax_lagebezeichnungkatalogeintrag.bezeichnung::text) || ' ' || ax_lagebezeichnungmithausnummer.hausnummer || ' ' || ax_gemeinde.bezeichnung) @@ to_tsquery('german', '" + unicode(self.getSearchStringAdresse()) + "')"
            query.exec_(sqlAdresse)
            if(query.size() > 0):
                item_titleAdresse = QTreeWidgetItem(self.treeWidget)
                item_titleAdresse.setText(0,u"Adressen")
                item_titleAdresse.setChildIndicatorPolicy(QTreeWidgetItem.ShowIndicator)

            #------------------------------------------ Eigentümer suchen
            if(self.accessControl.checkAccessControlIsActive() == False or self.accessControl.checkUserHasEigentuemerAccess() == True):
                if(self.checkPostnasSeachTable() == True):
                    sqlEigentuemer = "SELECT gml_id FROM postnas_search WHERE vector @@ to_tsquery('german', '" + self.getSearchStringEigentuemer() + "') AND typ = 'eigentuemer'"
                else:
                    sqlEigentuemer = "SELECT ax_person.gml_id FROM ax_person WHERE to_tsvector('german',CASE WHEN nachnameoderfirma IS NOT NULL THEN nachnameoderfirma || ' ' || reverse(nachnameoderfirma) || ' ' ELSE '' END || CASE WHEN vorname IS NOT NULL THEN vorname || ' ' || reverse(vorname) || ' ' ELSE '' END || CASE WHEN geburtsname IS NOT NULL THEN geburtsname || ' ' || reverse(geburtsname) ELSE '' END || CASE WHEN namensbestandteil IS NOT NULL THEN namensbestandteil || ' ' || reverse(namensbestandteil) ELSE '' END || CASE WHEN akademischergrad IS NOT NULL THEN akademischergrad || ' ' || reverse(akademischergrad) ELSE '' END)  @@ to_tsquery('german', '" + self.getSearchStringEigentuemer() + "') AND endet IS NULL"
                query.exec_(sqlEigentuemer)

                if(query.size() > 0):
                    item_titleEigentuemer = QTreeWidgetItem(self.treeWidget)
                    item_titleEigentuemer.setText(0,u"Eigentümer")
                    item_titleEigentuemer.setChildIndicatorPolicy(QTreeWidgetItem.ShowIndicator)

            self.db.close()
            #----------------------------------------- Suchergebnis aufbereiten
            if(self.treeWidget.topLevelItemCount() == 0):
                item_empty = QTreeWidgetItem(self.treeWidget)
                item_empty.setText(0, "Keine Ergebnisse")
            else:
                self.showButton.setEnabled(True)
                if(self.treeWidget.topLevelItemCount() == 1 and self.treeWidget.topLevelItem(0).text(0) != "Keine Ergebnisse"):
                    self.treeWidget.expandItem(self.treeWidget.topLevelItem(0))
                    if(self.treeWidget.topLevelItem(0).childCount() == 1):
                        self.treeWidget.expandItem(self.treeWidget.topLevelItem(0).child(0))
                        if(self.treeWidget.topLevelItem(0).text(0) == u"Eigentümer"):
                            self.addMapPerson("'" + self.treeWidget.topLevelItem(0).child(0).text(1) + "'")
                        if(self.treeWidget.topLevelItem(0).child(0).childCount() == 1):
                            self.treeWidget.expandItem(self.treeWidget.topLevelItem(0).child(0).child(0))
                            if(self.treeWidget.topLevelItem(0).child(0).child(0).childCount() == 1):
                                if(self.treeWidget.topLevelItem(0).child(0).child(0).child(0).text(2) == "flurstueck"):
                                    self.addMapFlurstueck(self.treeWidget.topLevelItem(0).child(0).child(0).child(0).text(1),self.treeWidget.topLevelItem(0).child(0).child(0).child(0).text(3))
                                if(self.treeWidget.topLevelItem(0).child(0).child(0).child(0).text(2) == "strasse"):
                                    self.addMapHausnummer("'" + self.treeWidget.topLevelItem(0).child(0).child(0).child(0).text(1) + "'")
        else:
            self.treeWidget.clear()
        QApplication.setOverrideCursor(Qt.ArrowCursor)

    def on_treeWidget_itemDoubleClicked(self, item):
        if(item.text(2) == "flurstueck"):
            self.addMapFlurstueck(item.text(1),item.text(3))
        if(item.text(2) == "flur"):
            self.addMapFlur(item.text(3))
        if(item.text(2) == "gemarkung"):
            self.addMapGemarkung(item.text(3))
        if(item.text(2) == "hausnummer"):
            self.addMapHausnummer("'" + item.text(1) + "'")
        if(item.text(2) == "person"):
            self.addMapPerson("'" + item.text(1) + "'")

    def on_treeWidget_itemExpanded(self, item):
        QApplication.setOverrideCursor(Qt.WaitCursor)

        if(item.text(0) == u"Flurstücke"):
            self.treeLoadGemarkung(item)
        elif(item.text(2) == "gemarkung"):
            self.treeLoadFlur(item)
        elif(item.text(2) == "flur"):
            self.treeLoadFlurstueck(item)
        elif(item.text(0) == u"Adressen"):
            self.treeLoadAdresseGemeinde(item)
        elif(item.text(2) == "gemeinde"):
            self.treeLoadAdresseStrasse(item)
        elif(item.text(2) == "strasse"):
            self.treeLoadAdresseHausnummer(item)
        elif(item.text(0) == u"Eigentümer"):
            self.treeLoadEigentuemer(item)
        elif(item.text(2) == "person"):
            self.treeLoadEigentuemerFlurstuecke(item)

        QApplication.setOverrideCursor(Qt.ArrowCursor)

    def keyPressEvent(self, event):
        if (event.key() == QtCore.Qt.Key_Return or event.key() == QtCore.Qt.Key_Enter):
            self.on_showButton_pressed()

    def on_resetButton_pressed(self):
        self.treeWidget.clear()
        self.lineEdit.clear()
        self.resetSuchergebnisLayer()
        self.showButton.setEnabled(False)
        self.resetButton.setEnabled(False)

    def treeLoadGemarkung(self,item):
        if(item.childCount() == 0):
            self.loadDbSettings()
            self.db.open()
            query = QSqlQuery(self.db)
            if(self.checkPostnasSeachTable() == True):
                sqlGemarkung = "SELECT ax_gemarkung.bezeichnung,ax_flurstueck.gemarkungsnummer,ax_flurstueck.land \
                FROM postnas_search \
                JOIN ax_flurstueck on postnas_search.gml_id = ax_flurstueck.gml_id AND ax_flurstueck.endet IS NULL \
                LEFT JOIN ax_gemarkung ON ax_flurstueck.land::text = ax_gemarkung.land::text AND ax_flurstueck.gemarkungsnummer::text = ax_gemarkung.gemarkungsnummer::text AND ax_gemarkung.endet IS NULL \
                WHERE vector @@ to_tsquery('german', '" + self.getSearchStringFlurstueck() + "') AND typ IN ('flurstueck_aktuell','flurstueck_historisch','flurstueck_historisch_ungenau') \
                UNION \
                SELECT ax_gemarkung.bezeichnung,ax_historischesflurstueck.gemarkungsnummer,ax_historischesflurstueck.land \
                FROM postnas_search \
                JOIN ax_historischesflurstueck on postnas_search.gml_id = ax_historischesflurstueck.gml_id AND ax_historischesflurstueck.endet IS NULL \
                LEFT JOIN ax_gemarkung ON ax_historischesflurstueck.land::text = ax_gemarkung.land::text AND ax_historischesflurstueck.gemarkungsnummer::text = ax_gemarkung.gemarkungsnummer::text AND ax_gemarkung.endet IS NULL \
                WHERE vector @@ to_tsquery('german', '" + self.getSearchStringFlurstueck() + "') AND typ IN ('flurstueck_aktuell','flurstueck_historisch','flurstueck_historisch_ungenau') \
                UNION \
                SELECT ax_gemarkung.bezeichnung,ax_historischesflurstueckohneraumbezug.gemarkungsnummer,ax_historischesflurstueckohneraumbezug.land \
                FROM postnas_search \
                JOIN ax_historischesflurstueckohneraumbezug on postnas_search.gml_id = ax_historischesflurstueckohneraumbezug.gml_id AND ax_historischesflurstueckohneraumbezug.endet IS NULL \
                LEFT JOIN ax_gemarkung ON ax_historischesflurstueckohneraumbezug.land::text = ax_gemarkung.land::text AND ax_historischesflurstueckohneraumbezug.gemarkungsnummer::text = ax_gemarkung.gemarkungsnummer::text AND ax_gemarkung.endet IS NULL \
                WHERE vector @@ to_tsquery('german', '" + self.getSearchStringFlurstueck() + "') AND typ IN ('flurstueck_aktuell','flurstueck_historisch','flurstueck_historisch_ungenau')"
            else:
                sqlGemarkung = "SELECT ax_gemarkung.bezeichnung,ax_flurstueck.gemarkungsnummer,ax_flurstueck.land \
                FROM ax_flurstueck \
                LEFT JOIN ax_gemarkung ON ax_flurstueck.land::text = ax_gemarkung.land::text AND ax_flurstueck.gemarkungsnummer::text = ax_gemarkung.gemarkungsnummer::text AND ax_gemarkung.endet IS NULL \
                WHERE to_tsvector('german'::regconfig, CASE WHEN ax_flurstueck.gemarkungsnummer IS NULL THEN '0000' ELSE ax_flurstueck.gemarkungsnummer END || ' ' || CASE WHEN ax_flurstueck.flurnummer IS NULL THEN '000' ELSE ax_flurstueck.flurnummer END || ' ' || CASE WHEN ax_flurstueck.zaehler IS NULL THEN 0 ELSE ax_flurstueck.zaehler END || ' ' || CASE WHEN ax_flurstueck.nenner IS NULL THEN '' ELSE ax_flurstueck.nenner END || ' ' || CASE WHEN ax_flurstueck.gemarkungsnummer IS NULL THEN '0000' ELSE ax_flurstueck.gemarkungsnummer END || CASE WHEN ax_flurstueck.flurnummer IS NULL THEN '000' ELSE ax_flurstueck.flurnummer END || CASE WHEN ax_flurstueck.zaehler IS NULL THEN 0 ELSE ax_flurstueck.zaehler END || CASE WHEN ax_flurstueck.nenner IS NULL THEN '' ELSE ax_flurstueck.nenner END || ' ' || CASE WHEN ax_flurstueck.gemarkungsnummer IS NULL THEN '0000' ELSE lpad(ax_flurstueck.gemarkungsnummer::text, 4, '0'::text) END || CASE WHEN ax_flurstueck.flurnummer IS NULL THEN '000' ELSE lpad(ax_flurstueck.flurnummer::text, 3, '0'::text) END || CASE WHEN ax_flurstueck.zaehler IS NULL THEN '' ELSE lpad(ax_flurstueck.zaehler::text, 5, '0'::text) END || CASE WHEN ax_flurstueck.nenner IS NULL THEN '' ELSE lpad(ax_flurstueck.nenner::text, 3, '0'::text) END || ' ' || CASE WHEN ax_flurstueck.gemarkungsnummer IS NULL THEN '0000' ELSE ax_flurstueck.gemarkungsnummer END || '-' || CASE WHEN ax_flurstueck.flurnummer IS NULL THEN '000' ELSE ax_flurstueck.flurnummer END || '-' || CASE WHEN ax_flurstueck.zaehler IS NULL THEN 0 ELSE ax_flurstueck.zaehler END || '-' || CASE WHEN ax_flurstueck.nenner IS NULL THEN '' ELSE '/' || ax_flurstueck.nenner END || ' ' || CASE WHEN ax_flurstueck.gemarkungsnummer IS NULL THEN '0000' ELSE lpad(ax_flurstueck.gemarkungsnummer::text, 4, '0'::text) END || '-' || CASE WHEN ax_flurstueck.flurnummer IS NULL THEN '000' ELSE lpad(ax_flurstueck.flurnummer::text, 3, '0'::text) END || '-' || CASE WHEN ax_flurstueck.zaehler IS NULL THEN '' ELSE lpad(ax_flurstueck.zaehler::text, 5, '0'::text) END || '-' || CASE WHEN ax_flurstueck.nenner IS NULL THEN '' ELSE '/' || lpad(ax_flurstueck.nenner::text, 3, '0'::text) END || ' ' || CASE WHEN ax_gemarkung.bezeichnung IS NOT NULL THEN ax_gemarkung.bezeichnung ELSE '' END) @@ to_tsquery('german', '" + self.getSearchStringFlurstueck() + "') \
                UNION \
                SELECT ax_gemarkung.bezeichnung,ax_historischesflurstueck.gemarkungsnummer,ax_historischesflurstueck.land \
                FROM ax_historischesflurstueck \
                LEFT JOIN ax_gemarkung ON ax_historischesflurstueck.land::text = ax_gemarkung.land::text AND ax_historischesflurstueck.gemarkungsnummer::text = ax_gemarkung.gemarkungsnummer::text AND ax_gemarkung.endet IS NULL \
                WHERE to_tsvector('german'::regconfig,CASE WHEN ax_historischesflurstueck.gemarkungsnummer IS NULL THEN '0000' ELSE ax_historischesflurstueck.gemarkungsnummer END || ' ' || CASE WHEN ax_historischesflurstueck.flurnummer IS NULL THEN '000' ELSE ax_historischesflurstueck.flurnummer END || ' ' || CASE WHEN ax_historischesflurstueck.zaehler IS NULL THEN '' ELSE ax_historischesflurstueck.zaehler END || ' ' || CASE WHEN ax_historischesflurstueck.nenner IS NULL THEN '' ELSE ax_historischesflurstueck.nenner END || ' ' || CASE WHEN ax_historischesflurstueck.gemarkungsnummer IS NULL THEN '0000' ELSE ax_historischesflurstueck.gemarkungsnummer END || CASE WHEN ax_historischesflurstueck.flurnummer IS NULL THEN '000' ELSE ax_historischesflurstueck.flurnummer END || CASE WHEN ax_historischesflurstueck.zaehler IS NULL THEN '' ELSE ax_historischesflurstueck.zaehler END || CASE WHEN ax_historischesflurstueck.nenner IS NULL THEN '' ELSE ax_historischesflurstueck.nenner END || ' ' || CASE WHEN ax_historischesflurstueck.gemarkungsnummer IS NULL THEN '0000' ELSE lpad(ax_historischesflurstueck.gemarkungsnummer::text, 4, '0'::text) END || CASE WHEN ax_historischesflurstueck.flurnummer IS NULL THEN '000' ELSE lpad(ax_historischesflurstueck.flurnummer::text, 3, '0'::text) END || CASE WHEN ax_historischesflurstueck.zaehler IS NULL THEN '' ELSE lpad(ax_historischesflurstueck.zaehler::text, 5, '0'::text) END || CASE WHEN ax_historischesflurstueck.nenner IS NULL THEN '' ELSE lpad(ax_historischesflurstueck.nenner::text, 3, '0'::text) END || ' ' || CASE WHEN ax_historischesflurstueck.gemarkungsnummer IS NULL THEN '0000' ELSE ax_historischesflurstueck.gemarkungsnummer END || '-' || CASE WHEN ax_historischesflurstueck.flurnummer IS NULL THEN '000' ELSE ax_historischesflurstueck.flurnummer END || '-' || CASE WHEN ax_historischesflurstueck.zaehler IS NULL THEN '' ELSE ax_historischesflurstueck.zaehler END || '-' || CASE WHEN ax_historischesflurstueck.nenner IS NULL THEN '' ELSE '/' || ax_historischesflurstueck.nenner END || ' ' || CASE WHEN ax_historischesflurstueck.gemarkungsnummer IS NULL THEN '0000' ELSE lpad(ax_historischesflurstueck.gemarkungsnummer::text, 4, '0'::text) END || '-' || CASE WHEN ax_historischesflurstueck.flurnummer IS NULL THEN '000' ELSE lpad(ax_historischesflurstueck.flurnummer::text, 3, '0'::text) END || '-' || CASE WHEN ax_historischesflurstueck.zaehler IS NULL THEN '' ELSE lpad(ax_historischesflurstueck.zaehler::text, 5, '0'::text) END || '-' || CASE WHEN ax_historischesflurstueck.nenner IS NULL THEN '' ELSE '/' || lpad(ax_historischesflurstueck.nenner::text, 3, '0'::text) END || ' ' || CASE WHEN ax_gemarkung.bezeichnung IS NOT NULL THEN ax_gemarkung.bezeichnung ELSE '' END) @@ to_tsquery('german', '" + self.getSearchStringFlurstueck() + "') \
                UNION \
                SELECT ax_gemarkung.bezeichnung,ax_historischesflurstueckohneraumbezug.gemarkungsnummer,ax_historischesflurstueckohneraumbezug.land \
                FROM ax_historischesflurstueckohneraumbezug \
                LEFT JOIN ax_gemarkung ON ax_historischesflurstueckohneraumbezug.land::text = ax_gemarkung.land::text AND ax_historischesflurstueckohneraumbezug.gemarkungsnummer::text = ax_gemarkung.gemarkungsnummer::text AND ax_gemarkung.endet IS NULL \
                WHERE to_tsvector('german'::regconfig,CASE WHEN ax_historischesflurstueckohneraumbezug.gemarkungsnummer IS NULL THEN '0000' ELSE ax_historischesflurstueckohneraumbezug.gemarkungsnummer END || ' ' || CASE WHEN ax_historischesflurstueckohneraumbezug.flurnummer IS NULL THEN '000' ELSE ax_historischesflurstueckohneraumbezug.flurnummer END || ' ' || CASE WHEN ax_historischesflurstueckohneraumbezug.zaehler IS NULL THEN '' ELSE ax_historischesflurstueckohneraumbezug.zaehler END || ' ' || CASE WHEN ax_historischesflurstueckohneraumbezug.nenner IS NULL THEN '' ELSE ax_historischesflurstueckohneraumbezug.nenner END || ' ' || CASE WHEN ax_historischesflurstueckohneraumbezug.gemarkungsnummer IS NULL THEN '0000' ELSE ax_historischesflurstueckohneraumbezug.gemarkungsnummer END || CASE WHEN ax_historischesflurstueckohneraumbezug.flurnummer IS NULL THEN '000' ELSE ax_historischesflurstueckohneraumbezug.flurnummer END || CASE WHEN ax_historischesflurstueckohneraumbezug.zaehler IS NULL THEN '' ELSE ax_historischesflurstueckohneraumbezug.zaehler END || CASE WHEN ax_historischesflurstueckohneraumbezug.nenner IS NULL THEN '' ELSE ax_historischesflurstueckohneraumbezug.nenner END || ' ' || CASE WHEN ax_historischesflurstueckohneraumbezug.gemarkungsnummer IS NULL THEN '0000' ELSE lpad(ax_historischesflurstueckohneraumbezug.gemarkungsnummer::text, 4, '0'::text) END || CASE WHEN ax_historischesflurstueckohneraumbezug.flurnummer IS NULL THEN '000' ELSE lpad(ax_historischesflurstueckohneraumbezug.flurnummer::text, 3, '0'::text) END || CASE WHEN ax_historischesflurstueckohneraumbezug.zaehler IS NULL THEN '' ELSE lpad(ax_historischesflurstueckohneraumbezug.zaehler::text, 5, '0'::text) END || CASE WHEN ax_historischesflurstueckohneraumbezug.nenner IS NULL THEN '' ELSE lpad(ax_historischesflurstueckohneraumbezug.nenner::text, 3, '0'::text) END || ' ' || CASE WHEN ax_historischesflurstueckohneraumbezug.gemarkungsnummer IS NULL THEN '0000' ELSE ax_historischesflurstueckohneraumbezug.gemarkungsnummer END || '-' || CASE WHEN ax_historischesflurstueckohneraumbezug.flurnummer IS NULL THEN '000' ELSE ax_historischesflurstueckohneraumbezug.flurnummer END || '-' || CASE WHEN ax_historischesflurstueckohneraumbezug.zaehler IS NULL THEN '' ELSE ax_historischesflurstueckohneraumbezug.zaehler END || '-' || CASE WHEN ax_historischesflurstueckohneraumbezug.nenner IS NULL THEN '' ELSE '/' || ax_historischesflurstueckohneraumbezug.nenner END || ' ' || CASE WHEN ax_historischesflurstueckohneraumbezug.gemarkungsnummer IS NULL THEN '0000' ELSE lpad(ax_historischesflurstueckohneraumbezug.gemarkungsnummer::text, 4, '0'::text) END || '-' || CASE WHEN ax_historischesflurstueckohneraumbezug.flurnummer IS NULL THEN '000' ELSE lpad(ax_historischesflurstueckohneraumbezug.flurnummer::text, 3, '0'::text) END || '-' || CASE WHEN ax_historischesflurstueckohneraumbezug.zaehler IS NULL THEN '' ELSE lpad(ax_historischesflurstueckohneraumbezug.zaehler::text, 5, '0'::text) END || '-' || CASE WHEN ax_historischesflurstueckohneraumbezug.nenner IS NULL THEN '' ELSE '/' || lpad(ax_historischesflurstueckohneraumbezug.nenner::text, 3, '0'::text) END || ' ' || CASE WHEN ax_gemarkung.bezeichnung IS NOT NULL THEN ax_gemarkung.bezeichnung ELSE '' END) @@ to_tsquery('german', '" + self.getSearchStringFlurstueck() + "')"
            query.exec_(sqlGemarkung)
            if(query.size() > 0):
                fieldGemarkungsnummer = query.record().indexOf("gemarkungsnummer")
                fieldGemarkungsname = query.record().indexOf("bezeichnung")
                fieldLand = query.record().indexOf("land")
                fieldZaehler = query.record().indexOf("zaehler")
                fieldNenner = query.record().indexOf("nenner")
                while(query.next()):
                    gemarkungsnummer = query.value(fieldGemarkungsnummer)
                    gemarkungsname = query.value(fieldGemarkungsname)
                    land = query.value(fieldLand)
                    item_gemarkung = QTreeWidgetItem(item)
                    if(gemarkungsname == None):
                        item_gemarkung.setText(0, "Gemarkung " + str(gemarkungsnummer))
                    else:
                        item_gemarkung.setText(0, "Gemarkung " + unicode(gemarkungsname) + " / " + str(gemarkungsnummer))
                    item_gemarkung.setText(1, str(gemarkungsnummer))
                    item_gemarkung.setText(2, "gemarkung")
                    item_gemarkung.setText(3, str(land).zfill(2) + str(gemarkungsnummer).zfill(4))
                    item_gemarkung.setChildIndicatorPolicy(QTreeWidgetItem.ShowIndicator)
            self.db.close()

    def treeLoadFlur(self,item):
        if(item.childCount() == 0):
            self.loadDbSettings()
            self.db.open()
            query = QSqlQuery(self.db)
            if(self.checkPostnasSeachTable() == True):
                sqlFlur = "SELECT * FROM (SELECT ax_gemarkung.bezeichnung,ax_flurstueck.gemarkungsnummer,ax_flurstueck.flurnummer,ax_flurstueck.land \
                FROM postnas_search \
                JOIN ax_flurstueck on postnas_search.gml_id = ax_flurstueck.gml_id AND ax_flurstueck.endet IS NULL \
                LEFT JOIN ax_gemarkung ON ax_flurstueck.land::text = ax_gemarkung.land::text AND ax_flurstueck.gemarkungsnummer::text = ax_gemarkung.gemarkungsnummer::text AND ax_gemarkung.endet IS NULL \
                WHERE vector @@ to_tsquery('german', '" + self.getSearchStringFlurstueck() + "') AND ax_flurstueck.gemarkungsnummer = '"+ item.text(1) + "' AND typ IN ('flurstueck_aktuell','flurstueck_historisch','flurstueck_historisch_ungenau') AND ax_flurstueck.flurnummer IS NOT NULL \
                UNION \
                SELECT ax_gemarkung.bezeichnung,ax_historischesflurstueck.gemarkungsnummer,ax_historischesflurstueck.flurnummer,ax_historischesflurstueck.land \
                FROM postnas_search \
                JOIN ax_historischesflurstueck on postnas_search.gml_id = ax_historischesflurstueck.gml_id AND ax_historischesflurstueck.endet IS NULL \
                LEFT JOIN ax_gemarkung ON ax_historischesflurstueck.land::text = ax_gemarkung.land::text AND ax_historischesflurstueck.gemarkungsnummer::text = ax_gemarkung.gemarkungsnummer::text AND ax_gemarkung.endet IS NULL \
                WHERE vector @@ to_tsquery('german', '" + self.getSearchStringFlurstueck() + "') AND ax_historischesflurstueck.gemarkungsnummer = '"+ item.text(1) + "' AND typ IN ('flurstueck_aktuell','flurstueck_historisch','flurstueck_historisch_ungenau') AND ax_historischesflurstueck.flurnummer IS NOT NULL \
                UNION \
                SELECT ax_gemarkung.bezeichnung,ax_historischesflurstueckohneraumbezug.gemarkungsnummer,ax_historischesflurstueckohneraumbezug.flurnummer,ax_historischesflurstueckohneraumbezug.land \
                FROM postnas_search \
                JOIN ax_historischesflurstueckohneraumbezug on postnas_search.gml_id = ax_historischesflurstueckohneraumbezug.gml_id AND ax_historischesflurstueckohneraumbezug.endet IS NULL \
                LEFT JOIN ax_gemarkung ON ax_historischesflurstueckohneraumbezug.land::text = ax_gemarkung.land::text AND ax_historischesflurstueckohneraumbezug.gemarkungsnummer::text = ax_gemarkung.gemarkungsnummer::text AND ax_gemarkung.endet IS NULL \
                WHERE vector @@ to_tsquery('german', '" + self.getSearchStringFlurstueck() + "') AND ax_historischesflurstueckohneraumbezug.gemarkungsnummer = '"+ item.text(1) + "' AND typ IN ('flurstueck_aktuell','flurstueck_historisch','flurstueck_historisch_ungenau') AND ax_historischesflurstueckohneraumbezug.flurnummer IS NOT NULL) as subquery ORDER BY gemarkungsnummer::integer, flurnummer::integer"
            else:
                sqlFlur = "SELECT * FROM (SELECT ax_gemarkung.bezeichnung,ax_flurstueck.gemarkungsnummer,ax_flurstueck.flurnummer,ax_flurstueck.land \
                FROM ax_flurstueck \
                LEFT JOIN ax_gemarkung ON ax_flurstueck.land::text = ax_gemarkung.land::text AND ax_flurstueck.gemarkungsnummer::text = ax_gemarkung.gemarkungsnummer::text AND ax_gemarkung.endet IS NULL \
                WHERE to_tsvector('german'::regconfig, CASE WHEN ax_flurstueck.gemarkungsnummer IS NULL THEN '0000' ELSE ax_flurstueck.gemarkungsnummer END || ' ' || CASE WHEN ax_flurstueck.flurnummer IS NULL THEN '000' ELSE ax_flurstueck.flurnummer END || ' ' || CASE WHEN ax_flurstueck.zaehler IS NULL THEN 0 ELSE ax_flurstueck.zaehler END || ' ' || CASE WHEN ax_flurstueck.nenner IS NULL THEN '' ELSE ax_flurstueck.nenner END || ' ' || CASE WHEN ax_flurstueck.gemarkungsnummer IS NULL THEN '0000' ELSE ax_flurstueck.gemarkungsnummer END || CASE WHEN ax_flurstueck.flurnummer IS NULL THEN '000' ELSE ax_flurstueck.flurnummer END || CASE WHEN ax_flurstueck.zaehler IS NULL THEN 0 ELSE ax_flurstueck.zaehler END || CASE WHEN ax_flurstueck.nenner IS NULL THEN '' ELSE ax_flurstueck.nenner END || ' ' || CASE WHEN ax_flurstueck.gemarkungsnummer IS NULL THEN '0000' ELSE lpad(ax_flurstueck.gemarkungsnummer::text, 4, '0'::text) END || CASE WHEN ax_flurstueck.flurnummer IS NULL THEN '000' ELSE lpad(ax_flurstueck.flurnummer::text, 3, '0'::text) END || CASE WHEN ax_flurstueck.zaehler IS NULL THEN '' ELSE lpad(ax_flurstueck.zaehler::text, 5, '0'::text) END || CASE WHEN ax_flurstueck.nenner IS NULL THEN '' ELSE lpad(ax_flurstueck.nenner::text, 3, '0'::text) END || ' ' || CASE WHEN ax_flurstueck.gemarkungsnummer IS NULL THEN '0000' ELSE ax_flurstueck.gemarkungsnummer END || '-' || CASE WHEN ax_flurstueck.flurnummer IS NULL THEN '000' ELSE ax_flurstueck.flurnummer END || '-' || CASE WHEN ax_flurstueck.zaehler IS NULL THEN 0 ELSE ax_flurstueck.zaehler END || '-' || CASE WHEN ax_flurstueck.nenner IS NULL THEN '' ELSE '/' || ax_flurstueck.nenner END || ' ' || CASE WHEN ax_flurstueck.gemarkungsnummer IS NULL THEN '0000' ELSE lpad(ax_flurstueck.gemarkungsnummer::text, 4, '0'::text) END || '-' || CASE WHEN ax_flurstueck.flurnummer IS NULL THEN '000' ELSE lpad(ax_flurstueck.flurnummer::text, 3, '0'::text) END || '-' || CASE WHEN ax_flurstueck.zaehler IS NULL THEN '' ELSE lpad(ax_flurstueck.zaehler::text, 5, '0'::text) END || '-' || CASE WHEN ax_flurstueck.nenner IS NULL THEN '' ELSE '/' || lpad(ax_flurstueck.nenner::text, 3, '0'::text) END || ' ' || CASE WHEN ax_gemarkung.bezeichnung IS NOT NULL THEN ax_gemarkung.bezeichnung ELSE '' END) @@ to_tsquery('german', '" + self.getSearchStringFlurstueck() + "') AND ax_flurstueck.gemarkungsnummer = '"+ item.text(1) + "' AND ax_flurstueck.flurnummer IS NOT NULL \
                UNION \
                SELECT ax_gemarkung.bezeichnung,ax_historischesflurstueck.gemarkungsnummer,ax_historischesflurstueck.flurnummer,ax_historischesflurstueck.land \
                FROM ax_historischesflurstueck \
                LEFT JOIN ax_gemarkung ON ax_historischesflurstueck.land::text = ax_gemarkung.land::text AND ax_historischesflurstueck.gemarkungsnummer::text = ax_gemarkung.gemarkungsnummer::text AND ax_gemarkung.endet IS NULL \
                WHERE to_tsvector('german'::regconfig,CASE WHEN ax_historischesflurstueck.gemarkungsnummer IS NULL THEN '0000' ELSE ax_historischesflurstueck.gemarkungsnummer END || ' ' || CASE WHEN ax_historischesflurstueck.flurnummer IS NULL THEN '000' ELSE ax_historischesflurstueck.flurnummer END || ' ' || CASE WHEN ax_historischesflurstueck.zaehler IS NULL THEN '' ELSE ax_historischesflurstueck.zaehler END || ' ' || CASE WHEN ax_historischesflurstueck.nenner IS NULL THEN '' ELSE ax_historischesflurstueck.nenner END || ' ' || CASE WHEN ax_historischesflurstueck.gemarkungsnummer IS NULL THEN '0000' ELSE ax_historischesflurstueck.gemarkungsnummer END || CASE WHEN ax_historischesflurstueck.flurnummer IS NULL THEN '000' ELSE ax_historischesflurstueck.flurnummer END || CASE WHEN ax_historischesflurstueck.zaehler IS NULL THEN '' ELSE ax_historischesflurstueck.zaehler END || CASE WHEN ax_historischesflurstueck.nenner IS NULL THEN '' ELSE ax_historischesflurstueck.nenner END || ' ' || CASE WHEN ax_historischesflurstueck.gemarkungsnummer IS NULL THEN '0000' ELSE lpad(ax_historischesflurstueck.gemarkungsnummer::text, 4, '0'::text) END || CASE WHEN ax_historischesflurstueck.flurnummer IS NULL THEN '000' ELSE lpad(ax_historischesflurstueck.flurnummer::text, 3, '0'::text) END || CASE WHEN ax_historischesflurstueck.zaehler IS NULL THEN '' ELSE lpad(ax_historischesflurstueck.zaehler::text, 5, '0'::text) END || CASE WHEN ax_historischesflurstueck.nenner IS NULL THEN '' ELSE lpad(ax_historischesflurstueck.nenner::text, 3, '0'::text) END || ' ' || CASE WHEN ax_historischesflurstueck.gemarkungsnummer IS NULL THEN '0000' ELSE ax_historischesflurstueck.gemarkungsnummer END || '-' || CASE WHEN ax_historischesflurstueck.flurnummer IS NULL THEN '000' ELSE ax_historischesflurstueck.flurnummer END || '-' || CASE WHEN ax_historischesflurstueck.zaehler IS NULL THEN '' ELSE ax_historischesflurstueck.zaehler END || '-' || CASE WHEN ax_historischesflurstueck.nenner IS NULL THEN '' ELSE '/' || ax_historischesflurstueck.nenner END || ' ' || CASE WHEN ax_historischesflurstueck.gemarkungsnummer IS NULL THEN '0000' ELSE lpad(ax_historischesflurstueck.gemarkungsnummer::text, 4, '0'::text) END || '-' || CASE WHEN ax_historischesflurstueck.flurnummer IS NULL THEN '000' ELSE lpad(ax_historischesflurstueck.flurnummer::text, 3, '0'::text) END || '-' || CASE WHEN ax_historischesflurstueck.zaehler IS NULL THEN '' ELSE lpad(ax_historischesflurstueck.zaehler::text, 5, '0'::text) END || '-' || CASE WHEN ax_historischesflurstueck.nenner IS NULL THEN '' ELSE '/' || lpad(ax_historischesflurstueck.nenner::text, 3, '0'::text) END || ' ' || CASE WHEN ax_gemarkung.bezeichnung IS NOT NULL THEN ax_gemarkung.bezeichnung ELSE '' END) @@ to_tsquery('german', '" + self.getSearchStringFlurstueck() + "') AND ax_historischesflurstueck.gemarkungsnummer = '"+ item.text(1) + "' AND ax_historischesflurstueck.flurnummer IS NOT NULL \
                UNION \
                SELECT ax_gemarkung.bezeichnung,ax_historischesflurstueckohneraumbezug.gemarkungsnummer,ax_historischesflurstueckohneraumbezug.flurnummer,ax_historischesflurstueckohneraumbezug.land \
                FROM ax_historischesflurstueckohneraumbezug \
                LEFT JOIN ax_gemarkung ON ax_historischesflurstueckohneraumbezug.land::text = ax_gemarkung.land::text AND ax_historischesflurstueckohneraumbezug.gemarkungsnummer::text = ax_gemarkung.gemarkungsnummer::text AND ax_gemarkung.endet IS NULL \
                WHERE to_tsvector('german'::regconfig,CASE WHEN ax_historischesflurstueckohneraumbezug.gemarkungsnummer IS NULL THEN '0000' ELSE ax_historischesflurstueckohneraumbezug.gemarkungsnummer END || ' ' || CASE WHEN ax_historischesflurstueckohneraumbezug.flurnummer IS NULL THEN '000' ELSE ax_historischesflurstueckohneraumbezug.flurnummer END || ' ' || CASE WHEN ax_historischesflurstueckohneraumbezug.zaehler IS NULL THEN '' ELSE ax_historischesflurstueckohneraumbezug.zaehler END || ' ' || CASE WHEN ax_historischesflurstueckohneraumbezug.nenner IS NULL THEN '' ELSE ax_historischesflurstueckohneraumbezug.nenner END || ' ' || CASE WHEN ax_historischesflurstueckohneraumbezug.gemarkungsnummer IS NULL THEN '0000' ELSE ax_historischesflurstueckohneraumbezug.gemarkungsnummer END || CASE WHEN ax_historischesflurstueckohneraumbezug.flurnummer IS NULL THEN '000' ELSE ax_historischesflurstueckohneraumbezug.flurnummer END || CASE WHEN ax_historischesflurstueckohneraumbezug.zaehler IS NULL THEN '' ELSE ax_historischesflurstueckohneraumbezug.zaehler END || CASE WHEN ax_historischesflurstueckohneraumbezug.nenner IS NULL THEN '' ELSE ax_historischesflurstueckohneraumbezug.nenner END || ' ' || CASE WHEN ax_historischesflurstueckohneraumbezug.gemarkungsnummer IS NULL THEN '0000' ELSE lpad(ax_historischesflurstueckohneraumbezug.gemarkungsnummer::text, 4, '0'::text) END || CASE WHEN ax_historischesflurstueckohneraumbezug.flurnummer IS NULL THEN '000' ELSE lpad(ax_historischesflurstueckohneraumbezug.flurnummer::text, 3, '0'::text) END || CASE WHEN ax_historischesflurstueckohneraumbezug.zaehler IS NULL THEN '' ELSE lpad(ax_historischesflurstueckohneraumbezug.zaehler::text, 5, '0'::text) END || CASE WHEN ax_historischesflurstueckohneraumbezug.nenner IS NULL THEN '' ELSE lpad(ax_historischesflurstueckohneraumbezug.nenner::text, 3, '0'::text) END || ' ' || CASE WHEN ax_historischesflurstueckohneraumbezug.gemarkungsnummer IS NULL THEN '0000' ELSE ax_historischesflurstueckohneraumbezug.gemarkungsnummer END || '-' || CASE WHEN ax_historischesflurstueckohneraumbezug.flurnummer IS NULL THEN '000' ELSE ax_historischesflurstueckohneraumbezug.flurnummer END || '-' || CASE WHEN ax_historischesflurstueckohneraumbezug.zaehler IS NULL THEN '' ELSE ax_historischesflurstueckohneraumbezug.zaehler END || '-' || CASE WHEN ax_historischesflurstueckohneraumbezug.nenner IS NULL THEN '' ELSE '/' || ax_historischesflurstueckohneraumbezug.nenner END || ' ' || CASE WHEN ax_historischesflurstueckohneraumbezug.gemarkungsnummer IS NULL THEN '0000' ELSE lpad(ax_historischesflurstueckohneraumbezug.gemarkungsnummer::text, 4, '0'::text) END || '-' || CASE WHEN ax_historischesflurstueckohneraumbezug.flurnummer IS NULL THEN '000' ELSE lpad(ax_historischesflurstueckohneraumbezug.flurnummer::text, 3, '0'::text) END || '-' || CASE WHEN ax_historischesflurstueckohneraumbezug.zaehler IS NULL THEN '' ELSE lpad(ax_historischesflurstueckohneraumbezug.zaehler::text, 5, '0'::text) END || '-' || CASE WHEN ax_historischesflurstueckohneraumbezug.nenner IS NULL THEN '' ELSE '/' || lpad(ax_historischesflurstueckohneraumbezug.nenner::text, 3, '0'::text) END || ' ' || CASE WHEN ax_gemarkung.bezeichnung IS NOT NULL THEN ax_gemarkung.bezeichnung ELSE '' END) @@ to_tsquery('german', '" + self.getSearchStringFlurstueck() + "') AND ax_historischesflurstueckohneraumbezug.gemarkungsnummer = '"+ item.text(1) + "' AND ax_historischesflurstueckohneraumbezug.flurnummer IS NOT NULL) as subquery ORDER BY gemarkungsnummer::integer, flurnummer::integer"
            query.exec_(sqlFlur)
            if(query.size() > 0):
                fieldGemarkungsnummer = query.record().indexOf("gemarkungsnummer")
                fieldGemarkungsname = query.record().indexOf("bezeichnung")
                fieldFlurnummer = query.record().indexOf("flurnummer")
                fieldLand = query.record().indexOf("land")
                while(query.next()):
                    gemarkungsnummer = query.value(fieldGemarkungsnummer)
                    gemarkungsname = query.value(fieldGemarkungsname)
                    flurnummer = query.value(fieldFlurnummer)
                    land = query.value(fieldLand)

                    item_flur = QTreeWidgetItem(item)
                    item_flur.setText(0, "Flur " + str(flurnummer))
                    item_flur.setText(1, str(flurnummer))
                    item_flur.setText(2, "flur")
                    item_flur.setText(3, str(land).zfill(2) + str(gemarkungsnummer).zfill(4) + str(flurnummer).zfill(3))
                    item_flur.setText(4, str(gemarkungsnummer))
                    item_flur.setChildIndicatorPolicy(QTreeWidgetItem.ShowIndicator)
            else:
                self.treeLoadFlurstueck(item,False)
            self.db.close()

    def treeLoadFlurstueck(self,item,flurnummer = True):
        if(item.childCount() == 0):
            self.loadDbSettings()
            self.db.open()
            query = QSqlQuery(self.db)

            if(self.checkPostnasSeachTable() == True):
                if(flurnummer == True):
                    sqlFlurstueck = "SELECT * FROM (SELECT ax_gemarkung.bezeichnung,ax_flurstueck.gemarkungsnummer,ax_flurstueck.flurnummer,ax_flurstueck.land,ax_flurstueck.zaehler::integer,ax_flurstueck.nenner::integer,postnas_search.typ,ax_flurstueck.flurstueckskennzeichen \
                    FROM postnas_search \
                    JOIN ax_flurstueck on postnas_search.gml_id = ax_flurstueck.gml_id AND ax_flurstueck.endet IS NULL \
                    LEFT JOIN ax_gemarkung ON ax_flurstueck.land::text = ax_gemarkung.land::text AND ax_flurstueck.gemarkungsnummer::text = ax_gemarkung.gemarkungsnummer::text AND ax_gemarkung.endet IS NULL \
                    WHERE vector @@ to_tsquery('german', '" + self.getSearchStringFlurstueck() + "') AND ax_flurstueck.gemarkungsnummer = '"+ item.text(4) + "' AND ax_flurstueck.flurnummer = '"+ item.text(1) + "' AND typ IN ('flurstueck_aktuell','flurstueck_historisch','flurstueck_historisch_ungenau') \
                    UNION \
                    SELECT ax_gemarkung.bezeichnung,ax_historischesflurstueck.gemarkungsnummer,ax_historischesflurstueck.flurnummer,ax_historischesflurstueck.land,ax_historischesflurstueck.zaehler::integer,ax_historischesflurstueck.nenner::integer,postnas_search.typ,ax_historischesflurstueck.flurstueckskennzeichen \
                    FROM postnas_search \
                    JOIN ax_historischesflurstueck on postnas_search.gml_id = ax_historischesflurstueck.gml_id AND ax_historischesflurstueck.endet IS NULL \
                    LEFT JOIN ax_gemarkung ON ax_historischesflurstueck.land::text = ax_gemarkung.land::text AND ax_historischesflurstueck.gemarkungsnummer::text = ax_gemarkung.gemarkungsnummer::text AND ax_gemarkung.endet IS NULL \
                    WHERE vector @@ to_tsquery('german', '" + self.getSearchStringFlurstueck() + "') AND ax_historischesflurstueck.gemarkungsnummer = '"+ item.text(4) + "' AND ax_historischesflurstueck.flurnummer = '"+ item.text(1) + "' AND typ IN ('flurstueck_aktuell','flurstueck_historisch','flurstueck_historisch_ungenau') \
                    UNION \
                    SELECT ax_gemarkung.bezeichnung,ax_historischesflurstueckohneraumbezug.gemarkungsnummer,ax_historischesflurstueckohneraumbezug.flurnummer,ax_historischesflurstueckohneraumbezug.land,ax_historischesflurstueckohneraumbezug.zaehler::integer,ax_historischesflurstueckohneraumbezug.nenner::integer,postnas_search.typ,ax_historischesflurstueckohneraumbezug.flurstueckskennzeichen \
                    FROM postnas_search \
                    JOIN ax_historischesflurstueckohneraumbezug on postnas_search.gml_id = ax_historischesflurstueckohneraumbezug.gml_id AND ax_historischesflurstueckohneraumbezug.endet IS NULL \
                    LEFT JOIN ax_gemarkung ON ax_historischesflurstueckohneraumbezug.land::text = ax_gemarkung.land::text AND ax_historischesflurstueckohneraumbezug.gemarkungsnummer::text = ax_gemarkung.gemarkungsnummer::text AND ax_gemarkung.endet IS NULL \
                    WHERE vector @@ to_tsquery('german', '" + self.getSearchStringFlurstueck() + "') AND ax_historischesflurstueckohneraumbezug.gemarkungsnummer = '"+ item.text(4) + "' AND ax_historischesflurstueckohneraumbezug.flurnummer = '"+ item.text(1) + "' AND typ IN ('flurstueck_aktuell','flurstueck_historisch','flurstueck_historisch_ungenau')) as subquery ORDER BY gemarkungsnummer,flurnummer,zaehler,nenner"
                else:
                    sqlFlurstueck = "SELECT * FROM (SELECT ax_gemarkung.bezeichnung,ax_flurstueck.gemarkungsnummer,ax_flurstueck.flurnummer,ax_flurstueck.land,ax_flurstueck.zaehler::integer,ax_flurstueck.nenner::integer,postnas_search.typ,ax_flurstueck.flurstueckskennzeichen \
                    FROM postnas_search \
                    JOIN ax_flurstueck on postnas_search.gml_id = ax_flurstueck.gml_id AND ax_flurstueck.endet IS NULL \
                    LEFT JOIN ax_gemarkung ON ax_flurstueck.land::text = ax_gemarkung.land::text AND ax_flurstueck.gemarkungsnummer::text = ax_gemarkung.gemarkungsnummer::text AND ax_gemarkung.endet IS NULL \
                    WHERE vector @@ to_tsquery('german', '" + self.getSearchStringFlurstueck() + "') AND ax_flurstueck.gemarkungsnummer = '"+ item.text(1) + "' AND ax_flurstueck.flurnummer IS NULL AND typ IN ('flurstueck_aktuell','flurstueck_historisch','flurstueck_historisch_ungenau') \
                    UNION \
                    SELECT ax_gemarkung.bezeichnung,ax_historischesflurstueck.gemarkungsnummer,ax_historischesflurstueck.flurnummer,ax_historischesflurstueck.land,ax_historischesflurstueck.zaehler::integer,ax_historischesflurstueck.nenner::integer,postnas_search.typ,ax_historischesflurstueck.flurstueckskennzeichen \
                    FROM postnas_search \
                    JOIN ax_historischesflurstueck on postnas_search.gml_id = ax_historischesflurstueck.gml_id AND ax_historischesflurstueck.endet IS NULL \
                    LEFT JOIN ax_gemarkung ON ax_historischesflurstueck.land::text = ax_gemarkung.land::text AND ax_historischesflurstueck.gemarkungsnummer::text = ax_gemarkung.gemarkungsnummer::text AND ax_gemarkung.endet IS NULL \
                    WHERE vector @@ to_tsquery('german', '" + self.getSearchStringFlurstueck() + "') AND ax_historischesflurstueck.gemarkungsnummer = '"+ item.text(1) + "' AND ax_historischesflurstueck.flurnummer IS NULL AND typ IN ('flurstueck_aktuell','flurstueck_historisch','flurstueck_historisch_ungenau') \
                    UNION \
                    SELECT ax_gemarkung.bezeichnung,ax_historischesflurstueckohneraumbezug.gemarkungsnummer,ax_historischesflurstueckohneraumbezug.flurnummer,ax_historischesflurstueckohneraumbezug.land,ax_historischesflurstueckohneraumbezug.zaehler::integer,ax_historischesflurstueckohneraumbezug.nenner::integer,postnas_search.typ,ax_historischesflurstueckohneraumbezug.flurstueckskennzeichen \
                    FROM postnas_search \
                    JOIN ax_historischesflurstueckohneraumbezug on postnas_search.gml_id = ax_historischesflurstueckohneraumbezug.gml_id AND ax_historischesflurstueckohneraumbezug.endet IS NULL \
                    LEFT JOIN ax_gemarkung ON ax_historischesflurstueckohneraumbezug.land::text = ax_gemarkung.land::text AND ax_historischesflurstueckohneraumbezug.gemarkungsnummer::text = ax_gemarkung.gemarkungsnummer::text AND ax_gemarkung.endet IS NULL \
                    WHERE vector @@ to_tsquery('german', '" + self.getSearchStringFlurstueck() + "') AND ax_historischesflurstueckohneraumbezug.gemarkungsnummer = '"+ item.text(1) + "' AND ax_historischesflurstueckohneraumbezug.flurnummer IS NULL AND typ IN ('flurstueck_aktuell','flurstueck_historisch','flurstueck_historisch_ungenau')) as subquery ORDER BY gemarkungsnummer,flurnummer,zaehler,nenner"
            else:
                if(flurnummer == True):
                    sqlFlurstueck = "SELECT * FROM (SELECT ax_gemarkung.bezeichnung,ax_flurstueck.gemarkungsnummer,ax_flurstueck.flurnummer,ax_flurstueck.land,ax_flurstueck.zaehler::integer,ax_flurstueck.nenner::integer,'flurstueck_aktuell' as typ,ax_flurstueck.flurstueckskennzeichen \
                    FROM ax_flurstueck \
                    LEFT JOIN ax_gemarkung ON ax_flurstueck.land::text = ax_gemarkung.land::text AND ax_flurstueck.gemarkungsnummer::text = ax_gemarkung.gemarkungsnummer::text AND ax_gemarkung.endet IS NULL \
                    WHERE to_tsvector('german'::regconfig, CASE WHEN ax_flurstueck.gemarkungsnummer IS NULL THEN '0000' ELSE ax_flurstueck.gemarkungsnummer END || ' ' || CASE WHEN ax_flurstueck.flurnummer IS NULL THEN '000' ELSE ax_flurstueck.flurnummer END || ' ' || CASE WHEN ax_flurstueck.zaehler IS NULL THEN 0 ELSE ax_flurstueck.zaehler END || ' ' || CASE WHEN ax_flurstueck.nenner IS NULL THEN '' ELSE ax_flurstueck.nenner END || ' ' || CASE WHEN ax_flurstueck.gemarkungsnummer IS NULL THEN '0000' ELSE ax_flurstueck.gemarkungsnummer END || CASE WHEN ax_flurstueck.flurnummer IS NULL THEN '000' ELSE ax_flurstueck.flurnummer END || CASE WHEN ax_flurstueck.zaehler IS NULL THEN 0 ELSE ax_flurstueck.zaehler END || CASE WHEN ax_flurstueck.nenner IS NULL THEN '' ELSE ax_flurstueck.nenner END || ' ' || CASE WHEN ax_flurstueck.gemarkungsnummer IS NULL THEN '0000' ELSE lpad(ax_flurstueck.gemarkungsnummer::text, 4, '0'::text) END || CASE WHEN ax_flurstueck.flurnummer IS NULL THEN '000' ELSE lpad(ax_flurstueck.flurnummer::text, 3, '0'::text) END || CASE WHEN ax_flurstueck.zaehler IS NULL THEN '' ELSE lpad(ax_flurstueck.zaehler::text, 5, '0'::text) END || CASE WHEN ax_flurstueck.nenner IS NULL THEN '' ELSE lpad(ax_flurstueck.nenner::text, 3, '0'::text) END || ' ' || CASE WHEN ax_flurstueck.gemarkungsnummer IS NULL THEN '0000' ELSE ax_flurstueck.gemarkungsnummer END || '-' || CASE WHEN ax_flurstueck.flurnummer IS NULL THEN '000' ELSE ax_flurstueck.flurnummer END || '-' || CASE WHEN ax_flurstueck.zaehler IS NULL THEN 0 ELSE ax_flurstueck.zaehler END || '-' || CASE WHEN ax_flurstueck.nenner IS NULL THEN '' ELSE '/' || ax_flurstueck.nenner END || ' ' || CASE WHEN ax_flurstueck.gemarkungsnummer IS NULL THEN '0000' ELSE lpad(ax_flurstueck.gemarkungsnummer::text, 4, '0'::text) END || '-' || CASE WHEN ax_flurstueck.flurnummer IS NULL THEN '000' ELSE lpad(ax_flurstueck.flurnummer::text, 3, '0'::text) END || '-' || CASE WHEN ax_flurstueck.zaehler IS NULL THEN '' ELSE lpad(ax_flurstueck.zaehler::text, 5, '0'::text) END || '-' || CASE WHEN ax_flurstueck.nenner IS NULL THEN '' ELSE '/' || lpad(ax_flurstueck.nenner::text, 3, '0'::text) END || ' ' || CASE WHEN ax_gemarkung.bezeichnung IS NOT NULL THEN ax_gemarkung.bezeichnung ELSE '' END) @@ to_tsquery('german', '" + self.getSearchStringFlurstueck() + "') AND ax_flurstueck.gemarkungsnummer = '"+ item.text(4) + "' AND ax_flurstueck.flurnummer = '"+ item.text(1) + "' \
                    UNION \
                    SELECT ax_gemarkung.bezeichnung,ax_historischesflurstueck.gemarkungsnummer,ax_historischesflurstueck.flurnummer,ax_historischesflurstueck.land,ax_historischesflurstueck.zaehler::integer,ax_historischesflurstueck.nenner::integer,'flurstueck_historisch' as typ,ax_historischesflurstueck.flurstueckskennzeichen \
                    FROM ax_historischesflurstueck \
                    LEFT JOIN ax_gemarkung ON ax_historischesflurstueck.land::text = ax_gemarkung.land::text AND ax_historischesflurstueck.gemarkungsnummer::text = ax_gemarkung.gemarkungsnummer::text AND ax_gemarkung.endet IS NULL \
                    WHERE to_tsvector('german'::regconfig,CASE WHEN ax_historischesflurstueck.gemarkungsnummer IS NULL THEN '0000' ELSE ax_historischesflurstueck.gemarkungsnummer END || ' ' || CASE WHEN ax_historischesflurstueck.flurnummer IS NULL THEN '000' ELSE ax_historischesflurstueck.flurnummer END || ' ' || CASE WHEN ax_historischesflurstueck.zaehler IS NULL THEN '' ELSE ax_historischesflurstueck.zaehler END || ' ' || CASE WHEN ax_historischesflurstueck.nenner IS NULL THEN '' ELSE ax_historischesflurstueck.nenner END || ' ' || CASE WHEN ax_historischesflurstueck.gemarkungsnummer IS NULL THEN '0000' ELSE ax_historischesflurstueck.gemarkungsnummer END || CASE WHEN ax_historischesflurstueck.flurnummer IS NULL THEN '000' ELSE ax_historischesflurstueck.flurnummer END || CASE WHEN ax_historischesflurstueck.zaehler IS NULL THEN '' ELSE ax_historischesflurstueck.zaehler END || CASE WHEN ax_historischesflurstueck.nenner IS NULL THEN '' ELSE ax_historischesflurstueck.nenner END || ' ' || CASE WHEN ax_historischesflurstueck.gemarkungsnummer IS NULL THEN '0000' ELSE lpad(ax_historischesflurstueck.gemarkungsnummer::text, 4, '0'::text) END || CASE WHEN ax_historischesflurstueck.flurnummer IS NULL THEN '000' ELSE lpad(ax_historischesflurstueck.flurnummer::text, 3, '0'::text) END || CASE WHEN ax_historischesflurstueck.zaehler IS NULL THEN '' ELSE lpad(ax_historischesflurstueck.zaehler::text, 5, '0'::text) END || CASE WHEN ax_historischesflurstueck.nenner IS NULL THEN '' ELSE lpad(ax_historischesflurstueck.nenner::text, 3, '0'::text) END || ' ' || CASE WHEN ax_historischesflurstueck.gemarkungsnummer IS NULL THEN '0000' ELSE ax_historischesflurstueck.gemarkungsnummer END || '-' || CASE WHEN ax_historischesflurstueck.flurnummer IS NULL THEN '000' ELSE ax_historischesflurstueck.flurnummer END || '-' || CASE WHEN ax_historischesflurstueck.zaehler IS NULL THEN '' ELSE ax_historischesflurstueck.zaehler END || '-' || CASE WHEN ax_historischesflurstueck.nenner IS NULL THEN '' ELSE '/' || ax_historischesflurstueck.nenner END || ' ' || CASE WHEN ax_historischesflurstueck.gemarkungsnummer IS NULL THEN '0000' ELSE lpad(ax_historischesflurstueck.gemarkungsnummer::text, 4, '0'::text) END || '-' || CASE WHEN ax_historischesflurstueck.flurnummer IS NULL THEN '000' ELSE lpad(ax_historischesflurstueck.flurnummer::text, 3, '0'::text) END || '-' || CASE WHEN ax_historischesflurstueck.zaehler IS NULL THEN '' ELSE lpad(ax_historischesflurstueck.zaehler::text, 5, '0'::text) END || '-' || CASE WHEN ax_historischesflurstueck.nenner IS NULL THEN '' ELSE '/' || lpad(ax_historischesflurstueck.nenner::text, 3, '0'::text) END || ' ' || CASE WHEN ax_gemarkung.bezeichnung IS NOT NULL THEN ax_gemarkung.bezeichnung ELSE '' END) @@ to_tsquery('german', '" + self.getSearchStringFlurstueck() + "') AND ax_historischesflurstueck.gemarkungsnummer = '"+ item.text(4) + "' AND ax_historischesflurstueck.flurnummer = '"+ item.text(1) + "' \
                    UNION \
                    SELECT ax_gemarkung.bezeichnung,ax_historischesflurstueckohneraumbezug.gemarkungsnummer,ax_historischesflurstueckohneraumbezug.flurnummer,ax_historischesflurstueckohneraumbezug.land,ax_historischesflurstueckohneraumbezug.zaehler::integer,ax_historischesflurstueckohneraumbezug.nenner::integer,'flurstueck_historisch_ungenau' as typ,ax_historischesflurstueckohneraumbezug.flurstueckskennzeichen \
                    FROM ax_historischesflurstueckohneraumbezug \
                    LEFT JOIN ax_gemarkung ON ax_historischesflurstueckohneraumbezug.land::text = ax_gemarkung.land::text AND ax_historischesflurstueckohneraumbezug.gemarkungsnummer::text = ax_gemarkung.gemarkungsnummer::text AND ax_gemarkung.endet IS NULL \
                    WHERE to_tsvector('german'::regconfig,CASE WHEN ax_historischesflurstueckohneraumbezug.gemarkungsnummer IS NULL THEN '0000' ELSE ax_historischesflurstueckohneraumbezug.gemarkungsnummer END || ' ' || CASE WHEN ax_historischesflurstueckohneraumbezug.flurnummer IS NULL THEN '000' ELSE ax_historischesflurstueckohneraumbezug.flurnummer END || ' ' || CASE WHEN ax_historischesflurstueckohneraumbezug.zaehler IS NULL THEN '' ELSE ax_historischesflurstueckohneraumbezug.zaehler END || ' ' || CASE WHEN ax_historischesflurstueckohneraumbezug.nenner IS NULL THEN '' ELSE ax_historischesflurstueckohneraumbezug.nenner END || ' ' || CASE WHEN ax_historischesflurstueckohneraumbezug.gemarkungsnummer IS NULL THEN '0000' ELSE ax_historischesflurstueckohneraumbezug.gemarkungsnummer END || CASE WHEN ax_historischesflurstueckohneraumbezug.flurnummer IS NULL THEN '000' ELSE ax_historischesflurstueckohneraumbezug.flurnummer END || CASE WHEN ax_historischesflurstueckohneraumbezug.zaehler IS NULL THEN '' ELSE ax_historischesflurstueckohneraumbezug.zaehler END || CASE WHEN ax_historischesflurstueckohneraumbezug.nenner IS NULL THEN '' ELSE ax_historischesflurstueckohneraumbezug.nenner END || ' ' || CASE WHEN ax_historischesflurstueckohneraumbezug.gemarkungsnummer IS NULL THEN '0000' ELSE lpad(ax_historischesflurstueckohneraumbezug.gemarkungsnummer::text, 4, '0'::text) END || CASE WHEN ax_historischesflurstueckohneraumbezug.flurnummer IS NULL THEN '000' ELSE lpad(ax_historischesflurstueckohneraumbezug.flurnummer::text, 3, '0'::text) END || CASE WHEN ax_historischesflurstueckohneraumbezug.zaehler IS NULL THEN '' ELSE lpad(ax_historischesflurstueckohneraumbezug.zaehler::text, 5, '0'::text) END || CASE WHEN ax_historischesflurstueckohneraumbezug.nenner IS NULL THEN '' ELSE lpad(ax_historischesflurstueckohneraumbezug.nenner::text, 3, '0'::text) END || ' ' || CASE WHEN ax_historischesflurstueckohneraumbezug.gemarkungsnummer IS NULL THEN '0000' ELSE ax_historischesflurstueckohneraumbezug.gemarkungsnummer END || '-' || CASE WHEN ax_historischesflurstueckohneraumbezug.flurnummer IS NULL THEN '000' ELSE ax_historischesflurstueckohneraumbezug.flurnummer END || '-' || CASE WHEN ax_historischesflurstueckohneraumbezug.zaehler IS NULL THEN '' ELSE ax_historischesflurstueckohneraumbezug.zaehler END || '-' || CASE WHEN ax_historischesflurstueckohneraumbezug.nenner IS NULL THEN '' ELSE '/' || ax_historischesflurstueckohneraumbezug.nenner END || ' ' || CASE WHEN ax_historischesflurstueckohneraumbezug.gemarkungsnummer IS NULL THEN '0000' ELSE lpad(ax_historischesflurstueckohneraumbezug.gemarkungsnummer::text, 4, '0'::text) END || '-' || CASE WHEN ax_historischesflurstueckohneraumbezug.flurnummer IS NULL THEN '000' ELSE lpad(ax_historischesflurstueckohneraumbezug.flurnummer::text, 3, '0'::text) END || '-' || CASE WHEN ax_historischesflurstueckohneraumbezug.zaehler IS NULL THEN '' ELSE lpad(ax_historischesflurstueckohneraumbezug.zaehler::text, 5, '0'::text) END || '-' || CASE WHEN ax_historischesflurstueckohneraumbezug.nenner IS NULL THEN '' ELSE '/' || lpad(ax_historischesflurstueckohneraumbezug.nenner::text, 3, '0'::text) END || ' ' || CASE WHEN ax_gemarkung.bezeichnung IS NOT NULL THEN ax_gemarkung.bezeichnung ELSE '' END) @@ to_tsquery('german', '" + self.getSearchStringFlurstueck() + "') AND ax_historischesflurstueckohneraumbezug.gemarkungsnummer = '"+ item.text(4) + "' AND ax_historischesflurstueckohneraumbezug.flurnummer = '"+ item.text(1) + "') as subquery ORDER BY gemarkungsnummer,flurnummer,zaehler,nenner"
                else:
                    sqlFlurstueck = "SELECT * FROM (SELECT ax_gemarkung.bezeichnung,ax_flurstueck.gemarkungsnummer,ax_flurstueck.flurnummer,ax_flurstueck.land,ax_flurstueck.zaehler::integer,ax_flurstueck.nenner::integer,'flurstueck_aktuell' as typ,ax_flurstueck.flurstueckskennzeichen \
                    FROM ax_flurstueck \
                    LEFT JOIN ax_gemarkung ON ax_flurstueck.land::text = ax_gemarkung.land::text AND ax_flurstueck.gemarkungsnummer::text = ax_gemarkung.gemarkungsnummer::text AND ax_gemarkung.endet IS NULL \
                    WHERE to_tsvector('german'::regconfig, CASE WHEN ax_flurstueck.gemarkungsnummer IS NULL THEN '0000' ELSE ax_flurstueck.gemarkungsnummer END || ' ' || CASE WHEN ax_flurstueck.flurnummer IS NULL THEN '000' ELSE ax_flurstueck.flurnummer END || ' ' || CASE WHEN ax_flurstueck.zaehler IS NULL THEN 0 ELSE ax_flurstueck.zaehler END || ' ' || CASE WHEN ax_flurstueck.nenner IS NULL THEN '' ELSE ax_flurstueck.nenner END || ' ' || CASE WHEN ax_flurstueck.gemarkungsnummer IS NULL THEN '0000' ELSE ax_flurstueck.gemarkungsnummer END || CASE WHEN ax_flurstueck.flurnummer IS NULL THEN '000' ELSE ax_flurstueck.flurnummer END || CASE WHEN ax_flurstueck.zaehler IS NULL THEN 0 ELSE ax_flurstueck.zaehler END || CASE WHEN ax_flurstueck.nenner IS NULL THEN '' ELSE ax_flurstueck.nenner END || ' ' || CASE WHEN ax_flurstueck.gemarkungsnummer IS NULL THEN '0000' ELSE lpad(ax_flurstueck.gemarkungsnummer::text, 4, '0'::text) END || CASE WHEN ax_flurstueck.flurnummer IS NULL THEN '000' ELSE lpad(ax_flurstueck.flurnummer::text, 3, '0'::text) END || CASE WHEN ax_flurstueck.zaehler IS NULL THEN '' ELSE lpad(ax_flurstueck.zaehler::text, 5, '0'::text) END || CASE WHEN ax_flurstueck.nenner IS NULL THEN '' ELSE lpad(ax_flurstueck.nenner::text, 3, '0'::text) END || ' ' || CASE WHEN ax_flurstueck.gemarkungsnummer IS NULL THEN '0000' ELSE ax_flurstueck.gemarkungsnummer END || '-' || CASE WHEN ax_flurstueck.flurnummer IS NULL THEN '000' ELSE ax_flurstueck.flurnummer END || '-' || CASE WHEN ax_flurstueck.zaehler IS NULL THEN 0 ELSE ax_flurstueck.zaehler END || '-' || CASE WHEN ax_flurstueck.nenner IS NULL THEN '' ELSE '/' || ax_flurstueck.nenner END || ' ' || CASE WHEN ax_flurstueck.gemarkungsnummer IS NULL THEN '0000' ELSE lpad(ax_flurstueck.gemarkungsnummer::text, 4, '0'::text) END || '-' || CASE WHEN ax_flurstueck.flurnummer IS NULL THEN '000' ELSE lpad(ax_flurstueck.flurnummer::text, 3, '0'::text) END || '-' || CASE WHEN ax_flurstueck.zaehler IS NULL THEN '' ELSE lpad(ax_flurstueck.zaehler::text, 5, '0'::text) END || '-' || CASE WHEN ax_flurstueck.nenner IS NULL THEN '' ELSE '/' || lpad(ax_flurstueck.nenner::text, 3, '0'::text) END || ' ' || CASE WHEN ax_gemarkung.bezeichnung IS NOT NULL THEN ax_gemarkung.bezeichnung ELSE '' END) @@ to_tsquery('german', '" + self.getSearchStringFlurstueck() + "') AND ax_flurstueck.gemarkungsnummer = '"+ item.text(1) + "' AND ax_flurstueck.flurnummer IS NULL \
                    UNION \
                    SELECT ax_gemarkung.bezeichnung,ax_historischesflurstueck.gemarkungsnummer,ax_historischesflurstueck.flurnummer,ax_historischesflurstueck.land,ax_historischesflurstueck.zaehler::integer,ax_historischesflurstueck.nenner::integer,'flurstueck_historisch' as typ,ax_historischesflurstueck.flurstueckskennzeichen \
                    FROM ax_historischesflurstueck \
                    LEFT JOIN ax_gemarkung ON ax_historischesflurstueck.land::text = ax_gemarkung.land::text AND ax_historischesflurstueck.gemarkungsnummer::text = ax_gemarkung.gemarkungsnummer::text AND ax_gemarkung.endet IS NULL \
                    WHERE to_tsvector('german'::regconfig,CASE WHEN ax_historischesflurstueck.gemarkungsnummer IS NULL THEN '0000' ELSE ax_historischesflurstueck.gemarkungsnummer END || ' ' || CASE WHEN ax_historischesflurstueck.flurnummer IS NULL THEN '000' ELSE ax_historischesflurstueck.flurnummer END || ' ' || CASE WHEN ax_historischesflurstueck.zaehler IS NULL THEN '' ELSE ax_historischesflurstueck.zaehler END || ' ' || CASE WHEN ax_historischesflurstueck.nenner IS NULL THEN '' ELSE ax_historischesflurstueck.nenner END || ' ' || CASE WHEN ax_historischesflurstueck.gemarkungsnummer IS NULL THEN '0000' ELSE ax_historischesflurstueck.gemarkungsnummer END || CASE WHEN ax_historischesflurstueck.flurnummer IS NULL THEN '000' ELSE ax_historischesflurstueck.flurnummer END || CASE WHEN ax_historischesflurstueck.zaehler IS NULL THEN '' ELSE ax_historischesflurstueck.zaehler END || CASE WHEN ax_historischesflurstueck.nenner IS NULL THEN '' ELSE ax_historischesflurstueck.nenner END || ' ' || CASE WHEN ax_historischesflurstueck.gemarkungsnummer IS NULL THEN '0000' ELSE lpad(ax_historischesflurstueck.gemarkungsnummer::text, 4, '0'::text) END || CASE WHEN ax_historischesflurstueck.flurnummer IS NULL THEN '000' ELSE lpad(ax_historischesflurstueck.flurnummer::text, 3, '0'::text) END || CASE WHEN ax_historischesflurstueck.zaehler IS NULL THEN '' ELSE lpad(ax_historischesflurstueck.zaehler::text, 5, '0'::text) END || CASE WHEN ax_historischesflurstueck.nenner IS NULL THEN '' ELSE lpad(ax_historischesflurstueck.nenner::text, 3, '0'::text) END || ' ' || CASE WHEN ax_historischesflurstueck.gemarkungsnummer IS NULL THEN '0000' ELSE ax_historischesflurstueck.gemarkungsnummer END || '-' || CASE WHEN ax_historischesflurstueck.flurnummer IS NULL THEN '000' ELSE ax_historischesflurstueck.flurnummer END || '-' || CASE WHEN ax_historischesflurstueck.zaehler IS NULL THEN '' ELSE ax_historischesflurstueck.zaehler END || '-' || CASE WHEN ax_historischesflurstueck.nenner IS NULL THEN '' ELSE '/' || ax_historischesflurstueck.nenner END || ' ' || CASE WHEN ax_historischesflurstueck.gemarkungsnummer IS NULL THEN '0000' ELSE lpad(ax_historischesflurstueck.gemarkungsnummer::text, 4, '0'::text) END || '-' || CASE WHEN ax_historischesflurstueck.flurnummer IS NULL THEN '000' ELSE lpad(ax_historischesflurstueck.flurnummer::text, 3, '0'::text) END || '-' || CASE WHEN ax_historischesflurstueck.zaehler IS NULL THEN '' ELSE lpad(ax_historischesflurstueck.zaehler::text, 5, '0'::text) END || '-' || CASE WHEN ax_historischesflurstueck.nenner IS NULL THEN '' ELSE '/' || lpad(ax_historischesflurstueck.nenner::text, 3, '0'::text) END || ' ' || CASE WHEN ax_gemarkung.bezeichnung IS NOT NULL THEN ax_gemarkung.bezeichnung ELSE '' END) @@ to_tsquery('german', '" + self.getSearchStringFlurstueck() + "') AND ax_historischesflurstueck.gemarkungsnummer = '"+ item.text(1) + "' AND ax_historischesflurstueck.flurnummer IS NULL \
                    UNION \
                    SELECT ax_gemarkung.bezeichnung,ax_historischesflurstueckohneraumbezug.gemarkungsnummer,ax_historischesflurstueckohneraumbezug.flurnummer,ax_historischesflurstueckohneraumbezug.land,ax_historischesflurstueckohneraumbezug.zaehler::integer,ax_historischesflurstueckohneraumbezug.nenner::integer,'flurstueck_historisch_ungenau' as typ,ax_historischesflurstueckohneraumbezug.flurstueckskennzeichen \
                    FROM ax_historischesflurstueckohneraumbezug \
                    LEFT JOIN ax_gemarkung ON ax_historischesflurstueckohneraumbezug.land::text = ax_gemarkung.land::text AND ax_historischesflurstueckohneraumbezug.gemarkungsnummer::text = ax_gemarkung.gemarkungsnummer::text AND ax_gemarkung.endet IS NULL \
                    WHERE to_tsvector('german'::regconfig,CASE WHEN ax_historischesflurstueckohneraumbezug.gemarkungsnummer IS NULL THEN '0000' ELSE ax_historischesflurstueckohneraumbezug.gemarkungsnummer END || ' ' || CASE WHEN ax_historischesflurstueckohneraumbezug.flurnummer IS NULL THEN '000' ELSE ax_historischesflurstueckohneraumbezug.flurnummer END || ' ' || CASE WHEN ax_historischesflurstueckohneraumbezug.zaehler IS NULL THEN '' ELSE ax_historischesflurstueckohneraumbezug.zaehler END || ' ' || CASE WHEN ax_historischesflurstueckohneraumbezug.nenner IS NULL THEN '' ELSE ax_historischesflurstueckohneraumbezug.nenner END || ' ' || CASE WHEN ax_historischesflurstueckohneraumbezug.gemarkungsnummer IS NULL THEN '0000' ELSE ax_historischesflurstueckohneraumbezug.gemarkungsnummer END || CASE WHEN ax_historischesflurstueckohneraumbezug.flurnummer IS NULL THEN '000' ELSE ax_historischesflurstueckohneraumbezug.flurnummer END || CASE WHEN ax_historischesflurstueckohneraumbezug.zaehler IS NULL THEN '' ELSE ax_historischesflurstueckohneraumbezug.zaehler END || CASE WHEN ax_historischesflurstueckohneraumbezug.nenner IS NULL THEN '' ELSE ax_historischesflurstueckohneraumbezug.nenner END || ' ' || CASE WHEN ax_historischesflurstueckohneraumbezug.gemarkungsnummer IS NULL THEN '0000' ELSE lpad(ax_historischesflurstueckohneraumbezug.gemarkungsnummer::text, 4, '0'::text) END || CASE WHEN ax_historischesflurstueckohneraumbezug.flurnummer IS NULL THEN '000' ELSE lpad(ax_historischesflurstueckohneraumbezug.flurnummer::text, 3, '0'::text) END || CASE WHEN ax_historischesflurstueckohneraumbezug.zaehler IS NULL THEN '' ELSE lpad(ax_historischesflurstueckohneraumbezug.zaehler::text, 5, '0'::text) END || CASE WHEN ax_historischesflurstueckohneraumbezug.nenner IS NULL THEN '' ELSE lpad(ax_historischesflurstueckohneraumbezug.nenner::text, 3, '0'::text) END || ' ' || CASE WHEN ax_historischesflurstueckohneraumbezug.gemarkungsnummer IS NULL THEN '0000' ELSE ax_historischesflurstueckohneraumbezug.gemarkungsnummer END || '-' || CASE WHEN ax_historischesflurstueckohneraumbezug.flurnummer IS NULL THEN '000' ELSE ax_historischesflurstueckohneraumbezug.flurnummer END || '-' || CASE WHEN ax_historischesflurstueckohneraumbezug.zaehler IS NULL THEN '' ELSE ax_historischesflurstueckohneraumbezug.zaehler END || '-' || CASE WHEN ax_historischesflurstueckohneraumbezug.nenner IS NULL THEN '' ELSE '/' || ax_historischesflurstueckohneraumbezug.nenner END || ' ' || CASE WHEN ax_historischesflurstueckohneraumbezug.gemarkungsnummer IS NULL THEN '0000' ELSE lpad(ax_historischesflurstueckohneraumbezug.gemarkungsnummer::text, 4, '0'::text) END || '-' || CASE WHEN ax_historischesflurstueckohneraumbezug.flurnummer IS NULL THEN '000' ELSE lpad(ax_historischesflurstueckohneraumbezug.flurnummer::text, 3, '0'::text) END || '-' || CASE WHEN ax_historischesflurstueckohneraumbezug.zaehler IS NULL THEN '' ELSE lpad(ax_historischesflurstueckohneraumbezug.zaehler::text, 5, '0'::text) END || '-' || CASE WHEN ax_historischesflurstueckohneraumbezug.nenner IS NULL THEN '' ELSE '/' || lpad(ax_historischesflurstueckohneraumbezug.nenner::text, 3, '0'::text) END || ' ' || CASE WHEN ax_gemarkung.bezeichnung IS NOT NULL THEN ax_gemarkung.bezeichnung ELSE '' END) @@ to_tsquery('german', '" + self.getSearchStringFlurstueck() + "') AND ax_historischesflurstueckohneraumbezug.gemarkungsnummer = '"+ item.text(1) + "' AND ax_historischesflurstueckohneraumbezug.flurnummer IS NULL) as subquery ORDER BY gemarkungsnummer,flurnummer,zaehler,nenner"
            query.exec_(sqlFlurstueck)
            if(query.size() > 0):
                fieldGemarkungsnummer = query.record().indexOf("gemarkungsnummer")
                fieldGemarkungsname = query.record().indexOf("bezeichnung")
                fieldFlurnummer = query.record().indexOf("flurnummer")
                fieldLand = query.record().indexOf("land")
                fieldZaehler = query.record().indexOf("zaehler")
                fieldNenner = query.record().indexOf("nenner")
                fieldTyp = query.record().indexOf("typ")
                fieldFlurstueckskennzeichen = query.record().indexOf("flurstueckskennzeichen")
                while(query.next()):
                    gemarkungsnummer = query.value(fieldGemarkungsnummer)
                    gemarkungsname = query.value(fieldGemarkungsname)
                    flurnummer = query.value(fieldFlurnummer)
                    land = query.value(fieldLand)
                    zaehler = query.value(fieldZaehler)
                    nenner = query.value(fieldNenner)
                    typ = query.value(fieldTyp)
                    flurstueckskennzeichen = query.value(fieldFlurstueckskennzeichen)

                    item_flst = QTreeWidgetItem(item)
                    if(nenner == None):
                        if(typ == "flurstueck_aktuell"):
                            item_flst.setText(0, str(zaehler))
                        elif(typ == "flurstueck_historisch_ungenau"):
                            item_flst.setText(0, str(zaehler) + " (historisch, ungenau)")
                        elif(typ == "flurstueck_historisch"):
                            item_flst.setText(0, str(zaehler) + " (historisch)")
                    else:
                        if(typ == "flurstueck_aktuell"):
                            item_flst.setText(0, str(zaehler) + " / " + str(nenner))
                        elif(typ == "flurstueck_historisch_ungenau"):
                            item_flst.setText(0, str(zaehler) + " / " + str(nenner) + " (historisch, ungenau)")
                        elif(typ == "flurstueck_historisch"):
                            item_flst.setText(0, str(zaehler) + " / " + str(nenner) + " (historisch)")
                    item_flst.setText(1, flurstueckskennzeichen)
                    item_flst.setText(2, "flurstueck")
                    item_flst.setText(3, typ)
            self.db.close()

    def treeLoadAdresseGemeinde(self,item):
        if(item.childCount() == 0):
            self.loadDbSettings()
            self.db.open()
            query = QSqlQuery(self.db)
            if(self.checkPostnasSeachTable() == True):
                sqlGemeinde = "SELECT ax_gemeinde.bezeichnung as gemeinde FROM postnas_search \
                JOIN ax_lagebezeichnungmithausnummer ON postnas_search.gml_id = ax_lagebezeichnungmithausnummer.gml_id \
                JOIN ax_lagebezeichnungkatalogeintrag ON ax_lagebezeichnungkatalogeintrag.land = ax_lagebezeichnungmithausnummer.land AND ax_lagebezeichnungkatalogeintrag.regierungsbezirk = ax_lagebezeichnungmithausnummer.regierungsbezirk AND ax_lagebezeichnungkatalogeintrag.kreis = ax_lagebezeichnungmithausnummer.kreis AND ax_lagebezeichnungkatalogeintrag.gemeinde = ax_lagebezeichnungmithausnummer.gemeinde AND ax_lagebezeichnungkatalogeintrag.lage = ax_lagebezeichnungmithausnummer.lage \
                JOIN ax_gemeinde ON ax_lagebezeichnungkatalogeintrag.land = ax_gemeinde.land AND ax_lagebezeichnungkatalogeintrag.regierungsbezirk = ax_gemeinde.regierungsbezirk AND ax_lagebezeichnungkatalogeintrag.kreis = ax_gemeinde.kreis AND ax_lagebezeichnungkatalogeintrag.gemeinde = ax_gemeinde.gemeinde AND ax_gemeinde.endet IS NULL \
                WHERE vector @@ to_tsquery('german', '" + self.getSearchStringAdresse() + "') GROUP BY ax_gemeinde.bezeichnung ORDER BY gemeinde"
            else:
                sqlGemeinde = "SELECT ax_gemeinde.bezeichnung as gemeinde FROM ax_lagebezeichnungmithausnummer \
                JOIN ax_lagebezeichnungkatalogeintrag ON ax_lagebezeichnungkatalogeintrag.land = ax_lagebezeichnungmithausnummer.land AND ax_lagebezeichnungkatalogeintrag.regierungsbezirk = ax_lagebezeichnungmithausnummer.regierungsbezirk AND ax_lagebezeichnungkatalogeintrag.kreis = ax_lagebezeichnungmithausnummer.kreis AND ax_lagebezeichnungkatalogeintrag.gemeinde = ax_lagebezeichnungmithausnummer.gemeinde AND ax_lagebezeichnungkatalogeintrag.lage = ax_lagebezeichnungmithausnummer.lage \
                JOIN ax_gemeinde ON ax_lagebezeichnungkatalogeintrag.land = ax_gemeinde.land AND ax_lagebezeichnungkatalogeintrag.regierungsbezirk = ax_gemeinde.regierungsbezirk AND ax_lagebezeichnungkatalogeintrag.kreis = ax_gemeinde.kreis AND ax_lagebezeichnungkatalogeintrag.gemeinde = ax_gemeinde.gemeinde AND ax_gemeinde.endet IS NULL \
                WHERE to_tsvector('german', ax_lagebezeichnungkatalogeintrag.bezeichnung || ' ' || reverse(ax_lagebezeichnungkatalogeintrag.bezeichnung::text) || ' ' || ax_lagebezeichnungmithausnummer.hausnummer || ' ' || ax_gemeinde.bezeichnung) @@ to_tsquery('german', '" + self.getSearchStringAdresse() + "') GROUP BY ax_gemeinde.bezeichnung ORDER BY gemeinde"
            query.exec_(sqlGemeinde)
            if(query.size() > 0):
                fieldGemeinde = query.record().indexOf("gemeinde")
                while(query.next()):
                    gemeinde = query.value(fieldGemeinde)

                    itemGemeinde = QTreeWidgetItem(item)
                    itemGemeinde.setText(0, unicode(gemeinde))
                    itemGemeinde.setText(2, "gemeinde")
                    itemGemeinde.setChildIndicatorPolicy(QTreeWidgetItem.ShowIndicator)
            self.db.close()

    def treeLoadAdresseStrasse(self,item):
        if(item.childCount() == 0):
            self.loadDbSettings()
            self.db.open()
            query = QSqlQuery(self.db)

            if(self.checkPostnasSeachTable() == True):
                sqlStrasse = "SELECT ax_lagebezeichnungkatalogeintrag.bezeichnung as name_strasse FROM postnas_search \
                JOIN ax_lagebezeichnungmithausnummer ON postnas_search.gml_id = ax_lagebezeichnungmithausnummer.gml_id \
                JOIN ax_lagebezeichnungkatalogeintrag ON ax_lagebezeichnungkatalogeintrag.land = ax_lagebezeichnungmithausnummer.land AND ax_lagebezeichnungkatalogeintrag.regierungsbezirk = ax_lagebezeichnungmithausnummer.regierungsbezirk AND ax_lagebezeichnungkatalogeintrag.kreis = ax_lagebezeichnungmithausnummer.kreis AND ax_lagebezeichnungkatalogeintrag.gemeinde = ax_lagebezeichnungmithausnummer.gemeinde AND ax_lagebezeichnungkatalogeintrag.lage = ax_lagebezeichnungmithausnummer.lage \
                JOIN ax_gemeinde ON ax_lagebezeichnungkatalogeintrag.land = ax_gemeinde.land AND ax_lagebezeichnungkatalogeintrag.regierungsbezirk = ax_gemeinde.regierungsbezirk AND ax_lagebezeichnungkatalogeintrag.kreis = ax_gemeinde.kreis AND ax_lagebezeichnungkatalogeintrag.gemeinde = ax_gemeinde.gemeinde AND ax_gemeinde.endet IS NULL \
                WHERE vector @@ to_tsquery('german', '" + self.getSearchStringAdresse() + "') AND ax_gemeinde.bezeichnung = '" + item.text(0) + "' GROUP BY ax_lagebezeichnungkatalogeintrag.bezeichnung ORDER BY ax_lagebezeichnungkatalogeintrag.bezeichnung"
            else:
                sqlStrasse = "SELECT ax_lagebezeichnungkatalogeintrag.bezeichnung as name_strasse FROM ax_lagebezeichnungmithausnummer \
                JOIN ax_lagebezeichnungkatalogeintrag ON ax_lagebezeichnungkatalogeintrag.land = ax_lagebezeichnungmithausnummer.land AND ax_lagebezeichnungkatalogeintrag.regierungsbezirk = ax_lagebezeichnungmithausnummer.regierungsbezirk AND ax_lagebezeichnungkatalogeintrag.kreis = ax_lagebezeichnungmithausnummer.kreis AND ax_lagebezeichnungkatalogeintrag.gemeinde = ax_lagebezeichnungmithausnummer.gemeinde AND ax_lagebezeichnungkatalogeintrag.lage = ax_lagebezeichnungmithausnummer.lage \
                JOIN ax_gemeinde ON ax_lagebezeichnungkatalogeintrag.land = ax_gemeinde.land AND ax_lagebezeichnungkatalogeintrag.regierungsbezirk = ax_gemeinde.regierungsbezirk AND ax_lagebezeichnungkatalogeintrag.kreis = ax_gemeinde.kreis AND ax_lagebezeichnungkatalogeintrag.gemeinde = ax_gemeinde.gemeinde AND ax_gemeinde.endet IS NULL \
                WHERE to_tsvector('german', ax_lagebezeichnungkatalogeintrag.bezeichnung || ' ' || reverse(ax_lagebezeichnungkatalogeintrag.bezeichnung::text) || ' ' || ax_lagebezeichnungmithausnummer.hausnummer || ' ' || ax_gemeinde.bezeichnung) @@ to_tsquery('german', '" + self.getSearchStringAdresse() + "') AND ax_gemeinde.bezeichnung = '" + item.text(0) + "' GROUP BY ax_lagebezeichnungkatalogeintrag.bezeichnung ORDER BY ax_lagebezeichnungkatalogeintrag.bezeichnung"
            query.exec_(sqlStrasse)
            if(query.size() > 0):
                fieldStrasse = query.record().indexOf("name_strasse")
                while(query.next()):
                    strasse = query.value(fieldStrasse)

                    itemStrasse = QTreeWidgetItem(item)
                    itemStrasse.setText(0,unicode(strasse))
                    itemStrasse.setText(2,"strasse")
                    itemStrasse.setChildIndicatorPolicy(QTreeWidgetItem.ShowIndicator)
            self.db.close()

    def treeLoadAdresseHausnummer(self,item):
        if(item.childCount() == 0):
            self.loadDbSettings()
            self.db.open()
            query = QSqlQuery(self.db)
            if(self.checkPostnasSeachTable() == True):
                sqlHausnummer = "SELECT postnas_search.gml_id,ax_lagebezeichnungmithausnummer.hausnummer \
                FROM postnas_search \
                JOIN ax_lagebezeichnungmithausnummer ON postnas_search.gml_id = ax_lagebezeichnungmithausnummer.gml_id \
                JOIN ax_lagebezeichnungkatalogeintrag ON ax_lagebezeichnungkatalogeintrag.land = ax_lagebezeichnungmithausnummer.land AND ax_lagebezeichnungkatalogeintrag.regierungsbezirk = ax_lagebezeichnungmithausnummer.regierungsbezirk AND ax_lagebezeichnungkatalogeintrag.kreis = ax_lagebezeichnungmithausnummer.kreis AND ax_lagebezeichnungkatalogeintrag.gemeinde = ax_lagebezeichnungmithausnummer.gemeinde AND ax_lagebezeichnungkatalogeintrag.lage = ax_lagebezeichnungmithausnummer.lage \
                JOIN ax_gemeinde ON ax_lagebezeichnungkatalogeintrag.land = ax_gemeinde.land AND ax_lagebezeichnungkatalogeintrag.regierungsbezirk = ax_gemeinde.regierungsbezirk AND ax_lagebezeichnungkatalogeintrag.kreis = ax_gemeinde.kreis AND ax_lagebezeichnungkatalogeintrag.gemeinde = ax_gemeinde.gemeinde AND ax_gemeinde.endet IS NULL \
                WHERE vector @@ to_tsquery('german', '"+self.getSearchStringAdresse()+"') AND ax_gemeinde.bezeichnung = '"+item.parent().text(0)+"' AND ax_lagebezeichnungkatalogeintrag.bezeichnung = '"+item.text(0)+"' ORDER BY regexp_replace(ax_lagebezeichnungmithausnummer.hausnummer,'[^0-9]','','g')::int,hausnummer"
            else:
                sqlHausnummer = "SELECT ax_lagebezeichnungmithausnummer.gml_id,ax_lagebezeichnungmithausnummer.hausnummer \
                FROM ax_lagebezeichnungmithausnummer \
                JOIN ax_lagebezeichnungkatalogeintrag ON ax_lagebezeichnungkatalogeintrag.land = ax_lagebezeichnungmithausnummer.land AND ax_lagebezeichnungkatalogeintrag.regierungsbezirk = ax_lagebezeichnungmithausnummer.regierungsbezirk AND ax_lagebezeichnungkatalogeintrag.kreis = ax_lagebezeichnungmithausnummer.kreis AND ax_lagebezeichnungkatalogeintrag.gemeinde = ax_lagebezeichnungmithausnummer.gemeinde AND ax_lagebezeichnungkatalogeintrag.lage = ax_lagebezeichnungmithausnummer.lage \
                JOIN ax_gemeinde ON ax_lagebezeichnungkatalogeintrag.land = ax_gemeinde.land AND ax_lagebezeichnungkatalogeintrag.regierungsbezirk = ax_gemeinde.regierungsbezirk AND ax_lagebezeichnungkatalogeintrag.kreis = ax_gemeinde.kreis AND ax_lagebezeichnungkatalogeintrag.gemeinde = ax_gemeinde.gemeinde AND ax_gemeinde.endet IS NULL \
                WHERE to_tsvector('german', ax_lagebezeichnungkatalogeintrag.bezeichnung || ' ' || reverse(ax_lagebezeichnungkatalogeintrag.bezeichnung::text) || ' ' || ax_lagebezeichnungmithausnummer.hausnummer || ' ' || ax_gemeinde.bezeichnung) @@ to_tsquery('german', '"+self.getSearchStringAdresse()+"') AND ax_gemeinde.bezeichnung = '"+item.parent().text(0)+"' AND ax_lagebezeichnungkatalogeintrag.bezeichnung = '"+item.text(0)+"' ORDER BY regexp_replace(ax_lagebezeichnungmithausnummer.hausnummer,'[^0-9]','','g')::int,hausnummer"
            query.exec_(sqlHausnummer)
            if(query.size() > 0):
                fieldGmlID = query.record().indexOf("gml_id")
                fieldHausnummer = query.record().indexOf("hausnummer")
                while(query.next()):
                    hausnummer = query.value(fieldHausnummer)
                    gmlId = query.value(fieldGmlID)

                    itemHausnummer = QTreeWidgetItem(item)
                    itemHausnummer.setText(0,unicode(hausnummer))
                    itemHausnummer.setText(1,unicode(gmlId))
                    itemHausnummer.setText(2,"hausnummer")
            self.db.close()

    def treeLoadEigentuemer(self,item):
        if(item.childCount() == 0):
            self.loadDbSettings()
            self.db.open()
            query = QSqlQuery(self.db)

            if(self.checkPostnasSeachTable() == True):
                sqlEigentuemer = "SELECT * FROM (SELECT ax_person.gml_id,nachnameoderfirma,vorname,geburtsname,namensbestandteil,akademischergrad FROM postnas_search \
                JOIN ax_person ON ax_person.gml_id = postnas_search.gml_id  \
                JOIN ax_namensnummer ON ax_person.gml_id = ax_namensnummer.benennt AND ax_namensnummer.endet IS NULL \
                JOIN ax_buchungsblatt ON ax_buchungsblatt.gml_id = ax_namensnummer.istbestandteilvon AND ax_buchungsblatt.endet IS NULL \
                WHERE vector @@ to_tsquery('german','"+self.getSearchStringEigentuemer()+"') \
                UNION \
                SELECT ax_person.gml_id,nachnameoderfirma,vorname,geburtsname,namensbestandteil,akademischergrad \
                FROM postnas_search \
                JOIN ax_person ON ax_person.gml_id = postnas_search.gml_id AND ax_person.endet IS NULL \
                JOIN ax_namensnummer ON ax_person.gml_id = ax_namensnummer.benennt AND ax_namensnummer.endet IS NULL \
                JOIN ax_buchungsblatt ON ax_buchungsblatt.gml_id = ax_namensnummer.istbestandteilvon AND ax_buchungsblatt.endet IS NULL \
                WHERE vector @@ to_tsquery('german','"+self.getSearchStringEigentuemer()+"')) as foo \
                ORDER BY CASE WHEN akademischergrad IS NOT NULL THEN akademischergrad ELSE '' END || CASE WHEN namensbestandteil IS NOT NULL THEN namensbestandteil ELSE '' END || nachnameoderfirma || CASE WHEN vorname IS NOT NULL THEN vorname ELSE '' END || CASE WHEN geburtsname IS NOT NULL THEN geburtsname ELSE '' END"
            else:
                sqlEigentuemer = "SELECT * FROM (SELECT ax_person.gml_id,nachnameoderfirma,vorname,geburtsname,namensbestandteil,akademischergrad \
                FROM ax_person \
                JOIN ax_namensnummer ON ax_person.gml_id = ax_namensnummer.benennt AND ax_namensnummer.endet IS NULL \
                JOIN ax_buchungsblatt ON ax_buchungsblatt.gml_id = ax_namensnummer.istbestandteilvon AND ax_buchungsblatt.endet IS NULL \
                WHERE to_tsvector('german',CASE WHEN nachnameoderfirma IS NOT NULL THEN nachnameoderfirma || ' ' || reverse(nachnameoderfirma) || ' ' ELSE '' END || CASE WHEN vorname IS NOT NULL THEN vorname || ' ' || reverse(vorname) || ' ' ELSE '' END || CASE WHEN geburtsname IS NOT NULL THEN geburtsname || ' ' || reverse(geburtsname) ELSE '' END || CASE WHEN namensbestandteil IS NOT NULL THEN namensbestandteil || ' ' || reverse(namensbestandteil) ELSE '' END || CASE WHEN akademischergrad IS NOT NULL THEN akademischergrad || ' ' || reverse(akademischergrad) ELSE '' END) @@ to_tsquery('german','"+self.getSearchStringEigentuemer()+"') \
                UNION \
                SELECT ax_person.gml_id,nachnameoderfirma,vorname,geburtsname,namensbestandteil,akademischergrad \
                FROM ax_person \
                JOIN ax_namensnummer ON ax_person.gml_id = ax_namensnummer.benennt AND ax_namensnummer.endet IS NULL \
                JOIN ax_buchungsblatt ON ax_buchungsblatt.gml_id = ax_namensnummer.istbestandteilvon AND ax_buchungsblatt.endet IS NULL \
                WHERE to_tsvector('german',CASE WHEN nachnameoderfirma IS NOT NULL THEN nachnameoderfirma || ' ' || reverse(nachnameoderfirma) || ' ' ELSE '' END || CASE WHEN vorname IS NOT NULL THEN vorname || ' ' || reverse(vorname) || ' ' ELSE '' END || CASE WHEN geburtsname IS NOT NULL THEN geburtsname || ' ' || reverse(geburtsname) ELSE '' END || CASE WHEN namensbestandteil IS NOT NULL THEN namensbestandteil || ' ' || reverse(namensbestandteil) ELSE '' END || CASE WHEN akademischergrad IS NOT NULL THEN akademischergrad || ' ' || reverse(akademischergrad) ELSE '' END) @@ to_tsquery('german','"+self.getSearchStringEigentuemer()+"')) as foo \
                ORDER BY CASE WHEN akademischergrad IS NOT NULL THEN akademischergrad ELSE '' END || CASE WHEN namensbestandteil IS NOT NULL THEN namensbestandteil ELSE '' END || nachnameoderfirma || CASE WHEN vorname IS NOT NULL THEN vorname ELSE '' END || CASE WHEN geburtsname IS NOT NULL THEN geburtsname ELSE '' END"
            query.exec_(sqlEigentuemer)
            if(query.size() > 0):
                fieldGmlID = query.record().indexOf("gml_id")
                fieldNachnameOderFirma = query.record().indexOf("nachnameoderfirma")
                fieldVorname = query.record().indexOf("vorname")
                fieldGeburtsname = query.record().indexOf("geburtsname")
                fieldNamensbestandteil = query.record().indexOf("namensbestandteil")
                fieldAkademischerGrad = query.record().indexOf("akademischergrad")
                while(query.next()):
                    gmlId = query.value(fieldGmlID)
                    nachnameOderFirma = query.value(fieldNachnameOderFirma)
                    vorname = query.value(fieldVorname)
                    geburtsname = query.value(fieldGeburtsname)
                    namensbestandteil = query.value(fieldNamensbestandteil)
                    akademischergrad = query.value(fieldAkademischerGrad)

                    person = ""
                    if(akademischergrad != None):
                        person += akademischergrad + " "
                    if(namensbestandteil != None):
                        person += namensbestandteil + " "
                    person += nachnameOderFirma
                    if(vorname != None):
                        person += ", " + vorname
                    if(geburtsname != None):
                        person += " (geb. " + geburtsname + ")"

                    itemPerson = QTreeWidgetItem(item)
                    itemPerson.setText(0, unicode(person))
                    itemPerson.setText(1, unicode(gmlId))
                    itemPerson.setText(2, unicode("person"))
                    itemPerson.setChildIndicatorPolicy(QTreeWidgetItem.ShowIndicator)
            self.db.close()

    def treeLoadEigentuemerFlurstuecke(self,item):
        if(item.childCount() == 0):
            self.loadDbSettings()
            self.db.open()
            query = QSqlQuery(self.db)
            sqlEigentuemerFlurstuecke = "SELECT * FROM (SELECT ax_flurstueck.land,gemarkungsnummer,flurnummer,ax_flurstueck.zaehler,ax_flurstueck.nenner,ax_flurstueck.flurstueckskennzeichen \
            FROM ax_person \
            JOIN ax_namensnummer ON ax_person.gml_id = ax_namensnummer.benennt AND ax_namensnummer.endet IS NULL \
            JOIN ax_buchungsblatt ON ax_buchungsblatt.gml_id = ax_namensnummer.istbestandteilvon AND ax_buchungsblatt.endet IS NULL \
            JOIN ax_buchungsstelle ON ax_buchungsstelle.istbestandteilvon = ax_buchungsblatt.gml_id AND ax_buchungsstelle.endet IS NULL \
            JOIN ax_flurstueck ON ax_flurstueck.istgebucht = ax_buchungsstelle.gml_id AND ax_flurstueck.endet IS NULL \
            WHERE ax_person.gml_id = '"+item.text(1)+"' \
            UNION \
            SELECT ax_flurstueck.land,gemarkungsnummer,flurnummer,ax_flurstueck.zaehler,ax_flurstueck.nenner,ax_flurstueck.flurstueckskennzeichen \
            FROM ax_person \
            JOIN ax_namensnummer ON ax_person.gml_id = ax_namensnummer.benennt AND ax_namensnummer.endet IS NULL \
            JOIN ax_buchungsblatt ON ax_buchungsblatt.gml_id = ax_namensnummer.istbestandteilvon AND ax_buchungsblatt.endet IS NULL \
            JOIN ax_buchungsstelle ON ax_buchungsstelle.istbestandteilvon = ax_buchungsblatt.gml_id AND ax_buchungsstelle.endet IS NULL \
            JOIN ax_buchungsstelle as ax_buchungsstelle_2 ON ax_buchungsstelle_2.gml_id = ANY(ax_buchungsstelle.an) AND ax_buchungsstelle_2.endet IS NULL \
            JOIN ax_flurstueck ON ax_flurstueck.istgebucht = ax_buchungsstelle_2.gml_id AND ax_flurstueck.endet IS NULL \
            WHERE ax_person.gml_id = '"+item.text(1)+"') as foo \
            ORDER BY land, gemarkungsnummer,flurnummer,zaehler,nenner"
            query.exec_(sqlEigentuemerFlurstuecke)
            if(query.size() > 0):
                fieldLand = query.record().indexOf("land")
                fieldGemarkungsnummer = query.record().indexOf("gemarkungsnummer")
                fieldFlurnummer = query.record().indexOf("flurnummer")
                fieldZaehler = query.record().indexOf("zaehler")
                fieldNenner = query.record().indexOf("nenner")
                fieldFlurstueckskennzeichen = query.record().indexOf("flurstueckskennzeichen")
                while(query.next()):
                    land = query.value(fieldLand)
                    gemarkungsnummer = query.value(fieldGemarkungsnummer)
                    flurnummer = query.value(fieldFlurnummer)
                    zaehler = query.value(fieldZaehler)
                    nenner = query.value(fieldNenner)
                    flurstueckskennzeichen = query.value(fieldFlurstueckskennzeichen)
                    flurstueck = unicode(land).zfill(2) + unicode(gemarkungsnummer).zfill(4) + '-' + unicode(flurnummer).zfill(3) + '-' + unicode(zaehler).zfill(5)
                    if(nenner != None):
                        flurstueck += "/" + unicode(nenner).zfill(3)

                    itemFlurstueck = QTreeWidgetItem(item)
                    itemFlurstueck.setText(0,unicode(flurstueck))
                    itemFlurstueck.setText(1, flurstueckskennzeichen)
                    itemFlurstueck.setText(2, "flurstueck")
                    itemFlurstueck.setText(3, "flurstueck_aktuell")

    def getSearchStringFlurstueck(self):
        return unicode(self.lineEdit.text().replace(" ", " & "))

    def getSearchStringAdresse(self):
        searchStringAdresse = unicode("")
        if(len(''.join([i for i in self.lineEdit.text() if not i.isdigit()])) > 0):
            searchStringAdresse += unicode((''.join([i for i in self.lineEdit.text() if not i.isdigit()])).strip()).replace(" ", ":* & ") + ":* "
            if(len(searchStringAdresse) > 0 and len(''.join([i for i in self.lineEdit.text() if i.isdigit()])) > 0):
                searchStringAdresse += " & "
            searchStringAdresse += unicode((''.join([i for i in self.lineEdit.text() if i.isdigit()])).strip()).replace(" ", " & ")
            searchStringAdresse += " | " + unicode((''.join([i for i in self.lineEdit.text() if not i.isdigit()])).strip()[::-1]).replace(" ", ":* & ") + ":* "
            if(len(''.join([i for i in self.lineEdit.text() if i.isdigit()])) > 0):
                searchStringAdresse = searchStringAdresse + " & " + unicode((''.join([i for i in self.lineEdit.text() if i.isdigit()]))).replace(" ", ":* & ")
        return unicode(searchStringAdresse)

    def getSearchStringEigentuemer(self):
        searchStringEigentuemer = self.lineEdit.text().replace(" ", ":* & ") + ":*"
        searchStringEigentuemer += " | " + self.lineEdit.text()[::-1].replace(" ", ":* & ") + ":*"
        return searchStringEigentuemer

    def on_showButton_pressed(self):
        searchStringFlst = "";
        searchStringFlur = "";
        searchStringGemarkung = "";
        searchStringStrasse = "";
        searchStringPerson = "";
        searchTyp = "";

        for item in self.treeWidget.selectedItems():
            if(item.text(2) == "flurstueck"):
                if(len(searchStringFlst) > 0):
                    searchStringFlst += "','"
                searchStringFlst += item.text(1)
                searchTyp = item.text(3)
            if(item.text(2) == "flur"):
                if(len(searchStringFlur) > 0):
                    searchStringFlur += '|'
                searchStringFlur += item.text(3)
            if(item.text(2) == "gemarkung"):
                if(len(searchStringGemarkung) > 0):
                    searchStringGemarkung += '|'
                searchStringGemarkung += item.text(3)
            if(item.text(2) == "strasse"):
                if(len(searchStringStrasse) >0):
                    searchStringStrasse += ','
                searchStringStrasse += "'" + item.text(1) + "'"
            if(item.text(2) == "person"):
                if(len(searchStringPerson) > 0):
                    searchStringPerson += ','
                searchStringPerson += "'" + item.text(1) + "'"

        if(len(searchStringGemarkung) > 0):
            self.addMapGemarkung(searchStringGemarkung)
            pass

        if(len(searchStringFlur) > 0):
            self.addMapFlur(searchStringFlur)
            pass

        if(len(searchStringFlst) > 0):
            self.addMapFlurstueck(searchStringFlst,searchTyp)

        if(len(searchStringStrasse) > 0):
            self.addMapHausnummer(searchStringStrasse)

        if(len(searchStringPerson) > 0):
            self.addMapPerson(searchStringPerson)

    def addMapPerson(self,personGmlId):
        sqlLayer = "(SELECT row_number() over () as id,* FROM (SELECT nachnameoderfirma,vorname,geburtsname,namensbestandteil,akademischergrad,ax_flurstueck.land,gemarkungsnummer,flurnummer,ax_flurstueck.zaehler,ax_flurstueck.nenner,ax_flurstueck.flurstueckskennzeichen,ax_flurstueck.wkb_geometry FROM ax_person JOIN ax_namensnummer ON ax_person.gml_id = ax_namensnummer.benennt AND ax_namensnummer.endet IS NULL JOIN ax_buchungsblatt ON ax_buchungsblatt.gml_id = ax_namensnummer.istbestandteilvon AND ax_buchungsblatt.endet IS NULL JOIN ax_buchungsstelle ON ax_buchungsstelle.istbestandteilvon = ax_buchungsblatt.gml_id AND ax_buchungsstelle.endet IS NULL JOIN ax_flurstueck ON ax_flurstueck.istgebucht = ax_buchungsstelle.gml_id AND ax_flurstueck.endet IS NULL WHERE ax_person.gml_id IN ("+personGmlId+") UNION SELECT nachnameoderfirma,vorname,geburtsname,namensbestandteil,akademischergrad,ax_flurstueck.land,gemarkungsnummer,flurnummer,ax_flurstueck.zaehler,ax_flurstueck.nenner,ax_flurstueck.flurstueckskennzeichen,ax_flurstueck.wkb_geometry FROM ax_person JOIN ax_namensnummer ON ax_person.gml_id = ax_namensnummer.benennt AND ax_namensnummer.endet IS NULL JOIN ax_buchungsblatt ON ax_buchungsblatt.gml_id = ax_namensnummer.istbestandteilvon AND ax_buchungsblatt.endet IS NULL JOIN ax_buchungsstelle ON ax_buchungsstelle.istbestandteilvon = ax_buchungsblatt.gml_id AND ax_buchungsstelle.endet IS NULL JOIN ax_buchungsstelle as ax_buchungsstelle_2 ON ax_buchungsstelle_2.gml_id = ANY(ax_buchungsstelle.an) AND ax_buchungsstelle_2.endet IS NULL JOIN ax_flurstueck ON ax_flurstueck.istgebucht = ax_buchungsstelle_2.gml_id AND ax_flurstueck.endet IS NULL WHERE ax_person.gml_id IN ("+personGmlId+") AND ax_person.endet IS NULL) as foo)"
        self.resetSuchergebnisLayer()
        uri = QgsDataSourceURI()
        uri.setConnection(self.dbHost, "5432", self.dbDatabasename, self.dbUsername, self.dbPassword)
        uri.setDataSource("", sqlLayer, "wkb_geometry","","id")
        vlayer = QgsVectorLayer(uri.uri(),  "Suchergebnis", "postgres")
        self.addSuchergebnisLayer(vlayer)

    def addMapHausnummer(self,searchString):
        if(len(searchString) > 0):
            self.resetSuchergebnisLayer()
            uri = QgsDataSourceURI()
            uri.setConnection(self.dbHost, "5432", self.dbDatabasename, self.dbUsername, self.dbPassword)
            uri.setDataSource("public", "ap_pto", "wkb_geometry","ARRAY[" + searchString + "]::character(16)[] @> dientzurdarstellungvon")
            vlayer = QgsVectorLayer(uri.uri(),  "Suchergebnis", "postgres")

            self.addSuchergebnisLayer(vlayer,"strasse")

    def addMapFlurstueck(self, searchString, typ = None):
        if(len(searchString) > 0):
            self.resetSuchergebnisLayer()

            uri = QgsDataSourceURI()
            uri.setConnection(self.dbHost, "5432", self.dbDatabasename, self.dbUsername, self.dbPassword)
            if(typ == "flurstueck_aktuell"):
                uri.setDataSource("public", "ax_flurstueck", "wkb_geometry", "flurstueckskennzeichen IN ('" +  searchString + "')")
            elif(typ == "flurstueck_historisch"):
                uri.setDataSource("public", "ax_historischesflurstueck", "wkb_geometry", "flurstueckskennzeichen IN ('" +  searchString + "')")
            elif(typ == "flurstueck_historisch_ungenau"):
                sqlLayer = "(SELECT row_number() over () as id, st_setsrid(st_extent(wkb_geometry),25832) as wkb_geometry FROM ax_flurstueck WHERE flurstueckskennzeichen IN (" + self.getNachfolger(searchString) + "))"
                uri.setDataSource("", sqlLayer, "wkb_geometry","","id")

            vlayer = QgsVectorLayer(uri.uri(),  "Suchergebnis", "postgres")

            self.addSuchergebnisLayer(vlayer,typ)

    def getNachfolger(self,flurstueck):
        returnString = None
        if(len(flurstueck.replace("'","").split(",")) > 1):
            for f in flurstueck.replace("'","").split(","):
                if(returnString != None):
                    returnString += ","
                    returnString += self.getNachfolger(f)
                else:
                    returnString = self.getNachfolger(f)
            return returnString
        else:
            if(hasattr(self,"db") == False):
                self.loadDbSettings()
            else:
                if(self.db.isOpen() == False):
                    self.db.open()
            queryHist = QSqlQuery(self.db)
            queryAktuell = QSqlQuery(self.db)

            sqlFlurstueckOhneRaumbezug = "SELECT flurstueckskennzeichen,array_to_string(nachfolgerflurstueckskennzeichen,',') as nachfolgerflurstueckskennzeichen FROM ax_historischesflurstueck WHERE flurstueckskennzeichen = '" + flurstueck + "' UNION SELECT flurstueckskennzeichen,array_to_string(nachfolgerflurstueckskennzeichen,',') as nachfolgerflurstueckskennzeichen FROM ax_historischesflurstueckohneraumbezug WHERE flurstueckskennzeichen = '" + flurstueck + "'";
            sqlAktuell = "SELECT flurstueckskennzeichen,st_astext(wkb_geometry) as wkt FROM ax_flurstueck WHERE flurstueckskennzeichen = '" + flurstueck + "' AND endet IS NULL";


            queryHist.exec_(sqlFlurstueckOhneRaumbezug)
            if(queryHist.size() == 0):
                queryAktuell.exec_(sqlAktuell)
                if(queryAktuell.size() > 0):
                    while(queryAktuell.next()):
                        if(returnString == None):
                            returnString = "'" + queryAktuell.value(queryAktuell.record().indexOf("flurstueckskennzeichen")) + "'"
                        else:
                            returnString += ",'" + queryAktuell.value(queryAktuell.record().indexOf("flurstueckskennzeichen")) + "'"
            else:
                while(queryHist.next()):
                    flurstuecke = queryHist.value(queryHist.record().indexOf("nachfolgerflurstueckskennzeichen")).split(',')
                    for f in flurstuecke:
                        if(returnString != None):
                            returnString += ","
                            returnString += self.getNachfolger(f)
                        else:
                            returnString = self.getNachfolger(f)

            return returnString

    def addMapFlur(self, searchString):
        if(len(searchString) > 0):
            self.resetSuchergebnisLayer()

            uri = QgsDataSourceURI()
            uri.setConnection(self.dbHost, "5432", self.dbDatabasename, self.dbUsername, self.dbPassword)
            uri.setDataSource("public", "ax_flurstueck", "wkb_geometry", "flurstueckskennzeichen SIMILAR TO '(" +  searchString + ")%'")
            vlayer = QgsVectorLayer(uri.uri(),  "Suchergebnis", "postgres")

            self.addSuchergebnisLayer(vlayer)

    def addMapGemarkung(self, searchString):
        if(len(searchString) > 0):
            self.resetSuchergebnisLayer()

            uri = QgsDataSourceURI()
            uri.setConnection(self.dbHost, "5432", self.dbDatabasename, self.dbUsername, self.dbPassword)
            uri.setDataSource("public", "ax_flurstueck", "wkb_geometry", "flurstueckskennzeichen SIMILAR TO '(" +  searchString + ")%'")
            vlayer = QgsVectorLayer(uri.uri(),  "Suchergebnis", "postgres")

            self.addSuchergebnisLayer(vlayer)

    def addSuchergebnisLayer(self, vlayer, typ = "aktuell"):
        symbol = QgsSymbolV2.defaultSymbol(vlayer.geometryType())
        if(symbol != None):
            symbol.setAlpha(1)

            if(typ == "flurstueck_historisch" or typ == "flurstueck_historisch_ungenau"):
                myColour = QtGui.QColor('#FDBF6F')
            else:
                myColour = QtGui.QColor('#F08080')
            symbol.setColor(myColour)

            myRenderer = QgsSingleSymbolRendererV2(symbol)
            vlayer.setRendererV2(myRenderer)
            vlayer.setBlendMode(13)
            if(typ == "flurstueck_historisch" or typ == "flurstueck_historisch_ungenau"):
                vlayer.rendererV2().symbol().symbolLayer(0).setBorderStyle(2)
            elif(typ == "strasse"):
                vlayer.rendererV2().symbol().symbolLayer(0).setSize(10)

            # Insert Layer at Top of Legend
            QgsMapLayerRegistry.instance().addMapLayer(vlayer, False)
            QgsProject.instance().layerTreeRoot().insertLayer(0, vlayer)

            canvas = self.iface.mapCanvas()
            if(canvas.hasCrsTransformEnabled() == True):
                transform = QgsCoordinateTransform(vlayer.crs(), canvas.mapSettings().destinationCrs())
                canvas.setExtent(transform.transform(vlayer.extent().buffer(50)))
            else:
                canvas.setExtent(vlayer.extent().buffer(50))

            self.resetButton.setEnabled(True)

    def resetSuchergebnisLayer(self):
         if(len(self.map.mapLayersByName("Suchergebnis")) > 0):
            self.map.removeMapLayer(self.map.mapLayersByName("Suchergebnis")[0].id())

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