import pygame

class Laser(pygame.sprite.Sprite):
    '''
    Класс для создания лазеров на весь экран в модуле pygame

    Атрибуты:
    plane (str): x or y
    '''

    ticks_per_second = 60

    def __init__(self, plane:str, pos, timer, group, width = 50):
        pygame.sprite.Sprite.__init__(self)

        self.activate = 0
        self.timer = timer
        self.pre_timer = 2
        self.width = width
        self.type = plane
        self.pos = pos
        self.width = width

        # if self.activate == 0:
        if plane == 'y':
            self.image = pygame.Surface((100000, width))
            self.image.fill((255, 155, 155))
            self.rect = self.image.get_rect(center = (0, pos))
        if plane == 'x':
            self.image = pygame.Surface((width, width * 100))
            self.image.fill((255, 155, 155))
            self.rect = self.image.get_rect(center = (pos, 0))

        self.add(group)

    def update(self, tps = ticks_per_second):
        if self.pre_timer > 0:
            self.pre_timer -= 1 / tps
            self.__decrease()
            return 'initialization'
        else:
            self.image.fill((255, 0, 0))
            self.activate = 1
            self.timer -= 1 / tps

        if self.timer <= 0:
            self.kill()

    def __decrease(self, tps = ticks_per_second):
        self.image = pygame.Surface((100000, self.width))
        self.image.fill((255, 155, 155))

        # decrease = self.width // tps * 2
        # self.width -= decrease

        # if self.activate == 0:
        #     if self.type == 'y':
        #         self.image = pygame.Surface((100000, self.width))
        #         self.image.fill((255, 155, 155))
        #         self.rect = self.image.get_rect(center = (0, self.pos))
        #     if self.type == 'x':
        #         self.image = pygame.Surface((self.width, self.width * 100))
        #         self.image.fill((255, 155, 155))
        #         self.rect = self.image.get_rect(center = (self.pos, 0))
        
        if self.activate == 1:
            if self.type == 'y':
                self.image = pygame.Surface((100000, self.width))
                self.image.fill((255, 0, 0))
                self.rect = self.image.get_rect(center = (0, self.pos))
            if self.type == 'x':
                self.image = pygame.Surface((self.width, self.width * 100))
                self.image.fill((255, 0, 0))
                self.rect = self.image.get_rect(center = (self.pos, 0))

    def get_active(self):
        return self.activate

    def set_tps(tps_custom):
        global ticks_per_second

        ticks_per_second = tps_custom

    def get_tps():
        return ticks_per_second