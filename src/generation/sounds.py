import numpy as np
import wave

SAMPLE_RATE = 44100
DURATION = 0.12
VOLUME = 2

# jump
FREQ_START = 600
FREQ_END = 900
t = np.linspace(0, DURATION, int(SAMPLE_RATE * DURATION), False)

# sweep w górę (typowy "jump")
freq = np.linspace(FREQ_START, FREQ_END, t.size)
signal = np.sin(2 * np.pi * freq * t)

# szybki fade-out
envelope = np.linspace(1, 0, t.size)
signal *= envelope

# normalizacja
audio = (signal * VOLUME * 32767).astype(np.int16)

with wave.open("../sounds/jump.wav", "w") as f:
    f.setnchannels(1)
    f.setsampwidth(2)
    f.setframerate(SAMPLE_RATE)
    f.writeframes(audio.tobytes())

print("jump.wav wygenerowany")


# biały szum
noise = np.random.normal(0, 1, int(SAMPLE_RATE * DURATION))

# filtr – zostawiamy tylko "miękkie" częstotliwości
noise = np.convolve(noise, np.ones(400) / 400, mode="same")

# obwiednia (szybki start, szybkie wyciszenie)
attack = int(0.02 * SAMPLE_RATE)
release = int(0.08 * SAMPLE_RATE)
envelope = np.concatenate(
    [
        np.linspace(0, 1, attack),
        np.linspace(1, 0, release),
    ]
)

noise = noise[: envelope.size] * envelope
audio = (noise * VOLUME * 32767).astype(np.int16)

with wave.open("../sounds/jump_rustle.wav", "w") as f:
    f.setnchannels(1)
    f.setsampwidth(2)
    f.setframerate(SAMPLE_RATE)
    f.writeframes(audio.tobytes())

print("jump_rustle.wav wygenerowany")


FREQ = 880  # przyjemne, nie za wysokie
t = np.linspace(0, DURATION, int(SAMPLE_RATE * DURATION), False)

# miękka fala (trochę retro, ale delikatna)
signal = np.sin(2 * np.pi * FREQ * t)

# obwiednia – szybki atak, szybkie wyciszenie
attack = int(0.01 * SAMPLE_RATE)
release = int(0.05 * SAMPLE_RATE)
envelope = np.concatenate(
    [
        np.linspace(0, 1, attack),
        np.linspace(1, 0, release),
    ]
)

signal = signal[: envelope.size] * envelope
audio = (signal * VOLUME * 32767).astype(np.int16)

with wave.open("../sounds/npc_talk.wav", "w") as f:
    f.setnchannels(1)
    f.setsampwidth(2)
    f.setframerate(SAMPLE_RATE)
    f.writeframes(audio.tobytes())

print("npc_talk.wav wygenerowany")


def tone(freq, duration):
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration), False)
    return np.sin(2 * np.pi * freq * t)


sound = np.concatenate(
    [
        tone(900, 0.03),
        np.zeros(int(0.01 * SAMPLE_RATE)),
        tone(1100, 0.03),
    ]
)

envelope = np.linspace(1, 0, sound.size)
sound *= envelope

audio = (sound * VOLUME * 32767).astype(np.int16)

with wave.open("npc_talk.wav", "w") as f:
    f.setnchannels(1)
    f.setsampwidth(2)
    f.setframerate(SAMPLE_RATE)
    f.writeframes(audio.tobytes())

print("npc_talk.wav wygenerowany")


t = np.linspace(0, DURATION, int(SAMPLE_RATE * DURATION), False)

# bardzo delikatny ton (prawie niesłyszalny)
tone = np.sin(2 * np.pi * 700 * t) * 0.2

# miękki szum
noise = np.random.normal(0, 1, t.size)
noise = np.convolve(noise, np.ones(300) / 300, mode="same") * 0.8

# miks
signal = tone + noise

# obwiednia – zero kliknięcia
attack = int(0.015 * SAMPLE_RATE)
release = int(0.055 * SAMPLE_RATE)
envelope = np.concatenate(
    [
        np.linspace(0, 1, attack),
        np.linspace(1, 0, release),
    ]
)

signal = signal[: envelope.size] * envelope
audio = (signal * VOLUME * 32767).astype(np.int16)

with wave.open("../sounds/npc_soft_cue.wav", "w") as f:
    f.setnchannels(1)
    f.setsampwidth(2)
    f.setframerate(SAMPLE_RATE)
    f.writeframes(audio.tobytes())

print("npc_soft_cue.wav wygenerowany")


def hm_sound(freq, duration):
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration), False)

    # bardzo miękki ton
    tone = np.sin(2 * np.pi * freq * t) * 0.25

    # szelest / oddech
    noise = np.random.normal(0, 1, t.size)
    noise = np.convolve(noise, np.ones(400) / 400, mode="same") * 0.7

    signal = tone + noise

    # miękka obwiednia
    attack = int(0.03 * SAMPLE_RATE)
    release = int((duration - 0.03) * SAMPLE_RATE)
    envelope = np.concatenate(
        [
            np.linspace(0, 1, attack),
            np.linspace(1, 0, release),
        ]
    )

    return signal[: envelope.size] * envelope


hm1 = hm_sound(600, 0.12)
pause = np.zeros(int(0.05 * SAMPLE_RATE))
hm2 = hm_sound(500, 0.12)

sound = np.concatenate([hm1, pause, hm2])
audio = (sound * VOLUME * 32767).astype(np.int16)

with wave.open("../sounds/npc_hmhm.wav", "w") as f:
    f.setnchannels(1)
    f.setsampwidth(2)
    f.setframerate(SAMPLE_RATE)
    f.writeframes(audio.tobytes())

print("npc_hmhm.wav wygenerowany")


def mmh(duration, strength):
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration), False)

    # prawie niesłyszalny ton (tylko "ciało")
    tone = np.sin(2 * np.pi * 520 * t) * 0.15

    # oddech / szelest
    noise = np.random.normal(0, 1, t.size)
    noise = np.convolve(noise, np.ones(500) / 500, mode="same") * 0.9

    signal = (tone + noise) * strength

    # bardzo miękka obwiednia
    attack = int(0.04 * SAMPLE_RATE)
    release = int((duration - 0.04) * SAMPLE_RATE)
    envelope = np.concatenate(
        [
            np.linspace(0, 1, attack),
            np.linspace(1, 0, release),
        ]
    )

    return signal[: envelope.size] * envelope


hm1 = mmh(0.14, strength=1)
pause = np.zeros(int(0.04 * SAMPLE_RATE))
hm2 = mmh(0.14, strength=0.85)  # ciszej, NIE niżej

sound = np.concatenate([hm1, pause, hm2])
audio = (sound * VOLUME * 32767).astype(np.int16)

with wave.open("../sounds/npc_mmhm.wav", "w") as f:
    f.setnchannels(1)
    f.setsampwidth(2)
    f.setframerate(SAMPLE_RATE)
    f.writeframes(audio.tobytes())

print("npc_mmhm.wav wygenerowany")
