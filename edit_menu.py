import pygame
from smrun_lib import *
import json

class edit_menu():
    def __init__(self,dir):
        #Init list & group
        self.group_sprite = pygame.sprite.Group()
        self.list_sprite=[]
        #Init Object
        self.menu_bar_is_running=True
        self.dir = dir
        self.all_line = []
        self.background=Image(0,0,dir+"/map.png")
        self.tool_bar = edit_tool_bar()
        self.cycle_tool = {1:self.tool_bar.home,2:self.tool_bar.save,3:self.tool_bar.select,4:self.tool_bar.ground}
        self.cycle_idx = 3
        with open(self.dir+'/box.json') as json_file:
            self.data = json.load(json_file)
        self.K_home = False
        self.K_left = False
        self.K_right = False
        self.K_up = False
        self.K_down = False
        self.K_lctrl = False
        self.in_edition = False
        self.active_line = None
        #Add Objet to list
        self.list_sprite.append(self.background)
        for ground in self.data.get("ground"):
            temp_ground=Line(ground.get("x"),ground.get("y"), ground.get("color"), ground.get("size_x"), ground.get("size_y"))
            self.list_sprite.append(temp_ground)
            self.all_line.append(temp_ground)
            print("ok")
        #Add Objet to group
        for sprite in self.list_sprite:
            self.group_sprite.add(sprite)

    def update(self):
        self.group_sprite.update()

    def event(self,all_events=[]):
        if all_events==[]:
            if self.K_home:
                if not self.cycle_tool[self.cycle_idx] in self.group_sprite:
                    self.group_sprite.add(self.cycle_tool[self.cycle_idx])
                if self.K_left:
                    self.K_left=False
                    self.group_sprite.remove(self.cycle_tool[self.cycle_idx])
                    if self.cycle_idx == len(self.cycle_tool):
                        self.cycle_idx = 1
                    else:
                        self.cycle_idx +=1
                    self.group_sprite.add(self.cycle_tool[self.cycle_idx])
            else:
                if  self.cycle_tool[self.cycle_idx] in self.group_sprite:
                    self.group_sprite.remove(self.cycle_tool[self.cycle_idx])

            if self.in_edition and not self.active_line==None:
                if self.K_left:
                    if self.K_lctrl:
                        if self.active_line.size_x>1:
                            self.active_line.size_x-=1
                            self.active_line.image=pygame.Surface((self.active_line.size_x,self.active_line.size_y))
                            self.active_line.image.fill(pygame.Color(self.active_line.color))
                    else:
                        self.active_line.rect.x-=1
                if self.K_right:
                    if self.K_lctrl:
                        self.active_line.size_x+=1
                        self.active_line.image=pygame.Surface((self.active_line.size_x,self.active_line.size_y))
                        self.active_line.image.fill(pygame.Color(self.active_line.color))
                    else:
                        self.active_line.rect.x+=1
                if self.K_up:
                    if self.K_lctrl:
                        if self.active_line.size_y>1:
                            self.active_line.size_y-=1
                            self.active_line.image=pygame.Surface((self.active_line.size_x,self.active_line.size_y))
                            self.active_line.image.fill(pygame.Color(self.active_line.color))
                    else:
                        self.active_line.rect.y-=1
                if self.K_down:
                    if self.K_lctrl:
                        self.active_line.size_y+=1
                        self.active_line.image=pygame.Surface((self.active_line.size_x,self.active_line.size_y))
                        self.active_line.image.fill(pygame.Color(self.active_line.color))
                    else:
                        self.active_line.rect.y+=1


            return 0
        else:
            for event in all_events:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_HOME:
                        self.K_home = True
                        self.in_edition=False
                    if event.key == pygame.K_LEFT:
                        self.K_left = True
                    if event.key == pygame.K_RIGHT:
                        self.K_right = True
                    if event.key == pygame.K_LCTRL:
                        self.K_lctrl = True
                    if event.key == pygame.K_UP:
                        self.K_up = True
                    if event.key == pygame.K_DOWN:
                        self.K_down = True
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_HOME:
                        self.K_home = False
                        if self.cycle_idx == 2:
                            self.data={"ground":[],"no_ground":[]}
                            for line in self.all_line:
                                self.data["ground"].append(line.get_json())
                                self.data["no_ground"].append(Line(line.rect.x,line.rect.y+1,"green",1,line.size_y-1).get_json())
                                self.data["no_ground"].append(Line(line.rect.x+line.size_x,line.rect.y+1,"green",1,line.size_y-1).get_json())
                            with open(self.dir+'/box.json', "w") as json_file:
                                json.dump(self.data, json_file, ensure_ascii=False)
                        elif self.cycle_idx == 1:
                            return 1
                            
                        if self.cycle_idx == 4:
                            self.in_edition = True
                        else:
                            self.in_edition = False
                    if event.key == pygame.K_LEFT:
                        self.K_left = False
                    if event.key == pygame.K_RIGHT:
                        self.K_right = False
                    if event.key == pygame.K_LCTRL:
                        self.K_lctrl = False
                    if event.key == pygame.K_UP:
                        self.K_up = False
                    if event.key == pygame.K_DOWN:
                        self.K_down = False
                    if event.key == pygame.K_DELETE:
                        if self.cycle_idx == 3 or self.cycle_idx == 4:
                            if self.active_line!=None:
                                self.all_line.remove(self.active_line)
                                self.group_sprite.remove(self.active_line)
                                self.active_line.kill()
                                self.active_line=None
                    if event.key == pygame.K_ESCAPE:
                        if self.cycle_idx == 3:
                            if self.active_line!=None:
                                self.active_line.rect.x = self.active_line_x
                                self.active_line.rect.y = self.active_line_y
                                self.active_line = None
                                self.in_edition = False


                if event.type == pygame.MOUSEMOTION:
                    if self.in_edition and not self.active_line==None:
                        self.active_line.rect.center = pygame.mouse.get_pos()
                if event.type == pygame.MOUSEBUTTONUP:
                    if self.cycle_idx == 4:
                        if self.in_edition:
                            if self.active_line!=None:
                                self.active_line=None
                            else:
                                self.active_line=Line(0,0,"Red",100,10)
                                self.all_line.append(self.active_line)
                                self.group_sprite.add(self.active_line)
                    elif self.cycle_idx == 3:
                            for sprite in self.all_line:
                                if sprite.rect.collidepoint(pygame.mouse.get_pos()):
                                    if self.active_line  != None:
                                        self.active_line = None
                                        self.in_edition = False
                                    else:
                                        self.active_line = sprite
                                        self.in_edition = True
                                        self.active_line_x, self.active_line_y = self.active_line.rect.x , self.active_line.rect.y

                            

            self.event([])
            
    def kill(self):
        for sprite in self.group_sprite:
            sprite.kill()

class edit_tool_bar:
    def __init__(self):
        #Init list & group
        self.group_sprite = pygame.sprite.Group()
        self.list_sprite=[]
        #Init Object
        self.image_cote =100
        self.home = Image(10,10,"Image/Home Square Button.png")
        self.home.image = pygame.transform.scale(self.home.image, (self.image_cote,self.image_cote))
        self.save = Image(10,10,"Image/save.png")
        self.save.image = pygame.transform.scale(self.save.image, (self.image_cote,self.image_cote))
        self.ground = Image(10,10,"Image/ground.png")
        self.ground.image = pygame.transform.scale(self.ground.image, (self.image_cote,self.image_cote))
        self.select = Image(10,10,"Image/select.png")
        self.select.image = pygame.transform.scale(self.select.image, (self.image_cote,self.image_cote))
        #Add Objet to list
        #self.list_sprite.append(self.home)
        #self.list_sprite.append(self.save)
        #self.list_sprite.append(self.ground)
        #self.list_sprite.append(self.select)
        #Add Objet to group
        for sprite in self.list_sprite:
            self.group_sprite.add(sprite)
