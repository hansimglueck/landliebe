#!/bin/bash

cd /home/pi/zelle
sudo python3 /home/pi/zelle/renderIVR.py
sudo asterisk -rx "dialplan reload"
# Rufen Sie die gewünschte Asterisk-Erweiterung auf
sudo asterisk -rx "channel originate PJSIP/11 application Playback activated"
