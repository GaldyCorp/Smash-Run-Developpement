import imp
import pygame
import json
from tkinter import filedialog
import shutil
from smrun_lib import *
from edit_menu import *
from main_menu import *
pygame.init()

class main_window:
    def __init__(self):
        # PARAMETER
        pygame.display.set_caption("Smash Run Editor")
        self.screen = pygame.display.set_mode((1365, 710), pygame.RESIZABLE) #pygame.FULLSCREEN
        self.clock = pygame.time.Clock()

        #Network

        # GROUPS
        self.all_sprites = pygame.sprite.Group()

        # RUNNING
        self.is_running=True
        self.menu_is_running=True
        self.editor_is_running=False

        # OBJECTS
        self.call_main_menu()

    def run(self):
        '''GameLoop'''
        while self.is_running:
            self.clock.tick(60)
            self.events()
            self.update()
            self.draw()

    def update(self):
        self.all_sprites.update()

    def call_main_menu(self):
        self.main_menu = main_menu()
        self.main_menu_sprites = pygame.sprite.Group()
        self.main_menu_sprites.add(self.main_menu.group_sprite)

    def call_editor(self,dir):
        self.editor_menu = edit_menu(dir)

    
    def events(self):
        all_events = pygame.event.get()

        if self.menu_is_running:
            code_out = self.main_menu.event(all_events) #code[0] ref : 0 -> RAS 1-> load edit menu with code[1] as directory
            if code_out[0] == 1:
                directory = code_out[1]
                self.main_menu.kill()
                self.main_menu=None
                self.menu_is_running=False
                #self.screen = pygame.display.set_mode((1365, 710))
                self.call_editor(directory)
                self.editor_is_running=True
                    
        if self.editor_is_running:
            code_out = self.editor_menu.event(all_events)
            if code_out == 1:
                self.editor_menu.kill()
                self.editor_menu=None
                self.editor_is_running=False
                self.call_main_menu()
                self.menu_is_running=True


        for event in all_events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.screen = pygame.display.set_mode((1365, 710), pygame.RESIZABLE)
                elif event.key == pygame.K_F11:
                    self.screen = pygame.display.set_mode((1920, 1080),pygame.FULLSCREEN)
    
            if event.type == pygame.QUIT:
                pygame.quit()

    def draw(self):
        self.all_sprites.draw(self.screen) # actualise les sprites
        if self.menu_is_running:
            self.main_menu.group_sprite.draw(self.screen)
        if self.editor_is_running:
            self.editor_menu.group_sprite.draw(self.screen)
        pygame.display.flip()

root=main_window()
root.run()
