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
