#!/usr/bin/python3
# -*-coding:utf-8 -*


class Data:
    """
    Classe représentant une donnée pouvant être collectée
    """

    def __init__(self, id, name, unit):
        """ Constructeur qui initialise les attributs"""
        self.id = id
        self.name = name
        self.unit = unit
