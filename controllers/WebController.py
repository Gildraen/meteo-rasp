#! /usr/bin/python
# -*- coding:utf-8 -*-

from flask import Flask, render_template, request, redirect
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

@app.route('/name/<string:macAddress>', methods=['POST'])
def changeName(macAddress):
	capteur = CaptionDAO.getByMacAddress(macAddress)
	print(request.form['name'])
	capteur.name = request.form['name']
	CaptionDAO.update(capteur)
	return redirect("/")







if __name__ == '__main__':
	app.run(debug=False)
