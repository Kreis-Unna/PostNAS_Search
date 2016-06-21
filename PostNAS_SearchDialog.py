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

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtSql import *
from PyQt4 import QtGui, uic, QtCore
from qgis.core import *
import qgis.core
from PostNAS_SearchDialogBase import Ui_PostNAS_SearchDialogBase
import time

class PostNAS_SearchDialog(QtGui.QDialog, Ui_PostNAS_SearchDialogBase):
    def __init__(self, parent=None,  iface=None):
        super(PostNAS_SearchDialog, self).__init__(parent)
        self.setupUi(self)
        self.iface = iface

        self.map = QgsMapLayerRegistry.instance()
        self.treeWidget.setColumnCount(1)

    def on_lineEdit_returnPressed(self):
        begintime = time.time()*1000
        searchString = self.lineEdit.text()
        QApplication.setOverrideCursor(Qt.WaitCursor)
        if(len(searchString) > 0):
            self.loadDbSettings()
            self.db.open()
            query = QSqlQuery(self.db)
            self.treeWidget.clear()

            #------------------------- Flurstück suchen
            searchStringFlurstueck = searchString.replace(" ", " & ")
            if(self.checkPostnasSeachTable() == True):
                sqlFlurstueck = "SELECT * FROM ( \
                        SELECT \
                        ax_flurstueck.gemarkungsnummer::integer,\
                        ax_gemarkung.bezeichnung,\
                        ax_flurstueck.land,\
                        ax_flurstueck.flurnummer::integer,\
                        ax_flurstueck.zaehler::integer,\
                        ax_flurstueck.nenner::integer,\
                        ax_flurstueck.flurstueckskennzeichen,\
                        'aktuell' AS typ \
                        FROM postnas_search \
                        JOIN ax_flurstueck on postnas_search.gml_id = ax_flurstueck.gml_id AND ax_flurstueck.endet IS NULL \
                        JOIN ax_gemarkung ON ax_flurstueck.land::text = ax_gemarkung.land::text AND ax_flurstueck.gemarkungsnummer::text = ax_gemarkung.gemarkungsnummer::text AND ax_gemarkung.endet IS NULL \
                        WHERE vector @@ to_tsquery('german', '" + unicode(searchStringFlurstueck) + "') \
                        UNION \
                        SELECT \
                             ax_historischesflurstueck.gemarkungsnummer::integer,\
                             ax_gemarkung.bezeichnung,\
                             ax_historischesflurstueck.land,\
                             ax_historischesflurstueck.flurnummer::integer,\
                             ax_historischesflurstueck.zaehler::integer,\
                             ax_historischesflurstueck.nenner::integer,\
                             ax_historischesflurstueck.flurstueckskennzeichen,\
                             'historisch' AS typ \
                        FROM postnas_search \
                        JOIN ax_historischesflurstueck on postnas_search.gml_id = ax_historischesflurstueck.gml_id AND ax_historischesflurstueck.endet IS NULL \
                        JOIN ax_gemarkung ON ax_historischesflurstueck.land::text = ax_gemarkung.land::text AND ax_historischesflurstueck.gemarkungsnummer::text = ax_gemarkung.gemarkungsnummer::text AND ax_gemarkung.endet IS NULL \
                        WHERE vector @@ to_tsquery('german', '" + unicode(searchStringFlurstueck) + "') \
                        UNION \
                        SELECT \
                             ax_historischesflurstueckohneraumbezug.gemarkungsnummer::integer, \
                             ax_gemarkung.bezeichnung, \
                             ax_historischesflurstueckohneraumbezug.land, \
                             ax_historischesflurstueckohneraumbezug.flurnummer::integer, \
                             ax_historischesflurstueckohneraumbezug.zaehler::integer, \
                             ax_historischesflurstueckohneraumbezug.nenner::integer, \
                             ax_historischesflurstueckohneraumbezug.flurstueckskennzeichen, \
                             'historisch_ungenau' AS typ \
                        FROM postnas_search \
                        JOIN ax_historischesflurstueckohneraumbezug on postnas_search.gml_id = ax_historischesflurstueckohneraumbezug.gml_id AND ax_historischesflurstueckohneraumbezug.endet IS NULL \
                        JOIN ax_gemarkung ON ax_historischesflurstueckohneraumbezug.land::text = ax_gemarkung.land::text AND ax_historischesflurstueckohneraumbezug.gemarkungsnummer::text = ax_gemarkung.gemarkungsnummer::text AND ax_gemarkung.endet IS NULL \
                        WHERE vector @@ to_tsquery('german', '" + unicode(searchStringFlurstueck) + "') \
                        ) as foo \
                        ORDER BY gemarkungsnummer,flurnummer,zaehler,nenner"
            else:
                sqlFlurstueck = "SELECT * FROM (SELECT \
                        ax_flurstueck.gemarkungsnummer::integer, \
                        ax_gemarkung.bezeichnung, \
                        ax_flurstueck.land, \
                        ax_flurstueck.flurnummer::integer, \
                        ax_flurstueck.zaehler::integer, \
                        ax_flurstueck.nenner::integer, \
                        ax_flurstueck.flurstueckskennzeichen, \
                        'aktuell' AS typ \
                    FROM ax_flurstueck \
                    JOIN ax_gemarkung ON ax_flurstueck.land::text = ax_gemarkung.land::text AND ax_flurstueck.gemarkungsnummer::text = ax_gemarkung.gemarkungsnummer::text AND ax_gemarkung.endet IS NULL \
                    WHERE to_tsvector('german'::regconfig, \
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
                        CASE WHEN ax_gemarkung.bezeichnung IS NOT NULL THEN ax_gemarkung.bezeichnung END) @@ to_tsquery('german', '" + unicode(searchStringFlurstueck) + "') \
                    UNION \
                    SELECT \
                        ax_historischesflurstueck.gemarkungsnummer::integer, \
                        ax_gemarkung.bezeichnung, \
                        ax_historischesflurstueck.land, \
                        ax_historischesflurstueck.flurnummer::integer, \
                        ax_historischesflurstueck.zaehler::integer, \
                        ax_historischesflurstueck.nenner::integer, \
                        ax_historischesflurstueck.flurstueckskennzeichen, \
                        'historisch' AS typ \
                    FROM ax_historischesflurstueck \
                    JOIN ax_gemarkung ON ax_historischesflurstueck.land::text = ax_gemarkung.land::text AND ax_historischesflurstueck.gemarkungsnummer::text = ax_gemarkung.gemarkungsnummer::text AND ax_gemarkung.endet IS NULL \
                    WHERE to_tsvector('german'::regconfig, \
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
        			) @@ to_tsquery('german', '" + unicode(searchStringFlurstueck) + "') \
                    UNION \
                    SELECT \
                        ax_historischesflurstueckohneraumbezug.gemarkungsnummer::integer, \
                        ax_gemarkung.bezeichnung, \
                        ax_historischesflurstueckohneraumbezug.land, \
                        ax_historischesflurstueckohneraumbezug.flurnummer::integer, \
                        ax_historischesflurstueckohneraumbezug.zaehler::integer, \
                        ax_historischesflurstueckohneraumbezug.nenner::integer, \
                        ax_historischesflurstueckohneraumbezug.flurstueckskennzeichen, \
                        'historisch_ungenau' AS typ \
                    FROM ax_historischesflurstueckohneraumbezug \
                    JOIN ax_gemarkung ON ax_historischesflurstueckohneraumbezug.land::text = ax_gemarkung.land::text AND ax_historischesflurstueckohneraumbezug.gemarkungsnummer::text = ax_gemarkung.gemarkungsnummer::text AND ax_gemarkung.endet IS NULL \
                    WHERE to_tsvector('german'::regconfig, \
				        CASE WHEN ax_historischesflurstueckohneraumbezug.gemarkungsnummer IS NULL THEN '0000' ELSE ax_historischesflurstueckohneraumbezug.gemarkungsnummer END || ' ' || \
				        CASE WHEN ax_historischesflurstueckohneraumbezug.flurnummer IS NULL THEN '000' ELSE ax_historischesflurstueckohneraumbezug.flurnummer END || ' ' || \
				        CASE WHEN ax_historischesflurstueckohneraumbezug.zaehler IS NULL THEN '' ELSE ax_historischesflurstueckohneraumbezug.zaehler END || ' ' || \
				        CASE WHEN ax_historischesflurstueckohneraumbezug.nenner IS NULL THEN '' ELSE ax_historischesflurstueckohneraumbezug.nenner END || ' ' || \
        				CASE WHEN ax_historischesflurstueckohneraumbezug.gemarkungsnummer IS NULL THEN '0000' ELSE ax_historischesflurstueckohneraumbezug.gemarkungsnummer END || \
        				CASE WHEN ax_historischesflurstueckohneraumbezug.flurnummer IS NULL THEN '000' ELSE ax_historischesflurstueckohneraumbezug.flurnummer END || \
        				CASE WHEN ax_historischesflurstueckohneraumbezug.zaehler IS NULL THEN '' ELSE ax_historischesflurstueckohneraumbezug.zaehler END || \
        				CASE WHEN ax_historischesflurstueckohneraumbezug.nenner IS NULL THEN '' ELSE ax_historischesflurstueckohneraumbezug.nenner END || ' ' || \
				        CASE WHEN ax_historischesflurstueckohneraumbezug.gemarkungsnummer IS NULL THEN '0000' ELSE lpad(ax_historischesflurstueckohneraumbezug.gemarkungsnummer::text, 4, '0'::text) END || \
				        CASE WHEN ax_historischesflurstueckohneraumbezug.flurnummer IS NULL THEN '000' ELSE lpad(ax_historischesflurstueckohneraumbezug.flurnummer::text, 3, '0'::text) END || \
				        CASE WHEN ax_historischesflurstueckohneraumbezug.zaehler IS NULL THEN '' ELSE lpad(ax_historischesflurstueckohneraumbezug.zaehler::text, 5, '0'::text) END || \
				        CASE WHEN ax_historischesflurstueckohneraumbezug.nenner IS NULL THEN '' ELSE lpad(ax_historischesflurstueckohneraumbezug.nenner::text, 3, '0'::text) END || ' ' || \
        				CASE WHEN ax_historischesflurstueckohneraumbezug.gemarkungsnummer IS NULL THEN '0000' ELSE ax_historischesflurstueckohneraumbezug.gemarkungsnummer END || '-' || \
        				CASE WHEN ax_historischesflurstueckohneraumbezug.flurnummer IS NULL THEN '000' ELSE ax_historischesflurstueckohneraumbezug.flurnummer END || '-' || \
        				CASE WHEN ax_historischesflurstueckohneraumbezug.zaehler IS NULL THEN '' ELSE ax_historischesflurstueckohneraumbezug.zaehler END || '-' || \
        				CASE WHEN ax_historischesflurstueckohneraumbezug.nenner IS NULL THEN '' ELSE '/' || ax_historischesflurstueckohneraumbezug.nenner END || ' ' || \
				        CASE WHEN ax_historischesflurstueckohneraumbezug.gemarkungsnummer IS NULL THEN '0000' ELSE lpad(ax_historischesflurstueckohneraumbezug.gemarkungsnummer::text, 4, '0'::text) END || '-' || \
				        CASE WHEN ax_historischesflurstueckohneraumbezug.flurnummer IS NULL THEN '000' ELSE lpad(ax_historischesflurstueckohneraumbezug.flurnummer::text, 3, '0'::text) END || '-' || \
				        CASE WHEN ax_historischesflurstueckohneraumbezug.zaehler IS NULL THEN '' ELSE lpad(ax_historischesflurstueckohneraumbezug.zaehler::text, 5, '0'::text) END || '-' || \
				        CASE WHEN ax_historischesflurstueckohneraumbezug.nenner IS NULL THEN '' ELSE '/' || lpad(ax_historischesflurstueckohneraumbezug.nenner::text, 3, '0'::text) END || ' ' || \
				        CASE WHEN ax_gemarkung.bezeichnung IS NOT NULL THEN ax_gemarkung.bezeichnung END \
        			) @@ to_tsquery('german', '" + unicode(searchStringFlurstueck) + "') \
        			) as foo ORDER BY gemarkungsnummer,flurnummer,zaehler,nenner"
            query.exec_(sqlFlurstueck)

            if(query.size() > 0):
                item_titleFlurstuecke = QTreeWidgetItem(self.treeWidget)
                item_titleFlurstuecke.setText(0,u"Flurstücke")

                fieldNrFlurst = query.record().indexOf("flurstueckskennzeichen")
                fieldGemarkungsnummer = query.record().indexOf("gemarkungsnummer")
                fieldGemarkungsname = query.record().indexOf("bezeichnung")
                fieldLand = query.record().indexOf("land")
                fieldFlurnummer = query.record().indexOf("flurnummer")
                fieldZaehler = query.record().indexOf("zaehler")
                fieldNenner = query.record().indexOf("nenner")
                fieldTyp = query.record().indexOf("typ")
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
                    flstTyp = query.value(fieldTyp)

                    if(item_titleFlurstuecke.childCount() > 0):
                        for i in range(0, item_titleFlurstuecke.childCount()):
                            if(item_titleFlurstuecke.child(i).text(1) == str(gemarkungsnummer)):
                                item_gemarkung = item_titleFlurstuecke.child(i)
                                break
                        if(item_gemarkung is None):
                            item_gemarkung = QTreeWidgetItem(item_titleFlurstuecke)
                            if(gemarkungsname == NULL):
                                item_gemarkung.setText(0, "Gemarkung " + str(gemarkungsnummer))
                            else:
                                item_gemarkung.setText(0, "Gemarkung " + unicode(gemarkungsname) + " / " + str(gemarkungsnummer))
                            item_gemarkung.setText(1, str(gemarkungsnummer))
                            item_gemarkung.setText(2, "gemarkung")
                            item_gemarkung.setText(3, str(land).zfill(2) + str(gemarkungsnummer).zfill(4))
                    else:
                        item_gemarkung = QTreeWidgetItem(item_titleFlurstuecke)
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
                        if(flurnummer != 0 and flurnummer != NULL):
                            item_flur = QTreeWidgetItem(item_gemarkung)
                            item_flur.setText(0, "Flur " + str(flurnummer))
                            item_flur.setText(1, str(flurnummer))
                            item_flur.setText(2, "flur")
                            item_flur.setText(3, str(land).zfill(2) + str(gemarkungsnummer).zfill(4) + str(flurnummer).zfill(3))

                    if(flurnummer != 0 and flurnummer != NULL):
                        item_flst = QTreeWidgetItem(item_flur)
                    else:
                        item_flst = QTreeWidgetItem(item_gemarkung)
                    if(nenner == NULL):
                        if(flstTyp == "aktuell"):
                            item_flst.setText(0, str(zaehler))
                        elif(flstTyp == "historisch_ungenau"):
                            item_flst.setText(0, str(zaehler) + " (historisch, ungenau)")
                        else:
                            item_flst.setText(0, str(zaehler) + " (historisch)")
                    else:
                        if(flstTyp == "aktuell"):
                            item_flst.setText(0, str(zaehler) + " / " + str(nenner))
                        elif(flstTyp == "historisch_ungenau"):
                            item_flst.setText(0, str(zaehler) + " / " + str(nenner) + " (historisch, ungenau)")
                        else:
                            item_flst.setText(0, str(zaehler) + " / " + str(nenner) + " (historisch)")
                    item_flst.setText(1, flurstuecknummer)
                    item_flst.setText(2, "flurstueck")
                    item_flst.setText(3, flstTyp)

            #------------------------------------------ Adresse suchen
            searchStringAdresse = unicode("")
            if(len(''.join([i for i in searchString if not i.isdigit()])) > 0):
                searchStringAdresse += unicode((''.join([i for i in searchString if not i.isdigit()])).strip()).replace(" ", ":* & ") + ":* "
                if(len(searchStringAdresse) > 0 and len(''.join([i for i in searchString if i.isdigit()])) > 0):
                    searchStringAdresse += " & "
                searchStringAdresse += unicode((''.join([i for i in searchString if i.isdigit()])).strip()).replace(" ", " & ")
                searchStringAdresse += " | " + unicode((''.join([i for i in searchString if not i.isdigit()])).strip()[::-1]).replace(" ", ":* & ") + ":* "
                if(len(''.join([i for i in searchString if i.isdigit()])) > 0):
                    searchStringAdresse = searchStringAdresse + " & " + unicode((''.join([i for i in searchString if i.isdigit()]))).replace(" ", ":* & ")
            if(self.checkPostnasSeachTable() == True):
                sqlAdresse = "SELECT postnas_search.gml_id,ax_lagebezeichnungkatalogeintrag.bezeichnung as name_strasse,ax_lagebezeichnungmithausnummer.hausnummer,ax_gemeinde.bezeichnung as gemeinde \
                    FROM postnas_search \
                    JOIN ax_lagebezeichnungmithausnummer ON postnas_search.gml_id = ax_lagebezeichnungmithausnummer.gml_id \
                    JOIN ax_lagebezeichnungkatalogeintrag ON ax_lagebezeichnungkatalogeintrag.land = ax_lagebezeichnungmithausnummer.land AND ax_lagebezeichnungkatalogeintrag.regierungsbezirk = ax_lagebezeichnungmithausnummer.regierungsbezirk AND ax_lagebezeichnungkatalogeintrag.kreis = ax_lagebezeichnungmithausnummer.kreis AND ax_lagebezeichnungkatalogeintrag.gemeinde = ax_lagebezeichnungmithausnummer.gemeinde AND ax_lagebezeichnungkatalogeintrag.lage = ax_lagebezeichnungmithausnummer.lage \
                    JOIN ax_gemeinde ON ax_lagebezeichnungkatalogeintrag.land = ax_gemeinde.land AND ax_lagebezeichnungkatalogeintrag.regierungsbezirk = ax_gemeinde.regierungsbezirk AND ax_lagebezeichnungkatalogeintrag.kreis = ax_gemeinde.kreis AND ax_lagebezeichnungkatalogeintrag.gemeinde = ax_gemeinde.gemeinde AND ax_gemeinde.endet IS NULL \
                    WHERE vector @@ to_tsquery('german', '"+ searchStringAdresse +"') ORDER BY gemeinde,name_strasse,regexp_replace(ax_lagebezeichnungmithausnummer.hausnummer,'[^0-9]','','g')::int,hausnummer"
            else:
                sqlAdresse = "SELECT ax_lagebezeichnungmithausnummer.gml_id,ax_lagebezeichnungkatalogeintrag.bezeichnung as name_strasse,ax_lagebezeichnungmithausnummer.hausnummer,ax_gemeinde.bezeichnung as gemeinde \
                    FROM ax_lagebezeichnungmithausnummer \
                    JOIN ax_lagebezeichnungkatalogeintrag ON ax_lagebezeichnungkatalogeintrag.land = ax_lagebezeichnungmithausnummer.land AND ax_lagebezeichnungkatalogeintrag.regierungsbezirk = ax_lagebezeichnungmithausnummer.regierungsbezirk AND ax_lagebezeichnungkatalogeintrag.kreis = ax_lagebezeichnungmithausnummer.kreis AND ax_lagebezeichnungkatalogeintrag.gemeinde = ax_lagebezeichnungmithausnummer.gemeinde AND ax_lagebezeichnungkatalogeintrag.lage = ax_lagebezeichnungmithausnummer.lage \
                    JOIN ax_gemeinde ON ax_lagebezeichnungkatalogeintrag.land = ax_gemeinde.land AND ax_lagebezeichnungkatalogeintrag.regierungsbezirk = ax_gemeinde.regierungsbezirk AND ax_lagebezeichnungkatalogeintrag.kreis = ax_gemeinde.kreis AND ax_lagebezeichnungkatalogeintrag.gemeinde = ax_gemeinde.gemeinde AND ax_gemeinde.endet IS NULL \
                    WHERE to_tsvector('german', ax_lagebezeichnungkatalogeintrag.bezeichnung || ' ' || reverse(ax_lagebezeichnungkatalogeintrag.bezeichnung::text) || ' ' || ax_lagebezeichnungmithausnummer.hausnummer) @@ to_tsquery('german', '"+ searchStringAdresse +"') ORDER BY gemeinde,name_strasse,regexp_replace(ax_lagebezeichnungmithausnummer.hausnummer,'[^0-9]','','g')::int,hausnummer"

            query.exec_(sqlAdresse)

            if(query.size() > 0):
                item_titleAdresse = QTreeWidgetItem(self.treeWidget)
                item_titleAdresse.setText(0,u"Adressen")

                fieldGmlId = query.record().indexOf("gml_id")
                fieldStrasseName = query.record().indexOf("name_strasse")
                fieldHausnummer = query.record().indexOf("hausnummer")
                fieldGemeinde = query.record().indexOf("gemeinde")

                while(query.next()):
                    gmlId = query.value(fieldGmlId)
                    strasseName = query.value(fieldStrasseName)
                    hausnummer = query.value(fieldHausnummer)
                    gemeinde = query.value(fieldGemeinde)

                    itemStrasse = None
                    itemHausnummer = None

                    listGemeinden = self.treeWidget.findItems(gemeinde,Qt.MatchExactly | Qt.MatchRecursive,0)
                    if(len(listGemeinden) > 0):
                        itemGemeinde = listGemeinden[0]
                    else:
                        itemGemeinde = QTreeWidgetItem(item_titleAdresse)
                        itemGemeinde.setText(0, unicode(gemeinde))

                    for i in range(0, itemGemeinde.childCount()):
                        if(itemGemeinde.child(i).text(0) == unicode(strasseName)):
                            itemStrasse = itemGemeinde.child(i)
                            break
                    if(itemStrasse is None):
                        itemStrasse = QTreeWidgetItem(itemGemeinde)
                        itemStrasse.setText(0,unicode(strasseName))

                    for i in range(0,itemStrasse.childCount()):
                        if(itemStrasse.child(i).text(0) == unicode(hausnummer)):
                            itemHausnummer = itemStrasse.child(i)
                            break
                    if(itemHausnummer is None):
                        itemHausnummer = QTreeWidgetItem(itemStrasse)
                        itemHausnummer.setText(0,unicode(hausnummer))
                        itemHausnummer.setText(1,unicode(gmlId))
                        itemHausnummer.setText(2,"strasse")

            #------------------------------------------ Eigentümer suchen
            searchStringEigentuemer = searchString.replace(" ", ":* & ") + ":*"
            searchStringEigentuemer += " | " + searchString[::-1].replace(" ", ":* & ") + ":*"
            if(self.checkPostnasSeachTable() == True):
                sqlEigentuemer = "SELECT * FROM (SELECT ax_person.gml_id,nachnameoderfirma,vorname,geburtsname,namensbestandteil,akademischergrad,ax_flurstueck.land,gemarkungsnummer,flurnummer,ax_flurstueck.zaehler,ax_flurstueck.nenner,ax_flurstueck.flurstueckskennzeichen \
                                FROM postnas_search \
                                JOIN ax_person ON ax_person.gml_id = postnas_search.gml_id \
                                JOIN ax_namensnummer ON ax_person.gml_id = ax_namensnummer.benennt AND ax_namensnummer.endet IS NULL \
                                JOIN ax_buchungsblatt ON ax_buchungsblatt.gml_id = ax_namensnummer.istbestandteilvon AND ax_buchungsblatt.endet IS NULL \
                                JOIN ax_buchungsstelle ON ax_buchungsstelle.istbestandteilvon = ax_buchungsblatt.gml_id AND ax_buchungsstelle.endet IS NULL \
                                JOIN ax_flurstueck ON ax_flurstueck.istgebucht = ax_buchungsstelle.gml_id AND ax_flurstueck.endet IS NULL \
                                WHERE vector @@ to_tsquery('german','"+ searchStringAdresse +"') \
                                UNION \
                                SELECT ax_person.gml_id,nachnameoderfirma,vorname,geburtsname,namensbestandteil,akademischergrad,ax_flurstueck.land,gemarkungsnummer,flurnummer,ax_flurstueck.zaehler,ax_flurstueck.nenner,ax_flurstueck.flurstueckskennzeichen \
                                FROM postnas_search \
                                JOIN ax_person ON ax_person.gml_id = postnas_search.gml_id AND ax_person.endet IS NULL \
                                JOIN ax_namensnummer ON ax_person.gml_id = ax_namensnummer.benennt AND ax_namensnummer.endet IS NULL \
                                JOIN ax_buchungsblatt ON ax_buchungsblatt.gml_id = ax_namensnummer.istbestandteilvon AND ax_buchungsblatt.endet IS NULL \
                                JOIN ax_buchungsstelle ON ax_buchungsstelle.istbestandteilvon = ax_buchungsblatt.gml_id AND ax_buchungsstelle.endet IS NULL \
                                JOIN ax_buchungsstelle as ax_buchungsstelle_2 ON ax_buchungsstelle_2.gml_id = ANY(ax_buchungsstelle.an) AND ax_buchungsstelle_2.endet IS NULL \
                                JOIN ax_flurstueck ON ax_flurstueck.istgebucht = ax_buchungsstelle_2.gml_id AND ax_flurstueck.endet IS NULL \
                                WHERE vector @@ to_tsquery('german','"+ searchStringAdresse +"')) as foo \
                                ORDER BY CASE WHEN akademischergrad IS NOT NULL THEN akademischergrad ELSE '' END || CASE WHEN namensbestandteil IS NOT NULL THEN namensbestandteil ELSE '' END || nachnameoderfirma || CASE WHEN vorname IS NOT NULL THEN vorname ELSE '' END || CASE WHEN geburtsname IS NOT NULL THEN geburtsname ELSE '' END, land, gemarkungsnummer,flurnummer,zaehler,nenner"
            else:
                sqlEigentuemer = ""

            query.exec_(sqlEigentuemer)

            if(query.size() > 0):
                item_titleEigentuemer = QTreeWidgetItem(self.treeWidget)
                item_titleEigentuemer.setText(0,u"Eigentümer")

                while(query.next()):
                    gmlId = query.value(query.record().indexOf("gml_id"))
                    nachnameOderFirma = query.value(query.record().indexOf("nachnameoderfirma"))
                    vorname = query.value(query.record().indexOf("vorname"))
                    geburtsname = query.value(query.record().indexOf("geburtsname"))
                    namensbestandteil = query.value(query.record().indexOf("namensbestandteil"))
                    akademischergrad = query.value(query.record().indexOf("akademischergrad"))
                    land = query.value(query.record().indexOf("land"))
                    gemarkungsnummer = query.value(query.record().indexOf("gemarkungsnummer"))
                    flurnummer = query.value(query.record().indexOf("flurnummer"))
                    zaehler = query.value(query.record().indexOf("zaehler"))
                    nenner = query.value(query.record().indexOf("nenner"))
                    flurstueckskennzeichen = query.value(query.record().indexOf("flurstueckskennzeichen"))

                    itemPerson = None
                    itemFlurstueck = None

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

                    listPerson = self.treeWidget.findItems(person,Qt.MatchExactly | Qt.MatchRecursive,0)
                    if(len(listPerson) > 0):
                        itemPerson = listPerson[0]
                    else:
                        itemPerson = QTreeWidgetItem(item_titleEigentuemer)
                        itemPerson.setText(0, unicode(person))
                        itemPerson.setText(1, unicode(gmlId))
                        itemPerson.setText(2, unicode("person"))

                    flurstueck = unicode(land).zfill(2) + unicode(gemarkungsnummer).zfill(4) + '-' + unicode(flurnummer).zfill(3) + '-' + unicode(zaehler).zfill(5)
                    if(nenner != None):
                        flurstueck += "/" + unicode(nenner).zfill(3)

                    for i in range(0, itemPerson.childCount()):
                        if(itemPerson.child(i).text(0) == flurstueck):
                            itemFlurstueck = itemPerson.child(i)
                            break
                    if(itemFlurstueck is None):
                        itemFlurstueck = QTreeWidgetItem(itemPerson)
                        itemFlurstueck.setText(0,unicode(flurstueck))
                        itemFlurstueck.setText(1, flurstueckskennzeichen)
                        itemFlurstueck.setText(2, "flurstueck")
                        itemFlurstueck.setText(3, "aktuell")


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
        if(item.text(2) == "strasse"):
            self.addMapHausnummer("'" + item.text(1) + "'")
        if(item.text(2) == "person"):
            self.addMapPerson("'" + item.text(1) + "'")

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
            if(typ == "aktuell"):
                uri.setDataSource("public", "ax_flurstueck", "wkb_geometry", "flurstueckskennzeichen IN ('" +  searchString + "')")
            elif(typ == "historisch"):
                uri.setDataSource("public", "ax_historischesflurstueck", "wkb_geometry", "flurstueckskennzeichen IN ('" +  searchString + "')")
            elif(typ == "historisch_ungenau"):
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

            if(typ == "historisch" or typ == "historisch_ungenau"):
                myColour = QtGui.QColor('#FDBF6F')
            else:
                myColour = QtGui.QColor('#F08080')
            symbol.setColor(myColour)

            myRenderer = QgsSingleSymbolRendererV2(symbol)
            vlayer.setRendererV2(myRenderer)
            vlayer.setBlendMode(13)
            if(typ == "historisch" or typ == "historisch_ungenau"):
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