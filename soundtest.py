"""
Created and tested by Erwin - PA3EFR
"""

import sounddevice as sd
import numpy as np

# Lijst van beschikbare apparaten
devices = sd.query_devices()
print("Beschikbare audio-apparaten:")
for idx, device in enumerate(devices):
    print(f"{idx}: {device['name']}")

# Selecteer het apparaatnummer van de ingebouwde luidsprekers
default_device = 15  # Pas dit aan op basis van de lijst van apparaten

# Afspelen van een testtoon op het geselecteerde apparaat
fs = 44100  # Samplingfrequentie
duration = 3  # seconden
frequency = 440.0  # Hz

t = np.linspace(0, duration, int(fs * duration), endpoint=False)
tone = 0.5 * np.sin(2 * np.pi * frequency * t)

sd.play(tone, samplerate=fs, device=default_device)
sd.wait()
print("Audio afgespeeld op apparaat:", devices[default_device]['name'])
