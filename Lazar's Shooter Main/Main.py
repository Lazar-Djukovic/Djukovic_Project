import pygame
import math
import random

pygame.init()

#Defining global constants - colours, screen, clock, and images
GROUNDGREEN = (43,132,88)
WHITE = (255,255,255)
BLACK = (0,0,0)
BULLETYELLOW = (250,253,15)
RED = (170,0,0)
LIGHT_RED = (255,20,10)
GREEN = (0,175,0)
LIGHT_GREEN = (0,255,0)
YELLOW = (253,165,15)
LIGHT_YELLOW = (252,226,5)
BROWN = (210,105,30)
WALL_GRAY = (47,69,83)
GRAY = (80,80,80)

#Screen resolution variables
display_width = 1280
display_height = 720
display = pygame.display.set_mode((display_width,display_height))

#Text fonts 
smallfont = pygame.font.Font("Fonts\RetroFont.ttf",30)
medfont = pygame.font.Font("Fonts\RetroFont.ttf",45)
largefont = pygame.font.Font("Fonts\RetroFont.ttf",70)

#Window caption and clock
pygame.display.set_caption('<Shooter/>')
clock = pygame.time.Clock()

refresh = 0

offset_speed = 4

#Loading and transforming all images, as well as setting colorkeys
Ground_img = pygame.image.load('Ground.png')

player_walk_img = [pygame.image.load('PlayerSprites/Player1.png'),pygame.image.load('PlayerSprites/Player2.png')]
player_idle_img = pygame.image.load('PlayerSprites/PlayerIdle.png')
player_hurt_img = pygame.image.load('PlayerSprites/PlayerHurt.png')

rifle_img = pygame.image.load('Weapons/Rifle.png').convert()
player_rifle_img = pygame.transform.scale(rifle_img,(64,64))
player_rifle_img.set_colorkey((BLACK))

revolver_img = pygame.image.load('Weapons/Revolver.png').convert()
player_revolver_img = pygame.transform.scale(revolver_img,(64,32))
player_revolver_img.set_colorkey((BLACK))

health_load_img = pygame.image.load('Items/health.png').convert()
health_img = pygame.transform.scale(health_load_img,(38,38))
health_img.set_colorkey((BLACK))

ammo_load_img = pygame.image.load('Items/ammo.png').convert()
ammo_img = pygame.transform.scale(ammo_load_img,(38,38))
ammo_img.set_colorkey((BLACK))

tree_load_img = pygame.image.load('Objects/tree_1.png').convert()
tree_1_img = pygame.transform.scale(tree_load_img,(128,128))
tree_1_img.set_colorkey((BLACK))


RedEnemy = [pygame.image.load('Enemies/RedAlien1.png'),pygame.image.load('Enemies/RedAlien2.png')]
RedEnemyH = pygame.image.load('Enemies/RedAlien2.png')
RedEnemyHit = pygame.transform.scale(RedEnemyH,(75,75))

background = (pygame.image.load('IntroBackground.png'))



