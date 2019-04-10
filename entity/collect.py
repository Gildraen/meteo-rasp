#!/usr/bin/python3
# -*-coding:utf-8 -*


class Collect:
    """
    Classe représentant la collecte d'une donnée par un capteur
    """

    def __init__(self, id, data, caption, date, value):
        """ Constructeur qui initialise les attributs"""
        self.id = id
        self.data = data
        self.caption = caption
        self.date = date
        self.value = value
