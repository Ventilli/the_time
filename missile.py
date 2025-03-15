import pygame  # импорт основного модуля

class Missile(pygame.sprite.Sprite):
    ticks_per_second = 60

    def __init__(self, filename, x, y, speed, rotate_speed, tox, toy, group, size = 100):
        # tox -= size
        # toy -= size

        pygame.sprite.Sprite.__init__(self)

        self.original_image = pygame.image.load(filename).convert_alpha()

        self.original_image = pygame.transform.scale(self.original_image, (size, size))
        self.image = self.original_image.copy()
        self.rect = self.image.get_rect(center = (x, y))

        self.timer = 5

        self.rotate_speed = rotate_speed
        self.rotate = -rotate_speed
        self.speed = speed
        self.x_difference = tox - x
        self.y_difference = toy - y
        self.x_to = tox
        self.y_to = toy
        self.add(group)
    
    def update(self, tps = ticks_per_second):
        self.image = pygame.transform.rotate(self.original_image, self.rotate)
        self.rotate -= self.rotate_speed

        self.rect.centerx += self.x_difference / self.speed / tps
        self.rect.centery += self.y_difference / self.speed / tps

        self.timer -= 1 / tps

        if self.timer <= 0:
            self.kill()

    def set_tps(tps_custom):
        global ticks_per_second

        ticks_per_second = tps_custom

    def get_tps():
        return ticks_per_second