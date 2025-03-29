# Grandfather 2.0 (c) 2025 Jon Staebell
#
# NOTE! requires crontab set up to run at 15/30/45 minutes during desired times. e.g.:
# 0,15,30,45 * 7-21 * * /path/to/python /path/to/grandfather.py
#
# Need to change the following parameters below:
#   webhook_url (optional, set to "" to disable Discord webhook calls on errors
#   device_friendly_name
#   clockvolume
#
# Requires simple server running on port 8000 (see media parameter)
#
import time, pychromecast, os, requests, socket, configparser, sys
from discord_webhook import DiscordWebhook

def main():
    params = get_config(sys.argv[0].replace(".py", ".ini"))
    webhook_url = params ['webhook_url']
    device_friendly_name = params ['device_friendly_name']
    clockvolume = params ['clockvolume']

    # build filepath, including IP address, to send to simple server
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8",80))
    media = 'http://' + s.getsockname()[0] + ':8000' + os.getcwd() + "/bong" + get_filename()  + ".wav"
    cast = get_cast(device_friendly_name)
    if cast  == "":
        call_webhook(webhook_url, "Grandfather Missing Chromecast " + device_friendly_name) #error or missing chromecast
    else:
        call_cast(cast, media, webhook_url, clockvolume)

def get_config(config_file):
    # return paramaters from configuration file
    param_dict = {}
    try:
        Config = configparser.ConfigParser()
        Config.read(config_file)
        param_dict['device_friendly_name'] = Config.get('required', 'device_friendly_name')
        param_dict['clockvolume'] = float(Config.get('required', 'clockvolume'))
        param_dict['webhook_url'] = Config.get('optional', 'webhook_url')
    except:
        print (f"invalid config file {config_file}")
        sys.exit() # exit on exceptions
    return param_dict


def call_cast(cast, media, webhook_url, clockvolume):
    # plays specified media on the specified chromecast
    # clockvolume is volume at which to play the media
    # calls optional webhook if there's an error playing the media
    #
    try:
        cast.wait() # wait until ready
        oldvolume = cast.status.volume_level # save current volume
        cast.set_volume(clockvolume) # set volume to specified
        mc = cast.media_controller
        mc.play_media(media, content_type = 'audio/wav')
        time.sleep(10) # allow to play
        cast.set_volume(oldvolume) # change volume back to previous
    except:
        call_webhook(webhook_url, "Grandfather error playing media " + media)

def get_cast(device_friendly_name):
    # returns the Chromecast specified. If pychromecast call errors or it's not found, returns ""
    #
    try:
        chromecasts = pychromecast.get_chromecasts()
    except:
        return ""

    # check to see if the Chromecast is available
    for cc in chromecasts:
            if cc.device.friendly_name == device_friendly_name:
                    return cc
    return ""


def call_webhook(webhook_url, output_message):
    # checks the webhook_url parameter, and if present, uses it to send webhook to Discord
    #
    # if url provided and minute is "00" (to avoid spamming notifications), notify Discord to add alert
    if webhook_url != "" and time.strftime("%M") == "00":
        webhook = DiscordWebhook(url=webhook_url, content=f"{output_message}")
        response = webhook.execute()
        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError as err:
            print("Error in trying to use Discord Webhook", err)

def get_filename():
    # Returns part of filename needed to specify the media file
    # if the minute is "00", returns the hour ("1", "2", etc.), else returns the minute ("15", "30", or "45")
    hour, minute = time.strftime("%I %M").split(" ")
    return hour if minute == "00" else minute

if __name__ == "__main__":
    main()
