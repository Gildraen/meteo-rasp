#!/usr/bin/python3
# -*-coding:utf-8 -*

import sys
sys.path.append('/home/projects/meteo-rasp/entity')
from caption import Caption
from db_connection import serverConnect


class CaptionDAO:
    """
    """
    @staticmethod
    def create(caption):
        """
        :param caption: Caption
        error : 'pymysql.err.IntegrityError: (1062, "Duplicata du champ 'mac1' pour la clef 'PRIMARY'")
        """
        connection = serverConnect()
        with connection.cursor() as cursor:
            sql = "INSERT INTO `caption` (`mac_address`, `name`) VALUES (%s, %s)"
            cursor.execute(sql, (caption.macAddress, caption.name))
        connection.commit()
        cursor.close()
        connection.close()

    @staticmethod
    def getAll():
        """
        :return: Array of Caption
        """
        result = []
        con = serverConnect()
        with con:
            cur = con.cursor()
            cur.execute("SELECT `mac_address`, `name` FROM `caption`")
            rows = cur.fetchall()
            for row in rows:
                result.append(Caption(row["mac_address"], row["name"]))
            cur.close()
        con.close()
        return result

    @staticmethod
    def getByMacAddress(macAddress):
        """
        :param macAddress: String
        :return: Caption
        """
        con = serverConnect()
        result = None
        with con:
            cur = con.cursor()
            cur.execute("SELECT `mac_address`, `name` FROM `caption` WHERE `mac_address` = %s",macAddress)
            row = cur.fetchone()
            if row is not None:
                result = Caption(row["mac_address"], row["name"])
            cur.close()
        con.close()
        return result

    @staticmethod
    def update(caption):
        """
        :param caption: Caption
        """
        connection = serverConnect()
        with connection.cursor() as cursor:
            sql = "UPDATE `caption` SET `name` =%s WHERE `mac_address` = %s"
            cursor.execute(sql, (caption.name, caption.macAddress))
        connection.commit()
        cursor.close()
        connection.close()

    @staticmethod
    def delete(caption):
        """
        :param caption: Caption
        """
        connection = serverConnect()
        with connection.cursor() as cursor:
            sql = "DELETE FROM `caption` WHERE `mac_address` = %s"
            cursor.execute(sql, (caption.macAddress))
        connection.commit()
        cursor.close()
        connection.close()

if __name__ == '__main__':
    aCaption = None
    for caption in CaptionDAO.getAll():
        print("Adresse Mac:{0} Nom:{1}".format(caption.macAddress, caption.name))
        aCaption = caption
    print("-----------------------------------------")
    aCaption.name = "new Name2"
    aCaption = CaptionDAO.getByMacAddress("mac2")
    """CaptionDAO.update(aCaption)
    for caption in CaptionDAO.getAll():
        print("Adresse Mac:{0} Nom:{1}".format(caption.macAddress, caption.name))
    CaptionDAO.delete(aCaption)
    for caption in CaptionDAO.getAll():
        print("Adresse Mac:{0} Nom:{1}".format(caption.macAddress, caption.name))"""
