#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pygame, random,  math, pandas as pd
from pygame import mixer

pygame.init() 

# Create a new surface and window. 
height, width = 600, 600	 #Surface variables 
screen = pygame.display.set_mode((height,width)) 

pygame.display.set_caption("Space spiders")

icon = pygame.image.load(('resources/images/spider.png'))
pygame.display.set_icon(icon)

title_spider = pygame.image.load(('resources/images/spider(2).png'))
#player parameters
playerImg = pygame.image.load(('resources/images/spaceship.png'))
p_x = 268
p_y = 500
pdx_i = 0.2
pdx = 0

#spider parameters
spider_no = 5
spiderImg = []
s_x = []
s_y = []
sdx_i = 0.3
sdy_i = 5
sdx = []
sdy = []
for i in range(spider_no):
    spiderImg.append(pygame.image.load(('resources/images/spider.png')))
    s_x.append(random.randint(0, width-32))
    s_y.append(random.randint(50, 150))
    sdx.append(sdx_i)
    sdy.append(sdy_i)

#bullet parameters    
bulletImg = pygame.image.load(('resources/images/bullet.png'))
b_x = p_x
b_y = p_y
bdx = 0
bdy = 1
bullet_state = "ready"

# background score
mixer.music.load("resources/sounds/bgm.wav")
mixer.music.play(-1)
# score
score_value = 0

# High score 
data = pd.read_csv('resources/high score.csv',header = None)
hi_score = data.iat[0,1] 

font1 = pygame.font.Font('resources/baby blocks.ttf',32)
scx = 10
scy = 10
 
def show_score(x,y):
    score = font1.render("score: " + str(score_value), True, (255,255,255))
    screen.blit(score,(x,y))
def high_score(x,y):
    h_score = font1.render("high score: " + str(hi_score), True, (255,255,255))
    screen.blit(h_score,(x,y))
# Game over
font2 = pygame.font.Font('resources/baby blocks.ttf',50)
def game_over(x,y):
    g_over = font2.render("GAME OVER", True, (255,0,0))
    screen.blit(g_over,(x,y))
# Play again
def play_again(x,y):
    play = font1.render("press Y to play again", True, (255,255,255))
    screen.blit(play,(x,y))
font3 = pygame.font.Font('resources/baby blocks.ttf',40)
def start_menu(x,y):
    title_card = font3.render("SPACE SPIDERS",True, (255,0,0))
    start1 = font1.render("press S to start or Q to quit", True, (255,255,255))
    start2 = font1.render("spacebar for shooting",True, (255,255,0))
    start3 = font1.render("side arrows to move", True, (255,255,0))
    screen.blit(title_card,(x,y))
    screen.blit(start1,(x+70,y+80))
    screen.blit(start2,(x+130,y+120))
    screen.blit(start3,(x+137,y+150))
def player(x,y):
    screen.blit(playerImg,(x,y))
    
def spider(x,y,i):
    screen.blit(spiderImg[i],(x,y))
def title_sp(x,y):
    screen.blit(title_spider,(x,y))
    
def fire_bullet(x,y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg,(x,y))
def F_collision(x1,y1,x2,y2):
    if bullet_state == "fire":
        distance = math.sqrt(math.pow(x1-x2,2)+math.pow(y1-y2,2))
        if distance < 25:
            return True 
        else:
            return False
    
running = True
x = True
s = True

while x:
    while s:
        screen.fill((0, 0, 0))
        start_menu (20, 250)
        title_sp(172, 0)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()               
             
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                if event.key == pygame.K_s:
                    s = False
                    break
        pygame.display.update()
        
    
    while running: 
        screen.fill((0, 0, 0))
    
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                his = pd.DataFrame( [hi_score])
                his.to_csv('resources/high score.csv', header = None)
                # helps in not hanging and quit
                pygame.quit()
                
             
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    his = pd.DataFrame( [hi_score])
                    his.to_csv('resources/high score.csv', header = None)
                    pygame.quit()
            
                if event.key == pygame.K_LEFT:
                    pdx = -1*pdx_i
                if event.key == pygame.K_RIGHT:
                    pdx = pdx_i
                if event.key == pygame.K_SPACE:
                    if bullet_state is "ready":
                        bullet_sound = mixer.Sound('resources/sounds/laser.wav')
                        bullet_sound.play()
                        bullet_state = "fire"
                        b_x = p_x
                
                
                
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    pdx = 0
            

# spaceship movement
        player(p_x,p_y)
        p_x += pdx
        if p_x >= (width-64):
            p_x = (width-64)
        elif p_x <= 0:
            p_x = 0
# spider movement
        for i in range(spider_no):
        
            spider(s_x[i],s_y[i],i)
            s_x[i] += sdx[i] 
            if s_x[i] >= (width-32):
                s_x[i] = (width-32)
                sdx[i] = -1*sdx_i
                s_y[i] += sdy[i]
                sdy[i] += 4
            elif s_x[i] <= 0:
                s_x[i] = 0
                sdx[i] = sdx_i
                s_y[i] += sdy[i]
                sdy[i] += 4
            if s_y[i] >= p_y:  
                his = pd.DataFrame( [hi_score])
                his.to_csv('resources/high score.csv', header = None)
                running = False
                break
            
# collision
            collision = F_collision(b_x,b_y,s_x[i],s_y[i])
            if collision:
                explosion = mixer.Sound('resources/sounds/explosion.wav')
                explosion.play()
                bullet_state = "ready"
                score_value +=1
                b_y = p_y
            
                s_x[i] = random.randint(0, width-32)
                s_y[i] = random.randint(50, 150)
            
            
# bullet movement
        if bullet_state is "fire":
            fire_bullet(b_x+20,b_y)
            b_y -= bdy
        if b_y <= 0:
            bullet_state = "ready"
            b_y = p_y
        show_score(scx,scy)
        
        if score_value >= hi_score:
            hi_score = score_value
        high_score(scx+350, scy)
    # important to add the display update line
        pygame.display.update()
 

 # play again window
    while running == False:
        screen.fill((0, 0, 0))
        game_over(70,250)
        play_again(150, 350) 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:        
                pygame.quit()
           
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q: 
                    pygame.quit()
                if event.key == pygame.K_y:
                    running = True 
                    score_value = 0
                    for i in range(spider_no):
                        s_x[i] = (random.randint(0, width-32))
                        s_y[i] = (random.randint(50, 150))
                        sdy[i] = sdy_i 
        
        pygame.display.update()
        if running:
            break


# In[55]:


file1 = open("high score.txt","r+") 
hi_s = file1.read()
print(hi_s)

file1.truncate(0)
file1.write(str(hi_score))
print(str(hi_score))


# In[65]:


import pandas as pd, csv
hi = 0
his = pd.DataFrame( [hi])
#print(his)
his.to_csv('high score.csv', header = None)
data = pd.read_csv('high score.csv',header = None)
print(data)
hi = data.iat[0,1]


