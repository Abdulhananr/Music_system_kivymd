import pygame
import time

pygame.init()
pygame.mixer.init()

# Load an audio file
pygame.mixer.music.load(r"E:\unicercity Semster 6\Project No 23\Done\Power_English_Update.mp3")

# Play the audio file
pygame.mixer.music.play()

# Sleep to allow time for playback (replace with proper event handling in your application)
time.sleep(10)

# Stop playback
pygame.mixer.music.stop()
