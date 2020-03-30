""" 
this is a shooting game loosely based on ironman.

plot-iron man saving the day
    lots of shooting
    cool sounds
    play to find out
    full of bugs
if you find one,keep it to yourself
images created using sprites from sprite sheet and edited using GIMP
sound from the marvel vs capcom game

(source-https://www.spriters-resource.com/game_boy_advance/invincibleironman/)

created using python3 with pygame module
dt of completion-30-3-2020
p.s- its my first game, completed in almost 4-5 days
    so be kind :)
 """
#--------importing necessary modules---------
import pygame
import random


#----creating our player---------
class Player(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        self.image=pygame.image.load("images_ironman/iron_man.png")
        #defining attributes of our player
        self.height=self.image.get_height()
        self.width=self.image.get_width()
        self.health=10
        self.kill=False
        self.heal=False
        self.rect=self.image.get_rect()
    
    #------player's x and y will be determined by mouse control    
    def update(self):
        pos=pygame.mouse.get_pos()
        self.rect.y=pos[1]-player.height/2
        self.rect.x=30


#-------------creating minions aka villain's robots----------
class Minion(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image=pygame.image.load(("images_minions/minion.png"))
        self.height=self.image.get_height()
        self.width=self.image.get_width()
        self.rect=self.image.get_rect()
        self.dy=5
        self.FireLaser=False
        self.health=5
    
    #---------to create itself more--------
    def add_minion(self):
        self.rect.x=800
        self.rect.y=random.randint(100,500)
    
    #---------move frowards and fire laser---------
    def update(self):
        self.rect.x-=5
        if self.rect.x < screen_width/2 + self.width:
            self.rect.x = 800
            self.rect.y=random.randint(100,500)
            self.FireLaser=True
        else:
            self.FireLaser=False


#----------player's bullet----------
class Bullet(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image=pygame.image.load("images_ironman/pulse.png")
        self.rect=self.image.get_rect()
    
    #--------speed of bullet-----------
    def update(self):
        self.rect.x+=10

#-------minion's bullet-----------
class Minion_bullet(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image=pygame.image.load(("images_minions/laser.png"))
        self.rect=self.image.get_rect()
    
    #-----------speed of bullet----------------
    def update(self):
        self.rect.x-=10


#----------------boss or villain -----------
class Boss(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image=pygame.image.load(("images_boss/bossidle.png"))
        self.height=self.image.get_height()
        self.width=self.image.get_width()
        self.rect=self.image.get_rect()
        self.health=30
        self.defeat=False
        self.arrival=False
        self.rect.y=300
        self.rect.x=500


#-----------boss's bullet------------
class BossBullet(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image=pygame.image.load("images_boss/blast.png")
        self.height=self.image.get_height()
        self.width=self.image.get_width()
        self.rect=self.image.get_rect()
    
    def update(self):
        self.rect.x-=13


#initialising a pygame
pygame.init()

#---------music and sounds------
pygame.mixer.music.load("boss_fight_music.mp3")
pygame.mixer.music.play(-1)
pulse=pygame.mixer.Sound("SOUNDS_IRONMAN/pulse.wav")
minion_laser=pygame.mixer.Sound("SOUNDS_viLLain/beam.wav")
boss_shot=pygame.mixer.Sound("SOUNDS_viLLain/boss_shot.wav")
player_win=pygame.mixer.Sound("SOUNDS_IRONMAN/tony_win_dialouge.wav")
boss_win=pygame.mixer.Sound("SOUNDS_viLLain/win_dialouge.wav")
tony_sarcastic=pygame.mixer.Sound("SOUNDS_IRONMAN/tony_sarcastic.wav")
tony_sarcastic.play()

#-----setting up screen dimensions---------
screen_width=900
screen_height=600
screen=pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption("IRON-MAN BY-JEEVS")
#clock to set our fps
clock=pygame.time.Clock()


#-------creating and grouping sprites
all_sprite=pygame.sprite.Group()
minion_list=pygame.sprite.Group()
playerBullet_list=pygame.sprite.Group()
minionBullet_list=pygame.sprite.Group()
boss_list=pygame.sprite.Group()
player_list=pygame.sprite.Group()
bossBullet_list=pygame.sprite.Group()
power_list=pygame.sprite.Group()

#assigning player
player=Player()
player_list.add(player)
all_sprite.add(player)
#assigning boss
boss=Boss()
boss_list.add(boss)


#------------constants-----------
bossWin=False
run=True
addMinion=True
minionCount=0
minion_dead=0
total_minion=0
supermove=False
ct=0
ct_b=0

#----------------images---------
bg=pygame.image.load("background.png")
player_logo=pygame.image.load("logo.png")
boss_logo=pygame.image.load("crimsondynamo.png")

player_dead=[
    pygame.image.load("images_ironman/dead(1).png"),
    pygame.image.load("images_ironman/dead(2).png"),
    pygame.image.load("images_ironman/dead(3).png"),
    pygame.image.load("images_ironman/dead(4).png")
    ]
#-----custom events----------------
PLAYERHEAL=pygame.USEREVENT+3       #player healing
MOVEBOSS=pygame.USEREVENT+1         #moving boss
BOSSATTACK=pygame.USEREVENT+2       #boss firing bullet
#--------setting timer for custom events-------
pygame.time.set_timer(MOVEBOSS,2000)
pygame.time.set_timer(BOSSATTACK,4000)
pygame.time.set_timer(PLAYERHEAL,3000)
#-----------redraw function to draw on screen-----------
def redraw():
    #-------setting up background image-------
    screen.blit(bg,(0,0))
    screen.blit(player_logo,(0,0))


    #-------message if player loses-----
    if player.kill:
        text=pygame.font.SysFont("times",44)
        text_surf=text.render("YOU LOST.PRESS ESC TO QUIT",True,(255,0,0))
        screen.blit(text_surf,(100,300))


    #--------message if player wins------
    if boss.defeat:
        text=pygame.font.SysFont("times",44)
        text_surf=text.render("YOU WON.PRESS ESC TO QUIT",True,(0,255,0))
        screen.blit(text_surf,(100,300))


    #-------player's logo and health bars--------
    Health_player=pygame.font.SysFont("comicsans",20)
    Health_player_surf=Health_player.render("HEALTH:{0}".format(player.health),True,(255,255,255))
    screen.blit(Health_player_surf,(64,25))
    pygame.draw.rect(screen,(255,0,0),(64,0,200,20))
    pygame.draw.rect(screen,(0,255,0),(64,0,player.health*20,20))


    #------minion's health bars--------
    if not(player.kill):
        for minion in minion_list:
            pygame.draw.rect(screen,(255,0,0),(minion.rect.x,minion.rect.y-30,50,5))
            pygame.draw.rect(screen,(0,255,0),(minion.rect.x,minion.rect.y-30,minion.health*10,5))

    #--------boss's logo and health bars--------
    if boss.arrival:
        screen.blit(boss_logo,(802,0))
        Health_boss=pygame.font.SysFont("comicsans",20)
        Health_boss_surf=Health_boss.render("HEALTH:{0}".format(boss.health),True,(255,255,255))
        screen.blit(Health_boss_surf,(502,25))
        pygame.draw.rect(screen,(255,0,0),(502,0,300,20))
        pygame.draw.rect(screen,(0,255,0),(502,0,boss.health*10,20))


    #-------condition for boss's arrival--------
    if boss.arrival and not(player.kill):
        boss_list.draw(screen)
    
    
    #---------conditon for continuing game-----
    if not(player.kill):
        all_sprite.draw(screen)
    
    
    #------drawing player and updating the sceen
    player_list.draw(screen)
    pygame.display.update()


#----------the gaming loop-----------
while run:
    #----------fetch all events---------
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run=False


        #----------press esc to quit--------
        keys=pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            run=False

        #------------on mouse click, player fires-----------
        if event.type==pygame.MOUSEBUTTONDOWN:
            pulse.play()
            player.image=pygame.image.load("images_ironman/iron_man_pulse.png")
            player_bullet=Bullet()
            player_bullet.rect.x=player.rect.x + player.width
            player_bullet.rect.y=player.rect.y
            playerBullet_list.add(player_bullet)
            all_sprite.add(player_bullet)
        if event.type==pygame.MOUSEBUTTONUP:
            player.image=pygame.image.load("images_ironman/iron_man.png")


        #--------------boss's attributes-----------
        if not(player.kill) and boss.arrival:
            #--------changes boss's posn---------
            if event.type==MOVEBOSS:              
                boss.rect.x=random.choice((600,screen_width-boss.width))
                boss.rect.y=random.randint(boss.width,screen_height-boss.width)
            
            #---------boss fires--------------
            if event.type==BOSSATTACK:
                boss_shot.play()
                boss_bullet=BossBullet()
                boss_bullet.rect.y=boss.rect.y
                boss_bullet.rect.x=boss.rect.x
                bossBullet_list.add(boss_bullet)
                all_sprite.add(boss_bullet)
            else:
                boss.image=pygame.image.load("images_boss/bossidle.png")
        
        
        #-------player heals if given condition is true
        if player.heal:
            if event.type==PLAYERHEAL:
                player.health+=1


 
#-------addminion-------------
    if addMinion and total_minion<5:
        if minionCount>1:
            addMinion=False
            minionCount=0
        else:
            minion=Minion()

            minion.add_minion()

            minion_list.add(minion)
            all_sprite.add(minion)
            minionCount+=1
            total_minion+=1 

    
#--------minion fires----------  
    if minion.FireLaser and not(player.kill):
        for minion in minion_list:
            minion_laser.play()
            minion_bullet=Minion_bullet()
            minion_bullet.rect.x=minion.rect.x
            minion_bullet.rect.y=minion.rect.y
            minionBullet_list.add(minion_bullet)
            all_sprite.add(minion_bullet)


#---------minion damage and kill--------
    minion_dokill=False
    for player_bullet in playerBullet_list:
        if player_bullet.rect.x>=screen_width:
            playerBullet_list.remove(player_bullet)
        for minion in minion_list:
            if minion.health==0:
                minion_dokill=True
                addMinion=True
                minion.image=pygame.image.load("images_minions/minion_blast.png")    
                minion_hit_list=pygame.sprite.spritecollide(player_bullet,minion_list,minion_dokill)
                for dead in minion_hit_list:
                    minion_dead+=1
            else:
                addMinion=False
                if pygame.sprite.collide_rect(player_bullet,minion):
                    minion.health-=1
                    playerBullet_list.remove(player_bullet)
                    all_sprite.remove(player_bullet)
                    minion_dokill=False




#-----------minion damage to player and player kill condition
    for minion_bullet in minionBullet_list:
        if minion_bullet.rect.x<=0:
            all_sprite.remove(minion_bullet)
        for player in player_list:
            if player.health<=0:
                player.kill=True
                pygame.sprite.spritecollide(minion_bullet,player_list,player.kill)
                player.heal=False
            else:
                if pygame.sprite.collide_rect(minion_bullet,player):
                    player.health-=1
                    player.image=pygame.image.load("images_ironman/hurt(1).png")
                    minionBullet_list.remove(minion_bullet)
                    all_sprite.remove(minion_bullet)
                    player.kill=False
    
    
#-----------player regeneration condition---------------

    if player.health==10:
        player.heal=False
    elif player.health <=6 and not(player.kill):
        player.heal=True
        

#-------------boss scenario-----------
    if boss.arrival:

        #-----------player damage to boss and boss defeat condition
        for player_bullet in playerBullet_list:
            if player_bullet.rect.x>boss.rect.x:
                playerBullet_list.remove(player_bullet)
                all_sprite.remove(player_bullet)
            if boss.health==0:
                pygame.time.set_timer(BOSSATTACK,0)
                player_win.play()
                boss.defeat=True
                pygame.sprite.spritecollide(player_bullet,boss_list,boss.defeat)
            else:
                if pygame.sprite.collide_rect(player_bullet,boss):
                    boss.health-=0.5
                    playerBullet_list.remove(player_bullet)
                    all_sprite.remove(player_bullet)
                    boss.defeat=False


        #--------------player damage by boss and player defeat condition 
        for boss_bullet in bossBullet_list:
            boss.image=pygame.image.load("images_boss/fight_stance2.png")
            if boss_bullet.rect.x <= 0:
                bossBullet_list.remove(boss_bullet)
                all_sprite.remove(boss_bullet)
            
            for player in player_list:
                if player.health<=0:
                    player.heal=False
                    player.kill=True
                    pygame.sprite.spritecollide(boss_bullet,player_list,player.kill)
                else:
                    if pygame.sprite.collide_rect(boss_bullet,player):
                        player.image=pygame.image.load("images_ironman/hurt(1).png")
                        player.health-=3
                        bossBullet_list.remove(boss_bullet)
                        all_sprite.remove(boss_bullet)
            

#--------if player dies, villain dialouge
    if player.kill and ct==0:
        boss_win.play()
        ct=1
        bossarrival=False
        player_list.remove(player)

        
#--------if player wins and player dialouge
    if boss.defeat and ct==0:
        ct+=1
        player_win.play()
        player_list.remove(player)
        boss_list.remove(boss)


#-----condition for arrival of boss------------  
    if minion_dead>=5:
        boss.arrival=True

#----------calling update method of all sprites--------- 
    all_sprite.update()

#--------------settinng fps,(here,30)----------
    clock.tick(30)

#-----callinf redraw function---------
    redraw()

#--------quitting pygame module----------
pygame.quit()   


















