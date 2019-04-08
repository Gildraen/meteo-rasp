import time
from bluepy.btle import Scanner, DefaultDelegate

class ScanDelegate(DefaultDelegate):
	def __init__(self):
		DefaultDelegate.__init__(self)

	def handleDiscovery(self, dev, isNewDev, isNewData)
			if (dev.addr == "d7:ef:13:27:15:29" or dev.addr == "d6:c6:c7:39:a2:e8"):
				print("Discovered device externe")
		elif isNewData:
			if (dev.addr == "d7:ef:13:27:15:29"):
				print("externe")
			elif (dev.addr == "d6:c6:c7:39:a2:e8"):
				print("interne")
			print(dev.getScanData())


scanner = Scanner().withDelegate(ScanDelegate())
scanner.clear()
scanner.start()
while True :
	print("still running...")
	scanner.process()
	time.sleep(2)
