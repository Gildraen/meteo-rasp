#!/usr/bin/python3
# -*-coding:utf-8 -*

import pymysql
import configparser

def serverConnect():
    """
    Retourne une connexion au SGBD
    erreur possible :
       - OperationalError err.args[0]==1044 : "Accès refusé! Vous ne disposez pas des droits nécessaires d'accès à la base"
       - InternalError err.args[0]==1049 : "La base de données n'éxiste pas"
    """
    config = configparser.ConfigParser()
    config.read("db.conf")

    host = config['options']['host']
    port = int(config['options']['port'])
    user = config['options']['user']
    pwd = config['options']['pwd']
    dbName = config['options']['database']

    return pymysql.connect(host=host, port=port, user=user, password=pwd,  db=dbName,
                               charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
