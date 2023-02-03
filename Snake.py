import pygame
from sys import exit
from random import randint

def display_score():
    current_time = pygame.time.get_ticks() - startTime
    current_time = int(current_time/ 1000)
    text = testFont.render(f'SCORE: {current_time}' ,False,0x05173d00)
    textRect = text.get_rect(center = (500,30))
    screen.blit(text,textRect)
    return current_time

def obstacle_movement(obstacle_list):
    if obstacle_list:
        for obstacle_rect in obstacle_list:
            obstacle_rect.x -= eSpeed
            screen.blit(GroundEnemy1,obstacle_rect)
        obstacle_list = [obstacle for obstacle in obstacle_list if obstacle.x>-100]
        return obstacle_list
    else: return []

def collisions(player, obstacles):
    if obstacles:
        for obstacles_rect in obstacles:
            if player.colliderect(obstacles_rect): return False
    return True

def player_animation():
    global Player,player_index
    if player_rect.bottom < 510:
        Player = Player_jump
    else:
        player_index += 0.15
        if player_index >= len(player_walk):
            player_index = 0
        Player = player_walk[int(player_index)]

pygame.init()
screen = pygame.display.set_mode((1000,600))#,pygame.FULLSCREEN)
pygame.display.set_caption("Test")
clock = pygame.time.Clock()
testFont = pygame.font.Font('Pixeltype.ttf',50)
gameActive = False
gameStart = True
startTime = 0
score = 0
HighScore = 0
eSpeed = 5
i = 0

Sky1 = pygame.image.load('Player/Sky1.png').convert()
Sky2 = pygame.image.load('Player/Sky2.png').convert()
Ground1 = pygame.image.load('Player/Ground.png').convert()
Ground2 = pygame.image.load('Player/Ground.png').convert()
Ground3 = pygame.image.load('Player/Ground.png').convert()
Ground1_rect = Ground1.get_rect(topleft = (0,500))
Ground2_rect = Ground2.get_rect(topleft = (700,500))
Ground3_rect = Ground3.get_rect(topleft = (1400,500))

starttext = pygame.transform.scale2x(testFont.render("JUMP",False,0xf5174300))
starttext_rect = starttext.get_rect(center = (500,180))

starttext1 = testFont.render("PRESS SPACE TO PLAY",False,0xf5174300)
starttext_rect1 = starttext1.get_rect(center = (500,420))

GroundEnemy1 = pygame.transform.scale(pygame.image.load('Player/Ground-enemy1.png').convert_alpha(),(100,73))

Enemy2 = pygame.transform.scale(pygame.image.load('Player/Ground-enemy1.png').convert_alpha(),(100,73))

Obstacle_rect_list = []

Player_stand = pygame.image.load('Player/player-standing.png').convert_alpha()

PlayerWalk1 = pygame.image.load('Player/walk_1.png').convert_alpha()
PlayerWalk2 = pygame.image.load('Player/walk_2.png').convert_alpha()
PlayerWalk3 = pygame.image.load('Player/walk_3.png').convert_alpha()
PlayerWalk4 = pygame.image.load('Player/walk_4.png').convert_alpha()
PlayerWalk5 = pygame.image.load('Player/walk_5.png').convert_alpha()
Player_jump = pygame.image.load('Player/player-jump.png').convert_alpha()
player_walk = [PlayerWalk1,PlayerWalk2,PlayerWalk3,PlayerWalk4,PlayerWalk5]
player_index = 0
Player = player_walk[player_index]
player_rect = Player.get_rect(midbottom = (100,510))

gravity = 0

obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer,1800)
while True:#game loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.MOUSEBUTTONDOWN and player_rect.bottom >= 500:
            gravity = -10.3
        if event.type == pygame.KEYDOWN:
            if (event.key == pygame.K_UP or event.key == pygame.K_SPACE) and player_rect.bottom >= 500:
                gameStart = False
                if gameActive == False:
                    startTime = pygame.time.get_ticks()
                gameActive = True
                gravity = -10.3
            if event.key == pygame.K_r and gameActive == False and gameStart == False:
                gameActive = True
                player_rect.bottom = 510
                startTime = pygame.time.get_ticks()
            if event.key == pygame.K_DOWN:
                if gravity > 0:
                    gravity+=8
                else:
                    gravity = 0
                    gravity+=8
        if event.type == obstacle_timer and gameActive and gameStart == False:
            if randint(0,2):
                Obstacle_rect_list.append(GroundEnemy1.get_rect(midbottom = (randint(1400,1600),490)))
            else:
                Obstacle_rect_list.append(Enemy2.get_rect(midbottom = (randint(1400,1600),290)))
    if gameActive and gameStart == False:
        screen.blit(Sky1,(0,0))
        screen.blit(Sky2,(700,0))
        screen.blit(Ground1,Ground1_rect)
        screen.blit(Ground2,Ground2_rect)
        screen.blit(Ground3,Ground3_rect)
        Ground1_rect.x -= 2
        Ground2_rect.x -= 2
        Ground3_rect.x -=2
        if(Ground1_rect.right < 0):
            Ground1_rect.left = 1400
        if(Ground2_rect.right < 0):
            Ground2_rect.left = 1400
        if(Ground3_rect.right < 0):
            Ground3_rect.left = 1400
        
        score = display_score()
        gravity+=0.25

        if player_rect.bottom > 510:
            player_rect.bottom = 510

        player_animation()
        screen.blit(Player,player_rect)

        Obstacle_rect_list=obstacle_movement(Obstacle_rect_list)

        player_rect.y += gravity

        gameActive =collisions(player_rect,Obstacle_rect_list)


    elif gameActive == False and gameStart == False:
        
        endtext = testFont.render("GAME OVER",False,0xf5174300)
        endtext_rect = endtext.get_rect(center = (500,120))

        endtext1 = testFont.render("PRESS R TO PLAY AGAIN",False,0xf5174300)
        endtext_rect1 = endtext1.get_rect(center = (500,450))

        scoreText = testFont.render(f'SCORE: {score}',False,0xf5174300)
        scoreText_rect = scoreText.get_rect(midtop = (500,150))

        if score > HighScore:
            HighScore = score

        highscoreText = testFont.render(f'HIGHSCORE: {HighScore}',False,0xf5174300)
        highscoreText_rect = highscoreText.get_rect(midtop = (500,200))

        Player = pygame.image.load('Player/player-standing.png').convert_alpha()
        screen.fill(0x05173d)
        screen.blit(endtext, endtext_rect)
        screen.blit(Player_stand,(450,240))
        screen.blit(endtext1, endtext_rect1)
        screen.blit(scoreText,scoreText_rect)
        screen.blit(highscoreText,highscoreText_rect)
        Obstacle_rect_list.clear()
        player_rect.midbottom = (100,500)
        gravity = 0
    else:
        starttext = pygame.transform.scale2x(testFont.render("CYBER JUMP",False,0xf5174300))
        starttext_rect = starttext.get_rect(center = (500,180))

        start1text = pygame.transform.scale2x(testFont.render("CYBER JUMP",False,0x4b173d00))
        start1text_rect = start1text.get_rect(center = (504,184))

        starttext1 = testFont.render("PRESS SPACE TO PLAY",False,0xf5174300)
        starttext_rect1 = starttext1.get_rect(center = (500,420))

        start1text1 = testFont.render("PRESS SPACE TO PLAY",False,0x4b173d00)
        start1text_rect1 = start1text1.get_rect(center = (502,422))

        screen.blit(Sky1,(0,0))
        screen.blit(Sky2,(700,0))
        screen.blit(Ground1,(0,500))
        screen.blit(Ground1,(700,500))
        screen.blit(Player_stand,player_rect)
        screen.blit(start1text, start1text_rect)
        screen.blit(starttext, starttext_rect)
        if (int(i) % 2 == 0):
            screen.blit(start1text1, start1text_rect1)
            screen.blit(starttext1, starttext_rect1)
        i += 0.02

    pygame.display.update()
    clock.tick(60)