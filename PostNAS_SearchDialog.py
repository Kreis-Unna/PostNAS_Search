# -*- coding: utf-8 -*-
"""
/***************************************************************************
    PostNAS_Search
    -------------------
    Date                : April 2015
    copyright          : (C) 2015 by Kreis-Unna
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

import os

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtSql import *
from PyQt4 import QtGui, uic, QtCore
from qgis.core import *
from Ui_PostNAS_SearchDialogBase import Ui_PostNAS_SearchDialogBase

class PostNAS_SearchDialog(QtGui.QDialog, Ui_PostNAS_SearchDialogBase):
    def __init__(self, parent=None,  iface=None):
        super(PostNAS_SearchDialog, self).__init__(parent)
        self.setupUi(self)
        self.iface = iface

        self.map = QgsMapLayerRegistry.instance()
        self.treeWidget.setColumnCount(1)

    def on_lineEdit_returnPressed(self):
        searchString = self.lineEdit.text()
        searchString = searchString.replace(" ", " & ")
        QApplication.setOverrideCursor(Qt.WaitCursor)
        if(len(searchString) > 0):
            self.loadDbSettings()
            self.db.open()
            query = QSqlQuery(self.db)
            query.prepare(
                "SELECT ax_flurstueck.gemarkungsnummer, \
                ax_gemarkung.bezeichnung, \
                ax_flurstueck.land, \
                ax_flurstueck.flurnummer, \
                ax_flurstueck.zaehler, \
                ax_flurstueck.nenner, \
                ax_flurstueck.flurstueckskennzeichen \
                FROM ax_flurstueck \
                LEFT JOIN ax_gemarkung ON ax_flurstueck.land::text = ax_gemarkung.land::text \
                    AND ax_flurstueck.gemarkungsnummer::text = ax_gemarkung.gemarkungsnummer::text \
                WHERE to_tsvector('german'::regconfig, \
                    ((((((((((((((((((((((( \
                    ax_flurstueck.flurstueckskennzeichen::text || \' \"\'::text) || \
                    lpad(ax_flurstueck.land::text, 2, \'0\'::text)) || \
                    lpad(ax_flurstueck.gemarkungsnummer::text, 4, \'0\'::text)) || \
                    \'-\'::text) || \
                    CASE \
                    	WHEN ax_flurstueck.flurnummer IS NULL THEN \'000\' \
                    	ELSE lpad(ax_flurstueck.flurnummer::text, 3, \'0\'::text) \
                    END) || \
                    \'-\'::text) || lpad(ax_flurstueck.zaehler::text, 5, \'0\'::text)) || \'/\'::text) || \
                    CASE \
                        WHEN ax_flurstueck.nenner IS NULL THEN \'000\'::text \
                        ELSE lpad(ax_flurstueck.nenner::text, 3, \'0\'::text) \
                    END) || \'\" \"\'::text) || ax_flurstueck.gemarkungsnummer::text) || \
                    \'-\'::text) || \
                    CASE \
                    	WHEN ax_flurstueck.flurnummer IS NULL THEN \'0\' \
                    	ELSE ax_flurstueck.flurnummer::text \
                    END) || \'-\'::text) || \
                    ax_flurstueck.zaehler::text) || \'/\'::text) || \
                    CASE \
                        WHEN ax_flurstueck.nenner IS NULL THEN \'0\'::text \
                        ELSE ax_flurstueck.nenner::text \
                    END) || \'\" \'::text) || \
                    CASE \
	                    WHEN ax_gemarkung.bezeichnung IS NULL THEN ''::text \
	                    ELSE ax_gemarkung.bezeichnung::text \
                    END) || \' \'::text) || \
                    CASE \
                    	WHEN ax_flurstueck.flurnummer IS NULL THEN \'0\' \
                    	ELSE ax_flurstueck.flurnummer::text \
                    END) || \' \"\'::text) || \
                    CASE \
                        WHEN ax_flurstueck.nenner IS NULL THEN ax_flurstueck.zaehler::text \
                        ELSE (ax_flurstueck.zaehler::text || \'/\'::text) || ax_flurstueck.nenner::text \
                    END) || \'\" \'::text || ax_flurstueck.zaehler::text) @@ to_tsquery(\'german\', :search) \
                ORDER BY ax_gemarkung.bezeichnung,flurstueckskennzeichen")
            query.bindValue(":search", unicode(searchString))
            query.exec_()
            self.treeWidget.clear()

            if(query.size() > 0):
                fieldNrFlurst = query.record().indexOf("flurstueckskennzeichen")
                fieldGemarkungsnummer = query.record().indexOf("gemarkungsnummer")
                fieldGemarkungsname = query.record().indexOf("bezeichnung")
                fieldLand = query.record().indexOf("land")
                fieldFlurnummer = query.record().indexOf("flurnummer")
                fieldZaehler = query.record().indexOf("zaehler")
                fieldNenner = query.record().indexOf("nenner")
                while(query.next()):
                    item_gemarkung = None
                    item_flur = None
                    flurstuecknummer = query.value(fieldNrFlurst)
                    gemarkungsnummer = query.value(fieldGemarkungsnummer)
                    gemarkungsname = query.value(fieldGemarkungsname)
                    land = query.value(fieldLand)
                    flurnummer = query.value(fieldFlurnummer)
                    zaehler = query.value(fieldZaehler)
                    nenner = query.value(fieldNenner)

                    if(self.treeWidget.topLevelItemCount() > 0):
                        for i in range(0, self.treeWidget.topLevelItemCount()):
                            if(self.treeWidget.topLevelItem(i).text(1) == str(gemarkungsnummer)):
                                item_gemarkung = self.treeWidget.topLevelItem(i)
                                break
                        if(item_gemarkung is None):
                            item_gemarkung = QTreeWidgetItem(self.treeWidget)
                            if(gemarkungsname == NULL):
                                item_gemarkung.setText(0, "Gemarkung " + str(gemarkungsnummer))
                            else:
                                item_gemarkung.setText(0, "Gemarkung " + unicode(gemarkungsname) + " / " + str(gemarkungsnummer))
                            item_gemarkung.setText(1, str(gemarkungsnummer))
                            item_gemarkung.setText(2, "gemarkung")
                            item_gemarkung.setText(3, str(land).zfill(2) + str(gemarkungsnummer).zfill(4))
                    else:
                        item_gemarkung = QTreeWidgetItem(self.treeWidget)
                        if(gemarkungsname == NULL):
                            item_gemarkung.setText(0, "Gemarkung " + str(gemarkungsnummer))
                        else:
                            item_gemarkung.setText(0, "Gemarkung " + unicode(gemarkungsname) + " / " + str(gemarkungsnummer))
                        item_gemarkung.setText(1, str(gemarkungsnummer))
                        item_gemarkung.setText(2, "gemarkung")
                        item_gemarkung.setText(3, str(land).zfill(2) + str(gemarkungsnummer).zfill(4))

                    for i in range(0, item_gemarkung.childCount()):
                        if(item_gemarkung.child(i).text(1) == str(flurnummer)):
                            item_flur = item_gemarkung.child(i)
                            break
                    if(item_flur is None):
                        if(flurnummer != 0):
                            item_flur = QTreeWidgetItem(item_gemarkung)
                            item_flur.setText(0, "Flur " + str(flurnummer))
                            item_flur.setText(1, str(flurnummer))
                            item_flur.setText(2, "flur")
                            item_flur.setText(3, str(land).zfill(2) + str(gemarkungsnummer).zfill(4) + str(flurnummer).zfill(3))

                    if(flurnummer != 0):
                        item_flst = QTreeWidgetItem(item_flur)
                    else:
                        item_flst = QTreeWidgetItem(item_gemarkung)
                    if(nenner == NULL):
                        item_flst.setText(0, str(zaehler))
                    else:
                        item_flst.setText(0, str(zaehler) + " / " + str(nenner))
                    item_flst.setText(1, flurstuecknummer)
                    item_flst.setText(2, "flurstueck")

                self.showButton.setEnabled(True)

                # Gemarkung aufklappen, wenn nur eine vorhanden ist
                if(self.treeWidget.topLevelItemCount() == 1):
                    self.treeWidget.expandItem(self.treeWidget.topLevelItem(0))

                # Flur aufklappen, wenn nur eine vorhanden ist
                if(self.treeWidget.topLevelItem(0).childCount() == 1):
                    self.treeWidget.expandItem(self.treeWidget.topLevelItem(0).child(0))

                # Wenn nur ein Flurstück gefunden wurd, dieses direkt anzeigen
                if (query.size() == 1):
                    self.addMapFlurstueck("'" + flurstuecknummer + "'")

                self.db.close()
            else:
                item_gemarkung = QTreeWidgetItem(self.treeWidget)
                item_gemarkung.setText(0, "Keine Ergebnisse")
        else:
            self.treeWidget.clear()
        QApplication.setOverrideCursor(Qt.ArrowCursor)

    def on_treeWidget_itemDoubleClicked(self, item):
        if(item.text(2) == "flurstueck"):
            self.addMapFlurstueck("'" + item.text(1) + "'")
        if(item.text(2) == "flur"):
            self.addMapFlur(item.text(3))
        if(item.text(2) == "gemarkung"):
            self.addMapGemarkung(item.text(3))

    def keyPressEvent(self, event):
        if (event.key() == QtCore.Qt.Key_Return or event.key() == QtCore.Qt.Key_Enter):
            self.on_showButton_pressed()

    def on_resetButton_pressed(self):
        self.treeWidget.clear()
        self.lineEdit.clear()
        self.resetSuchergebnisLayer()
        self.showButton.setEnabled(False)
        self.resetButton.setEnabled(False)

    def on_showButton_pressed(self):
        searchStringFlst = "";
        searchStringFlur = "";
        searchStringGemarkung = "";
        for item in self.treeWidget.selectedItems():
            if(item.text(2) == "flurstueck"):
                if(len(searchStringFlst) > 0):
                    searchStringFlst += ','
                searchStringFlst += "'" + item.text(1) + "'"
            if(item.text(2) == "flur"):
                if(len(searchStringFlur) > 0):
                    searchStringFlur += '|'
                searchStringFlur += item.text(3)
            if(item.text(2) == "gemarkung"):
                if(len(searchStringGemarkung) > 0):
                    searchStringGemarkung += '|'
                searchStringGemarkung += item.text(3)

        if(len(searchStringGemarkung) > 0):
            self.addMapGemarkung(searchStringGemarkung)
            pass

        if(len(searchStringFlur) > 0):
            self.addMapFlur(searchStringFlur)
            pass

        if(len(searchStringFlst) > 0):
            self.addMapFlurstueck(searchStringFlst)

    def addMapFlurstueck(self, searchString):
        if(len(searchString) > 0):
            self.resetSuchergebnisLayer()

            uri = QgsDataSourceURI()
            uri.setConnection(self.dbHost, "5432", self.dbDatabasename, self.dbUsername, self.dbPassword)
            uri.setDataSource("public", "ax_flurstueck", "wkb_geometry", "flurstueckskennzeichen IN (" +  searchString + ")")
            vlayer = QgsVectorLayer(uri.uri(),  "Suchergebnis", "postgres")

            self.addSuchergebnisLayer(vlayer)

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

    def addSuchergebnisLayer(self, vlayer):
        myOpacity = 1
        myColour = QtGui.QColor('#F08080')
        mySymbol1 = QgsSymbolV2.defaultSymbol(vlayer.geometryType())
        mySymbol1.setColor(myColour)
        mySymbol1.setAlpha(myOpacity)
        myRenderer = QgsSingleSymbolRendererV2(mySymbol1)
        vlayer.setRendererV2(myRenderer)
        vlayer.setBlendMode(13)

        # Insert Layer at Top of Legend
        QgsMapLayerRegistry.instance().addMapLayer(vlayer, False)
        QgsProject.instance().layerTreeRoot().insertLayer(0, vlayer)

        canvas = self.iface.mapCanvas()
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

        self.db = QSqlDatabase.addDatabase("QPSQL")
        self.db.setHostName(self.dbHost)
        self.db.setPort(int(self.dbPort))
        self.db.setDatabaseName(self.dbDatabasename)
        self.db.setUserName(self.dbUsername)
        self.db.setPassword(self.dbPassword)
