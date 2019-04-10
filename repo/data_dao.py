#!/usr/bin/python3
# -*-coding:utf-8 -*


import sys
sys.path.append('/home/projects/meteo-rasp/entity')
from data import Data
from db_connection import serverConnect


class DataDAO:
    @staticmethod
    def create(data):
        """
        :param data: Data
        :return: Data
        error : 'pymysql.err.IntegrityError: (1062, "Duplicata du champ 'xxx' pour la clef 'PRIMARY'")
        """
        connection = serverConnect()
        with connection.cursor() as cursor:
            sql = "INSERT INTO `data` (`name`, `unit`) VALUES (%s, %s)"
            cursor.execute(sql, (data.name, data.unit))
            data.id = int(connection.insert_id())
        connection.commit()
        cursor.close()
        connection.close()
        return data

    @staticmethod
    def getAll():
        """
        :return: Array of Data
        """
        result = []
        con = serverConnect()
        with con:
            cur = con.cursor()
            cur.execute("SELECT `id`, `name`, `unit` FROM `data`")
            rows = cur.fetchall()
            for row in rows:
                result.append(Data(row["id"], row["name"], row["unit"]))
            cur.close()
        con.close()
        return result

    @staticmethod
    def getById(id):
        """
        :param id: Integer
        :return: Data
        """
        con = serverConnect()
        result = None
        with con:
            cur = con.cursor()
            cur.execute("SELECT `id`, `name`, `unit` FROM `data` WHERE `id` = %s", int(id))
            row = cur.fetchone()
            if row is not None:
                result = Data(row["id"], row["name"], row["unit"])
            cur.close()
        con.close()
        return result

    @staticmethod
    def update(data):
        """
        :param data: Data
        """
        connection = serverConnect()
        with connection.cursor() as cursor:
            sql = "UPDATE `data` SET `name` =%s, `unit` = %s  WHERE `id` = %s"
            cursor.execute(sql, (data.name, data.unit, int(data.id)))
        connection.commit()
        cursor.close()
        connection.close()

    @staticmethod
    def delete(data):
        """
        :param data: Data
        """
        connection = serverConnect()
        with connection.cursor() as cursor:
            sql = "DELETE FROM `data` WHERE `id` = %s"
            cursor.execute(sql, (int(data.id)))
        connection.commit()
        cursor.close()
        connection.close()

if __name__ == '__main__':
    aData = Data(0, "data1", "%1")
    aData2 = Data(0, "data2", "%2")
    DataDAO.create(aData)
    DataDAO.create(aData2)
    for data in DataDAO.getAll():
        print("Id:{0} Nom:{1} Unité:{2}".format(data.id, data.name, data.unit))
    aData = DataDAO.getById(aData2.id)
    aData.name = "new Name2"
    print("-----------------------------------------")
    DataDAO.update(aData)
    for data in DataDAO.getAll():
        print("Id:{0} Nom:{1} Unité:{2}".format(data.id, data.name, data.unit))
    DataDAO.delete(aData)
    print("-----------------------------------------")
    for data in DataDAO.getAll():
        print("Id:{0} Nom:{1} Unité:{2}".format(data.id, data.name, data.unit))
