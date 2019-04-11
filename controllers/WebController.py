#! /usr/bin/python
# -*- coding:utf-8 -*-

from flask import Flask, render_template, request, redirect
from repo.caption_dao import CaptionDAO
from repo.collect_dao import CollectDAO
from entity.data import Data
from repo.contact_dao import ContactDAO
from repo.data_dao import DataDAO
from repo.threshold_dao import ThresholdDAO
import pygal
from pygal.style import NeonStyle
app = Flask(__name__)

@app.route('/')
def accueil():

	capteurs = CaptionDAO.getAll()
	data = {}

	for capteur in capteurs:
		print(capteur.name)
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

@app.route('/graph')
def graph():

	capteurs = CaptionDAO.getAll()
	data = {}

	for capteur in capteurs:
		humval = []
		tempval=[]
		collectsHum = CollectDAO.getAll(macAddress=capteur.macAddress, dataId=Data.HUMIDITY)
		collectsTemp = CollectDAO.getAll(macAddress=capteur.macAddress, dataId=Data.TEMPERATURE)
		for hum in collectsHum:
			humval.append(hum.value)
		for temp in collectsTemp:
			tempval.append(temp.value)
		print(capteur.name)
		#print(collectsHum[0].date)
		#print(collectsHum[len(collectsHum)-1].date)

		if collectsHum is not None:
			line_chart = pygal.Line(interpolate='cubic', style=NeonStyle, disable_xml_declaration=True)
			line_chart.title = capteur.name
			#line_chart.x_labels = map(str, range(collectsHum[0].date, collectsHum[len(collectsHum)-1].date))
			line_chart.add('HUMIDITY', humval)
			line_chart.add('TEMPERATURE', tempval)
			data[capteur] = dict({'graph': line_chart})
	return render_template('graph.html', data=data)



@app.route('/seuils/')
def seuils():
	data = dict({'thresholds' : ThresholdDAO.getAll(), 'contacts': ContactDAO.getAll(), 'datas':DataDAO.getAll()})
	return render_template('seuils.html', data=data)

if __name__ == '__main__':
	app.run(debug=False, host='0.0.0.0', port='5000')
