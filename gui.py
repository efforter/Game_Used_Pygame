import pygame
from pygame.locals import *
from pygame import mixer
from os import path

# set 게임
pygame.mixer.pre_init(44100, -16, 2, 512)
mixer.init()
pygame.init()

# fps 설정
clock = pygame.time.Clock()
fps = 60

# 화면 넓이, 높이
screen_width = 1000
screen_height = 1000

# set display
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('MyGUI')

# font 설정
font_score = pygame.font.SysFont('comicsansms', 20)
font_last = pygame.font.SysFont('comicsansms', 30)
font_stage = pygame.font.SysFont('comicsansms', 20, bold=True) 
font_life = pygame.font.SysFont('comicsansms', 40, bold=True)

# 변수 설정
tile_size = 50
game_over = 0
main_menu = True
die_display = False
level = 1
max_levels = 4
score = 0
life = 3.5
judge = 0
white = (255, 255, 255)

# 필요한 image
bg_img = pygame.image.load('img/map.png')
die_bg = pygame.image.load('img/die_background.png')
start_map = pygame.image.load('img/start_map.png')
restart_img = pygame.image.load('img/restart_btn.png')
exit_img = pygame.image.load('img/exit_btn.png')
start_img = pygame.image.load('img/start_btn.png')

# 필요한 sound
game_start_fx = pygame.mixer.Sound('img/bgm.mp3')
game_exit_fx = pygame.mixer.Sound('img/end.wav')
coin_fx = pygame.mixer.Sound('img/coin.wav')
jump_fx = pygame.mixer.Sound('img/jump.wav')
game_over_fx = pygame.mixer.Sound('img/game_over.wav')
game_start_fx.play(-1)
game_over_fx.set_volume(0.5)

# 화면에 text 출력
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

# 맵 구현
world_level1 = [
[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2], 
[2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2], 
[2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2], 
[2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2], 
[2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2], 
[2, 0, 0, 0, 0, 0, 0, 0, 0, 9, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2], 
[2, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2], 
[2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2], 
[2, 0, 0, 0, 9, 0, 0, 0, 9, 0, 9, 0, 0, 0, 9, 0, 0, 0, 0, 2], 
[2, 0, 0, 0, 3, 0, 0, 3, 4, 3, 4, 3, 0, 0, 3, 0, 0, 0, 0, 2], 
[2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2], 
[2, 0, 0, 0, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 10, 2], 
[2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2]
]
world_level2 = [
[1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2], 
[2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 2], 
[2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 2], 
[2, 0, 0, 0, 0, 9, 9, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 10, 2], 
[2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 3, 3, 2], 
[2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 2], 
[2, 0, 0, 3, 3, 0, 0, 0, 0, 0, 0, 0, 3, 0, 6, 0, 0, 0, 0, 2], 
[2, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 3, 0, 0, 0, 0, 3, 3, 2], 
[2, 0, 0, 0, 0, 0, 6, 0, 3, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 2], 
[2, 3, 3, 0, 0, 0, 0, 0, 3, 0, 0, 0, 3, 0, 7, 0, 0, 0, 0, 2], 
[2, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 3, 3, 3, 3, 0, 0, 0, 2], 
[2, 0, 0, 3, 3, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 9, 2], 
[2, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 2], 
[2, 0, 0, 0, 0, 0, 0, 3, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2], 
[2, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2], 
[2, 0, 0, 0, 7, 0, 0, 0, 3, 3, 3, 3, 8, 8, 8, 3, 3, 0, 0, 2], 
[2, 0, 3, 3, 3, 3, 0, 0, 3, 0, 9, 0, 3, 3, 3, 0, 0, 0, 0, 2], 
[2, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 2], 
[2, 0, 0, 0, 0, 7, 0, 9, 3, 0, 0, 0, 0, 0, 0, 0, 0, 3, 3, 2], 
[2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2]
]
world_level3 = [
[1, 0, 0, 0, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2], 
[2, 10, 0, 0, 0, 0, 0, 0, 0, 0, 9, 0, 0, 0, 0, 0, 0, 0, 0, 2],  
[2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2], 
[2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2], 
[2, 9, 0, 0, 0, 7, 0, 0, 8, 0, 7, 0, 0, 8, 8, 0, 0, 0, 0, 2], 
[2, 4, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 0, 0, 2], 
[2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 9, 2], 
[2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 2], 
[2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],  
[2, 0, 0, 0, 0, 7, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 2], 
[2, 0, 0, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2], 
[2, 9, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2], 
[2, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2], 
[2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2], 
[2, 0, 0, 0, 8, 8, 0, 0, 8, 0, 8, 0, 0, 8, 0, 0, 0, 0, 0, 2], 
[2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 0, 9, 2],  
[2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 2], 
[2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2], 
[2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],  
[2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2]
]
world_level4 = [
[1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2], 
[2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2], 
[2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 9, 2], 
[2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2], 
[2, 0, 0, 3, 3, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8, 2], 
[2, 0, 0, 0, 3, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 2], 
[2, 9, 0, 0, 3, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 2], 
[2, 4, 0, 0, 3, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 2], 
[2, 0, 0, 0, 3, 9, 0, 0, 0, 3, 0, 0, 0, 0, 0, 3, 0, 0, 0, 2], 
[2, 0, 0, 0, 3, 4, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 2], 
[2, 0, 0, 3, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 6, 0, 0, 0, 0, 2], 
[2, 0, 0, 0, 3, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2], 
[2, 0, 0, 0, 3, 0, 0, 3, 3, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 2], 
[2, 3, 0, 0, 3, 0, 0, 0, 0, 0, 0, 3, 3, 3, 0, 0, 0, 0, 9, 2], 
[2, 0, 0, 0, 3, 9, 0, 0, 0, 0, 3, 0, 0, 0, 3, 0, 0, 0, 4, 2], 
[2, 0, 0, 0, 3, 4, 0, 0, 0, 3, 0, 0, 0, 0, 0, 3, 0, 0, 0, 2], 
[2, 0, 0, 3, 3, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 2], 
[2, 0, 0, 0, 3, 0, 0, 3, 0, 0, 0, 11, 0, 0, 0, 0, 0, 0, 0, 2], 
[2, 0, 0, 0, 3, 8, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8, 2], 
[2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2]
]
world_level=[world_level1,world_level2,world_level3,world_level4]

