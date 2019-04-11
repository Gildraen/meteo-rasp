#!/usr/bin/python3
# -*-coding:utf-8 -*


class Threshold:
    """
    Classe représentant un seuil d'une donnée pour un capteur
    """

    def __init__(self, id, data, caption, value, higher, lastDate, frequency, contacts):
        """ Constructeur qui initialise les attributs"""
        self.id = id
        # type Data
        self.data = data
        # type Caption
        self.caption = caption
        # type float
        self.value = value
        # type boolean
        self.higher = higher
        # type datetime
        self.lastDate = lastDate
        # type integer
        self.frequency = frequency
        # type array of Contact
        self.contacts = contacts

    def containsContact(self, emailContact):
        """
        :param emailContact: String
        :return: Boolean
        """
        # type Contact
        for contact in self.contacts:
            if contact.email == emailContact:
                return True
        return False

    def getExtraEmails(self, emailList):
        """
        :param emailList: Array of String
        :return: Array of Contact
        """
        result = []
        for contact in self.contacts:
            if contact.email not in emailList:
                result.append(contact)
        return result

    def addContact(self, contact):
        """
        :param contact: Contact
        :return:
        """
        if contact is not None and not self.containsContact(contact.email):
            self.contacts.append(contact)

    def removeContact(self, contact):
        """
        :param contact: Contact
        :return:
        """
        i = 0
        index = 0
        found = False
        # type Contact
        for aContact in self.contacts:
            if contact is not None and aContact.email == contact.email:
                found = True
                index = i
            i = i + 1
        if found:
            del self.contacts[index]

if __name__ == '__main__':
    from entity.data import Data
    from entity.caption import Caption
    from entity.contact import Contact
    from datetime import datetime
    data = Data(1,"temp","%")
    caption = Caption("mac","aname")
    th = Threshold(1, data, caption, 10, True, datetime.now(), 10, [])
    for i in range(1, 5):
        th.addContact(Contact("email{0}".format(i), "fi", "las"))
    th.addContact(None)
    th.removeContact(None)
    for contact in th.contacts:
        print(contact.email)
    print("--------------------")
    th.removeContact(Contact("email3", "fi", "las"))
    for contact in th.contacts:
        print(contact.email)
    print("--------------------")
    th.removeContact(Contact("email8", "fi", "las"))
    for contact in th.contacts:
        print(contact.email)
    print("--------------------")

