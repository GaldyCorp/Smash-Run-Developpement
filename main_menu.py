import imp
import pygame
from smrun_lib import *
from tkinter import filedialog
import json
import shutil

class main_menu():
    def __init__(self):
        #Init list & group
        self.group_sprite = pygame.sprite.Group()
        self.list_sprite=[]
        #Init Object
        self.background=Image(0,0,"Image\Map\City1\map.png")
        self.load = menu_bouton("Load Button", 650,300,3)
        self.exit=menu_bouton("Exit Button",650,500,3)
        #Add Objet to list
        self.list_sprite.append(self.background)
        self.list_sprite.append(self.load)
        self.list_sprite.append(self.exit)
        #Add Objet to group
        for sprite in self.list_sprite:
            self.group_sprite.add(sprite)

    def update(self):
        self.group_sprite.update()

    def event(self,all_events=[]):
        if all_events==[]:
            return [0]
        else:
            for event in all_events:
                if event.type == pygame.MOUSEBUTTONUP:
                    if self.exit.rect.collidepoint(pygame.mouse.get_pos()):
                        pygame.quit()
                    elif self.load.rect.collidepoint(pygame.mouse.get_pos()):
                        try:                            
                            self.directory=filedialog.askdirectory()
                            print(self.directory)
                            try:
                                self.map=Image(0,0, str(self.directory)+"/map.png")
                                try:
                                    with open(self.directory+'/box.json') as json_file:
                                        None
                                except:
                                    with open(self.directory+'/box.json', "w") as json_file:
                                        json.dump({"ground":[]}, json_file, ensure_ascii=False)
                                return [1, self.directory]
                            except:
                                self.dir_image=filedialog.askopenfilename()
                                if self.dir_image[-4:]==".png":
                                    shutil.copyfile(self.dir_image, self.directory+"/map.png")
                        except:
                            self.directory=None
            return self.event()

    def kill(self):
        for sprite in self.group_sprite:
            sprite.kill()