#The main player class
class Player(pygame.sprite.Sprite):
  def __init__(self, x, y, width, height,health,weapon):
    super().__init__()

    self.width = width
    self.height = height

    self.image = pygame.Surface([self.width,self.height])

    self.rect = self.image.get_rect()
    self.rect.x = x
    self.rect.y = y

    #reload counter needed!

    #counter and variable to stop player for being damaged for a few seconds after taking damage.
    self.invincible = False
    self.damage_counter = 0

    self.counter = 0
    self.moving = False
    self.direction = 'front'
    self.collision = False
    self.health_needed = False

    self.health = health
    self.score = 0
    self.weapon = weapon
    self.damage = 0
    self.weaponimg = player_rifle_img
    self.weapon_list = ['Rifle','Revolver']
    self.new_position = 0,0

    #ammunition for all of the weapons
    self.ammo_type = 1
    self.rifle_ammo = 50
    self.pistol_ammo = 49
    self.stop = False
    

  #Function for handling, rotating and possibly switching weapons
  def handle_weapons(self,display):
    mouse_x, mouse_y = pygame.mouse.get_pos()

    rel_x, rel_y = mouse_x - self.rect.x, mouse_y - self.rect.y
    angle = (180/math.pi) * -math.atan2(rel_y, rel_x)

    if self.weapon == 'Rifle':
      self.weaponimg = player_rifle_img
      self.ammo_type = 1
    elif self.weapon == 'Revolver':
      self.weaponimg = player_revolver_img
      self.ammo_type = 2

    #Checking if the weapon is on the left or right side of the player and rotating accordingly
    if angle < 90 and angle > -90:
      player_weapon_copy = pygame.transform.rotate(self.weaponimg, angle)
    else:
      player_weapon_copy2 = pygame.transform.flip(self.weaponimg, False, True)
      player_weapon_copy = pygame.transform.rotate(player_weapon_copy2, angle)
    #endif

    display.blit(player_weapon_copy, (self.rect.x+30 - int(player_weapon_copy.get_width()/2),self.rect.y+35-int(player_weapon_copy.get_height()/2)))


