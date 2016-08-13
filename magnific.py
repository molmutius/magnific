import RPi.GPIO as GPIO
import picamera
import time
import subprocess, signal, os
import logging
import logging.handlers

log = logging.getLogger('Magnific')
log.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
consolehandler = logging.StreamHandler()
consolehandler.setLevel(logging.DEBUG)
consolehandler.setFormatter(formatter)
filehandler = logging.handlers.RotatingFileHandler('log', maxBytes=10000000)
filehandler.setLevel(logging.DEBUG)
filehandler.setFormatter(formatter)
log.addHandler(consolehandler)
log.addHandler(filehandler)

is_preview_mode = False

def preview():
    try:
        log.debug('preview mode on')
        subprocess.call(['sudo', 'killall', 'fbi'])
        camera.start_preview()
    except Exception as e:
        log.warn(e)
        
def still():
    try:
        log.debug('still mode on')
        camera.capture('/home/pi/Desktop/image.jpg')
        camera.stop_preview()
        subprocess.call(["sudo", "fbi", "-noverbose", "-d", "/dev/fb0", "-a", "-T", "2", "/home/pi/Desktop/image.jpg"])
    except Exception as e:
        log.warn(e)

def toggle_mode(arg):
    try:
        log.debug('toggle')
        global is_preview_mode
        is_preview_mode = not is_preview_mode
        if is_preview_mode:
            preview()
        else:
            still()
    except Exception as e:
        log.warn(e)

GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.IN, GPIO.PUD_UP)
GPIO.add_event_detect(17, GPIO.FALLING, callback=toggle_mode, bouncetime=1000)

if __name__ == '__main__':
    try:
        with picamera.PiCamera() as camera:
            camera.resolution = (1920, 1080)
            camera.framerate = 30
            camera.exposure_mode = 'auto'
            toggle_mode('')
            while True:
                time.sleep(1)
    except KeyboardInterrupt as e:
        log.debug('application stopped via keyboard interrupt ctrl+z')
        exit(0)
    except Exception as e:
        log.warn(e)
