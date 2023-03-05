# micro_game.py

import sys
import pygame
import random

pygame.init()

# set window
size = width,height = 800,640
screen = pygame.display.set_mode(size)
game_name = "Dodge! Bacteria"
pygame.display.set_caption(game_name)

# set other things
clock = pygame.time.Clock()
font_name = 'calibri'

# define color
black = 0,0,0
whiter_black = 130,130,130
white = 255,255,255
background_color = 240,240,255
button_color = 170,170,170
button_color_on = 190,190,190
button_color_light = 210,210,210

# define some function
def show_text(text,x,y,size,color):
    font = pygame.font.SysFont(font_name,size)
    text = font.render(text,True,color)
    text_rect = text.get_rect(center = [x,y])
    screen.blit(text,text_rect)

def show_text_left(text,x,y,size,color):
    font = pygame.font.SysFont(font_name,size)
    text = font.render(text,True,color)
    text_rect = text.get_rect(center = [x+text.get_width()/2,y])
    screen.blit(text,text_rect)

def show_text_dna(text,x,y,size,color,place_left):
    font = pygame.font.SysFont(font_name,size)
    text = font.render(text,True,color)
    if place_left:
        text_rect = text.get_rect(center = [x+16,y])
        image_dna_rect = image_dna.get_rect(center = (x-text_rect.width/2,y))
    else:
        text_rect = text.get_rect(center = [x-16,y])
        image_dna_rect = image_dna.get_rect(center = (x+text_rect.width/2,y))
    screen.blit(text,text_rect)
    screen.blit(image_dna,image_dna_rect)

# define class
class Player(pygame.sprite.Sprite):
    def __init__(self,self_upgrade_level):
        pygame.sprite.Sprite.__init__(self)
        self.img = pygame.image.load(r"image\Character_1.jpg")
        self.img = pygame.transform.scale(self.img,(upgrade0_info[self_upgrade_level[0]-1],upgrade0_info[self_upgrade_level[0]-1]))
        self.rect = self.img.get_rect(center = (width/2,height/2))
        self.speed = upgrade1_info[self_upgrade_level[1]-1]
        self.immume = [False,False,False]
        if self_upgrade_level[3]:
            self.immume[0] = True
        if self_upgrade_level[4]:
            self.immume[1] = True
        if self_upgrade_level[5]:
            self.immume[2] = True
    def update(self,pressed_key):
        if pressed_key[pygame.K_w]:
            self.rect.move_ip(0,-self.speed)
        if pressed_key[pygame.K_s]:
            self.rect.move_ip(0,self.speed)
        if pressed_key[pygame.K_d]:
            self.rect.move_ip(self.speed,0)
        if pressed_key[pygame.K_a]:
            self.rect.move_ip(-self.speed,0)
        if self.rect.top<0:
            self.rect.top=0
        if self.rect.bottom>height:
            self.rect.bottom=height
        if self.rect.left<0:
            self.rect.left=0
        if self.rect.right>width:
            self.rect.right=width

