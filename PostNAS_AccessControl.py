# -*- coding: utf-8 -*-

import os
import getpass
import json
from qgis.PyQt.QtCore import QSettings
from qgis.PyQt.QtSql import QSqlDatabase, QSqlQuery
from qgis.PyQt.QtWidgets import QMessageBox
from qgis.core import *
import qgis.core

class PostNAS_AccessControl:
    def __init__(self, username = None):
        if(username == None):
            self.username = getpass.getuser().lower()
        else:
            self.username = username.lower()
        self.access = None
        self.name = None
        self.db = self.__loadDB()

    def setUsername(self,username):
        self.username = username
        if(self.checkUserExists()):
            sql = "SELECT name,access FROM public.postnas_search_access_control WHERE lower(username) = :username"
            self.__openDB()
            queryLoadUserData = QSqlQuery(self.db)
            if (self.dbSchema.lower() != "public"):
                sql = sql.replace("public.", self.dbSchema + ".")
            queryLoadUserData.prepare(sql)
            queryLoadUserData.bindValue(":username",self.getUsername())
            queryLoadUserData.exec_()

            if(queryLoadUserData.size() == 1):
                while(queryLoadUserData.next()):
                    self.setName(queryLoadUserData.value(queryLoadUserData.record().indexOf("name")))
                    self.setAccess(queryLoadUserData.value(queryLoadUserData.record().indexOf("access")))

    def setAccess(self,access):
        self.access = access

    def setName(self,name):
        self.name = name

    def getUsername(self):
        return self.username.lower()

    def getAccess(self):
        return self.access

    def getName(self):
        return self.name

    def __checkUsername(self):
        pass

    def checkAccessControlIsActive(self):
        if os.path.isfile(os.path.dirname(os.path.realpath(__file__)) + '\config.json'):
            with open(os.path.dirname(os.path.realpath(__file__)) + '\config.json') as config_file:
                config = json.load(config_file)
            accessControl = config['accessControl']
            pass
        else:
            settings = QSettings("PostNAS", "PostNAS-Suche")
            accessControl = settings.value("accessControl")

        if(accessControl == 1):
            if (self.checkAccessTable() == False):
                accessControl = 0
        else:
            if (self.checkAccessTable() == True):
                accessControl = 1

        if os.path.isfile(os.path.dirname(os.path.realpath(__file__)) + '\config.json'):
            config['accessControl'] = accessControl
            with open(os.path.dirname(os.path.realpath(__file__)) + '\config.json', 'w') as config_file:
                json.dump(config, config_file)
        else:
            settings.setValue("accessControl", accessControl)

        if(accessControl == 1):
            return True
        else:
            return False

    def checkAccessTable(self):
        sql = "SELECT table_name FROM information_schema.tables WHERE table_name = 'postnas_search_access_control'";

        self.__openDB()
        query = QSqlQuery(self.db)
        query.exec_(sql)

        if(query.size() > 0):
            return True
        else:
            return False

    def createAccessTable(self):
        file_path = os.path.dirname(os.path.realpath(__file__)) + "/create_accesstable/create_table.sql"
        sql = open(file_path).read()

        self.__openDB()
        query = QSqlQuery(self.db)
        if (self.dbSchema.lower() != "public"):
            sql = sql.replace("public.", self.dbSchema + ".")
        query.exec_(sql)

        if(query.lastError().number() == -1):
            return True
        else:
            return False

    def checkAccessTableHasAdmin(self):
        sql = "SELECT lower(username) FROM public.postnas_search_access_control WHERE access = 0";
        self.__openDB()
        query = QSqlQuery(self.db)
        if (self.dbSchema.lower() != "public"):
            sql = sql.replace("public.", self.dbSchema + ".")
        query.exec_(sql)
        if(query.size() > 0):
            return True
        else:
            return False

    def insertUser(self):
        if(self.getUsername() != None):
            self.__openDB()
            sql = "INSERT INTO public.postnas_search_access_control (username,name,access) VALUES (:username,:name,:access)"
            query = QSqlQuery(self.db)
            if (self.dbSchema.lower() != "public"):
                sql = sql.replace("public.", self.dbSchema + ".")
            query.prepare(sql)
            query.bindValue(":username",self.getUsername().lower())
            query.bindValue(":name",self.name)
            query.bindValue(":access",self.access)
            query.exec_()
            if(query.lastError().number() == -1):
                return True
            else:
                return False
        else:
            return False

    def insertAdminUser(self):
        self.access = 0
        return self.insertUser()

    def updateUser(self,username_old):
        if(self.getUsername() != None):
            self.__openDB()
            sql = "UPDATE public.postnas_search_access_control SET username = :username, name = :name, access = :access WHERE username = :username_old"
            query = QSqlQuery(self.db)
            if (self.dbSchema.lower() != "public"):
                sql = sql.replace("public.", self.dbSchema + ".")
            query.prepare(sql)
            query.bindValue(":username",self.getUsername().lower())
            query.bindValue(":username_old",username_old)
            query.bindValue(":name",self.name)
            query.bindValue(":access",self.access)
            query.exec_()
            if(query.lastError().number() == -1):
                return True
            else:
                QgsMessageLog.logMessage("Datenbankfehler beim Update: " + query.lastError().text(),'PostNAS-Suche', Qgis.Critical)
                return False
        else:
            return False

    def checkUserIsAdmin(self):
        if(self.getUsername() != None):
            self.__openDB()
            sql = "SELECT lower(username) as username FROM public.postnas_search_access_control WHERE access = 0 AND lower(username) = :username"
            query = QSqlQuery(self.db)
            if (self.dbSchema.lower() != "public"):
                sql = sql.replace("public.", self.dbSchema + ".")
            query.prepare(sql)
            query.bindValue(":username",self.getUsername())
            query.exec_()

            if(query.lastError().number() == -1):
                if(query.size() > 0):
                    return True
                else:
                    return False
            else:
                return False
        else:
            return False

    def checkUserHasEigentuemerAccess(self):
        if(self.getUsername() != None):
            self.__openDB()
            sql = "SELECT lower(username) as username FROM public.postnas_search_access_control WHERE access IN (0,1) AND lower(username) = :username"
            queryEigentuemerAccess = QSqlQuery(self.db)
            if (self.dbSchema.lower() != "public"):
                sql = sql.replace("public.", self.dbSchema + ".")
            queryEigentuemerAccess.prepare(sql)
            queryEigentuemerAccess.bindValue(":username",self.getUsername())
            queryEigentuemerAccess.exec_()
            if(queryEigentuemerAccess.lastError().number() == -1):
                if(queryEigentuemerAccess.size() > 0):
                    return True
                else:
                    return False
            else:
                return False
        else:
            return False


    def loadUserAccessTable(self):
        sql = "SELECT lower(username) as username,name,bezeichnung FROM public.postnas_search_access_control LEFT JOIN public.postnas_search_accessmode ON postnas_search_access_control.access = postnas_search_accessmode.id";
        if (self.dbSchema.lower() != "public"):
            sql = sql.replace("public.", self.dbSchema + ".")
        self.__openDB()
        queryLoadAccessTable = QSqlQuery(self.db)
        queryLoadAccessTable.prepare(sql)
        queryLoadAccessTable.exec_()

        results = []
        if(queryLoadAccessTable.size() > 0):
            while(queryLoadAccessTable.next()):
                list = {'username': queryLoadAccessTable.value(queryLoadAccessTable.record().indexOf("username")),
                        'name': queryLoadAccessTable.value(queryLoadAccessTable.record().indexOf("name")),
                        'access': queryLoadAccessTable.value(queryLoadAccessTable.record().indexOf("bezeichnung"))}
                results.append(list)

        return results

    def deleteUser(self):
        sql = "DELETE FROM public.postnas_search_access_control WHERE lower(username) = :username"
        self.__openDB()
        queryDeleteUser = QSqlQuery(self.db)
        if (self.dbSchema.lower() != "public"):
            sql = sql.replace("public.", self.dbSchema + ".")
        queryDeleteUser.prepare(sql)
        queryDeleteUser.bindValue(":username",self.getUsername())
        queryDeleteUser.exec_()

        if(queryDeleteUser.lastError().number() == -1):
            return True
        else:
            QgsMessageLog.logMessage("Datenbankfehler beim Löschen: " + queryDeleteUser.lastError().text(), 'PostNAS-Suche',Qgis.Critical)
            return False

    def getAccessModes(self):
        sql = "SELECT id,bezeichnung FROM public.postnas_search_accessmode"
        self.__openDB()
        queryLoadAccessModes = QSqlQuery(self.db)
        if (self.dbSchema.lower() != "public"):
            sql = sql.replace("public.", self.dbSchema + ".")
        queryLoadAccessModes.prepare(sql)
        queryLoadAccessModes.exec_()

        results = []
        if(queryLoadAccessModes.size() > 0):
            while(queryLoadAccessModes.next()):
                list = {'id': queryLoadAccessModes.value(queryLoadAccessModes.record().indexOf("id")),
                        'bezeichnung': queryLoadAccessModes.value(queryLoadAccessModes.record().indexOf("bezeichnung"))}
                results.append(list)

        return results


    def checkUserExists(self):
        sql = "SELECT lower(username) as username FROM public.postnas_search_access_control WHERE lower(username) = :username"

        self.__openDB()
        queryCheckUserExists = QSqlQuery(self.db)
        if (self.dbSchema.lower() != "public"):
            sql = sql.replace("public.", self.dbSchema + ".")
        queryCheckUserExists.prepare(sql)
        queryCheckUserExists.bindValue(":username",self.getUsername())
        queryCheckUserExists.exec_()

        if(queryCheckUserExists.lastError().number() == -1):
            if(queryCheckUserExists.size() > 0):
                return True
            else:
                return False
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
        if(dbPort == ""):
            dbPort = "5432"
        db.setPort(int(dbPort)) 
        db.setDatabaseName(dbDatabasename)
        db.setUserName(dbUsername)
        db.setPassword(dbPassword)

        return db

    def __openDB(self):
        if(self.db.isOpen() == False):
            self.db.open()
