# -*- coding: utf-8 -*-

import os, getpass, datetime
from qgis.PyQt.QtCore import QSettings
from qgis.PyQt.QtSql import QSqlDatabase, QSqlQuery
from .PostNAS_AccessControl import PostNAS_AccessControl
from qgis.core import *
import qgis.core
import json

class PostNAS_Logging:
    def __init__(self):
        self.db = self.__loadDB()
        self.accessControl = PostNAS_AccessControl()
        self.username = getpass.getuser()

    def logEigentuemerList(self,search,result):
        if(self.__checkLoggingActive() == True) :
            if(self.__checkLoggingTableExists() == False):
                self.__createLoggingTable()
            self.__insertLogEntry("eigentuemerList",search,result)

    def logEigentuemerFlurstueck(self,search,result):
        if(self.__checkLoggingActive() == True) :
            if(self.__checkLoggingTableExists() == False):
                self.__createLoggingTable()
            self.__insertLogEntry("flurstueckList",search,result)

    def __insertLogEntry(self,requestType,search,result):
        self.__openDB()
        sql = "INSERT INTO public.postnas_search_logging (datum,username,requestType,search,result) VALUES (:datum,:username,:requestType,:search,:result)"

        query = QSqlQuery(self.db)
        if (self.dbSchema.lower() != "public"):
            sql = sql.replace("public.", self.dbSchema + ".")
        query.prepare(sql)
        query.bindValue(":datum",datetime.datetime.now().isoformat())
        query.bindValue(":username",self.username)
        query.bindValue(":requestType",requestType)
        query.bindValue(":search",search)
        query.bindValue(":result",str(result).replace("u'","'").replace("\'","\"").replace("[","{").replace("]","}"))
        query.exec_()

        if(query.lastError().number() == -1):
            return True
        else:
            return False

    def __checkLoggingActive(self):
        return True

    def __checkLoggingTableExists(self):
        sql = "SELECT table_name FROM information_schema.tables WHERE table_name = 'postnas_search_logging'";
        self.__openDB()
        query = QSqlQuery(self.db)
        query.exec_(sql)

        if(query.size() > 0):
            return True
        else:
            return False

    def __createLoggingTable(self):
        file_path = os.path.dirname(os.path.realpath(__file__)) + "/create_loggingtable/create_logging_table.sql"
        sql = open(file_path).read()

        if (self.dbSchema.lower() != "public"):
            sql = sql.replace("public.", self.dbSchema + ".")

        self.__openDB()
        query = QSqlQuery(self.db)
        query.exec_(sql)

        if(query.lastError().number() == -1):
            return True
        else:
            return False

    def __loadDB(self):
        if os.path.isfile(os.path.dirname(os.path.realpath(__file__)) + '\config.json'):
            with open(os.path.dirname(os.path.realpath(__file__)) + '\config.json') as config_file:
                config = json.load(config_file)
            dbHost = config['db']['host']
            dbDatabasename = config['db']['database']
            self.dbSchema = config['db']['schema']
            dbPort = config['db']['port']
            dbUsername = config['db']['user']
            dbPassword = config['db']['password']

            authcfg = config['authcfg']
        else:
            settings = QSettings("PostNAS", "PostNAS-Suche")

            dbHost = settings.value("host", "")
            dbDatabasename = settings.value("dbname", "")
            self.dbSchema = settings.value("schema", "public")
            dbPort = settings.value("port", "5432")
            dbUsername = settings.value("user", "")
            dbPassword = settings.value("password", "")

            authcfg = settings.value( "authcfg", "" )

        if authcfg != "" and hasattr(qgis.core,'QgsAuthManager'):
            amc = qgis.core.QgsAuthMethodConfig()
            if hasattr(qgis.core, "QGis"):
                qgis.core.QgsAuthManager.instance().loadAuthenticationConfig( authcfg, amc, True) 
            else:
                QgsApplication.instance().authManager().loadAuthenticationConfig( authcfg, amc, True)
            dbUsername = amc.config( "username", dbUsername )
            dbPassword = amc.config( "password", dbPassword )

        db = QSqlDatabase.addDatabase("QPSQL")
        db.setHostName(dbHost)
        db.setPort(int(dbPort))
        db.setDatabaseName(dbDatabasename)
        db.setUserName(dbUsername)
        db.setPassword(dbPassword)

        return db

    def __openDB(self):
        if(self.db.isOpen() == False):
            self.db.open()
