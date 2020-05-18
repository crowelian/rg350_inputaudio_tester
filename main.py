#! /usr/bin/env python

# Default starting point of any PyGame project!
import sys
import time
import pygame
import pygame.locals
import os

APPNAME = "Harri's RG350 Game"
MAX_FRAMES_PS = 30

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
LIGHT_RED = (227, 32, 25)
GREEN = (0, 255, 0)
LIGHT_GREEN = (101, 168, 91)
BLUE = (0, 0, 255)
LIGHT_BLUE = (91, 121, 168)

BTN_TEXT_1 = (24, 24, 28)
INFO_TEXT = (240, 240, 240)

## FOR BG
r_value = 200
g_value = 255
b_value = 255


# OpenDingux SDL button mappings
# This site was helpful: https://www.creationkit.com/fallout4/index.php?title=DirectX_Scan_Codes
BTN_DPAD_UP = pygame.locals.K_UP
BTN_DPAD_DOWN = pygame.locals.K_DOWN
BTN_DPAD_LEFT = pygame.locals.K_LEFT
BTN_DPAD_RIGHT = pygame.locals.K_RIGHT
BTN_A = pygame.locals.K_LCTRL
BTN_B = pygame.locals.K_LALT
BTN_X = pygame.locals.K_SPACE
BTN_Y = pygame.locals.K_LSHIFT
BTN_START = pygame.locals.K_RETURN
BTN_SELECT = pygame.locals.K_ESCAPE
BTN_LEFT_SHOULDER = pygame.locals.K_TAB
BTN_RIGHT_SHOULDER = pygame.locals.K_BACKSPACE
BTN_HOLD = pygame.locals.K_PAUSE  # NOTE OpenDingux=hold_slide
#BTN_L2 = THIS HAS TO BE GOTTEN WITH SCANCODE 104 
#BTN_R2 = THIS HAS TO BE GOTTEN WITH SCANCODE 109
BTN_L3 = pygame.locals.K_KP_DIVIDE
BTN_R3 = pygame.locals.K_KP_PERIOD


### Player settings:
xP = 50
yP = 50
widthP = 30
heightP = 50
vel = 5
gameIsOn = False
oneTimeCheck = False

### Parallax settings
bg0x = 0
bg1x = 0
bg2x = 0
velbg0 = vel * 0.1
velbg1 = vel * + 0.5
velbg2 = vel * 0.8

ballx = -45
bally = 20
ballVel = vel * 2.5


### Images

# surface = pygame.Surface((100, 100), pygame.SRCALPHA)
# ballimg = pygame.image.load('img/ball1.png')

_image_library = {}

def get_image(path):
        global _image_library
        image = _image_library.get(path)
        if image == None:
                canonicalized_path = path.replace('/', os.sep).replace('\\', os.sep)
                image = pygame.image.load(canonicalized_path)
                _image_library[path] = image
        return image

def blit_alpha(target, source, location, opacity):
        x = location[0]
        y = location[1]
        temp = pygame.Surface((source.get_width(), source.get_height())).convert()
        temp.blit(target, (-x, -y))
        temp.blit(source, (0, 0))
        temp.set_alpha(opacity)        
        target.blit(temp, location)




### DEBUG
roundNum = 0
ALL_DEBUG = False
PLAYER_DEBUG = True





###
### PyGame INIT
###
pygame.init()

if ALL_DEBUG:
    print "Init pygame!"

### Init AUDIO
musicVolume = 0.4
audioVolume = 0.8
pygame.mixer.pre_init(frequency=22050, size=-16, channels=2, buffer=512)
pygame.mixer.init()
if ALL_DEBUG:
    print "Init Audio..."

#sound1=pygame.mixer.Sound("sound.wav")
#sound1.set_volume(1.0)

pygame.mixer.music.load('IntroScreen.wav')
pygame.mixer.music.set_volume(musicVolume)
###pygame.mixer.music.load('IntroScreen.mp3')
pygame.mixer.music.play(-1)
print 'AUDIO:' + str(pygame.mixer.get_init()) + ' volume: ' + str(pygame.mixer.music.get_volume())
# Init FONTS



