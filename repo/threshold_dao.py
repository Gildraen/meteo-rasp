#!/usr/bin/python3
# -*-coding:utf-8 -*

from entity.threshold import Threshold
from entity.contact import Contact
from entity.data import Data
from entity.caption import Caption
from repo.db_connection import serverConnect


class ThresholdDAO:
    @staticmethod
    def create(threshold):
        """
        :param threshold: Threshold
        :return: Threshold
        error : 'pymysql.err.IntegrityError: (1062, "Duplicata du champ 'xxx' pour la clef 'PRIMARY'")
        id, data, caption, value, higher, lastDate, frequency, contacts
        """
        connection = serverConnect()
        with connection.cursor() as cursor:
            sql = """INSERT INTO `threshold` (`id_data`, `mac_address`, `value`, `higher`, `last_date`, `frequency`) \
                        VALUES (%s, %s, %s, %s, %s, %s)"""
            cursor.execute(sql, (threshold.data.id, threshold.caption.macAddress, threshold.value, threshold.higher,
                                 threshold.lastDate, threshold.frequency))
            threshold.id = int(connection.insert_id())
        connection.commit()
        cursor.close()
        # type Contact
        for contact in threshold.contacts:
            with connection.cursor() as cursor:
                sql = "INSERT INTO `recipient` (`address`, `id_threshold`) VALUES (%s, %s)"
                cursor.execute(sql, (contact.email, threshold.id))
                connection.commit()
                cursor.close()
        connection.close()
        return threshold

    @staticmethod
    def getAll():
        """
        :return: Array of Threshold
        """
        result = []
        con = serverConnect()
        with con:
            cur = con.cursor()
            sql = """SELECT t.id id, d.id did, d.name dname, d.unit dunit, c.mac_address mac, c.name cname, \
                      t.value tvalue, t.higher higher, t.last_date last_date, t.frequency frequency \
                      FROM threshold t \
                      JOIN caption c ON c.mac_address = t.mac_address \
                      JOIN `data` d ON d.id = t.id_data"""
            cur.execute(sql)
            rows = cur.fetchall()
            for row in rows:
                cur2 = con.cursor()
                sql2 = """SELECT c.address address, c.firstname firstname, c.lastname lastname \
                          FROM recipient r JOIN contact c on r.address = c.address \
                          WHERE r.id_threshold = %s"""
                cur2.execute(sql2, (row["id"]))
                rows2 = cur2.fetchall()
                contacts = []
                for row2 in rows2:
                    contacts.append(Contact(row2["address"], row2["firstname"], row2["lastname"]))
                data = Data(row["did"], row["dname"], row["dunit"])
                caption = Caption(row["mac"], row["cname"])
                threshold = Threshold(row["id"], data, caption, row["tvalue"], row["higher"],
                                      row["last_date"], row["frequency"], contacts)
                result.append(threshold)
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
    from repo.data_dao import DataDAO
    from repo.caption_dao import CaptionDAO
    from repo.contact_dao import ContactDAO
    from datetime import datetime
    temp = DataDAO.getById(1)
    caption1 = CaptionDAO.getAll()[0]
    contacts = ContactDAO.getAll()
    for i in range(1, 4):
        threshold = Threshold(0, temp, caption1, (10+i), True, datetime.now(), (20+i), contacts)
        ThresholdDAO.create(threshold)
        contacts.remove(contacts[0])




