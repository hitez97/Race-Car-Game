import pygame
import time
import random

pygame.init()

pygame.mixer.music.load('Side_Steppin.wav')
pygame.mixer.music.play(-1)
crash_sound = pygame.mixer.Sound('crash.wav')

display_width = 800
display_height = 600
size = (display_width, display_height)

black = (0,0,0)
white = (255,255,255)
grey = (127,127,127)
gray = (159, 163, 168)
block_color = (0,0,0)
green = (0,200,0)
bright_green = (0,255,0)
red = (200,0,0)
bright_red = (255,0,0)

car_width = 73

gameDisplay = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption('Not That Most Wanted DELUXE')
clock = pygame.time.Clock()

carImg = pygame.image.load('racecar.png')
bgImg = pygame.image.load('bg.png')
#defining stripes
stripes = []
stripe_count = 20
stripe_x = 185
stripe_y = -10
stripe_width = 20
stripe_height = 80
space = 20
for i in range(stripe_count):
    stripes.append([385, stripe_y])
    stripe_y += stripe_height + space
#constructing main menu background
class Background(pygame.sprite.Sprite):
    def __init__(self, image_file, location):
        pygame.sprite.Sprite.__init__(self)  #call Sprite initializer
        self.image = pygame.image.load(image_file)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location


def quitgame():
    pygame.quit()
    quit()

def button(text,x,y,w,h,ic,ac,action = None):
    mouse = pygame.mouse.get_pos()

    click = pygame.mouse.get_pressed()

    if x < mouse[0] < x + w and y < mouse[1] < y + h:
        pygame.draw.rect(gameDisplay,ac, (x, y, w, h))
        if click[0] == 1 and action != None :
            action()
    else:
        pygame.draw.rect(gameDisplay, ic, (x, y, w, h))

    font = pygame.font.Font("freesansbold.ttf", 20)
    textSurf, textRect = text_objects(text, font)
    textRect.center = ((x + (w / 2)), (y + (h / 2)))
    gameDisplay.blit(textSurf, textRect)


def things_dodged(count):
    font = pygame.font.SysFont(None, 25)
    text = font.render("Score: "+str(count), True, black)
    gameDisplay.blit(text,(0,0))

def car(x,y):
    gameDisplay.blit(carImg,(x,y))

def things(thingx, thingy, thingw, thingh, color):
    pygame.draw.rect(gameDisplay, color, [thingx, thingy, thingw, thingh])

def text_objects(text, font):
    textSurface = font.render(text, True, white)
    return textSurface, textSurface.get_rect()

def message_display(text):
    largeText = pygame.font.Font('freesansbold.ttf',40)
    TextSurf, TextRect = text_objects(text, largeText)
    TextRect.center = ((display_width/2),(display_height/2))
    gameDisplay.blit(TextSurf, TextRect)

    pygame.display.update()

    time.sleep(2)
    game_intro()


def crash():
    pygame.mixer.Sound.play(crash_sound)
    pygame.mixer.music.stop()
    message_display('You Crashed')


def game_intro():
    intro = True

    while intro:
        for event in pygame.event.get():
            print(event)
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        gameDisplay.fill(grey)
        BackGround = Background('bg.png', [0,0])
        gameDisplay.blit(BackGround.image, BackGround.rect)

        largeText = pygame.font.Font('freesansbold.ttf', 60)
        TextSurf, TextRect = text_objects("Not that MOST WANTED", largeText)
        TextRect.center = ((display_width / 2), (display_height / 4))
        gameDisplay.blit(TextSurf, TextRect)


        button("Go",150,450,100,50,green,bright_green,game_loop)
        button("Quit", 550, 450, 100, 50, red, bright_red,quitgame)

        pygame.display.update()
        clock.tick(15)

def game_loop():
    x = (display_width * 0.45)
    y = (display_height * 0.8)

    x_change = 0
    y_change = 0

    thing_startx = random.randrange(0, display_width)
    thing_starty = -600
    thing_speed = 4
    thing_width = 100
    thing_height = 100
    thingCount = 1
    dodged = 0
    gameExit = False

    while not gameExit:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x_change = -5
                if event.key == pygame.K_RIGHT:
                    x_change = 5

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    x_change = 0
                    y_change = 0

        x += x_change
        y += y_change

        gameDisplay.fill(gray)

        things(thing_startx, thing_starty, thing_width, thing_height, block_color)
        # Draw the stripes
        for i in range(stripe_count):
            pygame.draw.rect(gameDisplay, white, [stripes[i][0], stripes[i][1], stripe_width, stripe_height])
        # Move the stripes
        for i in range(stripe_count):
            stripes[i][1] += 3
            if stripes[i][1] > size[1]:
                stripes[i][1] = -40 - stripe_height



        thing_starty += thing_speed
        car(x,y)
        things_dodged(dodged)

        if x > display_width - car_width or x < 0:
            crash()

        if thing_starty > display_height:
            thing_starty = 0 - thing_height
            thing_startx = random.randrange(0,display_width)
            dodged += 1
            thing_speed += .5
            thing_width += (dodged * .4)
            print(dodged)


        if y < thing_starty+thing_height:
            print('vertical crossover')

            if x > thing_startx and x < thing_startx + thing_width or x+car_width > thing_startx and x + car_width < thing_startx+thing_width:
                print('horizontal crossover')
                crash()


        pygame.display.update()
        clock.tick(60)

game_intro()
game_loop()
pygame.quit()
quit()