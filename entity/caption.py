#!/usr/bin/python3
# -*-coding:utf-8 -*


class Caption:
    """
    Classe représentant un capteur
    """

    def __init__(self, macAddress, name, active=True):
        """ Constructeur qui initialise les attributs"""
        self.macAddress = macAddress
        self.name = name
        self.active = active
