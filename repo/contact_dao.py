#!/usr/bin/python3
# -*-coding:utf-8 -*

from entity.contact import Contact
from repo.db_connection import serverConnect


class ContactDAO:
    """
    """
    @staticmethod
    def create(contact):
        """
        :param contact: Contact
        error : 'pymysql.err.IntegrityError: (1062, "Duplicata du champ 'contact1@gmail.com' pour la clef 'PRIMARY'")
        """
        connection = serverConnect()
        with connection.cursor() as cursor:
            sql = "INSERT INTO `contact` (`address`, `firstname`, `lastname`) VALUES (%s, %s, %s)"
            cursor.execute(sql, (contact.email, contact.firstname, contact.lastname))
        connection.commit()
        cursor.close()
        connection.close()

    @staticmethod
    def getAll():
        """
        :return: Array of Contact
        """
        result = []
        con = serverConnect()
        with con:
            cur = con.cursor()
            cur.execute("SELECT `address`, `firstname`, `lastname` FROM `contact`")
            rows = cur.fetchall()
            for row in rows:
                result.append(Contact(row["address"], row["firstname"], row["lastname"]))
            cur.close()
        con.close()
        return result

    @staticmethod
    def getByEmail(email):
        """
        :param email: String
        :return: Contact
        """
        con = serverConnect()
        result = None
        with con:
            cur = con.cursor()
            cur.execute("SELECT `address`, `firstname`, `lastname` FROM `contact` WHERE `address` = %s", email)
            row = cur.fetchone()
            if row is not None:
                result = Contact(row["address"], row["firstname"], row["lastname"])
            cur.close()
        con.close()
        return result

    @staticmethod
    def update(contact):
        """
        :param contact: Contact
        """
        connection = serverConnect()
        with connection.cursor() as cursor:
            sql = "UPDATE `contact` SET `firstname` =%s, `lastname` =%s WHERE `address` = %s"
            cursor.execute(sql, (contact.firstname, contact.lastname, contact.email))
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
    aContact = Contact("contact1@gmail.com", "Prénom1", "Nom1")
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
        print("mail:{0} Prénom:{1} Nom:{2}".format(contact.email, contact.firstname, contact.lastname))
