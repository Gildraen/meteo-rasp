#! /usr/bin/python
# -*- coding:utf-8 -*-

from flask import Flask, render_template
from repo.caption_dao import CaptionDAO
from repo.collect_dao import CollectDAO
from entity.data import Data
app = Flask(__name__)

@app.route('/')
def accueil():

	capteurs = CaptionDAO.getAll()
	data = {}

	for capteur in capteurs:
		collectsHum = CollectDAO.getAll(macAddress=capteur.macAddress, dataId=Data.HUMIDITY)
		collectsTemp = CollectDAO.getAll(macAddress=capteur.macAddress, dataId=Data.TEMPERATURE)
		collectsBat = CollectDAO.getAll(macAddress=capteur.macAddress, dataId=Data.BATTERY)
		data[capteur] = dict({'temperature' : collectsTemp, 'humidity': collectsHum, 'battery':collectsBat})
	return render_template('accueil.html', data=data)

if __name__ == '__main__':
	app.run(debug=False)
