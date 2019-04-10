import time
from bluepy.btle import Scanner, DefaultDelegate

class ScanDelegate(DefaultDelegate):
	def __init__(self):
		DefaultDelegate.__init__(self)

	def handleDiscovery(self, dev, isNewDev, isNewData):
		if (dev.addr == "d7:ef:13:27:15:29" or dev.addr == "d6:c6:c7:39:a2:e8" or dev.addr == "f3:43:ad:d9:8f:5f"):
#			print("Discovered device", dev.addrType,  dev.getValueText(22))
			
			if isNewData and dev.getValueText(22) != None:
				datas = dev.getValueText(22)
#				print(datas)
				bat = int(datas[20:22],16)
				hum = str(int(datas[28:32],16)/100)
				temp = str(int(datas[24:28],16)/100)
				if (dev.addr == "d7:ef:13:27:15:29"):
					print("----------------------------")					
					print("externe =>")
				elif (dev.addr == "d6:c6:c7:39:a2:e8"):
					print("----------------------------")
					print("interne =>")
				elif (dev.addr == "f3:43:ad:d9:8f:5f"):
					print("----------------------------")
					print("jardin=>")
#				print(datas)
				print("Batterie : ", bat)
				print("Humidite : ", hum)
				print("Temperature : ", temp)
				print("----------------------------")

scanner = Scanner().withDelegate(ScanDelegate())
scanner.clear()
scanner.start()
while True :
	print("still running...")
	scanner.process()
	#time.sleep(2)
