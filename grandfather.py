#Grandfather clock application by Jon Staebell 1/4/2019

import datetime, time, pychromecast, urllib.request

# set beginning and ending hours for the clock chimes
beginhour = 7
endhour = 21

# Set volume for clock chimes between 0 and 1:
clockvolume = .2

# display debug messages?
debug = False

# Your Chromecast device Friendly Name
device_friendly_name = "Living Room speaker"

chromecasts = pychromecast.get_chromecasts()

# select Chromecast device
cast = next(cc for cc in chromecasts if cc.device.friendly_name == device_friendly_name)
time.sleep (0.5)

# wait for the device
cast.wait()
print(cast.device)
print(cast.status)
print ("starting")

# get media controller
mc = cast.media_controller
# need to make sure simplehttpserver is running to serve local audio file
filepath = 'http://192.168.2.95:8000/grandfather/'

bing15file = filepath + 'bing15.wav'
bing30file = filepath + 'bing30.wav'
bing45file = filepath + 'bing45.wav'

# function to cast file to Chromcast device
def castclock(clockfile):
	oldvolume = cast.status.volume_level
	cast.set_volume(clockvolume)
	if debug: print ("set volume to ", clockvolume)
	time.sleep(1)

	if debug: print(cast.status)
	if debug: print ('playing ',clockfile)
	mc.play_media(clockfile, content_type = 'audio/wav')

	time.sleep(60)

	cast.set_volume(oldvolume)
	if debug: print ("reset volume to ", oldvolume)
	time.sleep(10)

# debug chromecast
if debug:
	bongfile = filepath + 'bong12.wav'
	print ('Starting debug')
	castclock(bongfile)
	print ("end of debug")

while True:
	if debug: print ("in loop")
	currentDT = datetime.datetime.now()
	hour = currentDT.hour
	hour12 = hour%12
	if hour12 == 0:
		hour12 = 12
	minute = currentDT.minute
	second = currentDT.second

	if hour >= beginhour and hour <= endhour:

		if minute == 0:
			if debug: print (hour, ":",minute,":",second)
			bongfile = filepath + 'bong' + str(hour12) + '.wav'
			castclock(bongfile)

		if minute == 15:
			if debug:
				print (hour, ":",minute,":",second)
				print("Bing15")
			castclock(bing15file)

		if minute == 30:
			if debug:
				print (hour, ":",minute,":",second)
				print ("Bing30")
			castclock(bing30file)

		if minute == 45:
			if debug:
				print (hour, ":",minute,":",second)
				print ("Bing45")
			castclock(bing45file)

	time.sleep(10)

# end of code


