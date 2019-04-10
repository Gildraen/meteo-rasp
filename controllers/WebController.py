#! /usr/bin/python
# -*- coding:utf-8 -*-

from flask import Flask, render_template
import sys
sys.path.append('/home/projects/meteo-rasp/entity')
sys.path.append('/home/projects/meteo-rasp/repo')
from caption_dao import CaptionDAO
 
app = Flask(__name__)

@app.route('/')
def accueil():

	capteurs = CaptionDAO.getAll()
    data = {}
	
	for capteur in capteurs
		collects = CollectDAO.getAll(capteur.macAddress)
		data[capteur] = collects

    return render_template('accueil.html', data=data)
	
	
if __name__ == '__main__':
    app.run(debug=True)
    print('toto')