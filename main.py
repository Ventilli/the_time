from turtle import width, window_width
import pygame  # импорт основного модуля
from missile import *
from laser import *
from random import randint


pygame.init()  # импорт других необходимых расширений

MUSIC_END_EVENT = pygame.event.custom_type()
ENEMY_MISSILE_EVENT = pygame.event.custom_type()
ENEMY_SUPERMISSILE_EVENT = pygame.event.custom_type()
ENEMY_LASER_EVENT = pygame.event.custom_type()
ENEMY_SIDE_EVENT = pygame.event.custom_type()

pygame.mixer.music.set_endevent(MUSIC_END_EVENT)

pygame.time.set_timer(ENEMY_SUPERMISSILE_EVENT, 7000)
pygame.time.set_timer(ENEMY_LASER_EVENT, 5000)
pygame.time.set_timer(ENEMY_MISSILE_EVENT, 700)
pygame.time.set_timer(ENEMY_SIDE_EVENT, 100)

# screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
screen = pygame.display.set_mode((0, 0))
pygame.display.set_caption("Само время")

WIDTH = screen.get_width()
HEIGHT = screen.get_height()
WHITE = (255, 255, 255)
GRAY = (100, 100, 100)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
PURPLE = (183, 98, 228)
YELLOW = (255, 189, 100)

DEV_MODE = 1
MODE = 1        #1 - легкий, 2 - средний, 3 - сложный, 4+ - оченб сложный и больше
FPS = 60
tps = 60
clock = pygame.time.Clock()

star_damage = 100 // MODE
star_hp = 100 // MODE
boss_damage = 5 * MODE
boss_hp = 5000 * MODE
boss_y = -100
boss_is_motion = 0
side_atacks = 0
atacking = 1
boss_shield = 0
missiles_num = 0

rotate_speed = 1
rotate_speed_boss = 3
speed = tps // 12

x_s = WIDTH // 2
y_s = HEIGHT // 2

sprint_time = 2 * tps
sprint_timer = sprint_time
sprint_power = 250

if DEV_MODE == 1:
    sprint_time = 3
    sprint_timer = sprint_time
    star_hp = 100000



# ФУНКЦИИ

def create_laser():
    o = randint(0, 1)

    if o == 0:
        Laser('x', star_rect.centerx, 2, lasers_group, 25)
    if o == 1:
        Laser('y', star_rect.centery, 2, lasers_group, 25)

def create_missile(input, custom_x = WIDTH / 2, custom_y = 0):
    '''
    input (str): star_missile / time_missile / tick_tack_missile
    '''
    if input == 'star_missile':
        filename = 'final_project\sprites\sharovayamolnia.png'
        x = star_rect.centerx
        y = star_rect.centery
        spd = 1
        rotate_spd = 1
        x_to = pygame.mouse.get_pos()[0]
        y_to = pygame.mouse.get_pos()[1]
        size = 50
        group = missiles_group

        missile_live.play(1, 900)

    if input == 'tick_tack_missile':
        filename = 'final_project/sprites/tick_tack.png'
        x = custom_x
        y = custom_y
        spd = 1.3
        rotate_spd = 3
        x_to = star_rect.centerx
        y_to = star_rect.centery
        size = 250
        group = enemy_missiles_group

        tick_sound.play(1, 5000)

    if input == 'time_missile':
        filename = 'final_project/sprites/boss_missile.png'
        x = custom_x
        y = custom_y
        spd = 0.8
        rotate_spd = 1
        x_to = star_rect.centerx
        y_to = star_rect.centery
        size = 100
        group = enemy_missiles_group

    Missile(filename, x, y, spd, rotate_spd, x_to, y_to, group, size)

def colide_enemy_missiles():
    global star_hp

    for missile in enemy_missiles_group:
        if star_rect.colliderect(missile):
            missile.kill()
            star_hp -= boss_damage
    
    # print(star_hp)

def colide_missiles():
    global boss_hp

    for missile in missiles_group:
        bottom_g = (the_time_rect.bottom - the_time_rect.centery) / 2
        bottom_g += the_time_rect.centery
        top_g = (the_time_rect.top + the_time_rect.centery) / 2
        # top_g -= the_time_rect.centery

        if the_time_rect.collidepoint(missile.rect.center) and top_g < missile.rect.centery < bottom_g:
            missile.kill()
            boss_hp -= star_damage

def colide_lasers():
    global star_hp

    for laser in lasers_group:
        if star_rect.colliderect(laser) and laser.get_active() == 1:
            laser.kill()
            star_hp -= boss_damage * 3
    
def death():
    if star_hp <= 0:
        exit()
    if boss_hp <= 0:
        exit()


def boss_atacks(num, repeat = 1):
    global side_atacks, boss_is_motion, boss_y, atacking

    while repeat != 0:
        if num == 0:
            create_missile("time_missile")

        elif num == 1:
            create_missile('tick_tack_missile')

        elif num == 3:
            boss_is_motion = 1
            if boss_y < HEIGHT // 2:
                boss_y = HEIGHT + 100
            elif boss_y > HEIGHT // 2:
                boss_y = -100

            atacking = 0

        elif num == 4:
            side_atacks = 20

        else:
            create_laser()
        repeat -= 1
        
        colide_enemy_missiles()


