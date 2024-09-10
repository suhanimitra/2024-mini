#!/usr/bin/env python3
"""
PWM Tone Generator

based on https://www.coderdojotc.org/micropython/sound/04-play-scale/
"""

import machine
import utime

# GP16 is the speaker pin
SPEAKER_PIN = 16

# create a Pulse Width Modulation Object on this pin
speaker = machine.PWM(machine.Pin(SPEAKER_PIN))


def playtone(frequency: float, duration: float) -> None:
    speaker.duty_u16(1000)
    speaker.freq(frequency)
    utime.sleep(duration)


def quiet():
    speaker.duty_u16(0)

notes = {
    'C4': 261,
    'D4': 294,
    'E4': 329,
    'F4': 349,
    'G4': 392,
    'A4': 440,
    'B4': 493,
    'C5': 523
}

# Happy Birthday
melody = [
    ('C4', 0.4), ('C4', 0.4), ('D4', 0.8), ('C4', 0.8), ('F4', 0.8), ('E4', 1.6),
    ('C4', 0.4), ('C4', 0.4), ('D4', 0.8), ('C4', 0.8), ('G4', 0.8), ('F4', 1.6),
    ('C4', 0.4), ('C4', 0.4), ('C5', 0.8), ('A4', 0.8), ('F4', 0.8), ('E4', 0.8), ('D4', 1.6),
    ('B4', 0.4), ('B4', 0.4), ('A4', 0.8), ('F4', 0.8), ('G4', 0.8), ('F4', 1.6)
]


def play_song():
    for note, duration in melody:
        freq = notes[note]
        print(f"Playing note {note} at frequency {freq} Hz")
        playtone(freq, duration)
        quiet()
        utime.sleep(0.1)  # Pause between notes

# Play Happy Birthday
play_song()

# Turn off the PWM
quiet()