#!/usr/bin/python3
# -*-coding:utf-8 -*


class Contact:
    """
    Classe représentant une donnée pouvant être collectée
    """

    def __init__(self, email, firstname, lastname):
        """ Constructeur qui initialise les attributs"""
        self.email = email
        self.firstname = firstname
        self.lastname = lastname
