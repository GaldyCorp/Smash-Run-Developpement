import pygame

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
