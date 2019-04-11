#! /usr/bin/python
# -*- coding:utf-8 -*-

from flask import Flask, render_template
import sys
sys.path.append('/home/projects/meteo-rasp/entity')
sys.path.append('/home/projects/meteo-rasp/repo')
from caption_dao import CaptionDAO
from collect_dao import CollectDAO
from data import Data
app = Flask(__name__)

@app.route('/')
def accueil():

	capteurs = CaptionDAO.getAll()
	data = {}

	for capteur in capteurs:
		collectsHum = CollectDAO.getAll(macAddress=capteur.macAddress, DataId=Data.HUMIDITY)
		collectsTemp = CollectDAO.getAll(macAddress=capteur.macAddress, DataId=Data.TEMPERATURE)
		collectsBat = CollectDAO.getAll(macAddress=capteur.macAddress, DataId=Data.BATTERY)
		print(len(collectsBat))
		data[capteur] = dict({'temperature' : collectsTemp, 'humidity': collectsHum, 'battery':collectsBat})
	return render_template('accueil.html', data=data)

if __name__ == '__main__':
	app.run(debug=False)
