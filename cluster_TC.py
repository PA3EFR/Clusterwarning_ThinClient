"""
Created and tested by Erwin - PA3EFR
"""


import socket
import re
import winsound  # Voor Windows; gebruik 'playsound' voor andere systemen.

# Configuratie: pas deze waarden aan
HOST = "www.db0erf.de"  # Vervang door de host-IP van het DXCluster van lijst https://www.dxcluster.info/telnet/dxcluster_up.htm
PORT = 41113                    # Vervang door de poort van het DXCluster
CALLSIGN = "PD1EHO"     # Vervang door je callsign of gebruikersnaam
patterns = [r"B/", r"WWFF", r"POTA", r"COTA", r"SOTA", r"BOTA"]

import pyaudio
import numpy as np

# Initialiseer PyAudio
p = pyaudio.PyAudio()

# Lijst van apparaten
#print("Beschikbare apparaten:")
#for i in range(p.get_device_count()):
#    info = p.get_device_info_by_index(i)
#    print(f"{i}: {info['name']}")

# Specificeer apparaat-ID van ingebouwde luidsprekers
default_device_id = 15  # Pas dit aan op basis van bovenstaande lijst


def play_alarm():
    """Speelt een toon af als alarmgeluid."""
    fs = 44100  # Samplefrequentie
    duration = 1  # Duur van de toon in seconden
    frequency = 440.0  # Frequentie van de toon in Hertz

    # Genereer een sinusgolf
    t = np.linspace(0, duration, int(fs * duration), endpoint=False)
    tone = (np.sin(2 * np.pi * frequency * t) * 0.5).astype(np.float32)

    # Initialiseer PyAudio
    p = pyaudio.PyAudio()

    try:
        # Start een audio-stream op het opgegeven apparaat
        stream = p.open(format=pyaudio.paFloat32,
                        channels=1,
                        rate=fs,
                        output=True,
                        output_device_index= default_device_id)

        # Speel de toon af
        stream.write(tone.tobytes())
        stream.stop_stream()
        stream.close()
    finally:
        p.terminate()

def main():
    # Maak verbinding met het DXCluster
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        print(f"Verbinden met {HOST}:{PORT}...")
        s.connect((HOST, PORT))
        print("Verbonden. Verstuur login...")

        # Verstuur logincommando
        login_command = f"{CALLSIGN}\n"  # Vaak is het gewoon de callsign gevolgd door een newline
        s.sendall(login_command.encode("utf-8"))
        print(f"Ingelogd als: {CALLSIGN}")
        printnr = 0
        try:
            while True:
                # Ontvang data van de socket
                data = s.recv(1024).decode("utf-8")
                data = data.upper()
                if not data:
                    break  # Verbinding is gesloten door de server

                # Toon ontvangen data (optioneel)
                #print(data)


                # Controleer op pattern in de ontvangen tekst
                for pattern in patterns:
                    if re.search(pattern, data):
                        print(f"Alarm: '{pattern}'")
                        print (data)
                        play_alarm()

        except KeyboardInterrupt:
            print("Script gestopt door gebruiker.")
        except Exception as e:
            print(f"Fout opgetreden: {e}")

if __name__ == "__main__":
    main()