# level 초기화
def reset_level(level):
    player.reset(100, screen_height - 130)
    monster_group.empty()
    platform_group.empty()
    coin_group.empty()
    thorn_group.empty()
    exit_group.empty()
    # load level
    world = World(world_level[i])
    # coin 총합
    score_coin = Coin(tile_size // 2, tile_size // 2)
    coin_group.add(score_coin)
    return world

class Button():
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.clicked = False

    def draw(self):
        action = False
        pos = pygame.mouse.get_pos() # mouse 위치 잡기
        # check mouse
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                action = True
                self.clicked = True
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        # button 그리기
        screen.blit(self.image, self.rect)
        return action

class Player():
    def __init__(self, x, y):
        self.reset(x, y)

    def update(self, game_over):
        dx = 0
        dy = 0
        walking = 5
        col_thresh = 20

        if game_over == 0:
            key = pygame.key.get_pressed()
            if key[pygame.K_SPACE] and self.jump == False and self.up == False:
                jump_fx.play()
                self.speed = -18
                self.jump = True
            if key[pygame.K_SPACE] == False:
                self.jump = False
            if key[pygame.K_LEFT]:
                dx -= 5
                self.counter += 1
                self.direction = -1
            if key[pygame.K_RIGHT]:
                dx += 5
                self.counter += 1
                self.direction = 1
            if key[pygame.K_LEFT] == False and key[pygame.K_RIGHT] == False:
                self.counter = 0
                self.index = 0
                if self.direction == 1:
                    self.image = self.images_right[self.index]
                if self.direction == -1:
                    self.image = self.images_left[self.index]

            if self.counter > walking:
                self.counter = 0    
                self.index += 1
                if self.index >= len(self.images_right):
                    self.index = 0
                if self.direction == 1:
                    self.image = self.images_right[self.index]
                if self.direction == -1:
                    self.image = self.images_left[self.index]

            self.speed += 1
            if self.speed > 10:
                self.speed = 10
            dy += self.speed

            self.up = True
            for tile in world.tile_list:
                if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                    dx = 0
                if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                    if self.speed < 0:
                        dy = tile[1].bottom - self.rect.top
                        self.speed = 0
                    elif self.speed >= 0:
                        dy = tile[1].top - self.rect.bottom
                        self.speed = 0
                        self.up = False

            if pygame.sprite.spritecollide(self, monster_group, False):
                game_over = -1
                game_start_fx.stop()
                game_over_fx.play()

            if pygame.sprite.spritecollide(self, thorn_group, False):
                game_over = -1
                game_start_fx.stop()
                game_over_fx.play()

            if pygame.sprite.spritecollide(self, exit_group, False):
                if score >= 5:
                    if i == 3:
                        game_start_fx.stop()
                        game_exit_fx.play()
                    game_over = 1

            for platform in platform_group:
                if platform.rect.colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                    dx = 0
                if platform.rect.colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                    if abs((self.rect.top + dy) - platform.rect.bottom) < col_thresh:
                        self.speed = 0
                        dy = platform.rect.bottom - self.rect.top
                    elif abs((self.rect.bottom + dy) - platform.rect.top) < col_thresh:
                        self.rect.bottom = platform.rect.top - 1
                        self.up = False
                        dy = 0
                    if platform.move_x != 0:
                        self.rect.x += platform.move_direction

            self.rect.x += dx
            self.rect.y += dy


        elif game_over == -1:
            self.image = self.dead_image
            if self.rect.y > 20:
                self.rect.y -= 5

        screen.blit(self.image, self.rect)
        return game_over


    def reset(self, x, y):
        self.images_right = []
        self.images_left = []
        self.index = 0
        self.counter = 0
        for num in range(1, 3):
            img_right = pygame.image.load(f'img/character{num}.png')
            img_right = pygame.transform.scale(img_right, (40, 60))
            img_left = pygame.transform.flip(img_right, True, False)
            self.images_right.append(img_right)
            self.images_left.append(img_left)
        self.dead_image = pygame.image.load('img/dead.png')
        self.image = self.images_right[self.index]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.speed = 0
        self.jump = False
        self.direction = 0
        self.up = True

class World():
    def __init__(self, data):
        self.tile_list = []

        back_img = pygame.image.load('img/out_of_map.png')
        floor = pygame.image.load('img/floor.png')
        block = pygame.image.load('img/block.png')
        itembox = pygame.image.load('img/itembox.png')

        row_count = 0
        for row in data:
            col_count = 0
            for tile in row:
                if tile == 1:
                    img = pygame.transform.scale(back_img, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if tile == 2:
                    img = pygame.transform.scale(floor, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile) 
                if tile == 3:
                    img = pygame.transform.scale(block, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)     
                    self.tile_list.append(tile)
                if tile == 4:
                    img = pygame.transform.scale(itembox, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)   
                    self.tile_list.append(tile)
                if tile == 6:
                    platform = Platform(col_count * tile_size, row_count * tile_size, 0, 1)
                    platform_group.add(platform)    
                if tile == 7:
                    monster = Monster(col_count * tile_size, row_count * tile_size + 15)
                    monster_group.add(monster)   
                if tile == 8:
                    thorn = Thorn(col_count * tile_size, row_count * tile_size + (tile_size // 2))
                    thorn_group.add(thorn)
                if tile == 9:
                    coin = Coin(col_count * tile_size + (tile_size // 2), row_count * tile_size + (tile_size // 3 * 2))
                    coin_group.add(coin)
                if tile == 10:
                    exit = Exit(col_count * tile_size, row_count * tile_size - (tile_size // 2))
                    exit_group.add(exit)
                if tile == 11:
                    exit = Door(col_count * tile_size, row_count * tile_size - tile_size)
                    exit_group.add(exit)
                col_count += 1
            row_count += 1

    def draw(self):
        for tile in self.tile_list:
            screen.blit(tile[0], tile[1])

class Monster(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('img/monster.png')
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.move_direction = 1
        self.move_counter = 0

    def update(self):
        self.rect.x += self.move_direction
        self.move_counter += 1
        if abs(self.move_counter) > 50:
            self.move_direction *= -1
            self.move_counter *= -1

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, move_x, move_y):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load('img/platform.png')
        self.image = pygame.transform.scale(img, (tile_size, tile_size))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.move_counter = 0
        self.move_direction = 1
        self.move_x = move_x
        self.move_y = move_y

    def update(self):
        self.rect.x += self.move_direction * self.move_x
        self.rect.y += self.move_direction * self.move_y
        self.move_counter += 1
        if abs(self.move_counter) > 50:
            self.move_direction *= -1
            self.move_counter *= -1

class Thorn(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load('img/spikes.png')
        self.image = pygame.transform.scale(img, (tile_size, tile_size // 2))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load('img/coin.png')
        self.image = pygame.transform.scale(img, (tile_size // 3 * 2, tile_size // 3 * 2))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

class Exit(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load('img/portal.png')
        self.image = pygame.transform.scale(img, (tile_size*1.2, int(tile_size * 1.7)))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Door(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load('img/door.png')
        self.image = pygame.transform.scale(img, (tile_size * 3, int(tile_size * 3)))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

player = Player(100, screen_height - 130)

monster_group = pygame.sprite.Group()
platform_group = pygame.sprite.Group()
thorn_group = pygame.sprite.Group()
coin_group = pygame.sprite.Group()
exit_group = pygame.sprite.Group()

score_coin = Coin(tile_size // 2, tile_size // 2)
coin_group.add(score_coin)

i=0
world = World(world_level[i])

start_button = Button(screen_width // 2 - 260, screen_height // 2 + 110, start_img)
restart_button = Button(screen_width // 2 - 50, 60, restart_img)
exit_button = Button(screen_width // 2 - 50, 120, exit_img)


run = True          
while run:
    clock.tick(fps)
    screen.blit(bg_img, (0, 0))

    if main_menu == True:
        screen.blit(start_map, (0, 0))
        if start_button.draw():
            main_menu = False
        key = pygame.key.get_pressed()
        if key[pygame.K_SPACE]:
            main_menu = False
    else:
        world.draw()

        if game_over == 0:
            monster_group.update()
            platform_group.update()
            if pygame.sprite.spritecollide(player, coin_group, True):
                score += 1
                coin_fx.play()
            draw_text('x  ' + str(score), font_score, white, tile_size, 10)
        
        monster_group.draw(screen)
        platform_group.draw(screen)
        thorn_group.draw(screen)
        coin_group.draw(screen)
        exit_group.draw(screen)

        game_over = player.update(game_over)

        if die_display == True:
            if player.rect.y <= 50: 
                life -= 0.5
                screen.blit(die_bg, (0, 0))
                draw_text('1 - ' + str(i+1), font_life, white, screen_width // 2 + 20, screen_height // 2 - 182)
                draw_text('x   ' + str(int(life)), font_life, white, screen_width // 2 - 10, screen_height // 2 - 50)
                pygame.time.delay(2000)
                die_display = False
                judge += 1
            
        if game_over == -1:
            if judge <= 1:
                die_display = True
            if die_display == False:
                world = reset_level(level)
                game_start_fx.play(-1)
                game_over = 0
                score = 0
                judge = 0

        if game_over == 1:
            i += 1
            level += 1
            if level <= max_levels:
                score = 0
                world = reset_level(level)
                game_over = 0
            else:
                game_start_fx.stop()
                draw_text('restart', font_last, white, (screen_width // 2 + 30), 60)
                draw_text('exit', font_last, white, (screen_width // 2 + 30), 120)
                if restart_button.draw():
                    i = 0
                    life = 3.5
                    world = reset_level(level)
                    game_over = 0
                    score = 0
                    game_exit_fx.stop()
                    game_start_fx.play(-1)
                    main_menu = True
                if exit_button.draw():
                    pygame.quit()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

pygame.quit()