#function that updates the player object every frame
  def update(self,display,walls):

    keys = pygame.key.get_pressed()

    displayUpdate('n')

    if keys[pygame.K_a]:
      display_scroll[0] -= offset_speed
      for bullet in bullet_group:
        bullet.offset('x','pos')
      for enemy in enemy_group:
        enemy.rect.x += offset_speed
      self.moving = True
    #endif

    if keys[pygame.K_d]:
      display_scroll[0] += offset_speed
      for bullet in bullet_group:
        bullet.offset('x','neg')
      for enemy in enemy_group:
        enemy.rect.x -= offset_speed
      self.moving = True
    #endif

    if keys[pygame.K_w]:
      display_scroll[1] -= offset_speed
      for bullet in bullet_group:
        bullet.offset('y','pos')
      for enemy in enemy_group:
        enemy.rect.y += offset_speed
      self.moving = True
    #endif

    if keys[pygame.K_s]:
      display_scroll[1] += offset_speed
      for bullet in bullet_group:
        bullet.offset('y','neg')
      for enemy in enemy_group:
        enemy.rect.y -= offset_speed
      self.moving = True
    #endif

    #scrolling trough the weapons for the player
    if keys[pygame.K_1]:
      self.weapon = player.weapon_list[0]
    if keys[pygame.K_2]:
      self.weapon = player.weapon_list[1]

      
    wall_collision = pygame.sprite.spritecollide(self, walls, False)
    if wall_collision:
      # Move the player back to their previous position
      displayUpdate('o')
      return


    self.Shadow(self.rect.x,self.rect.y)

    #timer to switch between frames
    if self.counter + 1 >= 24:
      self.counter = 0
    #endif
    self.counter += 1
    
    #Animating the player by altering between images while he is moving
    if self.moving == True:
        display.blit(pygame.transform.scale(player_walk_img[self.counter//12], (self.width,self.height)), (self.rect.x,self.rect.y))
    else:
      display.blit(pygame.transform.scale(player_idle_img, (self.width,self.height)), (self.rect.x,self.rect.y))

    if self.invincible == True:
      if self.counter < 7:
        display.blit(pygame.transform.scale(player_hurt_img, (self.width,self.height)), (self.rect.x,self.rect.y))
    #endif

    #pygame.draw.rect(display, RED, (self.rect.x, self.rect.y, self.width, self.height))
    self.moving = False

    if self.health > 320:
      self.health = 320

    self.handle_weapons(display)
    self.PlayerHealth(950,660,320,50,self.health)

    textSurf, textRect = text_objects('Score:'+str(self.score),BLACK,'medium')
    display.blit(textSurf, textRect)

    textSurf2, textRect2 = text_objects('Ammo:'+str(self.AmmoType()),BLACK,'medium')
    display.blit(textSurf2,(950,610))

    if self.invincible == True:
      self.damage_counter += 1
      if self.damage_counter > 25:
        self.invincible = False
        self.damage_counter = 0

    if self.health < 320:
      self.health_needed = True
    else:
      self.health_needed = False

  def PlayerHealth(self,x,y,w,h,health):
    pygame.draw.rect(display, BLACK, (x-5,y-5,w+10,h+10))
    pygame.draw.rect(display, RED, (x,y,health,h))

  def Shadow(self,x,y):
    pygame.draw.ellipse(display, GRAY, [x+16,y+55,32,14])

  def Hit(self,enemy_damage):
    if self.invincible == False:
      self.health = self.health - enemy_damage
      self.invincible = True
    if self.health < 0:
      pygame.quit()


  def AmmoType(self):
    if self.ammo_type == 1:
      return(self.rifle_ammo)
    if self.ammo_type == 2:
      return(self.pistol_ammo)
    if self.ammo_type == 3:
      return(self.rocks)

  def Use(self):
    pass



#Class definition of players bullet
class PlayerBullet(pygame.sprite.Sprite):
  def __init__(self, x, y, mouse_x, mouse_y,size):
    super().__init__()
    self.size = size
    self.image = pygame.Surface([self.size,self.size])
    self.rect = self.image.get_rect()
    self.rect.x = x
    self.rect.y = y

    self.mouse_x = mouse_x
    self.mouse_y = mouse_y

    self.speed = 15
    
    #calculating the angle at which the bullet will be shot
    self.angle = math.atan2(y-self.mouse_y, x-self.mouse_x)
    self.x_velocity = math.cos(self.angle) * self.speed
    self.y_velocity = math.sin(self.angle) * self.speed

  def update(self,display,walls):
    self.rect.x -= int(self.x_velocity)
    self.rect.y -= int(self.y_velocity)

    if player.weapon == 'bow':
      pygame.draw.rect(display, BROWN, (self.rect.x, self.rect.y,self.size+5,self.size+3))
    else:
      pygame.draw.rect(display, BULLETYELLOW, (self.rect.x, self.rect.y,self.size,self.size))

  def Collide(self,position):
    self.kill()

  def offset(self,axis,direction):
      self.axis = axis
      self.direction = direction

      if self.axis == 'y':
        if self.direction == 'neg':
          self.rect.y -= offset_speed
        elif self.direction == 'pos':
          self.rect.y += offset_speed
      elif self.axis =='x':
        if self.direction == 'neg':
          self.rect.x -= offset_speed
        elif self.direction == 'pos':
          self.rect.x += offset_speed
          


#Class definition of the items
class Item(pygame.sprite.Sprite):
  def __init__(self, x, y, size, type):
    super().__init__()
    self.size = size
    self.image = pygame.Surface([self.size,self.size])
    self.rect = self.image.get_rect()
    self.x = x
    self.y = y

    self.type = type

  def update(self,display,walls):

    self.rect.x = self.x - display_scroll[0]
    self.rect.y = self.y - display_scroll[1]

    self.Shadow(self.rect.x,self.rect.y)
    
    if self.type == 'health':
      display.blit(health_img,(self.rect.x,self.rect.y))

    if self.type == 'ammo':
      display.blit(ammo_img,(self.rect.x,self.rect.y))

  def Shadow(self,x,y):
    pygame.draw.rect(display, GRAY, (x+12,y+18,19,19))

  def Use(self):
    if self.type == 'health':
      if player.health < 320:
        player.health += 50

    if self.type == 'ammo':
      player.rifle_ammo += random.randint(5,15)


#The enemy sprite class
class Enemy(pygame.sprite.Sprite):
  def __init__(self,x,y,width,height,health,damage):
    super().__init__()
    self.width = width
    self.height = height
    self.image = pygame.Surface([32,32])
    
    self.rect = self.image.get_rect()
    self.rect.x = x
    self.rect.y = y

    #Basic ai for random enemy movement, in the players general direction
    self.counter = 0
    self.reset_offset = 0
    self.offset_x = random.randrange(-160,200)
    self.offset_y = random.randrange(-160,200)

    self.health = health
    self.damage = damage
  
  def update(self,display,walls):

    self.Shadow(self.rect.x,self.rect.y)

    #pygame.draw.rect(display, RED, (self.rect.x, self.rect.y,32,32)) #This was a hitbox test
    if self.health < 0:
      all_sprites_group.remove(self)
      enemy_group.remove(self)

    if self.reset_offset == 0:
      self.offset_x = random.randrange(-150,150)
      self.offset_y = random.randrange(-150,150)
      self.reset_offset = random.randrange(120,150)
    else:
      self.reset_offset -= 1
    #endif

    if player.rect.x + self.offset_x > self.rect.x - display_scroll[0]:
      self.rect.x += 1
    elif player.rect.x + self.offset_x < self.rect.x - display_scroll[0]:
      self.rect.x -= 1
    #endif

    if player.rect.y + self.offset_y > self.rect.y - display_scroll[1]:
      self.rect.y += 1
    elif player.rect.y + self.offset_y < self.rect.y - display_scroll[1]:
      self.rect.y -= 1
    #endif

    if self.counter + 1 >= 40:
      self.counter = 0
    self.counter += 1
    #endif

    #Animating the enemy by altering between images while he is moving
    display.blit(pygame.transform.scale(RedEnemy[self.counter//20], (self.width,self.height)), (self.rect.x-16,self.rect.y-16))

  def hit(self):
    self.health -= 25
    display.blit(RedEnemyHit, (self.rect.x-19,self.rect.y-19))
    player.score += 10
  
  def Shadow(self,x,y):
    pygame.draw.ellipse(display, GRAY, [x-5,y+23,42,18])

  def Collide(self,direction):
    pass


#class BlueEnemy(Enemy):
    #def __init__(self,x,y,width,height,health):
        #super(BlueEnemy, self).__init__(self,x,y,width,height,health)
    


#Class for making walls which players can't go trought, but some enemies may be able to
class Wall(pygame.sprite.Sprite):
  def __init__(self,x,y,width,height):
    super().__init__()
    self.width = width
    self.height = height
    self.image = pygame.Surface([self.width,self.height])
    self.rect = self.image.get_rect()
    self.x = x
    self.y = y
    self.image.fill(RED)

  def update(self,display,walls):
    self.rect.x = self.x - display_scroll[0]
    self.rect.y = self.y - display_scroll[1]

    pygame.draw.rect(display, WALL_GRAY, (self.rect.x, self.rect.y,self.width,self.height))



#Class definition of the tree object
class Tree(pygame.sprite.Sprite):
  def __init__(self, x, y, size, type):
    super().__init__()
    self.size = size
    self.image = pygame.Surface([self.size,self.size])
    self.rect = self.image.get_rect()
    self.x = x
    self.y = y 

    self.type = type

  def update(self,display,walls):

    self.rect.x = self.x - display_scroll[0] 
    self.rect.y = self.y - display_scroll[1]

    self.Shadow(self.rect.x,self.rect.y)

    if self.type == 1:
      display.blit(tree_1_img,(self.rect.x-13,self.rect.y-15))
      
  def Shadow(self,x,y):
    pygame.draw.ellipse(display, GRAY, [x+22,y+105,60,18])

def displayUpdate(a):
  temp = 0,0
  if a == 'o':
    temp = display_scroll
  else:
    display_scroll = temp

#Four functions for easiliy writing any message and button on screen
def text_to_button(msg, color, buttonx,buttony,buttonw,buttonh, size ="small"):
  textSurf, textRect = text_objects(msg,color,size)
  textRect.center = ((buttonx+(buttonw/2), buttony + (buttonh/2)))
  display.blit(textSurf, textRect)

#function for rendering text and fonts
def text_objects(text,color,size):
  if size == "small":
    textSurface = smallfont.render(text,True,color)
  elif size == "medium":
    textSurface = medfont.render(text,True,color)
  elif size == "large":
    textSurface = largefont.render(text,True,color)

  return textSurface, textSurface.get_rect()

#function for displaying a message on the screen
def message_to_screen(msg,color, y_displace = 0, size = "small"):
  #screen_text = font.render(msg, True, color)
  #gameDisplay.blit(screen_text, [display_width/3, display_height/2])
  textSurf, textRect = text_objects(msg,color,size)
  textRect.center = (display_width/2), (display_height/2) + y_displace
  display.blit(textSurf, textRect)

#defining user interface buttons and its actions
def button(text, x,y,w,h, inactive_color, active_color, action = None):
  cur = pygame.mouse.get_pos()
  click = pygame.mouse.get_pressed()

  if x + w > cur[0] > x and y + h > cur[1] > y:
    pygame.draw.rect(display, active_color, (x,y,w,h))

    if click[0] == 1 and action != None:
      if action == "quit":
        pygame.quit()
        quit()
      #endif

      if action == "controls":
        controls()
      #endif

      if action == "play":
        gameLoop()
      #endif

      if action == "menu":
        game_intro()
      #endif
    #endif

  else:
    pygame.draw.rect(display, inactive_color, (x,y,w,h))
  #endif

  text_to_button(text,BLACK,x,y,w,h)

#Defining the game intro with background, buttons that start the game, show controls and let the player quit respectively
def game_intro():

  intro = True

  while intro:

    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        pygame.quit()
        quit()
      

    display.blit(background,(0,0))

    message_to_screen("Lazar's Shooting Game!", BLACK, -146, 'large')
    message_to_screen("Lazar's Shooting Game!", RED, -150, 'large')
    message_to_screen('Description', BLACK, -70)
    message_to_screen('---', BLACK, -40)
    #message_to_screen('Press C to play, P to pause or Q to quit', black, 100)

    pygame.draw.rect(display, BLACK, (558,383,180,70))
    pygame.draw.rect(display, BLACK, (558,473,180,70))
    pygame.draw.rect(display, BLACK, (558,563,180,70))

    button('Play', 560,380,180,70, GREEN, LIGHT_GREEN, action='play')
    button('Controls', 560,470,180,70, YELLOW, LIGHT_YELLOW,action = 'controls')
    button('Quit', 560,560,180,70, RED, LIGHT_RED, action = 'quit')


    pygame.display.update()
    clock.tick(15)

#The controls screen as a method
def controls():

  controls = True

  while controls:

    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        pygame.quit()
        quit()
  
    display.blit(background,(0,0))
    message_to_screen('Your objective is to collect as many points as possible by destroying enemies      ', BLACK, -90)
    message_to_screen('Aim using the mouse to point your weapon and shoot with left click                    ', BLACK, -55)
    message_to_screen('Collect health packs in order to heal and ammo boxes to get more bullets            ', BLACK, -20)

    message_to_screen('>Movement - W,A,S,D                                                                                       ', BLACK, 55)
    message_to_screen('>Shooting - Mouse 1 (Left click)                                                                         ', BLACK, 90)
    message_to_screen('>Aiming - Mouse Pointer                                                                                    ', BLACK, 125)
    message_to_screen('>Switching weapons - 1,2,3                                                                               ', BLACK, 160)
 
    pygame.draw.rect(display, BLACK, (558,383,180,70))
    pygame.draw.rect(display, BLACK, (558,473,180,70))
    pygame.draw.rect(display, BLACK, (558,563,180,70))

    button('Play', 560,380,180,70, GREEN, LIGHT_GREEN, action='play')
    button('Controls', 560,470,180,70, YELLOW, LIGHT_YELLOW,action = 'controls')
    button('Quit', 560,560,180,70, RED, LIGHT_RED, action = 'quit')

    pygame.display.update()
    clock.tick(15)

def SpawnItems():
  pass

def SpawnEnemies():
  pass


#The x and y for displacing screen and sprites
display_scroll = [0,0]

# A list for the player, may seem unnecessary as there is only one, but it allows
# me to use pygames built in sprite group collision system
player_group = pygame.sprite.Group()

#Creating a list of walls
wall_group = pygame.sprite.Group()

# Creating a list of enemies
enemy_group = pygame.sprite.Group()

# Creating a list of all sprites 
all_sprites_group = pygame.sprite.Group() 

# The list of bullets
bullet_group = pygame.sprite.Group()

# The health item group
health_group = pygame.sprite.Group()
# The ammo item group
ammo_group = pygame.sprite.Group()

# The list of all trees
tree_group = pygame.sprite.Group()

wall_collide_group = pygame.sprite.Group()


#Creating the instance of the player
player = Player(640,360,64,64,320,'Rifle')
all_sprites_group.add(player)
player_group.add(player)

# random creation of enemies, just a placeholder for testing
for i in range(5):
  enemy = [Enemy(random.randint(1,1000),random.randint(1,1000),64,64,50,30)]
  all_sprites_group.add(enemy)
  enemy_group.add(enemy)
#next i


#making border walls
bottom_wall = Wall(-2000,1500,4700,700)
top_wall = Wall(-1500,-1500,3500,700)
right_wall = Wall(2000,-1500,700,3000)
left_wall = Wall(-2000,-1500,700,3000)
#all_sprites_group.add(mywall)
wall_group.add(bottom_wall)
wall_group.add(top_wall)
wall_group.add(right_wall)
wall_group.add(left_wall)



for i in range(5):
  myhealth = Item(random.randint(1,1000),random.randint(1,1000),32,'health')
  all_sprites_group.add(myhealth)
  health_group.add(myhealth)

for i in range(5):
  myammo = Item(random.randint(1,1000),random.randint(1,1000),32,'ammo')
  all_sprites_group.add(myammo)
  ammo_group.add(myammo)


for i in range(30):
  mytree = Tree(random.randint(-1000,1000),random.randint(-1000,1000),100,1)
  all_sprites_group.add(mytree)
  tree_group.add(mytree)


#The main game loop
def gameLoop():
  gameExit = False
  gameOver = False

  while not gameExit:
    display.blit(Ground_img,(-2000 - display_scroll[0],-2000 - display_scroll[1]))

    mouse_x, mouse_y = pygame.mouse.get_pos()

    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        pygame.quit()
      #endif

      if event.type == pygame.MOUSEBUTTONDOWN:
        if event.button == 1:
          bullet = (PlayerBullet(player.rect.x+35, player.rect.y+30, mouse_x, mouse_y,5))
          bullet_group.add(bullet)
          all_sprites_group.add(bullet)
          player.rifle_ammo -= 1
        #endif
      #endif

    #the center of the map
    pygame.draw.rect(display, WHITE, (100-display_scroll[0],100-display_scroll[1],16,16))


    #collision detection for enemies and player bulletsss
    enemy_hit_list = pygame.sprite.groupcollide(enemy_group, bullet_group, False, True)
    for enemy in enemy_hit_list:
      #pygame.draw.rect(display, RED, (enemy.rect.x,enemy.rect.y,32,32))
      enemy.hit()

    player_hit_list = pygame.sprite.groupcollide(player_group , enemy_group, False, False)
    for enemy in player_hit_list:
      player.Hit(30)
      #enemy.damage attribute instead of this 30

    health_got_list = pygame.sprite.groupcollide(player_group , health_group, False, player.health_needed)
    for item in health_got_list:
      myhealth.Use()

    ammo_got_list = pygame.sprite.groupcollide(player_group , ammo_group, False, True)
    for item in ammo_got_list:
      myammo.Use()

    tree_hit_list = pygame.sprite.groupcollide(tree_group,bullet_group, False, True)
    for bullet in tree_hit_list:
      pass

    # Updates all of the sprites on screen
    wall_group.update(display,wall_group)
    all_sprites_group.update(display,wall_group)


    # Tick the clock and update the display
    clock.tick(60)
    pygame.display.update()
  # endfunction

# Calling the game loop as well as start screen, 
#  added __main__ beacuse i want to use libraries with this main code
if __name__ == '__main__':
  game_intro()
  gameLoop()