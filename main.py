from random import *
from re import X
import pygame
import json
import pyperclip
vec = pygame.math.Vector2


#GUI part
pygame.init()
COLOR_INACTIVE = pygame.Color('lightskyblue3')
COLOR_ACTIVE = pygame.Color('dodgerblue2')
COLOR_TEXT = pygame.Color('floralwhite')
FONT = pygame.font.Font(None, 32)
COLOR_WALL = pygame.Color('lightskyblue3')
COLOR_GROUND = pygame.Color('aquamarine4')
PLAYER_ACC = 2
PLAYER_FRICTION = -0.12
AIR_FRICTION = -0.05

class Line(pygame.sprite.Sprite):
    def __init__(self,x,y,color,size_x,size_y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((size_x,size_y))
        self.image.fill(pygame.Color(color))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.size_x = size_x
        self.size_y = size_y

class player(pygame.sprite.Sprite):
    def __init__(self,x,y,scale):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("Image/player2.gif")
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.garvity = 0.8
        self.pos = vec(x,y)
        self.vel = vec(0,0)
        self.acc = vec(0,0)
        self.scale=scale
        self.image_size=self.image.get_size()
        self.image = pygame.transform.scale(self.image, (self.image_size[0]//self.scale, self.image_size[1]//self.scale))
        self.is_jump=False
        self.is_fall=True
        self.climb=False

    

    def jump(self):
        self.vel.y = -20

    def fall(self):
        None


    def change_image(self,ref):
        self.ref=ref
        self.image = pygame.image.load(f"Image/{self.ref}.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.image.get_size()[0]//self.scale, self.image.get_size()[1]//self.scale))

class game:
    def __init__(self):
        self.group_sprite = pygame.sprite.Group()
        self.group_ground = pygame.sprite.Group()
        self.list_sprite=[]

        with open('Image/Map/City4/box.json') as json_file:
            data = json.load(json_file) 

        for ground in data.get("ground"):
            temp_ground=Line(ground.get("x"),ground.get("y"), ground.get("color"), ground.get("size_x"), ground.get("size_y"))
            self.group_ground.add(temp_ground)
            self.list_sprite.append(temp_ground)

        self.Player1 = player(100,300,1)
        self.key_left=False
        self.key_right=False
        self.key_up=False
        self.key_down=False
        self.list_sprite.append(self.Player1)
        for sprite in self.list_sprite:
            self.group_sprite.add(sprite)
    
    def is_touching_ground(self):
        return len(pygame.sprite.spritecollide(self.Player1, self.group_ground, False))>0
 
    def event(self,all_events=None):
        if all_events==None:
            self.Player1.acc = vec(0,self.Player1.garvity)
            if self.is_touching_ground() or self.Player1.is_jump or self.Player1.is_fall:
                self.Player1.is_fall=False
                if self.key_left and self.Player1.rect.x>=10:
                    self.Player1.acc.x = -PLAYER_ACC
                if self.key_right and self.Player1.rect.x<=1820:
                    self.Player1.acc.x = PLAYER_ACC

            if self.is_touching_ground() and not self.Player1.is_jump and not self.Player1.is_fall:
                if self.key_down:
                    self.Player1.acc.x = self.Player1.acc.x*2

            if self.Player1.vel.y > 0: #si tombe
                self.Player1.is_jump=False
                self.Player1.is_fall=True
                self.hits = pygame.sprite.spritecollide(self.Player1, self.group_ground, False)
                if self.hits:
                    self.Player1.pos.y = self.hits[0].rect.top
                    self.Player1.vel.y = 0

            if self.key_up and self.is_touching_ground():
                self.Player1.is_jump=True
                self.Player1.jump()

            self.Player1.acc.x += self.Player1.vel.x * PLAYER_FRICTION
            self.Player1.vel += self.Player1.acc
            self.Player1.pos += self.Player1.vel + 0.5 * self.Player1.acc
            self.Player1.rect.midbottom = self.Player1.pos

        else:
            for event in all_events:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.key_left = True
                    if event.key == pygame.K_RIGHT:
                        self.key_right = True
                    if event.key == pygame.K_UP:
                        self.key_up = True
                    if event.key == pygame.K_DOWN:
                        self.key_down = True
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        self.key_left = False   
                    if event.key == pygame.K_RIGHT:
                        self.key_right = False 
                    if event.key == pygame.K_UP:
                        self.key_up = False
                    if event.key == pygame.K_DOWN:
                        self.key_down = False
                    
            self.event()

class text():
    def __init__(self, x, y, w, h, info, data):
        self.group_sprite = pygame.sprite.Group()
        self.list_sprite=[]
        self.FONT = pygame.font.Font(None, 32)
        self.rect = pygame.Rect(x, y, w, h)
        self.color_text = COLOR_TEXT
        self.color = COLOR_TEXT
        self.data = data
        self.text = info
        self.active = False
        self.txt_surface = FONT.render(self.text, True, self.color)
        for sprite in self.list_sprite:
            self.group_sprite.add(sprite)
        
    def handle_event(self):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            # Toggle the active variable.
            self.active = True
            self.color = COLOR_ACTIVE
        else:
            self.active = False
            # Change the current color of the input box.
            self.color = COLOR_TEXT

    def set_text(self,new_text):
        self.text=new_text
        self.txt_surface = FONT.render(self.text, True, self.color)

    def draw(self, screen):
        # Blit the text.
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        # Blit the rect.
        pygame.draw.rect(screen, self.color, self.rect, 2)
    
    def kill(self):
        for sprite in self.list_sprite:
            sprite.kill()

class InputBox:
    
    def __init__(self, x, y, w, h, min_char=0 ,max_char=None,text='',titre='',show_valide=False):
        self.group_sprite = pygame.sprite.Group()
        self.list_sprite=[]
        self.FONT = pygame.font.Font(None, 32)
        self.rect = pygame.Rect(x, y, w, h)
        self.color = COLOR_INACTIVE
        self.text_color = COLOR_TEXT
        self.text = text
        self.show_valid=show_valide
        self.min_char=min_char
        self.max_char=max_char
        self.txt_surface = FONT.render(text, True, self.color)
        self.txt_pseudo_surface = FONT.render(titre, True, self.text_color)
        self.active = False
        if self.show_valid:
            #self.valide_bouton=menu_bouton("Menu/V Square Button",625,220,4)
            #self.list_sprite.append(self.valide_bouton)
            None
        for sprite in self.list_sprite:
            self.group_sprite.add(sprite)
        
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONUP:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = not self.active
            else:
                self.active = False
            # Change the current color of the input box.
            self.color = COLOR_ACTIVE if self.active else COLOR_INACTIVE
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    if event.key == pygame.K_v and pygame.key.get_mods() & pygame.KMOD_CTRL:
                        self.text = str(pyperclip.paste())
                    elif self.max_char==None:
                        self.text += event.unicode
                    elif len(self.text)<self.max_char:
                        self.text += event.unicode
                # Re-render the text.
                self.txt_surface = FONT.render(self.text, True, self.color)
        if self.max_char==None:
            self.update()

    def update(self):
        # Resize the box if the text is too long.
        width = max(200, self.txt_surface.get_width()+10)
        self.rect.w = width

    def draw(self, screen):
        # Blit the text.
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        screen.blit(self.txt_pseudo_surface, (self.rect.x+25, self.rect.y-50))
        
        # Blit the rect.
        pygame.draw.rect(screen, self.color, self.rect, 2)
    
    def kill(self):
        for sprite in self.list_sprite:
            sprite.kill()

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
    
    def update(self):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            if self.image.get_size()[0] <= 325:
                None
                #self.image = pygame.transform.scale(self.image, (self.image_size[0]//2, self.image_size[1]//2))
        else:
            if self.image.get_size()[0] >= 300:
                None
                #self.image = pygame.transform.scale(self.image, (self.image_size[0]//3, self.image_size[1]//3))
        self.rect = self.image.get_rect(center = self.rect.center)

    def change_image(self,ref):
        self.ref=ref
        self.image = pygame.image.load(f"Image/{self.ref}.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.image.get_size()[0]//self.scale, self.image.get_size()[1]//self.scale))

class main_menu(pygame.sprite.Sprite):
    def __init__(self,music_etat):
        super().__init__()
        self.group_main_menu = pygame.sprite.Group()
        self.list_sprite=[]
        self.play=menu_bouton("Menu/Play Button",350,200,3)
        self.exit=menu_bouton("Menu/Exit Button",350,400,3)
        self.border_ico=menu_bouton("border",1140,0,2)
        if music_etat:
            self.music=menu_bouton("Menu/Music Square Button On",1200,550,3)
        else:
            self.music=menu_bouton("Menu/Music Square Button Off",1200,550,3)
        self.list_sprite.append(self.play)
        self.list_sprite.append(self.exit)
        self.list_sprite.append(self.music)
        self.ico=None
        for sprite in self.list_sprite:
            self.group_main_menu.add(sprite)

    def set_music_Off(self):
        self.music.change_image("Menu/Music Square Button Off")

    def set_music_On(self):
        self.music.change_image("Menu/Music Square Button On")

    def update(self):
        self.group_main_menu.update()

    def kill(self):
        for sprite in self.list_sprite:
            sprite.kill()

class main_window:
    def __init__(self):
        # PARAMETER
        pygame.display.set_caption("Smash Run")
        self.screen = pygame.display.set_mode((1365, 710), pygame.RESIZABLE) #pygame.FULLSCREEN
        self.clock = pygame.time.Clock()

        #Network

        # GROUPS
        self.all_sprites = pygame.sprite.Group()
        #self.menu_sprites = pygame.sprite.Group()

        # RUNNING
        self.is_running=True
        self.game_is_running=True
        self.music_On=False

        # OBJECTS
        self.background = pygame.image.load("Image\Map\City4\map.png")
        self.call_game()
        

    def run(self):
        '''GameLoop'''
        while self.is_running:
            self.clock.tick(60)
            self.events()
            self.update()
            self.draw()

    def update(self):
        self.all_sprites.update()

    def call_game(self):
        self.game = game()
        self.all_sprites.add(self.game.group_sprite)
        if self.music_On:
            pygame.mixer.music.load('Audio/Menu Theme.mp3')
            pygame.mixer.music.set_volume(0.5)
            pygame.mixer.music.play(-1, 0.0)
        else:
            None
            #pygame.mixer.music.play(-1, 0.0)
            #pygame.mixer.music.pause()

    
    def events(self):
        
        all_events = pygame.event.get()
        if all_events==[]:
            if self.game_is_running:
                self.game.event()
        else:

            if self.game_is_running:
                self.game.event(all_events)

            for event in all_events:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.screen = pygame.display.set_mode((1365, 710), pygame.RESIZABLE)
                    elif event.key == pygame.K_F11:
                        self.screen = pygame.display.set_mode((1920, 1080))
                        self.screen = pygame.display.set_mode((1920, 1080),pygame.FULLSCREEN)

                if event.type == pygame.VIDEORESIZE:
                    None
                    #self.screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)

                if event.type == pygame.QUIT:
                    pygame.quit()

    def draw(self):
        self.screen.blit(self.background, (0,0)) # Dessine le backgound
        self.all_sprites.draw(self.screen) # actualise les sprites
        pygame.display.flip()

if __name__ == '__main__':
    root=main_window()
    #root.call_game()
    root.run()

