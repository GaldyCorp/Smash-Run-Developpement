import pygame
import json
from tkinter import filedialog
pygame.init()


class Line(pygame.sprite.Sprite):
    def __init__(self,x,y,color,size_x,size_y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((size_x,size_y))
        self.image.fill(pygame.Color(color))
        self.color = color
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.size_x = size_x
        self.size_y = size_y

    def get_json(self):
        return {"x":self.rect.x,"y":self.rect.y,"color":self.color,"size_x":self.size_x,"size_y":self.size_y}

class menu_bouton(pygame.sprite.Sprite):
    def __init__(self,ref,x,y,scale):
        pygame.sprite.Sprite.__init__(self)
        self.ref = ref
        if not type(self.ref)==type(''):
            self.image = ref
        else:
            self.image = pygame.image.load(f"Image/{self.ref}.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.scale=scale
        self.image_size=self.image.get_size()
        self.image = pygame.transform.scale(self.image, (self.image_size[0]//self.scale, self.image_size[1]//self.scale))

    def change_image(self,ref):
        self.ref=ref
        self.image = pygame.image.load(f"Image/{self.ref}.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.image.get_size()[0]//self.scale, self.image.get_size()[1]//self.scale))

class Image(pygame.sprite.Sprite):
    def __init__(self,x,y,ref):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(ref)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

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
        self.cycle_idx = 1
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


            return [0]
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
                            self.data={"ground":[]}
                            for line in self.all_line:
                                self.data["ground"].append(line.get_json())
                            with open(self.dir+'/box.json', "w") as json_file:
                                json.dump(self.data, json_file, ensure_ascii=False)
                            
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
                                None
                        except:
                            self.directory=None
            return self.event()

    def kill(self):
        for sprite in self.group_sprite:
            sprite.kill()

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
