import pygame
import numpy as np
import time

# Initialize Pygame mixer
pygame.mixer.init()

# Set the sample rate and duration of each tone (adjust as needed)
sample_rate = 44100
tone_duration = 0.5

# Set the number of tones in the siren sound
num_tones = 10

# Generate the siren sound waveform
frequency = 440
waveform_mono = np.zeros(int(sample_rate * tone_duration))
for _ in range(num_tones):
    t = np.linspace(0, tone_duration, int(sample_rate * tone_duration), endpoint=False)
    tone = np.sin(2 * np.pi * frequency * t)
    waveform_mono += tone
    frequency += 100

# Duplicate the mono waveform for both left and right channels
waveform_stereo = np.column_stack((waveform_mono, waveform_mono))

# Normalize the waveform
waveform_stereo /= np.max(np.abs(waveform_stereo))
waveform_stereo *= 32767

# Create a Pygame sound from the waveform
sound = pygame.sndarray.make_sound(waveform_stereo.astype(np.int16))

# Play the sound
sound.play()

# Wait for the sound to finish playing
pygame.time.wait(int(tone_duration * 1000 * num_tones))

# Clean up the sound
sound.stop()
pygame.mixer.quit()