# . . . код . . .

pygame.mixer.music.load('final_project\music\DETSTVO.ogg')
# pygame.mixer.music.play(-1)

missile_live = pygame.mixer.Sound('final_project\sounds\missile_sound.ogg')
missile_live.set_volume(0.1)
tick_sound = pygame.mixer.Sound('final_project/sounds/tickings.ogg')
tick_sound.set_volume(1.5)

star_o = pygame.image.load("final_project\sprites\hero.png").convert_alpha()
star_o = pygame.transform.scale(star_o, (40, 40))
star = star_o.copy()
star_rect = star.get_rect(center=(WIDTH / 2, HEIGHT // 2))

the_time_o = pygame.image.load('final_project\sprites\BOSS.png')
the_time_o = pygame.transform.scale(the_time_o, (700, 700))
the_time = the_time_o.copy()
the_time_rect = the_time.get_rect(center=(WIDTH // 2, -100))
boss_y = the_time_rect.centery

missiles_group = pygame.sprite.Group()
enemy_missiles_group = pygame.sprite.Group()
lasers_group = pygame.sprite.Group()

while True:
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            exit()
        
        keys = pygame.key.get_pressed()
        
        if side_atacks == 0 and atacking == 1:
            if event.type == ENEMY_MISSILE_EVENT:
                if missiles_num % 10 == 9:
                    boss_atacks(1)
                else:
                    boss_atacks(0, 3)
                missiles_num += 1
            if event.type == ENEMY_LASER_EVENT:
                boss_atacks(110)

        if event.type == ENEMY_SIDE_EVENT and side_atacks > 0:
            create_missile('time_missile', 0, HEIGHT // 2)
            create_missile('time_missile', WIDTH, HEIGHT // 2)
            side_atacks -= 1


        #Звезда

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3 and sprint_timer == sprint_time:
            if keys[pygame.K_w] and 0 < y_s - sprint_power:
                y_s -= sprint_power
            if keys[pygame.K_a] and 0 < x_s - sprint_power:
                x_s -= sprint_power
            if keys[pygame.K_s] and y_s + sprint_power < HEIGHT:
                y_s += sprint_power
            if keys[pygame.K_d] and x_s + sprint_power < WIDTH:
                x_s += sprint_power
            sprint_timer = 0

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # print(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1], star_rect[0], star_rect[1])
            create_missile('star_missile')
            # boss_atacks(0)
            # boss_atacks(1)
            # boss_atacks(3)

        # Режим разработчика
        if DEV_MODE == 1:
            if event.type == pygame.MOUSEWHEEL:
                create_missile('time_missile')
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 2:
                create_missile('tick_tack_missile')
            if keys[pygame.K_q]:
                boss_atacks(3)
            if keys[pygame.K_e]:
                boss_atacks(4)

    
    keys = pygame.key.get_pressed()

    # Звезда

    if keys[pygame.K_w] and 0 < y_s - speed:
        y_s -= speed
    if keys[pygame.K_a] and 0 < x_s - speed:
        x_s -= speed
    if keys[pygame.K_s] and y_s + speed < HEIGHT:
        y_s += speed
    if keys[pygame.K_d] and x_s + speed < WIDTH:
        x_s += speed
    
    if DEV_MODE == 1:
        font = pygame.font.SysFont(None, WIDTH // 30)
        text = font.render("Включен режим разработчика", 1, WHITE)
        text_rect = text.get_rect(center=(WIDTH // 5, 50))

        if keys[pygame.K_m] and DEV_MODE == 1:
            pygame.mixer.music.stop()


    # Закадровая белибердень

    if sprint_timer < sprint_time:
        sprint_timer += 1
        # print(sprint_time, sprint_timer)
    if boss_is_motion == 1:
        if boss_y == HEIGHT + 100:
            the_time_rect.centery += HEIGHT // tps * 2
            if the_time_rect.centery >= boss_y:
                the_time_rect.centery = boss_y
                atacking = 1
            
        if boss_y == -100:
            the_time_rect.centery -= HEIGHT // tps * 2
            if the_time_rect.centery <= boss_y:
                the_time_rect.centery = boss_y
                atacking = 1
        
    # create_missile('time_missile')

    # Обновление экрана

    rotate_speed += 1
    star = pygame.transform.rotate(star_o, rotate_speed)
    star_rect = star.get_rect()

    # rotate_speed_boss += 3
    # the_time = pygame.transform.rotate(the_time_o, rotate_speed_boss)
    # the_time_rect = the_time.get_rect()

    screen.fill(GRAY)

    death()
    # the_time_rect.center = (x_s, y_s)
    screen.blit(the_time, the_time_rect)
    
    lasers_group.update()
    lasers_group.draw(screen)

    star_rect.center = (x_s, y_s)
    screen.blit(star, star_rect)

    missiles_group.update()
    missiles_group.draw(screen)

    enemy_missiles_group.update()
    enemy_missiles_group.draw(screen)
    colide_enemy_missiles()
    colide_missiles()
    colide_lasers()
    
    screen.blit(text, text_rect)

    pygame.display.update()
    
    clock.tick(FPS)