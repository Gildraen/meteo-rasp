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
        :return: Threshold
        """
        con = serverConnect()
        result = None
        with con:
            cur = con.cursor()
            sql = """SELECT t.id id, d.id did, d.name dname, d.unit dunit, c.mac_address mac, c.name cname, \
                      t.value tvalue, t.higher higher, t.last_date last_date, t.frequency frequency \
                      FROM threshold t \
                      JOIN caption c ON c.mac_address = t.mac_address \
                      JOIN `data` d ON d.id = t.id_data
                      WHERE t.id = %s"""
            cur.execute(sql, id)
            row = cur.fetchone()
            if row is not None:
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
                result = Threshold(row["id"], data, caption, row["tvalue"], row["higher"],
                                   row["last_date"], row["frequency"], contacts)
            cur.close()
        con.close()
        return result

    @staticmethod
    def update(threshold):
        """
        :param threshold: Threshold
        """
        connection = serverConnect()
        cursor = connection.cursor()
        sql = """UPDATE `threshold` SET `id_data`=%s, `mac_address`=%s, `value`=%s, \
                `higher`=%s, `last_date`=%s, `frequency`=%s \
                WHERE `id` = %s"""
        cursor.execute(sql, (threshold.data.id, threshold.caption.macAddress, threshold.value,
                             threshold.higher, threshold.lastDate, threshold.frequency, threshold.id))
        connection.commit()
        cursor.close()
        cursor = connection.cursor()
        sql = """SELECT address FROM recipient WHERE id_threshold = %s"""
        cursor.execute(sql, threshold.id)
        rows = cursor.fetchall()
        addresses = []
        for row in rows:
            if not threshold.containsContact(row["address"]):
                cursor2 = connection.cursor()
                sql = "DELETE FROM recipient WHERE address = %s AND id_threshold = %s"
                cursor2.execute(sql, (row["address"], threshold.id))
                connection.commit()
                cursor2.close()
            else:
                addresses.append(row["address"])
        cursor.close()
        newContacts = threshold.getExtraEmails(addresses)
        for contact in newContacts:
            cursor2 = connection.cursor()
            sql = "INSERT INTO recipient (address,id_threshold) VALUES (%s, %s)"
            cursor2.execute(sql, (contact.email, threshold.id))
            connection.commit()
            cursor2.close()
        connection.close()

    @staticmethod
    def delete(threshold):
        """
        :param threshold: Threshold
        """
        connection = serverConnect()
        with connection.cursor() as cursor:
            sql = "DELETE FROM `threshold` WHERE `id` = %s"
            cursor.execute(sql, (int(threshold.id)))
        connection.commit()
        cursor.close()
        connection.close()


if __name__ == '__main__':
    """from repo.data_dao import DataDAO
    from repo.caption_dao import CaptionDAO
    from repo.contact_dao import ContactDAO
    from datetime import datetime
    temp = DataDAO.getById(1)
    caption1 = CaptionDAO.getAll()[0]
    contacts = ContactDAO.getAll()
    for i in range(1, 4):
        threshold = Threshold(0, temp, caption1, (10+i), True, datetime.now(), (20+i), contacts)
        ThresholdDAO.create(threshold)
        contacts.remove(contacts[0])"""
    from repo.contact_dao import ContactDAO
    th = ThresholdDAO.getById(1)
    if th is not None:
        print(
            "id:{0} value:{1} higher:{2} last_date:{3} frequency:{4} dataName:{5} captionName:{6} contacts:{7}".format(
                th.id, th.value, th.higher, th.lastDate, th.frequency, th.data.name, th.caption.name, len(th.contacts)
            ))
    else:
        print("none")
    th = ThresholdDAO.create(th)
    if ThresholdDAO.getById(th.id) is None:
        print("???? Error th.id should exist")

    else:
        print("insertion OK : {0}".format(th.id))
        print(
            "id:{0} value:{1} higher:{2} last_date:{3} frequency:{4} dataName:{5} captionName:{6} contacts:{7}".format(
                th.id, th.value, th.higher, th.lastDate, th.frequency, th.data.name, th.caption.name, len(th.contacts)
            ))
        for contact in th.contacts:
            print("      -{0}".format(contact.email))
        print("---------------------------------------------")
    import copy

    thCopie = copy.copy(th)
    th.value = 0
    th.removeContact(ContactDAO.getByEmail("contact2@gmail.com"))
    th.addContact(ContactDAO.getByEmail("email8"))
    ThresholdDAO.update(th)
    th2 = ThresholdDAO.getById(th.id)
    if th2 is None:
        print("???? Error th.id should exist")
    elif th2.value == 0:
        print("update OK : {0}".format(th2.id))
        print("id:{0} value:{1} higher:{2} last_date:{3} frequency:{4} dataName:{5} captionName:{6} contacts:{7}".format(
            th2.id, th2.value, th2.higher, th2.lastDate, th2.frequency, th2.data.name, th2.caption.name, len(th2.contacts)
            ))
        for contact in th2.contacts:
            print("      -{0}".format(contact.email))
        print("---------------------------------------------")
    ThresholdDAO.delete(th)
    if ThresholdDAO.getById(th.id) is not None:
        print("???? Error th.id should not exist:{0}".format(th.id))
    else:
        print("deletion OK : {0}".format(th.id))