def dropShadowText(screen, text, size, x, y, colour=(255,255,255), drop_colour=(128,128,128), font=None):
    # how much 'shadow distance' is best?
    dropshadow_offset = 1 + (size // 15)
    text_font = pygame.font.Font(font, size)
    # make the drop-shadow
    text_bitmap = text_font.render(text, True, drop_colour)
    screen.blit(text_bitmap, (x+dropshadow_offset, y+dropshadow_offset) )
    # make the overlay text
    text_bitmap = text_font.render(text, True, colour)
    screen.blit(text_bitmap, (x, y) )


font = pygame.font.Font('Titillium-Black.otf', 25)
font_light = pygame.font.Font('Titillium-Thin.otf', 15)
# title text 
text1 = font.render(APPNAME, True, BTN_TEXT_1)


# debug / brand text
text2 = font_light.render("softa.site", True, INFO_TEXT)
# pause text
textPause = font_light.render("PAUSED", True, INFO_TEXT)
 




# Set the width and height of the screen [width, height]
SCREEN_WIDTH = 320
SCREEN_HEIGHT = 240
size = (SCREEN_WIDTH, SCREEN_HEIGHT)
screen = pygame.display.set_mode(size)
if ALL_DEBUG:
    print "Set screen size"

pygame.display.set_caption(APPNAME)


# set icon
icon = pygame.image.load('icon.png')
pygame.display.set_icon(icon)


# Loop until the user clicks the close button.
done = False
 
# Used to manage how fast the screen updates
clock = pygame.time.Clock()
 
pressed_keys_unicode = "softa.site"
scanCode = "0"

# -------- Main Program Loop -----------
while not done:
    # --- Main event loop
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            # Debug the buttons on RG350
            if ALL_DEBUG:
                print event.unicode + str(event)
            pressed_keys_unicode = event.unicode + " | sc: " + str(event.scancode) + " | k: " + str(event.key)
            scanCode = str(event.scancode)
            # EMPTY the title screen text
            if text1 != "":
                text1 = font.render(APPNAME, True, BTN_TEXT_1)
            

        if event.type == pygame.QUIT:
            done = True # Quit
            pressed_keys_unicode = "EXIT via esc!"

        elif event.type == pygame.KEYDOWN:
                if event.key == BTN_SELECT:
                    text1 = font.render("SELECT", True, RED) 
                    pressed_keys_unicode = "EXIT via Select!"
                    done = True # Quit if select button pressed!
    ##### END OF while not DONE the MAIN GAME LOOP                
        

    

    
 
    ### --- Game logic should go here
    # Get the set of keys pressed and check for user input
    pressed_keys = pygame.key.get_pressed()

    # Player movement here:
    if pressed_keys[BTN_DPAD_UP]:
        if ALL_DEBUG:
            print "go up"
        text1 = font.render("UP", True, BTN_TEXT_1)
        if gameIsOn == False:
            musicVolume += 0.1
            pygame.mixer.music.set_volume(musicVolume)
            textPause = font_light.render("music:"+str(pygame.mixer.music.get_volume()), True, INFO_TEXT)
    if pressed_keys[BTN_DPAD_DOWN]:
        if ALL_DEBUG:
            print "go down"
        text1 = font.render("DOWN", True, BTN_TEXT_1)
        if gameIsOn == False:
            musicVolume -= 0.1
            pygame.mixer.music.set_volume(musicVolume)
            textPause = font_light.render("music:"+str(pygame.mixer.music.get_volume()), True, INFO_TEXT)
    if pressed_keys[BTN_DPAD_LEFT]:
        if ALL_DEBUG:
            print "go left"
        text1 = font.render("LEFT", True, BTN_TEXT_1)
        if gameIsOn:
            xP -= vel
            bg0x -= velbg0
            bg1x -= velbg1
            bg2x -= velbg2
            ballx -= ballVel

    if pressed_keys[BTN_DPAD_RIGHT]:
        if ALL_DEBUG:
            print "go right"
        text1 = font.render("RIGHT", True, BTN_TEXT_1)
        if gameIsOn:
            xP += vel
            bg0x += velbg0
            bg1x += velbg1
            bg2x += velbg2
            ballx += ballVel

    if pressed_keys[BTN_A]:
        if ALL_DEBUG:
            print "a button"
        text1 = font.render("A-button", True, BTN_TEXT_1)
    if pressed_keys[BTN_B]:
        if ALL_DEBUG:
            print "b button"
        text1 = font.render("B-button", True, BTN_TEXT_1)
    if pressed_keys[BTN_X]:
        if ALL_DEBUG:
            print "x button"
        text1 = font.render("X-button", True, BTN_TEXT_1)
    if pressed_keys[BTN_Y]:
        if ALL_DEBUG:
            print "y button"
        text1 = font.render("Y-button", True, BTN_TEXT_1)   
    if pressed_keys[BTN_START]:
        if ALL_DEBUG:
            print "start button"
        text1 = font.render("START", True, RED)

        
        if oneTimeCheck != True:
            if gameIsOn:
                gameIsOn = False
                print "paused"
                textPause = font_light.render("PAUSED", True, INFO_TEXT)
                pygame.mixer.music.stop()
                pygame.mixer.music.load('pause.wav')
                pygame.mixer.music.play(-1)

            elif gameIsOn != True:
                gameIsOn = True
                print "unPaused"
                textPause = font.render("", True, RED)
                pygame.mixer.music.stop()
                pygame.mixer.music.load('IntroScreen.wav')
                pygame.mixer.music.play(-1)
                
        oneTimeCheck = False
        time.sleep(.2)
        

    if pressed_keys[BTN_SELECT]:
        if ALL_DEBUG:
            print "select button"
        text1 = font.render("SELECT", True, RED) 
    if pressed_keys[BTN_LEFT_SHOULDER]:
        if ALL_DEBUG:
            print "L1 button"
        text1 = font.render("L1", True, LIGHT_BLUE)
    if pressed_keys[BTN_RIGHT_SHOULDER]:
        if ALL_DEBUG:
            print "R1 button"
        text1 = font.render("R1", True, LIGHT_BLUE)
    if scanCode == "104":
        if ALL_DEBUG:
            print "L2 button"
        text1 = font.render("L2", True, LIGHT_GREEN)
        scanCode = "0" # RESET scanCode
    if scanCode == "109":
        if ALL_DEBUG:
            print "R2 button"
        text1 = font.render("R2", True, LIGHT_GREEN)
        scanCode = "0" # RESET scanCode
    if pressed_keys[BTN_L3]:
        if ALL_DEBUG:
            print "L3 button"
        text1 = font.render("L3", True, LIGHT_BLUE)
    if pressed_keys[BTN_R3]:
        if ALL_DEBUG:
            print "R3 button"
        text1 = font.render("R3", True, LIGHT_BLUE)

    ### --- Screen-clearing code goes here
    

    # Here, we clear the screen to white. Don't put other drawing commands
    # above this, or they will be erased with this command.
 
    # If you want a background image, replace this clear with blit'ing the
    # background image.
    screen.fill(WHITE)
    
    ##background_color = (r_value, g_value, b_value)
    ##print "set bg color"
    
    ##screen.fill(background_color)
    ##if ALL_DEBUG:
        ##print "fill screen"
    

    ### --- Drawing code should go here
    screen.blit(get_image('img/bg1.png'), (0, 0))
    bg2 = blit_alpha(screen, get_image('img/bg2.png'), (bg0x, 0), 255)
    bg3 = blit_alpha(screen, get_image('img/bg3.png'), (bg1x, 0), 255)
    bg4 = blit_alpha(screen, get_image('img/bg4.png'), (bg2x, 0), 255)

    
    # Player 
    pygame.draw.rect(screen, (255,0,0), (xP, yP, widthP, heightP))  #This takes: window/surface, color, rect 

    # draw on top of player...
    blit_alpha(screen, get_image('img/ball1.png'), (ballx, bally), 220)

    # Test text!
    screen.blit(text1,
        ((SCREEN_WIDTH - text1.get_width())/ 2, (SCREEN_HEIGHT - text1.get_height())/ 2))
    text2 = font_light.render(pressed_keys_unicode, True, INFO_TEXT)
    screen.blit(text2,
        ((SCREEN_WIDTH - text2.get_width())/ 2, (SCREEN_HEIGHT - text2.get_height())))
    screen.blit(textPause,
    ((SCREEN_WIDTH - text2.get_width())/ 2, (0 + text2.get_height())))
 
    ### --- Go ahead and update the screen with what we've drawn.
    ##pygame.display.flip()
    ##print "flip screen"
    pygame.display.update() # This updates the screen so we can see our rectangle
    if ALL_DEBUG:
        print "update"
 
    if ALL_DEBUG:
        print "round: " + str(roundNum)
    roundNum += 1

    ### --- Limit to 60 frames per second
    clock.tick(MAX_FRAMES_PS)
 
# Close the window and quit.
pygame.quit()