class Enemy(pygame.sprite.Sprite):
    def __init__(self,self_type,self_init_pos,self_size,self_speed):
        pygame.sprite.Sprite.__init__(self)
        self.color = black
        self.type = self_type
        self.init_pos = self_init_pos
        self.width = self_size[0]
        self.height = self_size[1]
        if self.type == 0:
            self.img = pygame.image.load(r"image\70_alcohol.png")
            self.img = pygame.transform.smoothscale(self.img,(self.width,self.height))
            self.rect = self.img.get_rect(center = self.init_pos)
        elif self.type == 1:
            if self.width > self.height:
                self.img = pygame.image.load(r"image\bacteriophage_rotate.png")
            else:
                self.img = pygame.image.load(r"image\bacteriophage.png")
            self.img = pygame.transform.smoothscale(self.img,(self.width,self.height))
            self.rect = self.img.get_rect(center = self.init_pos)
        elif self.type == 2:
            self.img = pygame.image.load(r"image\Penicillin_core.png")
            self.img = pygame.transform.smoothscale(self.img,(self.width,self.height))
            self.rect = pygame.Rect((self.init_pos[0]-1,self.init_pos[1]-1),(2,2))
            self.inflate_end = False
        self.speedx = self_speed[0]
        self.speedy = self_speed[1]
    def update(self):
        self.rect.move_ip(self.speedx,self.speedy)
        if self.type == 0:
            if self.rect.top < 0:
                self.rect.top = 0
                self.speedy = -self.speedy
            if self.rect.bottom > height:
                self.rect.bottom = height
                self.speedy = -self.speedy
            if self.rect.left < 0:
                self.rect.left = 0
                self.speedx = -self.speedx
            if self.rect.right > width:
                self.rect.right = width
                self.speedx = -self.speedx
        elif self.type == 1:
            if self.speedx > 0:
                if self.rect.left > width:
                    self.kill()
            if self.speedy > 0:
                if self.rect.top > height:
                    self.kill()
        elif self.type == 2:
            if not self.inflate_end:
                if self.rect.width < self.width:
                    self.rect.inflate_ip(2,2)
                else:
                    self.inflate_end = True
                    self.rect = self.img.get_rect(center = self.init_pos)

# define some variable
frame_rate = 70
playing = True
in_menu = True
in_upgrade = False
in_stat = False
in_game = False
is_clicked = False
is_dead = False
in_stage = False
to_next_stage = False
goto_dead = False
start_clicked = False
upgrade_clicked = False
dna_clicked = False
stat_clicked = False
back_clicked = False
buy_clicked = False
upgrades_clicked = [False,False,False,False,False,False,False]
dead_clicked = False
DNA = 0
upgrade_count = 7
upgrade_chosen = 0
upgrade_name = ["Smaller size","More mobility","Faster synthesis","Penicillin resistance","Bacteriophage rejection","Alcohol tolerance","Harsh environment"]
upgrade_level = [1,1,1,0,0,0,0]
upgrade_max = [10,5,10,1,1,1,1]
base_cost = [50,500,50,60000,120000,180000,50000]
upgrade0_info = [40,36,32,30,27,24,22,20,18,16]
upgrade1_info = [2,3,4,5,6]
upgrade2_info = [1,2,3,5,8,12,16,20,25,30]
expo = [2,4,2,1,1,1,1]
init_stage_num = 1
experiment_time = 0
total_earned_dna = 0
longest_survive_time = 0
button_pressed = 0
cheat_text = ""
cheat_message = ""
print_dna = False
cheat_stage_num = 0
enemy_group = pygame.sprite.Group()

# define some button
start_game_button = pygame.Rect((100,425),(260,50))
to_upgrade_button = pygame.Rect((440,425),(260,50))
get_dna_button = pygame.Rect((590,45),(200,50))
back_menu_button = pygame.Rect((30,10),(120,50))
to_stat_button = pygame.Rect((30,10),(120,50))
upgrade_buy_button = pygame.Rect((520,550),(140,40))
dead_button = pygame.Rect((300,400),(200,50))

# define some square
upgrade_square_1 = pygame.Rect((30,100),(360,70))
upgrade_square_2 = pygame.Rect((30,175),(360,70))
upgrade_square_3 = pygame.Rect((30,250),(360,70))
upgrade_square_4 = pygame.Rect((30,325),(360,70))
upgrade_square_5 = pygame.Rect((30,400),(360,70))
upgrade_square_6 = pygame.Rect((30,475),(360,70))
upgrade_square_7 = pygame.Rect((30,550),(360,70))
upgrade_square_8 = pygame.Rect((410,100),(360,520))
upgrade_square = [upgrade_square_1,upgrade_square_2,upgrade_square_3,upgrade_square_4,upgrade_square_5,upgrade_square_6,upgrade_square_7]
stat_square = pygame.Rect((350,500),(400,40))

# load some image
image_dna = pygame.image.load(r"image\DNA.png")
image_dna = pygame.transform.smoothscale(image_dna,(32,45))

