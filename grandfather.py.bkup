# Grandfather 2.1 (c) 2025 Jon Staebell
#
# NOTE! requires crontab set up to run at 15/30/45 minutes during desired times. e.g.:
# 0,15,30,45 7-21 * * * /path/to/python /path/to/grandfather.py  >> /var/log/grandfather.log 2>&1
# (sends output to grandfather.log file. View with tail -f /var/log/grandfather.log)
#
# Need to change the following parameters below:
#   DEVICE_FRIENDLY_NAME
#   CLOCK_VOLUME
#   PORT (for simple server)
#
# Requires simple server running on port 8000 (see PORT parameter in main)
#
# Optional: include any argument to command line to trigger startup message
# e.g. python grandfather.py d
#
import time, pychromecast, os, socket, datetime, sys
import signal

def handler(signum, frame):
    raise TimeoutError("Grandfather.py took too long and was terminated.")

signal.signal(signal.SIGALRM, handler)
signal.alarm(120)  # Max 2 minutes runtime

def main():
    try:
        # config
        DEVICE_FRIENDLY_NAME = 'Living Room speaker'
        CLOCK_VOLUME = 0.2
        PORT = 8000

        if len(sys.argv) > 1:
            call_error("Grandfather triggered")

        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]

        filename = get_filename()
        if filename:
            media_path = f"/projects/grandfather/bong{filename}.wav"
            if not os.path.exists(f"/home/jon/{media_path}"):
                call_error(f"Missing media file: {media_path}")
                return

            media = f"http://{ip}:{PORT}{media_path}"
            cast = get_cast(DEVICE_FRIENDLY_NAME)
            if cast:
                call_cast(cast, media, CLOCK_VOLUME)
            else:
                call_error("Grandfather Missing Chromecast " + DEVICE_FRIENDLY_NAME)
        else:
            call_error("Grandfather invoked at invalid time")
    finally:
        signal.alarm(0)  # always cancel alarm, even on early return


def call_cast(cast, media_url, volume):
    try:
        cast.wait()
        old_volume = cast.status.volume_level
        cast.set_volume(volume)

        mc = cast.media_controller
        mc.play_media(media_url, content_type='audio/wav')
        mc.block_until_active()

        # Wait for media to start (timeout safety)
        for _ in range(30):  # 3 seconds max
            if mc.status.player_state == "PLAYING":
                break
            time.sleep(0.1)
        else:
            call_error(f"Media did not start playing within timeout: {media_url}")
            return 

        # wait for file to finish playing, then reset volume to previous level
        time.sleep(30)
        cast.set_volume(old_volume)
    except Exception as e:
        call_error(f"Error playing media: {media_url} — {e}")

def get_cast(device_friendly_name, timeout=5):
    try:
        chromecasts, browser = pychromecast.get_chromecasts(timeout=timeout)
    except Exception as e:
        call_error(f"Error discovering Chromecast devices: {e}")
        return None

    if not chromecasts:
        call_error("No Chromecast devices found.")
        return None

    # Normalize names and compare case-insensitively
    for cc in chromecasts:
        try:
            name = cc.cast_info.friendly_name.strip().lower()
            target = device_friendly_name.strip().lower()
            if name == target:
                return cc
        except Exception:
            continue

    call_error(f"No Chromecast matching '{device_friendly_name}' found.")
    return None

def call_error(output_message):
    # reports error condition
    print (datetime.datetime.now(),output_message)

def get_filename():
    # Returns part of filename needed to specify the media file
    # if the minute is "00", returns the hour ("1", "2", etc.), else returns the minute ("15", "30", or "45")
    # if minute is not "00","15","30", or "45" return None because program invoked at wrong time
    hour, minute = time.strftime("%I %M").split(" ")
    if minute in ("00","15","30","45"):
         return hour if minute == "00" else minute
    else:
        return None

if __name__ == "__main__":
    try:
        main()
    except TimeoutError as e:
        print(datetime.datetime.now(), "Timed out:", e)
