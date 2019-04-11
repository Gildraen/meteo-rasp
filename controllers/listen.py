# -*- coding: utf-8 -*-

import time
import sys
import datetime
sys.path.append('/home/projects/meteo-rasp/entity')
sys.path.append('/home/projects/meteo-rasp/repo')
from caption import Caption
from collect import Collect
from data import Data
from caption_dao import CaptionDAO
from collect_dao import CollectDAO
from data_dao import DataDAO


from bluepy.btle import Scanner, DefaultDelegate

class ScanDelegate(DefaultDelegate):
	def __init__(self):
		DefaultDelegate.__init__(self)
		self.capteurs = CaptionDAO.getAll()
		self.macAddress = list()
		for capteur in self.capteurs:
			self.macAddress.append(capteur.macAddress)
		self.dataHum = DataDAO.getById(Data.HUMIDITY)
		self.dataTemp = DataDAO.getById(Data.TEMPERATURE)
		self.dataBat = DataDAO.getById(Data.BATTERY)


	def handleDiscovery(self, dev, isNewDev, isNewData):
		if (dev.addr in self.macAddress and isNewData and dev.getValueText(22) != None):
			datas = dev.getValueText(22)
			bat = int(datas[20:22],16)
			hum = int(datas[28:32],16)/100
			temp = int(datas[24:28],16)/100
			#testData(bat, self.dataBat)
			#testData(hum, self.dataHum)
			#testData(temp, self.dataTemp)
			caption = CaptionDAO.getByMacAddress(dev.addr)
			print("----------------------------")
			print(caption.name)
			print("Batterie : ", bat)
			print("Humidite : ", hum)
			print("Temperature : ", temp)
			print("----------------------------")
			collectHum = Collect(0, self.dataHum, caption, datetime.datetime.now(),hum)
			collectBat = Collect(0, self.dataBat, caption, datetime.datetime.now(),bat)
			collectTemp = Collect(0, self.dataTemp, caption, datetime.datetime.now(),temp)
			CollectDAO.create(collectHum)
			CollectDAO.create(collectBat)
			CollectDAO.create(collectTemp)

	def sendMail(message):
		TO = 'recipient@mailservice.com'	
		SUBJECT = 'Problem data'

		# Gmail Sign In
		gmail_sender = 'meteo.rasp.jbgsp@gmail.com'
		gmail_passwd = 'spjyukypntznaxul'

		server = smtplib.SMTP('smtp.gmail.com', 587)
		server.ehlo()
		server.starttls()
		server.login(gmail_sender, gmail_passwd)

		BODY = '\r\n'.join(['To: %s' % TO,
                	    'From: %s' % gmail_sender,
                    	'Subject: %s' % SUBJECT,
                    	'', message])

		try:
    			server.sendmail(gmail_sender, [TO], BODY)
    			print ('email sent')
		except:
	    		print ('error sending mail')

		server.quit()

	def testData(data, dataTest)
		#TODO
		

	
		
scanner = Scanner().withDelegate(ScanDelegate())
#scanner.clear()
#scanner.start()
while True :
	scanner.clear()
	scanner.start()
	print('...')
	scanner.process()
	scanner.stop()

