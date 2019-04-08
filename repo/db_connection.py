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


if __name__ == '__main__':
    import pymysql.cursors
    connection = serverConnect()
    try:
        with connection.cursor() as cursor:
            # Create a new record
            sql = "INSERT INTO `caption` (`mac_address`, `name`) VALUES (%s, %s)"
            cursor.execute(sql, ('mac1', 'nom1'))

        # connection is not autocommit by default. So you must commit to save
        # your changes.
        connection.commit()
        cursor.close()

        with connection.cursor() as cursor:
            # Create a new record
            sql = "INSERT INTO `caption` (`mac_address`, `name`) VALUES (%s, %s)"
            cursor.execute(sql, ('mac2', 'nom2'))
        # connection is not autocommit by default. So you must commit to save
        # your changes.
        connection.commit()
        cursor.close()

        with connection.cursor() as cursor:
            # Read a single record
            sql = "SELECT `mac_address`, `name` FROM `caption`"
            cursor.execute(sql)
            result = cursor.fetchall()
            for r in result:
                print(r)

    finally:
        connection.close()
