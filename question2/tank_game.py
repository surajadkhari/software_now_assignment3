## https://github.com/rupin01-uni/softwarenow3.git
    
import pygame
import time
import random

pygame.init()

display_width = 800
display_height = 600

gameDisplay = pygame.display.set_mode((display_width, display_height))

#fire_sound = pygame.mixer.Sound("1.mp3")
#explosion_sound = pygame.mixer.Sound("1.mp3")

#pygame.mixer.music.load("1.mp3")
#pygame.mixer.music.play(-1)


pygame.display.set_caption('Fighter Tank')

icon = pygame.image.load("D:\Assignment_3_Group_124_SYD\ic.jpeg")
pygame.display.set_icon(icon)
#----------------------------------------colors----------------------------------------------
wheat=(245,222,179)

white = (255, 255, 255)
black = (0, 0, 0)
blue = (0,0,255)

red = (200, 0, 0)
light_red = (255, 0, 0)

yellow = (200, 200, 0)
light_yellow = (255, 255, 0)

green = (34, 177, 76)
light_green = (0, 255, 0)

#--------------------------------for picking current time for the frames per second----------------------
clock = pygame.time.Clock()
#--------------------------------geometry of tank and its turret------------------------------------------
tankWidth = 40
tankHeight = 20

turretWidth = 5
wheelWidth = 5

ground_height = 35
#--------------------------------------------fonts with size, for text_object function----------------
smallfont = pygame.font.SysFont("comicsansms", 25)
medfont = pygame.font.SysFont("comicsansms", 50)
largefont = pygame.font.SysFont("Yu Mincho Demibold", 85)
vsmallfont = pygame.font.SysFont("Yu Mincho Demibold", 25)

#--------------------------------------------defining score function----------------------------------
def score(score):
    text = smallfont.render("Score: " + str(score), True, white)
    gameDisplay.blit(text, [0, 0])

#---defining function to get the fonts and sizes assigned with them by size names by default size="small"--
def text_objects(text, color, size="small"):
    if size == "small":
        textSurface = smallfont.render(text, True, color)
    if size == "medium":
        textSurface = medfont.render(text, True, color)
    if size == "large":
        textSurface = largefont.render(text, True, color)
    if size == "vsmall":
        textSurface = vsmallfont.render(text, True, color)

    return textSurface, textSurface.get_rect()

#---------------------fuction for texts that has to appear over button----------------------------------------
def text_to_button(msg, color, buttonx, buttony, buttonwidth, buttonheight, size="vsmall"):
    textSurf, textRect = text_objects(msg, color, size)
    textRect.center = ((buttonx + (buttonwidth / 2)), buttony + (buttonheight / 2))
    gameDisplay.blit(textSurf, textRect)

#--------------------fuction for texts that has to appear over screen----------------------------------------
def message_to_screen(msg, color, y_displace=0, size="small"):
    textSurf, textRect = text_objects(msg, color, size)
    textRect.center = (int(display_width / 2), int(display_height / 2) + y_displace)
    gameDisplay.blit(textSurf, textRect)

#----------------------fuction for players tank , defining turrets positins and wheels dimensions------------
def tank(x, y, turPos):
    x = int(x)
    y = int(y)

    possibleTurrets = [(x - 27, y - 2),
                       (x - 26, y - 5),
                       (x - 25, y - 8),
                       (x - 23, y - 12),
                       (x - 20, y - 14),
                       (x - 18, y - 15),
                       (x - 15, y - 17),
                       (x - 13, y - 19),
                       (x - 11, y - 21)
                       ]

    pygame.draw.circle(gameDisplay, blue, (x, y), int(tankHeight / 2))
    pygame.draw.rect(gameDisplay, blue, (x - tankHeight, y, tankWidth, tankHeight))

    pygame.draw.line(gameDisplay, blue, (x, y), possibleTurrets[turPos], turretWidth)

    pygame.draw.circle(gameDisplay, blue, (x - 15, y + 20), wheelWidth)
    pygame.draw.circle(gameDisplay, blue, (x - 10, y + 20), wheelWidth)

    pygame.draw.circle(gameDisplay, blue, (x - 15, y + 20), wheelWidth)
    pygame.draw.circle(gameDisplay, blue, (x - 10, y + 20), wheelWidth)
    pygame.draw.circle(gameDisplay, blue, (x - 5, y + 20), wheelWidth)
    pygame.draw.circle(gameDisplay, blue, (x, y + 20), wheelWidth)
    pygame.draw.circle(gameDisplay, blue, (x + 5, y + 20), wheelWidth)
    pygame.draw.circle(gameDisplay, blue, (x + 10, y + 20), wheelWidth)
    pygame.draw.circle(gameDisplay, blue, (x + 15, y + 20), wheelWidth)

    return possibleTurrets[turPos]

#----------------------fuction for computers tank , defining turrets positins and wheels dimensions------------
def enemy_tank(x, y, turPos):
    x = int(x)
    y = int(y)

    possibleTurrets = [(x + 27, y - 2),
                       (x + 26, y - 5),
                       (x + 25, y - 8),
                       (x + 23, y - 12),
                       (x + 20, y - 14),
                       (x + 18, y - 15),
                       (x + 15, y - 17),
                       (x + 13, y - 19),
                       (x + 11, y - 21)
                       ]

    pygame.draw.circle(gameDisplay, red, (x, y), int(tankHeight / 2))
    pygame.draw.rect(gameDisplay, red, (x - tankHeight, y, tankWidth, tankHeight))

    pygame.draw.line(gameDisplay, red, (x, y), possibleTurrets[turPos], turretWidth)

    pygame.draw.circle(gameDisplay, red, (x - 15, y + 20), wheelWidth)
    pygame.draw.circle(gameDisplay, red, (x - 10, y + 20), wheelWidth)

    pygame.draw.circle(gameDisplay, red, (x - 15, y + 20), wheelWidth)
    pygame.draw.circle(gameDisplay, red, (x - 10, y + 20), wheelWidth)
    pygame.draw.circle(gameDisplay, red, (x - 5, y + 20), wheelWidth)
    pygame.draw.circle(gameDisplay, red, (x, y + 20), wheelWidth)
    pygame.draw.circle(gameDisplay, red, (x + 5, y + 20), wheelWidth)
    pygame.draw.circle(gameDisplay, red, (x + 10, y + 20), wheelWidth)
    pygame.draw.circle(gameDisplay, red, (x + 15, y + 20), wheelWidth)

    return possibleTurrets[turPos]

#-----------------------------------------Game control Screen------------------------------------------------
def game_controls():
    gcont = True

    while gcont:
        for event in pygame.event.get():
            # print(event)
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        gameDisplay.fill(black)
        message_to_screen("Controls", white, -100, size="large")
        message_to_screen("Fire: Spacebar", wheat, -30)
        message_to_screen("Move Turret: Up and Down arrows", wheat, 10)
        message_to_screen("Move Tank: Left and Right arrows", wheat, 50)
        message_to_screen("Press D to raise Power % AND Press A to lower Power % ", wheat, 140)
        message_to_screen("Pause: P", wheat, 90)

        button("Play", 150, 500, 100, 50, green, light_green, action="play")
        button("Main", 350, 500, 100, 50, yellow, light_yellow, action="main")
        button("Quit", 550, 500, 100, 50, red, light_red, action="quit")

        pygame.display.update()

        clock.tick(15)
