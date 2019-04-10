#!/usr/bin/python3
# -*-coding:utf-8 -*

from entity.data import Data
from entity.caption import Caption
from entity.collect import Collect
from repo.caption_dao import CaptionDAO
from repo.data_dao import DataDAO
from repo.db_connection import serverConnect


class CollectDAO:
    @staticmethod
    def create(collect):
        """
        :param collect: Collect
        error : 'pymysql.err.IntegrityError: (1062, "Duplicata du champ 'xxx' pour la clef 'PRIMARY'")
        """
        connection = serverConnect()
        with connection.cursor() as cursor:
            sql = "INSERT INTO `collect` (`id_data`, `mac_address`, `date` , `value`) VALUES (%s, %s, %s, %s)"
            cursor.execute(sql, (collect.data.id, collect.caption.macAddress, collect.date,collect.value))
            collect.id = int(connection.insert_id())
        connection.commit()
        cursor.close()
        connection.close()

    @staticmethod
    def getAll(**kwargs):
        """
        option keywords can be 'macAddress' or 'dataId'
        :return: Array of Collect
        """
        result = []
        con = serverConnect()
        with con:
            cur = con.cursor()
            sql = """SELECT c.id id, c.id_data id_data , d.name dname, d.unit unit, c.mac_address mac, ca.name caname, \
                    c.date cdate, c.value cvalue FROM collect c \
                    JOIN data d ON d.id = c.id_data \
                    JOIN `caption` ca ON ca.mac_address = c.mac_address"""
            whereArgs = []
            whereValues = ()
            if 'macAddress' in kwargs or 'dataId' in kwargs:
                sql = sql + " WHERE "
            if ('macAddress' in kwargs):
                whereArgs.append("ca.mac_address = %s")
                whereValues = whereValues + (kwargs['macAddress'],)
            if ('dataId' in kwargs):
                whereArgs.append("c.id_data = %s")
                whereValues = whereValues + (kwargs['dataId'],)
            sql = sql + " and ".join(whereArgs)
            cur.execute(sql,whereValues)
            rows = cur.fetchall()
            for row in rows:
                data = Data(row["id_data"], row["dname"], row["unit"])
                caption = Caption(row["mac"], row["caname"])
                result.append(Collect(row["id"], data, caption, row["cdate"], row["cvalue"]))
            cur.close()
        con.close()
        return result

    @staticmethod
    def update(collect):
        """
        :param collect: Collect
        """
        connection = serverConnect()
        with connection.cursor() as cursor:
            sql = "UPDATE `collect` SET `id_data` =%s, `mac_address` =%s, `date` =%s, `value` =%s WHERE `id` = %s"
            cursor.execute(sql, (collect.data.id, collect.caption.macAddress, collect.date, collect.value, collect.id))
        connection.commit()
        cursor.close()
        connection.close()

    @staticmethod
    def delete(contact):
        """
        :param contact: Contact
        """
        connection = serverConnect()
        with connection.cursor() as cursor:
            sql = "DELETE FROM `contact` WHERE `address` = %s"
            cursor.execute(sql, (contact.email))
        connection.commit()
        cursor.close()
        connection.close()

if __name__ == '__main__':
    import datetime
    """jardin = CaptionDAO.getByMacAddress('f3:43:ad:d9:8F:5f')
    interne = CaptionDAO.getByMacAddress('d6:c6:c7:39:a2:e8')
    externe = CaptionDAO.getByMacAddress('d7:ef:13:27:15:29')
    temperature  = DataDAO.getById(1)
    humidite  = DataDAO.getById(2)
    now = datetime.datetime.now()
    date1 = now - datetime.timedelta(days=1)
    date2 = now - datetime.timedelta(days=2)
    date3 = now - datetime.timedelta(days=3)
    date4 = now - datetime.timedelta(days=4)
    date5 = now - datetime.timedelta(days=5)
    c1 = Collect(0,humidite,interne, now,30)
    c2 = Collect(0,humidite,interne, date1,29)
    c3 = Collect(0,humidite,interne, date2,28)
    c4 = Collect(0,humidite,interne, date3,27)
    c5 = Collect(0,humidite,interne, date4,26)
    c6 = Collect(0,humidite,interne, date5,25)
    CollectDAO.create(c1)
    CollectDAO.create(c2)
    CollectDAO.create(c3)
    CollectDAO.create(c4)
    CollectDAO.create(c5)
    CollectDAO.create(c6)"""


    for collect in CollectDAO.getAll():
        print("Capteur:{0} Données:{1} Valeur:{2} Date{3}".format(collect.caption.name ,
                                                                  collect.data.name, collect.value, collect.date))
    print("-----------------------------------------")
    for collect in CollectDAO.getAll(macAddress="d7:ef:13:27:15:29"):
        print("Capteur:{0} Données:{1} Valeur:{2} Date{3}".format(collect.caption.name ,
                                                                  collect.data.name, collect.value, collect.date))
    print("-----------------------------------------")
    for collect in CollectDAO.getAll(dataId="1"):
        print("Capteur:{0} Données:{1} Valeur:{2} Date{3}".format(collect.caption.name ,
                                                                  collect.data.name, collect.value, collect.date))
    print("-----------------------------------------")
    for collect in CollectDAO.getAll(dataId="1",macAddress="d7:ef:13:27:15:29"):
        print("Capteur:{0} Données:{1} Valeur:{2} Date{3}".format(collect.caption.name ,
                                                                  collect.data.name, collect.value, collect.date))
    """for collect in CollectDAO.getAll(dataId="1"):
        print("Capteur:{0} Données:{1} Valeur:{2} Date{3}".format(collect.caption.name ,
                                                                  collect.data.name, collect.value, collect.date))
    """

    """aContact = Contact("contact1@gmail.com", "Prénom1", "Nom1")
    aContact2 = Contact("contact2@gmail.com", "Prénom2", "Nom2")
    ContactDAO.create(aContact)
    ContactDAO.create(aContact2)
    for contact in ContactDAO.getAll():
        print("mail:{0} Prénom:{1} Nom:{2}".format(contact.email, contact.firstname, contact.lastname))
    print("-----------------------------------------")
    aContact = ContactDAO.getByEmail(aContact2.email)
    aContact.firstname = "new firstname2"
    ContactDAO.update(aContact)
    for contact in ContactDAO.getAll():
        print("mail:{0} Prénom:{1} Nom:{2}".format(contact.email, contact.firstname, contact.lastname))
    ContactDAO.delete(aContact)
    print("-----------------------------------------")
    for contact in ContactDAO.getAll():
        print("mail:{0} Prénom:{1} Nom:{2}".format(contact.email, contact.firstname, contact.lastname))"""