# main game loop
while playing:
    player = Player(upgrade_level)
    init_pos2 = random.randint(0,3)
    if init_pos2 == 0:
         enemy = Enemy(2,(100,200),(150,150),(0,0))
    elif init_pos2 == 1:
        enemy = Enemy(2,(700,180),(150,150),(0,0))
    elif init_pos2 == 2:
        enemy = Enemy(2,(140,480),(150,150),(0,0))
    elif init_pos2 == 3:
        enemy = Enemy(2,(725,500),(150,150),(0,0))
    enemy_group.add(enemy)
    enemy = Enemy(0,(400,615),(50,50),(4,4))
    enemy_group.add(enemy)
    spawn_timer = 3000
    enemy_num2 = 0
    start_time = pygame.time.get_ticks()
    while in_menu:
        screen.fill(background_color)
        enemy_group.update()
        for enemy in enemy_group:
            if enemy.type == 2 and not enemy.inflate_end:
                screen.fill((201,230,29),enemy.rect)
            else:
                screen.blit(enemy.img,enemy.rect)
        screen.blit(player.img,player.rect)
        mouse_pos = pygame.mouse.get_pos()
        if start_clicked:
            screen.fill(button_color_light,start_game_button)
        elif start_game_button.collidepoint(mouse_pos):
            screen.fill(button_color_on,start_game_button)
        else:
            screen.fill(button_color,start_game_button)
        if upgrade_clicked:
            screen.fill(button_color_light,to_upgrade_button)
        elif to_upgrade_button.collidepoint(mouse_pos):
            screen.fill(button_color_on,to_upgrade_button)
        else:
            screen.fill(button_color,to_upgrade_button)
        if dna_clicked:
            screen.fill(button_color_light,get_dna_button)
        elif get_dna_button.collidepoint(mouse_pos):
            screen.fill(button_color_on,get_dna_button)
        else:
            screen.fill(button_color,get_dna_button)
        if stat_clicked:
            screen.fill(button_color_light,to_stat_button)
        elif to_stat_button.collidepoint(mouse_pos):
            screen.fill(button_color_on,to_stat_button)
        else:
            screen.fill(button_color,to_stat_button)
        show_text("Dodge! Bacteria",400,240,64,black)
        show_text("Start Experiment",230,450,30,black)
        show_text("Upgrade Bacteria",570,450,30,black)
        show_text("DNA synthesis",690,70,30,black)
        show_text("Stat",90,35,30,black)
        show_text_dna(": "+str(DNA),690,22,24,black,True)
        pygame.display.update()
        if (pygame.time.get_ticks()-start_time)/spawn_timer > (enemy_num2+1):
            enemy_num2 += 1
            spawn_pos = random.randint(0,1)
            if spawn_pos == 0:
                init_x = -20
                init_y = random.sample([80,160,240,400,480,560],1)[0]
                enemy = Enemy(1,(init_x,init_y),(40,20),(10,0))
            elif spawn_pos == 1:
                init_x = random.sample([100,200,300,500,600,700],1)[0]
                init_y = -20
                enemy = Enemy(1,(init_x,init_y),(20,40),(0,10))
            enemy_group.add(enemy)

        clock.tick(frame_rate) 
        for event in pygame.event.get():
            if (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE) or event.type == pygame.QUIT:
                playing = False
                in_menu = False
                in_upgrade = False
                in_stat = False
                in_game = False
                is_clicked = False
            elif event.type == pygame.MOUSEBUTTONDOWN and not is_clicked:
                if event.button == 1:
                    is_clicked = True
                    mouse_pos = event.pos
                    if start_game_button.collidepoint(mouse_pos):
                        start_clicked = True
                    if to_upgrade_button.collidepoint(mouse_pos):
                        upgrade_clicked = True
                    if get_dna_button.collidepoint(mouse_pos):
                        dna_clicked = True
                    if to_stat_button.collidepoint(mouse_pos):
                        stat_clicked = True
            elif event.type == pygame.MOUSEBUTTONUP:
                is_clicked = False
                if start_clicked:
                    start_clicked = False
                    enemy_group.empty()
                    in_menu = False
                    in_game = True
                    experiment_time += 1
                    button_pressed += 1
                    player = Player(upgrade_level)
                    if cheat_stage_num:
                        init_stage_num = cheat_stage_num
                    elif upgrade_level[6]:
                        init_stage_num = 6
                    else:
                        init_stage_num = 1
                    start_time = pygame.time.get_ticks() - 30000*(init_stage_num-1)
                    stage_num = init_stage_num
                elif upgrade_clicked:
                    upgrade_clicked = False
                    button_pressed += 1
                    enemy_group.empty()
                    in_menu = False
                    in_upgrade = True
                elif dna_clicked:
                    dna_clicked = False
                    DNA += upgrade2_info[upgrade_level[2]-1]
                    button_pressed += 1
                    total_earned_dna += upgrade2_info[upgrade_level[2]-1]
                elif stat_clicked:
                    stat_clicked = False
                    button_pressed += 1
                    enemy_group.empty()
                    in_menu = False
                    in_stat = True
                
    while in_upgrade:
        screen.fill(background_color)
        screen.fill(whiter_black,upgrade_square_8)
        mouse_pos = pygame.mouse.get_pos()
        if back_clicked:
            screen.fill(button_color_light,back_menu_button)
        elif back_menu_button.collidepoint(mouse_pos):
            screen.fill(button_color_on,back_menu_button)
        else:
            screen.fill(button_color,back_menu_button)
        for i in range(upgrade_count):
            if upgrades_clicked[i]:
                screen.fill(button_color_light,upgrade_square[i])
            elif upgrade_square[i].collidepoint(mouse_pos) :
                screen.fill(button_color_on,upgrade_square[i])
            else:
                screen.fill(button_color,upgrade_square[i])
            show_text(upgrade_name[i],210,135+75*i,34,black)
            if i == upgrade_chosen:
                show_text(upgrade_name[i],590,130,36,black)
                show_text("Current Effect:",590,330,36,black)
                if upgrade_level[upgrade_chosen] < upgrade_max[upgrade_chosen]:
                    show_text("Next Level Effect:",590,430,36,black)
                    if buy_clicked:
                        screen.fill(button_color_light,upgrade_buy_button)
                    elif upgrade_buy_button.collidepoint(mouse_pos):
                        screen.fill(button_color_on,upgrade_buy_button)
                    else:
                        screen.fill(button_color,upgrade_buy_button)
                    show_text("Level "+str(upgrade_level[i]),590,170,30,black)
                    show_text("Upgrade",590,570,30,black)
                    if i == 0:
                        show_text("Size "+str(upgrade0_info[upgrade_level[upgrade_chosen]-1]),590,370,30,black)
                        show_text("Size "+str(upgrade0_info[upgrade_level[upgrade_chosen]]),590,470,30,black)
                    elif i == 1:
                        show_text("Speed "+str(upgrade1_info[upgrade_level[upgrade_chosen]-1]),590,370,30,black)
                        show_text("Speed "+str(upgrade1_info[upgrade_level[upgrade_chosen]]),590,470,30,black)
                    elif i == 2:
                        show_text("DNA Gain x"+str(upgrade2_info[upgrade_level[upgrade_chosen]-1]),590,370,30,black)
                        show_text("DNA Gain x"+str(upgrade2_info[upgrade_level[upgrade_chosen]]),590,470,30,black)
                    elif i == 3:
                        show_text("None",590,370,30,black)
                        show_text("Immume penicillin",590,470,30,black)
                    elif i == 4:
                        show_text("None",590,370,30,black)
                        show_text("Immume bacteriophage",590,470,30,black)
                    elif i == 5:
                        show_text("None",590,370,30,black)
                        show_text("Immume 70% alcohol",590,470,30,black)
                    elif i == 6:
                        show_text("Start from stage 1",590,370,30,black)
                        show_text("Start from stage 6",590,470,30,black)
                        show_text("(also set initial timer to 02:30)",590,500,24,black)
                else:
                    screen.fill(button_color,upgrade_buy_button)
                    show_text("Level MAX",590,170,30,black)
                    show_text("Max level",590,570,30,black)
                    if i == 0:
                        show_text("Size "+str(upgrade0_info[upgrade_level[upgrade_chosen]-1]),590,370,30,black)
                    elif i == 1:
                        show_text("Speed "+str(upgrade1_info[upgrade_level[upgrade_chosen]-1]),590,370,30,black)
                    elif i == 2:
                        show_text("DNA Gain x"+str(upgrade2_info[upgrade_level[upgrade_chosen]-1]),590,370,30,black)
                    elif i == 3:
                        show_text("Immume penicillin",590,370,30,black)
                    elif i == 4:
                        show_text("Immume bacteriophage",590,370,30,black)
                    elif i == 5:
                        show_text("Immume 70% alcohol",590,370,30,black)
                    elif i == 6:
                        show_text("Start from stage 6",590,370,30,black)
                        show_text("(also set initial timer to 02:30)",590,400,24,black)
                if i == 0:
                    show_text('"Become smaller,',590,235,24,black)
                    show_text('survive longer"',590,265,24,black)
                elif i == 1:
                    show_text('"Move faster,',590,235,24,black)
                    show_text('survive longer"',590,265,24,black)
                elif i == 2:
                    show_text('"Be stronger more quickly"',590,250,24,black)
                elif i == 3:
                    show_text('"Now, you can not kill me"',590,250,24,black)
                elif i == 4:
                    show_text('"Bye Bye bacteriophage"',590,250,24,black)
                elif i == 5:
                    show_text('"Alcohol is useless on you, Wow"',590,250,24,black)
                elif i == 6:
                    show_text('"Harsh environment',590,235,24,black)
                    show_text('makes us improve"',590,265,24,black)
        show_text("Back",90,35,30,black)
        show_text_dna(": "+str(DNA),690,22,24,black,True)
        if upgrade_level[upgrade_chosen] < upgrade_max[upgrade_chosen]:
            upgrade_cost = base_cost[upgrade_chosen]*(expo[upgrade_chosen]**upgrade_level[upgrade_chosen])
        else:
            upgrade_cost = 0
        show_text_dna("Cost: "+str(upgrade_cost),590,530,30,black,False)
        pygame.display.update()

        clock.tick(frame_rate)
        for event in pygame.event.get():
            if (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE) or event.type == pygame.QUIT:
                playing = False
                in_menu = False
                in_upgrade = False
                in_stat = False
                in_game = False
                is_clicked = False
            elif event.type == pygame.MOUSEBUTTONDOWN and not is_clicked:
                if event.button == 1:
                    is_clicked = True
                    mouse_pos = event.pos
                    for i in range(upgrade_count):
                        if upgrade_square[i].collidepoint(mouse_pos):
                            upgrades_clicked[i] = True
                            break
                    if upgrade_buy_button.collidepoint(mouse_pos):
                        buy_clicked = True
                    if back_menu_button.collidepoint(mouse_pos):
                        back_clicked = True
            elif event.type == pygame.MOUSEBUTTONUP:
                is_clicked = False
                for i in range(upgrade_count):
                    if upgrades_clicked[i]:
                        upgrade_chosen = i
                        upgrades_clicked[i] = False
                        button_pressed += 1
                        break
                if buy_clicked:
                    buy_clicked = False
                    if upgrade_level[upgrade_chosen] < upgrade_max[upgrade_chosen]:
                        button_pressed += 1
                        if DNA >= upgrade_cost:
                            upgrade_level[upgrade_chosen] += 1
                            DNA -= upgrade_cost
                if back_clicked:
                    back_clicked = False
                    button_pressed += 1
                    in_menu = True
                    in_upgrade = False 
                    is_clicked = False

    while in_stat:
        screen.fill(background_color)
        screen.fill(button_color,stat_square)
        mouse_pos = pygame.mouse.get_pos()
        if back_clicked:
            screen.fill(button_color_light,back_menu_button)
        elif back_menu_button.collidepoint(mouse_pos):
            screen.fill(button_color_on,back_menu_button)
        else:
            screen.fill(button_color,back_menu_button)
        show_text("Back",90,35,30,black)
        show_text("Total experiment time(s): "+str(experiment_time),400,175,40,black)
        show_text_dna("Total earned DNA: "+str(total_earned_dna),400,250,40,black,False)
        time_text='%d:%02d'%(longest_survive_time//60000,(longest_survive_time//1000)%60)
        show_text("Longest survive time: "+time_text,400,325,40,black)
        show_text("Total button pressed: "+str(button_pressed),400,400,40,black)
        show_text("Enter secret code: ",200,520,40,black)
        show_text_left(cheat_text,360,520,30,black)
        if print_dna:
            show_text_dna(cheat_message,400,580,40,black,False)
        else:
            show_text(cheat_message,400,580,40,black)
        pygame.display.update()
        for event in pygame.event.get():
            if (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE) or event.type == pygame.QUIT:
                playing = False
                in_menu = False
                in_upgrade = False
                in_stat = False
                in_game = False
                is_clicked = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    cheat_text = cheat_text.split(" ")
                    if cheat_text[0] == "set":
                        if cheat_text[1] == "upgrade" and cheat_text[2] == "MAX" and len(cheat_text) == 3:
                            upgrade_level = upgrade_max
                            cheat_message = "Now your upgrade are all max level"
                            print_dna = False
                        elif cheat_text[1] == "initial" and cheat_text[2] == "stage" and cheat_text[3] == "num" and len(cheat_text) == 5:
                            try:
                                cheat_stage_num = int(cheat_text[4])
                                cheat_message = "Now you start the experiment from stage "+str(cheat_stage_num)
                                print_dna = False
                            except:
                                cheat_message = "Invalid stage number"
                                print_dna = False
                        else:
                            cheat_message = "Invalid code"
                            print_dna = False
                    elif cheat_text[0] == "add":
                        if cheat_text[1] == "DNA" and len(cheat_text) == 3:
                            try:
                                DNA += int(cheat_text[2])
                                cheat_message = "You gain "+str(cheat_text[2])
                                print_dna = True
                            except:
                                cheat_message = "Invalid DNA amount"
                                print_dna = False
                        else:
                            cheat_message = "Invalid code"
                            print_dna = False
                    else:
                        cheat_message = "Invalid code"
                        print_dna = False
                    cheat_text = ""
                elif event.key == pygame.K_BACKSPACE:
                    cheat_text = cheat_text[:-1]
                else:
                    cheat_text += event.unicode
            elif event.type == pygame.MOUSEBUTTONDOWN and not is_clicked:
                if event.button == 1:
                    is_clicked = True
                    mouse_pos = event.pos
                    if back_menu_button.collidepoint(mouse_pos):
                        back_clicked = True
            elif event.type == pygame.MOUSEBUTTONUP:
                is_clicked = False
                if back_clicked:
                    back_clicked = False
                    button_pressed += 1
                    in_menu = True
                    in_stat = False 
                    is_clicked = False
                
    while in_game:
        threshold_0 = 36000//(((stage_num-1)%5)+2)
        threshold_1 = 35000//(((stage_num-1)%5)+3)
        enemy_wave_0 = -1
        enemy_wave_1 = 0
        enemy_num_2 = ((stage_num-1)%5+1)//2
        enemy_per_wave0 = (stage_num-1)//10+1
        enemy_per_wave1 = (stage_num-1)//5+1
        size_0 = 50
        size_1w = 20
        size_1h = 40
        size_2 = 140+10*((stage_num+1)//3)
        speed_0 = 3+enemy_per_wave0
        speed_1 = 6+2*enemy_per_wave1
        stage_start_time = pygame.time.get_ticks()
        for i in range(enemy_num_2):
            init_x = random.randint(size_2/2,width-size_2/2)
            init_y = random.randint(size_2/2,height-size_2/2)
            enemy = Enemy(2,(init_x,init_y),(size_2,size_2),(0,0))
            enemy_group.add(enemy)
        in_stage = True
        while in_stage:
            screen.fill(background_color)
            enemy_group.update()
            for enemy in enemy_group:
                if enemy.type == 2 and not enemy.inflate_end:
                    screen.fill((201,230,29),enemy.rect)
                else:
                    screen.blit(enemy.img,enemy.rect)
            pressed_key = pygame.key.get_pressed()
            if not is_dead:
                player.update(pressed_key)
            screen.blit(player.img,player.rect)
            pass_time = pygame.time.get_ticks()-start_time
            time_text='%d:%02d'%(pass_time//60000,(pass_time//1000)%60)
            show_text("Stage "+str(stage_num),400,20,30,(0,0,255))
            show_text(time_text,400,50,24,(0,0,255))
            if upgrade_level[5] and upgrade_level[4] and upgrade_level[3]:
                show_text("To kill yourself, press K",400,620,30,(0,0,255))
            pygame.display.update()
            stage_time = pygame.time.get_ticks()-stage_start_time
            if (stage_time-2000)/threshold_0 > (enemy_wave_0+1):
                for i in range(enemy_per_wave0):
                    minus_signx = random.randint(0,1)
                    spd_x = speed_0*(-1)**minus_signx
                    minus_signy = random.randint(0,1)
                    spd_y = speed_0*(-1)**minus_signy
                    become_vertical = random.randint(0,2)
                    init_x = random.randint(size_0/2,width-size_0/2)
                    init_y = random.randint(size_0/2,height-size_0/2)
                    spawn_pos = random.randint(0,3)
                    if spawn_pos == 0:
                        init_y = size_0/2
                        if become_vertical == 1:
                            spd_x = 0
                    elif spawn_pos == 1:
                        init_y = height-size_0/2
                        if become_vertical == 1:
                            spd_x = 0
                    if spawn_pos == 2:
                        init_x = size_0/2
                        if become_vertical == 1:
                            spd_y = 0
                    elif spawn_pos == 3:
                        init_x = width-size_0/2
                        if become_vertical == 1:
                            spd_y = 0
                    enemy = Enemy(0,(init_x,init_y),(size_0,size_0),(spd_x,spd_y))
                    enemy_group.add(enemy)
                enemy_wave_0 += 1
            if stage_time/threshold_1 > (enemy_wave_1+1):
                for i in range(enemy_per_wave1):
                    spawn_pos = random.randint(0,1)
                    if spawn_pos == 0:
                        init_x = -size_1h/2
                        init_y = random.randint(size_1w,height-size_1w)
                        spd_x = speed_1
                        spd_y = 0
                        enemy = Enemy(1,(init_x,init_y),(size_1h,size_1w),(spd_x,spd_y))
                    elif spawn_pos == 1:
                        init_x = random.randint(size_1w,width-size_1w)
                        init_y = -size_1h/2
                        spd_x = 0
                        spd_y = speed_1
                        enemy = Enemy(1,(init_x,init_y),(size_1w,size_1h),(spd_x,spd_y))
                    enemy_group.add(enemy)
                enemy_wave_1 += 1
            if stage_time >= 29000:
                enemy_group.empty()
                stage_num += 1
                in_stage = False
                to_next_stage = True
            enemy_collide = pygame.sprite.spritecollideany(player,enemy_group)
            if enemy_collide:
                if (not (enemy_collide.type == 0 and player.immume[2])) and (not (enemy_collide.type == 1 and player.immume[1])) and (not (enemy_collide.type == 2 and player.immume[0])):
                    in_stage = False
                    to_next_stage = False
                    in_game = False
                    in_menu = True
                    is_dead = True
                    player.kill()
                    dead_time = pygame.time.get_ticks()
                    goto_dead = True

            clock.tick(frame_rate)
            for event in pygame.event.get():
                if (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE) or event.type == pygame.QUIT:
                    playing = False
                    in_menu = False
                    in_upgrade = False
                    in_stat = False
                    in_game = False
                    in_stage = False
                    to_next_stage = False
                    is_clicked = False
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_k:
                    in_stage = False
                    to_next_stage = False
                    in_game = False
                    in_menu = True
                    is_dead = True
                    player.kill()
                    dead_time = pygame.time.get_ticks()
                    goto_dead = True
                else:
                    is_clicked = False
                    
        while to_next_stage:
            screen.fill(background_color)
            pressed_key = pygame.key.get_pressed()
            player.update(pressed_key)
            screen.blit(player.img,player.rect)
            pass_time = pygame.time.get_ticks()-start_time
            time_text='%d:%02d'%(pass_time//60000,(pass_time//1000)%60)
            show_text("Stage "+str(stage_num),400,20,30,(0,0,255))
            show_text(time_text,400,50,24,(0,0,255))
            if upgrade_level[5] and upgrade_level[4] and upgrade_level[3]:
                show_text("To kill yourself, press K",400,620,30,(0,0,255))
            pygame.display.update()
            stage_time = pygame.time.get_ticks()-stage_start_time
            if stage_time >= 30000:
                to_next_stage = False

            clock.tick(frame_rate)
            for event in pygame.event.get():
                if (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE) or event.type == pygame.QUIT:
                    playing = False
                    in_menu = False
                    in_upgrade = False
                    in_stat = False
                    in_game = False
                    in_stage = False
                    to_next_stage = False
                    is_clicked = False
                else:
                    is_clicked = False
    while goto_dead:
        screen.fill(background_color)
        enemy_group.update()
        for enemy in enemy_group:
            if enemy.type == 2 and not enemy.inflate_end:
                screen.fill((201,230,29),enemy.rect)
            else:
                screen.blit(enemy.img,enemy.rect)
        time_text='%d:%02d'%(pass_time//60000,(pass_time//1000)%60)
        show_text("Stage "+str(stage_num),400,20,30,(0,0,255))
        show_text(time_text,400,50,24,(0,0,255))
        if upgrade_level[5] and upgrade_level[4] and upgrade_level[3]:
                show_text("To kill yourself, press K",400,620,30,(0,0,255))
        pygame.display.update()
        dead_pass_time = pygame.time.get_ticks()-dead_time
        if dead_pass_time >= 2000:
            goto_dead = False
            enemy_group.empty()
        
        clock.tick(frame_rate)
        for event in pygame.event.get():
            if (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE) or event.type == pygame.QUIT:
                playing = False
                in_menu = False
                in_upgrade = False
                in_stat = False
                in_game = False
                is_dead = False
                goto_dead = False
                is_clicked = False
            else:
                is_clicked = False
                
    while is_dead:
        screen.fill(background_color)
        mouse_pos = pygame.mouse.get_pos()
        if dead_clicked:
            screen.fill(button_color_light,dead_button)
        elif dead_button.collidepoint(mouse_pos):
            screen.fill(button_color_on,dead_button)
        else:
            screen.fill(button_color,dead_button)
        earned_DNA = (pass_time//1000)*10*upgrade2_info[upgrade_level[2]-1]
        show_text("You survived "+str(pass_time//60000)+" minute(s) "+str((pass_time//1000)%60)+" second(s)",400,250,40,black)
        show_text_dna("You earned "+str(earned_DNA),400,310,40,black,False)
        show_text("Continue",400,425,30,black)
        pygame.display.update()
        
        clock.tick(frame_rate)
        for event in pygame.event.get():
            if (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE) or event.type == pygame.QUIT:
                playing = False
                in_menu = False
                in_upgrade = False
                in_stat = False
                in_game = False
                is_dead = False
                is_clicked = False
            elif event.type == pygame.MOUSEBUTTONDOWN and not is_clicked:
                if event.button == 1:
                    is_clicked = True
                    mouse_pos = event.pos
                    if dead_button.collidepoint(mouse_pos):
                        dead_clicked = True
            elif event.type == pygame.MOUSEBUTTONUP:
                is_clicked = False
                if dead_clicked:
                    dead_clicked = False
                    is_dead = False
                    DNA += earned_DNA
                    total_earned_dna += earned_DNA
                    button_pressed += 1
                    if pass_time > longest_survive_time:
                        longest_survive_time = pass_time
                    
# leave the game
pygame.quit()
sys.exit()
