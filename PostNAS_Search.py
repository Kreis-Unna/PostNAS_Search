# -*- coding: utf-8 -*-

from qgis.PyQt.QtCore import *
from qgis.PyQt.QtGui import *
from qgis.PyQt.QtWidgets import QAction, QDockWidget
# Initialize Qt resources from file resources.py
from . import resources_rc
# Import the code for the dialog
from .PostNAS_SearchDialog import PostNAS_SearchDialog
from .PostNAS_ConfDialog import PostNAS_ConfDialog
from .PostNAS_CreateFulltextindex import PostNAS_CreateFulltextindex
import os.path

class PostNAS_Search:

    def __init__(self, iface):
        # Save reference to the QGIS interface
        self.iface = iface
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(self.plugin_dir,'i18n','PostNAS_Search_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)

        # Create the dialog (after translation) and keep reference
        self.dlg = PostNAS_SearchDialog(iface=self.iface)
        self.conf = PostNAS_ConfDialog(iface=self.iface)

        # Declare instance attributes
        self.actions = []
        self.menu = self.tr(u'&PostNAS_Search')

        self.searchDockWidget = None
        self.searchDockWidgetArea = Qt.LeftDockWidgetArea

    # noinspection PyMethodMayBeStatic
    def tr(self, message):
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate('PostNAS_Search', message)

    def initGui(self):
        # Create Conf-Action and Menuentry
        self.confAction = QAction("Einstellungen", self.iface.mainWindow())
        self.confAction.setWhatsThis("Konfiguration der PostNAS-Suche")
        self.confAction.setStatusTip("Konfiguration der PostNAS-Suche")
        self.confAction.triggered.connect(self.showConf)

        if hasattr(self.iface, "addPluginToDatabaseMenu"):
            self.iface.addPluginToDatabaseMenu("&PostNAS-Suche", self.confAction)
        else:
            self.iface.addPluginToMenu("&PostNAS-Suche", self.confAction)

        self.toggleSearchAction = QAction(u"Flurstücksuche", self.iface.mainWindow())
        self.toggleSearchAction.setWhatsThis(u"Starten/Schliessen der Flurstücksuche")
        self.toggleSearchAction.setStatusTip(u"Starten/Schliessen der Flurstücksuche")
        self.toggleSearchAction.triggered.connect(self.toggleWidget)

        if hasattr(self.iface, "addPluginToDatabaseMenu"):
            self.iface.addPluginToDatabaseMenu("&PostNAS-Suche", self.toggleSearchAction)
        else:
            self.iface.addPluginToMenu("&PostNAS-Suche", self.toggleSearchAction)

        self.fulltextindex = QAction(u"Volltextindex erstellen", self.iface.mainWindow())
        self.fulltextindex.setWhatsThis(u"Erzeugt einen Volltextindex in der Datenbank um die Suche zu beschleunigen")
        self.fulltextindex.setStatusTip(u"Erzeugt einen Volltextindex in der Datenbank um die Suche zu beschleunigen")
        self.fulltextindex.triggered.connect(self.createFulltextindex)

        if hasattr(self.iface, "addPluginToDatabaseMenu"):
            self.iface.addPluginToDatabaseMenu("&PostNAS-Suche", self.fulltextindex)
        else:
            self.iface.addPluginToMenu("&PostNAS-Suche", self.fulltextindex)

        # Create action that will start plugin configuration
        self.action = QAction(QIcon(":/plugins/PostNAS_Search/search_24x24.png"),u"Flurstücksuche", self.iface.mainWindow())
        self.action.setCheckable(True)
        # connect the action to the run method
        self.action.triggered.connect(self.toggleWidget)

        # Add toolbar button and menu item
        self.iface.addToolBarIcon(self.action)

    def toggleWidget(self, event):
        if self.searchDockWidget == None:
            self.searchDockWidget = QDockWidget(self.iface.mainWindow())
            self.searchDockWidget.setWindowTitle(self.tr(u'Suche'))
            self.searchDockWidget.setWidget(self.dlg)
            self.searchDockWidget.closeEvent = self.toggleWidget
            self.iface.addDockWidget(self.searchDockWidgetArea, self.searchDockWidget)
            self.action.setChecked(True)
        else:
            self.searchDockWidgetArea = self.iface.mainWindow().dockWidgetArea(self.searchDockWidget)
            self.iface.removeDockWidget(self.searchDockWidget)
            self.searchDockWidget = None
            self.action.setChecked(False)

    def showConf(self):
        dlg = PostNAS_ConfDialog(self)
        dlg.exec_()

    def createFulltextindex(self):
        dlg = PostNAS_CreateFulltextindex(self)
        dlg.exec_()

    def unload(self):
        # Remove the Toolbar Icon
        self.iface.removeToolBarIcon(self.action)
        # Remove DockWidget
        if self.searchDockWidget != None:
            self.iface.removeDockWidget(self.searchDockWidget)

        if hasattr(self.iface, "removePluginDatabaseMenu"):
            self.iface.removePluginDatabaseMenu("&PostNAS-Suche", self.confAction)
            self.iface.removePluginDatabaseMenu("&PostNAS-Suche", self.toggleSearchAction)
            self.iface.removePluginDatabaseMenu("&PostNAS-Suche", self.fulltextindex)
        else:
            self.iface.removePluginMenu("&PostNAS-Suche", self.confAction)
            self.iface.removePluginMenu("&PostNAS-Suche", self.toggleSearchAction)
            self.iface.removePluginMenu("&PostNAS-Suche", self.fulltextindex)

        if self.confAction:
            self.confAction.deleteLater()
            self.confAction = None

        if self.toggleSearchAction:
            self.toggleSearchAction.deleteLater()
            self.toggleSearchAction = None

        if self.fulltextindex:
            self.fulltextindex.deleteLater()
            self.fulltextindex = None
