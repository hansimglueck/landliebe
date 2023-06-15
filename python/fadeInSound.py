import time
import os

print ("start fadeInSound")
os.system("amixer set Headphone 0%")
time.sleep(23)
os.system("amixer set Headphone 70%")
for i in range(30):
	time.sleep(0.5)
	print(i)
	os.system("amixer set Headphone " + str(70+i) + "%")
	print("amixer set Headphone " + str(70+i) + "%")

print ("end")

