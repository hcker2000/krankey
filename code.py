# -------------------------------------------------------------------------
# Control NeoPixel-ring, servo-motor and bgPlayer-mini
#
# Note that you have to add neopixel.mpy and adafruit_motor from the
# library-bundle corresponding to your version of CircuitPython on the M0.
#
# This version uses the uart for communication with the bgPlayer.
#
# Author: Bernhard Bablok
# License: GPL3
#
# Website: https://github.com/bablokb/trinket-m0
#
# -------------------------------------------------------------------------

import time
import board
import digitalio
import busio
import random

from DFPlayer import DFPlayer

	
# --- constants   ----------------------------------------------------------
BG_PLAYER_VOL = 70
BG_PLAYER_TX = board.GP16
BG_PLAYER_RX = board.GP17

VOICE_PLAYER_VOL = 100
VOICE_PLAYER_TX = board.GP16
VOICE_PLAYER_RX = board.GP17

# --- objects   -----------------------------------------------------------
bgUart = busio.UART(board.GP16, board.GP17, baudrate=9600)
voiceUart = busio.UART(board.GP8, board.GP9, baudrate=9600)
bgPlayer = DFPlayer(volume=BG_PLAYER_VOL,uart=bgUart)
voicePlayer = DFPlayer(volume=VOICE_PLAYER_VOL,uart=voiceUart)
# voicePlayer.set_eq(DFPlayer.EQ_ROCK)

# --- initialization   ----------------------------------------------------
led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT

firstLoop = True
introPlaying = True
voicePlaying = False
switchTrack = False
nextVoiceTime = random.randint(1,2)
lastVoiceTime = time.monotonic()

# get random number between 1 and 100 
bgRandom = random.randint(1, 2)


voicePlayer.play(track=1)
 
time.sleep(0.200)

def generateNextVoiceTime():
	global voicePlaying
	global nextVoiceTime
	global lastVoiceTime
 
	voicePlaying = False
	nextVoiceTime = random.randint(1,8)
	lastVoiceTime = time.monotonic()

# --- main loop   --------------------------------------------------------

while True:
	time.sleep(0.100)
 
	if voicePlayer.get_status() != 1:
		introPlaying = False

	if introPlaying == False:
		if firstLoop == True:
			firstLoop = False
			if bgRandom == 1:
				bgPlayer.play(track=1)
			else:
				switchTrack = True
				bgPlayer.play(track=2)
    
		if bgPlayer.get_status() == 1:
			led.value = True
			# print("busy")
		else:
			if switchTrack == True:
				switchTrack = False
				bgPlayer.play(track=1)
			led.value = False
		print(voicePlaying)
		print(nextVoiceTime)
		print(time.monotonic() - lastVoiceTime)
		if voicePlaying == False:
			if nextVoiceTime < time.monotonic() - lastVoiceTime:
				voicePlaying = True
				bgPlayer.set_volume(25)
				voicePlayer.play(track=random.randint(2,21))
		else:
			if voicePlayer.get_status() != 1:
				bgPlayer.set_volume(BG_PLAYER_VOL)
				generateNextVoiceTime()

    
