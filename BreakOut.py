
import pygame, sys
from pygame.locals import *

SQUARE, CIRCLE = "square", "circle"
score = 0
FPS, timer = 60, 0

# GameObject class for all objects in game
class GameObject(pygame.sprite.Sprite):
    
    def __init__(self, left, top, width, height, shape, color, name):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.Surface([width, height])
 
        self.image.fill(color)
        
        self.name = name
        self.shape = shape

        self.dead = False
        
        self.top = top
        self.left = left
        self.width = width
        self.height = height
        
        self.color = color

        self.rect = self.image.get_rect()

        if self.shape == SQUARE:
            self.rect.x = left
            self.rect.y = top

        if self.shape == CIRCLE:
            self.image = pygame.image.load("img/glassball.png")
            self.image = pygame.transform.scale(self.image, (width, height))
            self.rect = self.image.get_rect()
            
            self.top = screen_size[1] - 50 - 20
            self.left = screen_size[0] // 2
            self.width = width

            self.rect.x = self.left
            self.rect.y = self.top
            
            self.speed_x = 6
            self.speed_y = 6

    # Deprecated now drawing with images
    def draw(self, color):
        
        if self.shape == SQUARE:
            pygame.draw.rect(screen, color, self.rect)
            
        elif self.shape == CIRCLE:
            pygame.draw.circle(screen, color, (self.left, self.top), self.width)
        
    # Updating the the properties of each GameObject
    def update(self):
        
        if not self.dead:
            
            if self.name == "player":
                
                if self.rect.left > screen_size[0] - self.width:
                    self.rect.left = screen_size[0] - self.width 
                elif self.rect.left < 0:
                    self.rect.left = 0
                
            elif self.name == "ball":
                
                if self.rect.left > screen_size[0] - self.width or self.rect.left < 0:
                    self.speed_x = -self.speed_x 
                elif self.rect.top < 0:
                    self.speed_y = -self.speed_y
                if self.rect.top > screen_size[1]:
                    self.dead = True
                    
                self.rect.top += self.speed_y
                if self.collision(sprites) or self.collision(player):
                    self.speed_y = -self.speed_y
                    
                    
                self.rect.left += self.speed_x
                if self.collision(sprites) or self.collision(player) :
                    self.speed_x = -self.speed_x


            #self.rect = pygame.Rect(self.left, self.top, self.width, self.height)
            #self.draw(self.color)

    # Detecting Collisions 
    def collision(self, ss):

        # With walls
        if isinstance(ss, pygame.sprite.RenderUpdates):
            for sp in ss:
                if self.is_collided_with(sp.rect):
                    global score
                    score += 10
                    ss.remove(sp)
                    return True
                
            return False

        # With player
        else:
            global FPS, timer
            
            if timer: timer -= 1
                
            elif self.is_collided_with(ss.rect):
                timer = 1 * FPS
                return True
            
            return False
       
    # Collision between two rects
    def is_collided_with(self, sprite):
        return self.rect.colliderect(sprite)
    
            
# initialize pygame  
pygame.init()

# width and height of the walls
w, h = 80, 20

# setting screen size
screen_size = 740, 600
pygame.display.set_mode(screen_size)

# setting screen window caption
pygame.display.set_caption("Break out")

# Making sprites group to render all at once
sprites = pygame.sprite.RenderUpdates()
all_sprites = pygame.sprite.Group()


# Getting screen surface
screen = pygame.display.get_surface()

# Background
bg = (0, 0, 0)
screen.fill(bg)

# Frames Per Second limit

fpsClock = pygame.time.Clock()


# Making walls GameObjects
for i in range(4):
    for y in range(7):
        wall = GameObject(25 + 100 * y, 25 + 50 * i, w, h,\
                          SQUARE, Color(90, 60, 10, 250), "gameObject" + str(i))
        #wall.draw(Color(0, 64, 64, 64))
        sprites.add(wall)
        #all_sprites.add(wall)

# Making player GameObject        
player = GameObject(screen_size[0] // 2 - (w + 30) // 2, screen_size[1] - 50, w + 30,\
                  h, SQUARE, Color(0, 66, 32, 200), "player")

all_sprites.add(player)

# Making ball GameObject
ball = GameObject(None, None, 10, 10, CIRCLE, Color(150, 48, 10, 10), "ball")
all_sprites.add(ball)

# make the mouse disappear when over the window
pygame.mouse.set_visible(0)
 
# This is a font we use to draw text on the screen
font = pygame.font.Font(None, 26)
 

# callback function to clear the screen
def clear_callback(surf, rect):
    surf.fill(bg, rect)

game_over = False

# Game Loop
while 1:
    
    fpsClock.tick(FPS)

    # Checking events
    for event in pygame.event.get():
        if event.type == QUIT:
            sys.exit()

    if(not game_over):

        # Checking key events
        keys = pygame.key.get_pressed()
    
        if keys[pygame.K_LEFT]:
            player.rect.left -= 12
        
        if keys[pygame.K_RIGHT]:
            player.rect.left += 12
 

        # Showing all sprites
        sprites.clear(screen, clear_callback)   
        all_sprites.clear(screen, clear_callback)

        sprites.update()
        all_sprites.update()

        sprites.draw(screen)
        all_sprites.draw(screen)

        # Checking if the game is over
        if ball.dead:
            screen.fill(bg, textpos)
            font = pygame.font.Font(None, 36)
            text = font.render("You Are Dead", True, (100, 50, 255))
            textpos = text.get_rect(center=(screen_size[0] // 2, screen_size[1] // 2 ))
            game_over = True
            

        elif not bool(sprites):
            screen.fill(bg, textpos)
            font = pygame.font.Font(None, 36)
            text = font.render("You Win", True, (100, 50, 255))
            textpos = text.get_rect(center=(screen_size[0] // 2, screen_size[1] // 2 ))
            game_over = True
            
        else:
            text = font.render("score = " + str(score), True, (0, 0, 255))
            textpos = text.get_rect(center=(70, screen_size[1] - 10))


        # Showing the text
        screen.fill(bg, textpos)
        screen.blit(text, textpos)

        # Updating the screen (new frame)
        pygame.display.update()
