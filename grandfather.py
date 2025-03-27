randfather clock application by Jon Staebell 1/4/2019
#updated static IP address 12/16/2021
#updated 12/18/20202, pychromecast doesn't support python 2 so
# ran pip install PyChromecast==1.0.3 zeroconf==0.19.1
# updated 2/27/2025 to handle Chromecast device offline

import datetime, time, pychromecast, urllib.request, socket
from discord_webhook import DiscordWebhook

# set url for discord webhook if Chromecast device offline
webhook_url = "https://discord.com/api/webhooks/1297969513353973770/0_IoX6hluZvKUPLtRnQ9e1uQ8piP0IkCYbM7Fw3JCoupgjwFlKDCNJDdkmZ542FIyxZj"


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
#cast = next(cc for cc in chromecasts if cc.device.friendly_name == device_friendly_name)
device_present = False
device_alarm = False

cast = ""

# check to see if the Chromecast is available

while not device_present:
        for cc in chromecasts:
                if cc.device.friendly_name == device_friendly_name:
                        device_present = True

        if not device_present:
                if not device_alarm:
                        message = device_friendly_name + " is not running, grandfather paused"
                        webhook = DiscordWebhook(url=webhook_url, content=message)
                        response = webhook.execute()
                        device_alarm = True
                time.sleep(60*5) # sleep for 5 minutes

cast = next(cc for cc in chromecasts if cc.device.friendly_name == device_friendly_name)

if debug:
        print (device_present, cast)
        _ = input("press any key to continue")

time.sleep (0.5)

# wait for the device
cast.wait()
if debug:
        print(cast.device)
        print(cast.status)
        print ("starting")

# get media controller
mc = cast.media_controller
# need to make sure simplehttpserver is running to serve local audio file
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8",80))
filepath = 'http://' + s.getsockname()[0] + ':8000/home/pi/grandfather/'
if debug: print(filepath)
#filepath = 'http://192.168.2.150:8000/home/pi/grandfather/'

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
