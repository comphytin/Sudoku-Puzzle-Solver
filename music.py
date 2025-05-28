import pygame

class Music:
    def __init__(self, track):
        self.track = pygame.mixer.Sound("audio/" + track + ".wav")
        self.music_started = False
    
    def setVolume(self):
        self.track.set_volume(0.1)
    
    def play(self):
        pass