from random import *
from re import X
import pygame
import json
from smrun_lib import * 
vec = pygame.math.Vector2


#GUI part
pygame.init()
COLOR_INACTIVE = pygame.Color('lightskyblue3')
COLOR_ACTIVE = pygame.Color('dodgerblue2')
COLOR_TEXT = pygame.Color('floralwhite')
FONT = pygame.font.Font(None, 32)
COLOR_WALL = pygame.Color('lightskyblue3')
COLOR_GROUND = pygame.Color('aquamarine4')
PLAYER_ACC = 1
PLAYER_FRICTION = -0.12
AIR_FRICTION = -0.05

class player(pygame.sprite.Sprite):
    def __init__(self,x,y,color):
        pygame.sprite.Sprite.__init__(self)
        self.size_x = 30
        self.size_y = 30
        self.image = pygame.Surface((self.size_x,self.size_y))
        self.image.fill(pygame.Color(color))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.garvity = 0.8
        self.pos = vec(x,y)
        self.vel = vec(0,0)
        self.acc = vec(0,0) 
        self.jump_count=0      
        self.is_jump=False
        self.is_fall=True
        self.climb=False
        self.key_left=False
        self.key_right=False
        self.key_up=False
        self.key_down=False
        self.key_jump=False

    def is_touching(self, obj):
        return len(pygame.sprite.spritecollide(self, obj, False))>0

    def jump(self):
        self.vel.y = -15

    def fall(self):
        None


class game:
    def __init__(self):
        self.group_sprite = pygame.sprite.Group()
        self.group_ground = pygame.sprite.Group()
        self.group_no_ground = pygame.sprite.Group()
        self.group_left = pygame.sprite.Group()
        self.group_right = pygame.sprite.Group()
        self.list_sprite=[]

        with open('Image/Map/City4/box.json') as json_file:
            data = json.load(json_file) 

        for ground in data.get("ground"):
            temp_ground=Line(ground.get("x"),ground.get("y"), ground.get("color"), ground.get("size_x"), ground.get("size_y"))
            
            temp_left=Line(temp_ground.rect.x,temp_ground.rect.y+1,"green",1,temp_ground.size_y-2)
            self.group_left.add(temp_left)
            
            temp_right=Line(temp_ground.rect.x+temp_ground.size_x-1,temp_ground.rect.y+1,"green",1,temp_ground.size_y-2)
            self.group_right.add(temp_right)
            
            temp_no_ground=Line(temp_ground.rect.x,temp_ground.rect.y+temp_ground.size_y,"black",temp_ground.size_x,1)
            self.group_no_ground.add(temp_no_ground)

            self.group_ground.add(temp_ground)
            self.list_sprite+=[temp_left]+[temp_right]+[temp_no_ground]+[temp_ground]
            

        self.Player1 = player(100,300,"white")
        self.Player2 = player(100,300,"blue")
        self.all_players = [self.Player1, self.Player2]

        self.list_sprite.append(self.Player1)
        self.list_sprite.append(self.Player2)
        for sprite in self.list_sprite:
            self.group_sprite.add(sprite)
 
    def event(self,all_events=None):
        if all_events==None:
            for player in self.all_players:
                player.acc = vec(0,player.garvity)
                if player.is_touching(self.group_ground) or player.is_jump or player.is_fall:
                    player.is_fall=False

                    if player.key_left and not player.is_touching(self.group_right):
                        player.acc.x = -PLAYER_ACC

                    if player.key_right and not player.is_touching(self.group_left):
                        player.acc.x = PLAYER_ACC

                if player.vel.y < 0:
                    self.hits = pygame.sprite.spritecollide(player, self.group_no_ground, False)
                    if self.hits:
                        player.pos.y = self.hits[0].rect.bottom+(player.size_x//2)+20
                        player.vel.y = 0
                        player.acc.y = 0
                        

                if player.vel.y > 0: #si tombe
                    player.is_jump=False
                    player.is_fall=True
                    self.hits = pygame.sprite.spritecollide(player, self.group_ground, False)
                    self.hits_no_ground = pygame.sprite.spritecollide(player, self.group_ground, False)
                    if self.hits:
                        player.pos.y = self.hits[0].rect.top 
                        player.vel.y = 0
                        player.jump_count=0
                    
                
                if player.key_jump and player.jump_count<2:
                    player.key_jump = False
                    if player.is_touching(self.group_ground):
                        player.is_jump=True
                        player.jump()
                        player.jump_count+=1
                    else:
                        if player.jump_count==0:
                            player.jump_count=2
                            player.is_jump=True
                            player.jump()
                        else:
                            player.is_jump=True
                            player.jump()
                            player.jump_count+=1
                        

                if player.vel.x < 0:
                    self.hits = pygame.sprite.spritecollide(player, self.group_right, False)
                    if self.hits:
                        player.pos.x = self.hits[0].rect.right+(player.size_x//2)-1                            
                        player.vel.x = 0
                        player.acc.x = 0

                if player.vel.x > 0: 
                        self.hits = pygame.sprite.spritecollide(player, self.group_left, False)
                        if self.hits:
                            player.pos.x = self.hits[0].rect.left-(player.size_x//2)+1
                            player.vel.x = 0
                            player.acc.x = 0

                player.acc.x += player.vel.x * PLAYER_FRICTION
                player.vel += player.acc
                player.pos += player.vel + 0.5 * player.acc
                player.rect.midbottom = player.pos

        else:
            for event in all_events:
                if event.type == pygame.KEYDOWN:
                    #Player1
                    if event.key == pygame.K_LEFT:
                        self.Player1.key_left = True
                    if event.key == pygame.K_RIGHT:
                        self.Player1.key_right = True
                    if event.key == pygame.K_UP:
                        self.Player1.key_up = True
                    if event.key == pygame.K_DOWN:
                        self.Player1.key_down = True
                    if event.key == pygame.K_RCTRL:
                        self.Player1.key_jump = True

                    #Player2
                    if event.key == pygame.K_q:
                        self.Player2.key_left = True
                    if event.key == pygame.K_d:
                        self.Player2.key_right = True
                    if event.key == pygame.K_z:
                        self.Player2.key_up = True
                    if event.key == pygame.K_s:
                        self.Player2.key_down = True
                    if event.key == pygame.K_SPACE:
                        self.Player2.key_jump = True

                if event.type == pygame.KEYUP:
                    #Player1
                    if event.key == pygame.K_LEFT:
                        self.Player1.key_left = False   
                    if event.key == pygame.K_RIGHT:
                        self.Player1.key_right = False 
                    if event.key == pygame.K_UP:
                        self.Player1.key_up = False
                    if event.key == pygame.K_DOWN:
                        self.Player1.key_down = False
                    if event.key == pygame.K_RCTRL:
                        self.Player1.key_jump = False
                    
                    #Player2
                    if event.key == pygame.K_q:
                        self.Player2.key_left = False
                    if event.key == pygame.K_d:
                        self.Player2.key_right = False
                    if event.key == pygame.K_z:
                        self.Player2.key_up = False
                    if event.key == pygame.K_s:
                        self.Player2.key_down = False
                    if event.key == pygame.K_SPACE:
                        self.Player2.key_jump = False
                    
            self.event()

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


test_mode=True
if __name__ == '__main__':
    if test_mode:
        root=main_window()
        root.run()
    else:
        try:
            root=main_window()
            root.run()
        except:
            None

