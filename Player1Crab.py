# for game win screen either make it 2x as big not 4x but keep space between the same but move it to the right a bit (add more to xpos) or make it centre depening on how many characters there are
#! make arena
# add grenades
# add random crab spawn locations at start of round (maybe make like 10 locations that it picks from)
# add stun/knockback for getting hit by gun
# add infinite range to bullets/ rework how bullets work
# revolver creates 5 bullets in a row from where shot
# add charge to throws
#! add gun spawning     use timerclock.roundtimer
#! add win screen
# add something when timer runs out
# if hold gun and try to walk down it causes an error




# Samurai Robo Crab Fighting by Rylie White

import pygame
import sys
import math
import random
pygame.init()
clock = pygame.time.Clock()

joysticks = []
for i in range(pygame.joystick.get_count()):
    joysticks.append(pygame.joystick.Joystick(i))   # initialise controller
for joystick in joysticks:
    joystick.init()
analog_keys = {0: 0, 1: 0, 2: 0, 3: 0, 4: -1, 5: -1}



## General Use Procedures and Functions

def getjoystickinputs(analog_keys):
    RT = False
    LT = False
    LeftHoriz = 0
    LeftVert = 0
    RightHoriz = analog_keys[2]
    RightVert = analog_keys[3]

    if analog_keys[0] < -0.4:
        LeftHoriz = -1
    elif analog_keys[0] > 0.4:
        LeftHoriz = 1

    if analog_keys[1] > 0.4:  # getting controller inputs
        LeftVert = -1  # for the sticks, -1 means it is pressed either left or down, 0 means neutral, and 1 means right or up.
    elif analog_keys[1] < -0.4:  # sticks have an integer value that scales from -1 to 1 depending on how much their pressed. 0.4 is the point...
        LeftVert = 1  # ...I chose to decide if the player is holding the stick in that direction

    if analog_keys[4] > 0.5:    # The trigger functions similarly so I again chose a point to decide if it is being pressed or not
        LT = True
    if analog_keys[5] > 0.5:
        RT = True
    return RT, LT, LeftHoriz, LeftVert, RightHoriz, RightVert

def render(image):
    screen.blit(pygame.transform.scale(image.img, (image.img.get_width() * 4, image.img.get_height() * 4)),
                (image.x * 4, image.y * 4))

class imgdata:
    def __init__(self, img, x, y):
        self.img = pygame.image.load(img)
        self.x = x
        self.y = y

def checkboundaries(x, y, halflength, halfwidth):
    if x < halfwidth + 4:
        x = halfwidth + 4
    if x > 1024 - halfwidth - 4:
        x = 1024 - halfwidth - 4
    if y < halflength + 4:
        y = halflength + 4
    if y > 960 - halflength - 4:
        y = 960 - halflength - 4
    return x, y

def getColour(crabcolours):
    colour = []
    for each in crabcolours:
        colour.append((255 - each) / 2.5)
    colour = (colour[0], colour[1], colour[2])
    return colour

def transform(image):
    image = pygame.transform.scale(image, (image.get_width() * 4, image.get_height() * 4))
    return image

def resetround(menu):
    menu = p1Score.checkwin(menu)
    menu = p2Score.checkwin(menu)
    i = len(bullet_group)
    for each in range(i):
        bullet_group.pop(0)
    i = len(gun_group)
    for each in range(i):
        gun_group.pop(0)
    crab.gun, crab2.gun = "none", "none"
    crab.spriteoffset, crab2.spriteoffset = 0, 0
    crab.akcounter, crab2.akcounter = 0, 0
    crab.x, crab2.x = 100, 900
    crab.y, crab2.y = 300, 300
    return menu

def winsfunction(wingame, menu):
    xdown = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.JOYBUTTONDOWN:
            xdown = True
        if event.type == pygame.JOYAXISMOTION:
            analog_keys[event.axis] = event.value  # gets all controller inputs that I want each frame
    joystickinputs = [xdown, getjoystickinputs(analog_keys)]
    cursor.update()
    cursor2.update()
    clocktimer.roundtimer -= 1
    screen.blit(wingame, (0, 0))
    if menu == "P1wins":
        P1nla.gamewindisplay()
    elif menu == "P2wins":
        P2nla.gamewindisplay()
    screen.blit(cursor.image, cursor.rect.topleft)
    screen.blit(cursor2.image, cursor2.rect.topleft)
    pygame.display.update()
    clock.tick(60)
    if clocktimer.roundtimer == 0:
        menu = "Title"
        p1Score.crabroundwins = 0
        p2Score.crabroundwins = 0
        clocktimer.timer = timerupdown.maxtimer
        for each in range(len(P1nla.tagletters)):
            P1nla.tagletters[each] = pygame.transform.scale(P1nla.tagletters[each], (
            P1nla.tagletters[each].get_width() / 4, P1nla.tagletters[each].get_height() / 4))
        for each in range(len(P2nla.tagletters)):
            P2nla.tagletters[each] = pygame.transform.scale(P2nla.tagletters[each], (
            P2nla.tagletters[each].get_width() / 4, P2nla.tagletters[each].get_height() / 4))
    return menu, joystickinputs




## Load Settings Objects


emptysettingsUI = pygame.image.load("emptySettingsUI.png")
emptysettingsUI = transform(emptysettingsUI)

image = pygame.image.load("SettingsThings.png")

class NumbersLetters():
    def __init__(self, type, value):
        super().__init__()
        self.type = type

        ## RGB Vals

        self.value = value
        self.numbers = []
        imgx = 2
        for each in range(10):
            blank = pygame.Surface((3, 5))
            blank.fill((1, 1, 1))
            blank.set_colorkey((1, 1, 1))
            blank.blit(image, (0, 0), (imgx, 2, 3, 5))
            blank = transform(blank)
            self.numbers.append(blank)
            imgx += 6

        ## Tags

        self.tag = ""
        self.tagletters = []
        imgx, imgy = 2, 10
        for each in range(26):
            blank = pygame.Surface((6, 8))
            blank.fill((1, 1, 1))
            blank.set_colorkey((1, 1, 1))
            blank.blit(image, (0, 0), (imgx, imgy, 6, 8))
            blank = transform(blank)
            self.tagletters.append(blank)
            imgx += 9

        ## RGB/Tag Buttons

        if self.type == "P2":
            self.blocks = []
            blockimg = pygame.image.load("Settings wierd thing.png")
            imgx = 0
            for each in range(2):
                block = pygame.Surface((31, 3))                         ## layer block thing that covers the top of the tags
                block.blit(blockimg, (imgx, 0, 31, 3))
                block = transform(block)
                self.blocks.append(block)
                imgx -= 32

        self.mode = "Tag"
        self.switch = []
        imgx, imgy = 0, 108
        for each in range(2):
            blank = pygame.Surface((13, 10))
            blank.fill((1, 1, 1))
            blank.set_colorkey((1, 1, 1))                       ## Tags that allow switching from tag to RGB mode and vice versa
            blank.blit(image, (0, 0), (imgx, imgy, 13, 10))
            blank = transform(blank)
            self.switch.append(blank)
            imgx += 18
            if self.type == "P2":
                for each in self.switch:
                    var = pygame.PixelArray(each)                   # default colour is blue for P1 so player 2 has to change the colour of their tags to pink
                    var.replace((83, 115, 164), (158, 99, 144))
        if self.type == "P1":
            xpos1, xpos2 = 4, 22
        elif self.type == "P2":
            xpos1, xpos2 = 221, 239
        self.rect1 = pygame.Rect(xpos1 * 4, 149 * 4, 13 * 4, 6 * 4)
        self.rect2 = pygame.Rect(xpos2 * 4, 149 * 4, 13 * 4, 7 * 4)

    def update(self, pressed):

        ## RGB Vals

        if self.type == "P1":
            xpos = 68
        elif self.type == "P2":
            xpos = 177
        ypos = 120
        counter = 0
        for each in self.value:
            screen.blit(self.numbers[int(each)], (xpos * 4, ypos * 4))
            xpos += 4
            counter += 1
            if counter % 3 == 0:
                ypos += 8
                xpos -= 12

        if len(self.value) == 9:
            valid = True
            counter = 0
            for each in range(3):
                part = self.value[counter] + self.value[counter + 1] + self.value[counter + 2]
                if int(part) > 255:
                    valid = False
                counter += 3
            if valid == True:
                if self.type == "P1":
                    crab.colour = (int(self.value[0:3]), int(self.value[3:6]), int(self.value[6:9]))
                elif self.type == "P2":
                    crab2.colour = (int(self.value[0:3]), int(self.value[3:6]), int(self.value[6:9]))


        ## Tags

        if self.type == "P1":
            xpos = 3
        elif self.type == "P2":
            xpos = 191
        ypos = 102
        for each in self.tag:
            each = each.lower()
            each = ord(each) - 97
            screen.blit(self.tagletters[int(each)], (xpos * 4, ypos * 4))
            xpos += 8

        ## RGB/Tag Buttons

        if self.type == "P1":
            xpos = 4
        elif self.type == "P2":
            xpos = 221
        ypos = 149
        if self.mode == "Tag":
            ypos -= 3
        screen.blit(self.switch[0], (xpos * 4, ypos * 4))
        xpos += 18
        ypos -= 3
        if self.mode == "Tag":
            ypos += 6
        screen.blit(self.switch[1], (xpos * 4, ypos * 4))

        if self.type == "P1":
            if pressed == True:
                if self.rect1.collidepoint((cursor.x, cursor.y)):
                    self.mode = "RGB"
                elif self.rect2.collidepoint((cursor.x, cursor.y)):
                    self.mode = "Tag"

        if self.type == "P2":
            if pressed == True:
                if self.rect1.collidepoint((cursor2.x, cursor2.y)):
                    self.mode = "RGB"
                elif self.rect2.collidepoint((cursor2.x, cursor2.y)):
                    self.mode = "Tag"
            screen.blit(self.blocks[0], (4 * 4, 146 * 4))  # layer that covers the top of the tags so it appears they get...
            screen.blit(self.blocks[1], (221 * 4, 146 * 4))  # ...pulled down from below the alphabet section

    def roundwindisplay(self):
        if self.type == "P1":
            xpos = 95
            ypos = 105
        elif self.type == "P2":
            xpos = 99
            ypos = 105                      # displays name at the end of a round
        for each in self.tag:
            each = each.lower()
            each = ord(each) - 97
            screen.blit(self.tagletters[int(each)], (xpos * 4, ypos * 4))
            xpos += 8

    def gamewindisplay(self):
        xpos = 4
        ypos = 90                      # displays name at the end of a round
        for each in self.tag:
            each = each.lower()
            each = ord(each) - 97
            screen.blit(self.tagletters[int(each)], (xpos * 4, ypos * 4))
            xpos += 32

P1nla = NumbersLetters("P1", "187067067")
P2nla = NumbersLetters("P2", "060194179")
P1nla.tag = "duck"
P2nla.tag = "gigachad"


class Alphabet():
    def __init__(self, type, x, y):
        super().__init__()
        self.type = type
        self.x = x
        self.y = y
        blank = pygame.Surface((7, 8))
        blank.fill((1, 1, 1))
        blank.set_colorkey((1, 1, 1))
        blank.blit(image, (0, 0), (self.x, self.y, 7, 8))
        blank = transform(blank)
        self.image = blank
        if self.type == "P1":
            self.y += 93
        elif self.type == "P2":
            self.x += 127
            self.y += 93
        self.x *= 4
        self.y *= 4
        self.rect = pygame.Rect(self.x + 4, self.y, 6 * 4, 8 * 4)

    def update(self, counter, pressed):
        screen.blit(self.image, (self.x, self.y))
        if self.type == "P1":
            if pressed == True:
                if P1nla.mode == "Tag":
                    if counter == 36:   ## backspace code
                        if len(P1nla.tag) != 0:
                            P1nla.tag = P1nla.tag.rstrip(P1nla.tag[-1])     ###### Make it so you can add numbers in name - do art
                    else:
                        if len(P1nla.tag) != 8:
                            if counter > 9:
                                counter = chr(counter + 87)     # inverse of ord code from earlier
                                P1nla.tag += str(counter)
                if P1nla.mode == "RGB":
                    if counter == 36:  ## backspace code
                        if len(P1nla.value) != 0:
                            P1nla.value = P1nla.value.rstrip(P1nla.value[-1])   #####                                                           problem - deletes all last values if theyre the same
                    if counter <= 9:
                        if len(P1nla.value) != 9:
                            P1nla.value += str(counter)
        if self.type == "P2":
            if pressed == True:
                if P2nla.mode == "Tag":
                    if counter == 36:   ## backspace code
                        if len(P2nla.tag) != 0:
                            P2nla.tag = P2nla.tag.rstrip(P2nla.tag[-1])     ###### Make it so you can add numbers in name - do art
                    else:
                        if len(P2nla.tag) != 8:
                            if counter > 9:
                                counter = chr(counter + 87)
                                P2nla.tag += str(counter)
                if P2nla.mode == "RGB":
                    if counter == 36:   ## backspace code
                        if len(P2nla.value) != 0:
                            P2nla.value = P2nla.value.rstrip(P2nla.value[-1])   #####                                                           problem - deletes all last values if theyre the same
                    if counter <= 9:
                        if len(P2nla.value) != 9:
                            P2nla.value += str(counter)

P1alpha = []
P2alpha = []
x, y, counter = 0, 21, 1
type = "P1"
for typenum in range(2):
    for each in range(37):
        letter = Alphabet(type, x, y)
        if typenum == 0:
            P1alpha.append(letter)
        elif typenum == 1:
            P2alpha.append(letter)
        x += 6
        counter += 1
        if type == "P1":
            if counter == 11 or counter == 31:
                x = 3
                y += 8
            elif counter == 21:
                x = 0
                y += 8              ##  where to display the letters of the alphabet
        elif type == "P2":
            if counter == 11:
                x = 65
                y += 8
            elif counter == 21:
                x = 68
                y += 8
            elif counter == 31:
                x = 89
                y += 8
            elif counter == 37:
                x = 83
    counter = 1
    x = 68
    y = 21
    type = "P2"


class Colours():
    def __init__(self, imgx, dif, colour, value):
        super().__init__()
        imgy = 63
        self.colour = colour
        self.image = pygame.Surface((15 - dif, 15))
        self.image.fill((1, 1, 1))
        self.image.set_colorkey((1, 1, 1))
        self.image.blit(image, (0, 0), (imgx, imgy, 15 - dif, 15))
        self.image = transform(self.image)
        self.value = value
        self.rect = self.image.get_rect()
        self.rect.topleft = ((imgx + 64) * 4, (imgy + 118) * 4)
        self.oldcolour = (0, 0, 0)

    def work(self, pressed, pressed2):
        colour = (0, 0, 0)
        if self.rect.collidepoint((cursor.x, cursor.y)) and crab.colour != self.colour:
            colour = (255, 255, 255)
            if pressed == True and crab2.colour != self.colour:
                colour = (17, 91, 198)
                crab.colour = self.colour
                P1nla.value = self.value
        if crab.colour == self.colour:
            colour = (17, 91, 198)
        else:
            if crab2.colour == self.colour:
                colour = (194, 30, 70)
        if self.oldcolour != colour:
            self.image = pygame.transform.scale(self.image, (self.image.get_width() / 4, self.image.get_height() / 4))
            var = pygame.PixelArray(self.image)
            var.replace(self.oldcolour, colour)
            self.image = transform(self.image)
            del var
        self.oldcolour = colour
        screen.blit(self.image, self.rect.topleft)

        if self.rect.collidepoint((cursor2.x, cursor2.y)) and crab2.colour != self.colour:
            colour = (255, 255, 255)
            if pressed2 == True and crab.colour != self.colour:
                colour = (17, 91, 198)
                crab2.colour = self.colour
                P2nla.value = self.value
        if crab.colour == self.colour:
            colour = (17, 91, 198)
        else:
            if crab.colour == self.colour:
                colour = (194, 30, 70)
        if self.oldcolour != colour:
            self.image = pygame.transform.scale(self.image, (self.image.get_width() / 4, self.image.get_height() / 4))
            var = pygame.PixelArray(self.image)
            var.replace(self.oldcolour, colour)
            self.image = transform(self.image)
            del var
        self.oldcolour = colour
        screen.blit(self.image, self.rect.topleft)

colourslist = [(187, 67, 67), (194, 193, 39), (65, 183, 34),  (60, 194, 179), (85, 48, 172), (168, 39, 194), (194, 39, 104)]
coloursvalueslist = [("187067067"), ("194193039"), ("065183034"), ("060194179"), ("085048172"), ("168039194"), ("194039104")]
colours_group = []
imgx, dif, counter = 0, 0, 0
for each in range(7):
    dif = 0
    if each == 2:
        dif = 1
    colour = Colours(imgx, dif, colourslist[counter], coloursvalueslist[counter])
    counter += 1
    imgx += 19
    if each == 3:
        imgx -= 1
    colours_group.append(colour)


class TimerUpDown():
    def __init__(self):
        super().__init__()
        for each in range(2):
            self.up = pygame.Rect(147 * 4, 52 * 4, 6 * 4, 7 * 4)
            self.down = pygame.Rect(141 * 4, 55 * 4, 6 * 4, 7 * 4)

    def work(self, pressed, pressed2):
        if (self.up.collidepoint((cursor.x, cursor.y)) and pressed == True) or (self.up.collidepoint((cursor2.x, cursor2.y)) and pressed2 == True):
            if clocktimer.timer % 100 == 0:
                clocktimer.timer -= 40
            clocktimer.timer += 70
        if (self.down.collidepoint((cursor.x, cursor.y)) and pressed == True) or (self.down.collidepoint((cursor2.x, cursor2.y)) and pressed2 == True):
            clocktimer.timer -= 30
        self.maxtimer = clocktimer.timer

timerupdown = TimerUpDown()


class MaxRoundUpDown():
    def __init__(self):
        super().__init__()
        for each in range(2):
            self.up = pygame.Rect(223 * 4, 36 * 4, 9 * 4, 9 * 4)
            self.down = pygame.Rect(223 * 4, 50 * 4, 9 * 4, 9 * 4)

    def work(self, pressed, pressed2):
        if (self.up.collidepoint((cursor.x, cursor.y)) and pressed == True) or (self.up.collidepoint((cursor2.x, cursor2.y)) and pressed2 == True):
            maxrounds.crabroundwins += 1
        if (self.down.collidepoint((cursor.x, cursor.y)) and pressed == True) or (self.down.collidepoint((cursor2.x, cursor2.y)) and pressed2 == True):
            maxrounds.crabroundwins -= 1

maxroundupdown = MaxRoundUpDown()


class GunOnOff():
    def __init__(self):
        self.onoff = ["0", "0", "0", "0"]
        self.gunlist = []
        self.sprites = []
        self.rects = []
        for each in range(4):       # set up the sprites for the 4 weapons
            x = 0
            for i in range(2):
                blank = pygame.Surface((6, 8))
                blank.fill((1, 1, 1))
                blank.set_colorkey((1, 1, 1))
                blank.blit(image, (0, 0), (x, 54, 6, 8))    # set up on and off sprite for each weapon
                blank = transform(blank)
                self.sprites.append(blank)
                x += 7
            if each == 0:
                rect = pygame.Rect(35 * 4, 38 * 4, 6 * 4, 8 * 4)
            elif each == 1:
                rect = pygame.Rect(63 * 4, 38 * 4, 6 * 4, 8 * 4)
            elif each == 2:
                rect = pygame.Rect(35 * 4, 54 * 4, 6 * 4, 8 * 4)
            elif each == 3:
                rect = pygame.Rect(63 * 4, 54 * 4, 6 * 4, 8 * 4)
            self.rects.append(rect)
            self.gunlist.append(self.sprites)

    def work(self, pressed, pressed2):
        for each in range(4):
            if (self.rects[each].collidepoint((cursor.x, cursor.y)) and pressed == True) or (self.rects[each].collidepoint((cursor2.x, cursor2.y)) and pressed2 == True):
                if self.onoff[each] == "0":
                    self.onoff[each] = "1"
                elif self.onoff[each] == "1":   # turn the weapon on or off if it is pressed
                    self.onoff[each] = "0"
            if each == 0:
                screen.blit(self.gunlist[each][int((self.onoff[each]))], (35 * 4,  38 * 4))
            elif each == 1:
                screen.blit(self.gunlist[each][int((self.onoff[each]))], (63 * 4, 38 * 4))
            elif each == 2:
                screen.blit(self.gunlist[each][int((self.onoff[each]))], (35 * 4, 54 * 4))
            elif each == 3:
                screen.blit(self.gunlist[each][int((self.onoff[each]))], (63 * 4, 54 * 4))

gunonoff = GunOnOff()


class ExitButton():
    def __init__(self):
        super().__init__()
        self.images = []
        x = 0
        for each in range(3):
            blank = pygame.Surface((17, 18))
            blank.fill((1, 1, 1))
            blank.set_colorkey((1, 1, 1))
            blank.blit(image, (0, 0), (x, 119, 17, 18))
            blank = transform(blank)
            self.rect = blank.get_rect()
            self.images.append(blank)
            x += 18
        self.exit = "none"
        self.menucounter = 0

    def display(self, pressed, pressed2):
        if (self.rect.collidepoint(cursor.x, cursor.y) and pressed == True) or self.exit == "P1":
            screen.blit(self.images[1], (0, 0))
            self.exit = "P1"
            self.menucounter += 0.12
        elif (self.rect.collidepoint(cursor2.x, cursor2.y) and pressed2 == True) or self.exit == "P2":
            screen.blit(self.images[2], (0, 0))
            self.exit = "P2"
            self.menucounter += 0.12
        else:
            screen.blit(self.images[0], (0, 0))
        return self.menucounter

exitbutton = ExitButton()




## Load Game objects


class Crab():
    def __init__(self, x, y, colour, crabtype):
        super().__init__()
        self.crabtype = crabtype
        self.keys = pygame.key.get_pressed()
        self.gun = "none"
        self.canshoot = 0
        self.maxshoot = 1
        self.akcounter = 0
        self.throwlagcounter = 0
        self.grabpressable = True
        self.dodgeroll = 0
        self.dodgerolldirection = 0
        self.invunerable = 0
        self.velocity = 8
        self.halflength = 28
        self.halfwidth = 28
        self.x = x
        self.y = y
        self.colour = colour
        del colour
        image = pygame.image.load("CrabSpriteSheet.png")
        self.spriteoffset = 0
        self.sprites = []
        imgposx = 1
        imgposy = 1
        for each in range(2):
            blank = pygame.Surface((25, 25))
            blank.fill((1,1,1))
            blank.set_colorkey((1, 1, 1))
            blank.blit(image, (0, 0), (imgposx, imgposy, 25, 25))
            blank = transform(blank)
            self.sprites.append(blank)
            imgposx += 27
        for each in range(5):                                           ## Getting sprites
            imgposx = 1
            imgposy += 27
            for each in range(3):
                blank = pygame.Surface((25, 25))
                blank.fill((1, 1, 1))
                blank.set_colorkey((1, 1, 1))
                blank.blit(image, (0, 0), (imgposx, imgposy, 25, 25))
                blank = transform(blank)
                self.sprites.append(blank)
                imgposx += 27
        for each in self.sprites:
            var = pygame.PixelArray(each)
            var.replace((187, 67, 67), self.colour)         ## Colour
            del var
        self.currentsprite = 0
        self.image = self.sprites[self.currentsprite]
        self.rect = pygame.Rect((0, 0), (0, 0))                             ## Used in rotation
        self.collisionrect = pygame.Rect((self.x, self.y), (40, 40))        ## Used in bullet collision

    def colourswitch(self):
        sprites = []
        for each in self.sprites:
            each = pygame.transform.scale(each, (each.get_width() / 4, each.get_height() / 4))
            var = pygame.PixelArray(each)
            if self.crabtype == "P1":
                var.replace(p1CrabPortrait.lightcrabcolour, self.colour)
            elif self.crabtype == "P2":
                var.replace(p2CrabPortrait.lightcrabcolour, self.colour)
            del var
            each = transform(each)
            sprites.append(each)
        self.sprites = sprites

    def animation(self):
        self.currentsprite += 0.05
        if self.dodgeroll != 0:
            if self.dodgeroll > 0.7:
                self.currentsprite = 2
            elif self.dodgeroll > 0.4:
                self.currentsprite = 3
            elif self.dodgeroll > 0.05:     ## animation for dodge roll
                self.currentsprite = 4
            else:
                self.currentsprite = 0
        else:
            if self.currentsprite >= self.spriteoffset + 2 or self.currentsprite < self.spriteoffset:   ## loops the next 2 frames because crab holding nothing is...
                self.currentsprite = self.spriteoffset      #...earlier on in the sprite list than the crab holding a shotgun but they're still in the same list for example
        self.image = self.sprites[int(self.currentsprite)]
        self.image = pygame.transform.scale(self.image, (self.image.get_width() / 4, self.image.get_height() / 4))
        var = pygame.PixelArray(self.image)
        colour = (self.colour[0]/3, self.colour[1]/3, self.colour[2]/3)
        if self.canshoot != 0 and self.dodgeroll <= 0:
            var.replace((0, 0, 0), (colour))    # change border colour while in gun lag
        else:
            var.replace((colour), (0, 0, 0))
        self.image = transform(self.image)

    def rotate(self):
        if self.crabtype == "P1":
            cursorx, cursory = cursor.rect.center
        elif self.crabtype == "P2":
            cursorx, cursory = cursor2.x, cursor2.y ## Gets the coordinates from correct cursor
        dx = self.x - cursorx
        dy = cursory - self.y  # reverse because 0,0 is in the top left instead of the bottom left
        rads = math.atan2(dy, dx)
        self.angle = math.degrees(rads)
        if self.dodgeroll > 0:
            self.angle += 112.5  # offsets "pizza slices" so they don't go along the x and y axis.
            if self.angle > 180:
                self.angle -= 360
            if self.angle < 0:
                self.angle -= 45
            self.angle /= 45
            self.angle = int(self.angle)  # turns the angles into integer values -4 to 3...
            self.angle *= 45  # ... to multiply to 45 to get angles -180 to 135 with 45 degree differences because...
        else:
            self.angle += 90
            if self.angle > 180:
                self.angle -= 360
        self.rotatedimage = pygame.transform.rotate(self.image, self.angle)  # ...the sprites only work in 8 directions
        self.newrect = self.rotatedimage.get_rect(center=self.image.get_rect(center=self.rect.center).center)
        self.image = self.rotatedimage
        self.rect = self.newrect

    def movement(self):
        self.keys = pygame.key.get_pressed()
        if self.dodgeroll == 0:
            counter = 0
            if self.crabtype == "P1":
                if self.keys[pygame.K_a] or self.keys[pygame.K_d]:
                    counter += 1
                if self.keys[pygame.K_w] or self.keys[pygame.K_s]:  # adjusts speed for moving diagonally
                    counter += 1
            elif self.crabtype == "P2":
                if joystickinputs[1][2] == -1 or joystickinputs[1][2] == 1:
                    counter += 1
                if joystickinputs[1][3] == -1 or joystickinputs[1][3] == 1:     ## adjusts speed for moving diagonally
                    counter += 1
            if counter >= 2:
                self.velocity = 3
            else:
                self.velocity = 4

            if self.gun == "none" or self.throwlagcounter < 20:      #if want move fast when pick up gun
                self.velocity *= 2
            else:
                if self.canshoot > 0:
                    self.velocity /= 3
                else:
                    self.velocity /= 1.4

            if self.crabtype == "P1":
                if self.keys[pygame.K_a]:
                    self.x -= self.velocity
                if self.keys[pygame.K_d]:
                    self.x += self.velocity
                if self.keys[pygame.K_w]:
                    self.y -= self.velocity
                if self.keys[pygame.K_s]:
                    self.y += self.velocity
            elif self.crabtype == "P2":
                if joystickinputs[1][2] == -1:
                    self.x -= self.velocity
                if joystickinputs[1][2] == 1:
                    self.x += self.velocity
                if joystickinputs[1][3] == 1:
                    self.y -= self.velocity
                if joystickinputs[1][3] == -1:
                    self.y += self.velocity
        self.x, self.y = checkboundaries(self.x, self.y, self.halflength, self.halfwidth)
        if self.y > 662 - self.halflength - 4:
            self.y = 662 - self.halflength - 4
        self.rect.center = (self.x, self.y)
        self.collisionrect.center = (self.x, self.y)

    def roll(self):
        if self.invunerable > 0:
            self.invunerable -= 1
        if self.crabtype == "P1":
            if self.dodgeroll == 0 and self.keys[pygame.K_SPACE]:
                self.invunerable = 30
                counter = 0
                self.dodgeroll = 1
                self.direction = self.keys
                self.velocity = 12
                if self.direction[pygame.K_a] or self.direction[pygame.K_d]:
                    counter += 1
                if self.direction[pygame.K_w] or self.direction[pygame.K_s]:
                    counter += 1
                if counter >= 2:
                    self.velocity = 9
            if self.dodgeroll > 0.7:
                if self.direction[pygame.K_a]:
                    self.x -= self.velocity
                if self.direction[pygame.K_d]:
                    self.x += self.velocity
                if self.direction[pygame.K_w]:
                    self.y -= self.velocity
                if self.direction[pygame.K_s]:
                    self.y += self.velocity
        if self.crabtype == "P2":
            if self.dodgeroll == 0 and joystickinputs[0] == True:
                self.dodgerolldirection = joystickinputs
                self.invunerable = 30
                counter = 0
                self.dodgeroll = 1
                self.direction = self.keys
                self.velocity = 12
                if joystickinputs[1][2] == -1 or joystickinputs[1][2] == 1:
                    counter += 1
                if joystickinputs[1][3] == -1 or joystickinputs[1][3] == 1:  ## adjusts speed for moving diagonally
                    counter += 1
                if counter >= 2:
                    self.velocity = 9
            if self.dodgeroll > 0.7:
                if self.dodgerolldirection[1][2] == -1:
                    self.x -= self.velocity
                if self.dodgerolldirection[1][2] == 1:
                    self.x += self.velocity
                if self.dodgerolldirection[1][3] == 1:
                    self.y -= self.velocity
                if self.dodgerolldirection[1][3] == -1:
                    self.y += self.velocity
        self.dodgeroll -= 0.02
        if self.dodgeroll < 0:
            self.dodgeroll = 0
        else:
            self.canshoot = 0.1

    def gunlag(self):
        if self.throwlagcounter < 100:  # used to maintain speed boost for 20 frames after gun is picked up
            self.throwlagcounter += 1

        if self.grabpressable == False:
            if self.crabtype == "P1":
                if not self.keys[pygame.K_e]:
                    self.grabpressable = True
            if self.crabtype == "P2":
                if not joystickinputs[1][1]:
                    self.grabpressable = True

    def shoot(self):
        shoot = False
        if self.crabtype == "P1":
            if event.button == 1 and self.canshoot <= 0 and self.gun != "none":  # shooting
                shoot = True
                cursor.currentsprite = 2
        elif self.crabtype == "P2":
            if self.canshoot <= 0 and self.gun != "none":  # shooting
                shoot = True
                cursor2.currentsprite = 2
        if shoot == True:
            if self.gun == "shotgun":
                self.canshoot = 4
                for each in range(5):
                    ran = random.randint(-35, 35)
                    offset = ran / 100
                    bullet = Bullet(offset, 12, self.crabtype)
                    bullet_group.append(bullet)
            elif self.gun == "pistol":
                self.canshoot = 1.25
                ran = random.randint(-10, 10)
                offset = ran / 100
                bullet = Bullet(offset, 16, self.crabtype)
                bullet_group.append(bullet)
            elif self.gun == "revolver":
                self.canshoot = 4
                offset = - 0.02
                for each in range(3):
                    bullet = Bullet(offset, 100, self.crabtype)
                    bullet.speed += 15  # maybe make each bullet a different speed
                    bullet_group.append(bullet)
                    offset += 0.02
            elif self.gun == "ak":
                if self.akcounter == 0:
                    self.akcounter = 25
                self.canshoot = 1
                ran = random.randint(-20, 20)
                offset = ran / 100
                bullet = Bullet(offset, 20, self.crabtype)
                bullet_group.append(bullet)
            self.maxshoot = self.canshoot


class Gun():
    def __init__(self, guntype, x, y):
        self.force = 0
        self.grabbed = "0"
        self.lastgrabbed = "0"
        self.guntype = guntype
        if guntype == 1:
            self.guntype = "pistol"
        elif guntype == 2:
            self.guntype = "shotgun"
        elif guntype == 3:
            self.guntype = "revolver"
        elif guntype == 4:
            self.guntype = "ak"
        self.dif = 0
        self.x = x
        self.y = y
        self.image = pygame.image.load("Guns.png")
        blank = pygame.Surface((21, 10))
        blank.fill((1, 1, 1))
        blank.set_colorkey((1, 1, 1))
        if self.guntype == "pistol":
            blank.blit(self.image, (0, 0), (0, 0, 21, 10))
        if self.guntype == "shotgun":
            blank.blit(self.image, (0, 0), (22, 0, 21, 10))
        if self.guntype == "revolver":
            blank.blit(self.image, (0, 0), (0, 11, 21, 10))
        if self.guntype == "ak":
            blank.blit(self.image, (0, 0), (22, 11, 21, 10))
        self.image = blank
        self.image = transform(self.image)
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)

    def update(self):
        if self.grabbed == "P1":
            self.x = crab.x
            self.y = crab.y
        if self.grabbed == "P2":
            self.x = crab2.x
            self.y = crab2.y
        self.rect.center = (self.x, self.y)

    def grab(self):
        if crab.keys[pygame.K_e] and crab.grabpressable == True:
            self.dif = math.sqrt((abs(self.x - crab.x)) ** 2 + (abs(self.y - crab.y)) ** 2)
            if self.dif < 100 and self.grabbed == "0" and crab.gun == "none":
                closest = True
                for each in gun_group:
                    if each.grabbed == 0:
                        if each.dif < self.dif:
                            closest = False
                if closest == True:
                    crab.grabpressable = False
                    crab.gun = self.guntype
                    crab.throwlagcounter = 0
                    self.grabbed = "P1"
                    self.lastgrabbed = "P1"
                del closest
            elif self.grabbed == "P1" and crab.canshoot <= 0:
                crab.grabpressable = False
                crab.gun = "none"
                self.angle = math.atan2(self.y - cursor.y, self.x - cursor.x)
                self.grabbed = "0"
                self.force = 25
            if crab.gun == "pistol":
                crab.spriteoffset = 5
            elif crab.gun == "ak":
                crab.spriteoffset = 8
            elif crab.gun == "revolver":
                crab.spriteoffset = 11      # which sprites to use
            elif crab.gun == "shotgun":
                crab.spriteoffset = 14
            elif crab.gun == "none":
                crab.spriteoffset = 0

        #if grab button on PS4 pressed:
        if joystickinputs[1][1] and crab2.grabpressable == True:
            self.dif = math.sqrt((abs(self.x - crab2.x)) ** 2 + (abs(self.y - crab2.y)) ** 2)
            if self.dif < 100 and self.grabbed == "0" and crab2.gun == "none":
                closest = True
                for each in gun_group:
                    if each.grabbed == 0:
                        if each.dif < self.dif:
                            closest = False
                if closest == True:
                    crab2.grabpressable = False
                    crab2.gun = self.guntype
                    crab2.throwlagcounter = 0
                    self.grabbed = "P2"
                    self.lastgrabbed = "P2"
                del closest
            elif self.grabbed == "P2" and crab2.canshoot <= 0:
                crab2.grabpressable = False
                crab2.gun = "none"
                self.grabbed = "0"
                self.force = 25
                self.angle = math.atan2(self.y - cursor2.y, self.x - cursor2.x) #### CURSOR 2 SHIT DEAL WITH THIS
            if crab2.gun == "pistol":
                crab2.spriteoffset = 5
            elif crab2.gun == "ak":
                crab2.spriteoffset = 8
            elif crab2.gun == "revolver":
                crab2.spriteoffset = 11  # which sprites to use
            elif crab2.gun == "shotgun":
                crab2.spriteoffset = 14
            elif crab2.gun == "none":
                crab2.spriteoffset = 0

    def thrown(self):
        if self.force > 0:
            self.force -= 0.5
            self.x_vel = math.cos(self.angle) * self.force
            self.y_vel = math.sin(self.angle) * self.force
            self.x -= self.x_vel
            self.y -= self.y_vel
        if self.y < 0 + 8 or self.y > 652:
            self.force += 0.6
            self.angle *= -1
        if self.x < 0 + 8 or self.x > 1024 - 8:
            self.force += 0.6
            self.angle = 3 - self.angle


class Cursor():
    def __init__(self, cursortype):
        super().__init__()
        self.x = 0
        self.y = 0
        self.cursortype = cursortype
        self.sprites = []
        if self.cursortype == "P1":
            self.sprites.append(pygame.image.load("CrosshairF1.png"))
            self.sprites.append(pygame.image.load("CrosshairF2.png"))
            self.sprites.append(pygame.image.load("CrosshairFire.png"))
        elif self.cursortype == "P2":
            self.sprites.append(pygame.image.load("Crosshair2F1.png"))
            self.sprites.append(pygame.image.load("Crosshair2F2.png"))
            self.sprites.append(pygame.image.load("Crosshair2Fire.png"))
        for i in range(len(self.sprites)):
            self.sprites[i] = transform(self.sprites[i])
        self.currentsprite = 0
        self.image = self.sprites[int(self.currentsprite)]
        self.rect = self.image.get_rect()
    def update(self):
        self.currentsprite += 0.03
        if (self.currentsprite > 2 and self.currentsprite < 2 + 0.03) or self.currentsprite > 2.5:
            self.currentsprite = 0
        if self.cursortype == "P1":
            self.x, self.y = pygame.mouse.get_pos()         # work out x and y for P1 cursor
        elif self.cursortype == "P2" and menu == "Game":
            if joystickinputs[1][4] > 0.1 or joystickinputs[1][4] < -0.1:
                self.x = crab2.x + joystickinputs[1][4] * 150                   # work out x and y for P2 cursor during gameplay
            if joystickinputs[1][5] > 0.1 or joystickinputs[1][5] < -0.1:
                self.y = crab2.y + joystickinputs[1][5] * 150
        elif self.cursortype == "P2" and menu != "Game":
            if joystickinputs[1][4] > 0.1 or joystickinputs[1][4] < -0.1:
                self.x += joystickinputs[1][4] * 8                              # work out x and y for P2 cursor
            if joystickinputs[1][5] > 0.1 or joystickinputs[1][5] < -0.1:
                self.y += joystickinputs[1][5] * 8
        self.x, self.y = checkboundaries(self.x, self.y, 0, 0)
        self.image = self.sprites[int(self.currentsprite)]
        self.rect.center = (self.x, self.y)


class Bullet():
    def __init__(self, offset, dist, crabtype):
        super().__init__()
        self.maxdist = dist
        self.offset = offset
        self.crabtype = crabtype
        if crabtype == "P1":
            self.xpos, self.ypos = crab.rect.center
            self.angle = math.atan2(self.ypos - cursor.y, self.xpos - cursor.x)
        if crabtype == "P2":                                                            ## calculates angle
            self.xpos, self.ypos = crab2.rect.center
            self.angle = math.atan2(self.ypos - cursor2.y, self.xpos - cursor2.x)
        self.dist = 0
        self.speed = 30
        self.angle += self.offset
        self.image = pygame.image.load("Bullet.png")
        self.image = transform(self.image)
        self.rect = self.image.get_rect()
        self.rect.center = (self.xpos, self.ypos)
        # work out angle

    def update(self, counter):
        self.dist += 1
        self.x_vel = math.cos(self.angle) * self.speed
        self.y_vel = math.sin(self.angle) * self.speed
        self.xpos -= self.x_vel
        self.ypos -= self.y_vel
        self.rect.center = (self.xpos, self.ypos)
        if self.dist > self.maxdist:
            bullet_group.pop(counter)
        # move a bit based on angle
        # measure distance

    def collision(self):
        if self.crabtype == "P1" and self.rect.colliderect(crab2.collisionrect) and crab2.invunerable == 0:
            clocktimer.roundtimer = -60
            p1Score.crabroundwins += 1
            return True, "blue"
        elif self.crabtype == "P2" and self.rect.colliderect(crab.collisionrect) and crab.invunerable == 0:  ## few seconds to display winner before resetting to the next round
            clocktimer.roundtimer = -60
            p2Score.crabroundwins += 1
            return True, "pink"
        else:
            return False, "0"



class Timer():
    def __init__(self):
        self.sprites = []
        self.timer = 2000
        timerupdown.maxtimer = self.timer
        self.roundtimer = 0
        image = pygame.image.load("numbers.png")
        xpos = 1
        ypos = 29
        for each in range(10):
            blank = pygame.Surface((8, 12))
            blank.set_colorkey((0, 0, 0))
            blank.blit(image, (0, 0), (xpos, ypos, 8, 12))
            blank = transform(blank)
            self.sprites.append(blank)
            xpos += 9

    def work(self):
        if menu == "Game":
            self.timer -= 0.05  # 0.05  # 6 mins 40 secs to count down from 2000 i think
        if self.timer < 0:
            self.timer = 0
        stringtimer = str(int(self.timer))
        if int(stringtimer[len(stringtimer)-2]) >= 6 and len(stringtimer) > 1:
            self.timer += 60    #  reverse the functions here...
            self.timer -= 100   #  ... and here to make the clock count up/down
        stringtimer = str(int(self.timer))
        while len(stringtimer) < 4:
            stringtimer = "0" + stringtimer
        if menu == "Game":
            screen.blit(self.sprites[int(stringtimer[-1])], (138 * 4, 227 * 4))
            screen.blit(self.sprites[int(stringtimer[-2])], (130 * 4, 227 * 4))
            screen.blit(self.sprites[int(stringtimer[-3])], (118 * 4, 227 * 4))
            screen.blit(self.sprites[int(stringtimer[-4])], (110 * 4, 227 * 4))
        elif menu == "Settings":
            screen.blit(self.sprites[int(stringtimer[-1])], (131 * 4, 51 * 4))
            screen.blit(self.sprites[int(stringtimer[-2])], (123 * 4, 51 * 4))
            screen.blit(self.sprites[int(stringtimer[-3])], (111 * 4, 51 * 4))
            screen.blit(self.sprites[int(stringtimer[-4])], (103 * 4, 51 * 4))

    def gunSpawn(self):
        if self.roundtimer % 600 == 0:  # gun spawn timings here
            a = random.randint(1, 4)
            b = random.randint(8, 1024 - 8)
            c = random.randint(8, 652 - 8)
            gun = Gun(a, b, c)
            gun_group.append(gun)


class RoundNos():
    def __init__(self, crab, max):
        self.sprites = []
        self.crab = crab
        self.crabroundwins = max
        image = pygame.image.load("numbers.png")
        xpos = 1
        ypos = 1
        for each in range(10):
            blank = pygame.Surface((17, 27))
            blank.fill ((1, 1, 1))
            blank.set_colorkey((1, 1, 1))
            blank.blit(image, (0, 0), (xpos, ypos, 17, 27))
            if self.crab == "crab2":
                var = pygame.PixelArray(blank)
                var.replace((6, 42, 97), (110, 7, 32))
            elif self.crab == "settings":
                var = pygame.PixelArray(blank)
                var.replace((6, 42, 97), (28, 5, 35))
            blank = pygame.transform.scale(blank, (blank.get_width() * 4, blank.get_height() * 4))
            self.sprites.append(blank)
            xpos += 18

    def work(self):
        if self.crab == "crab1":
            screen.blit(self.sprites[int(self.crabroundwins)], (56 * 4, 212 * 4))
        elif self.crab == "crab2":
            screen.blit(self.sprites[int(self.crabroundwins)], (183 * 4, 212 * 4))
        elif self.crab == "settings":
            if self.crabroundwins < 1:
                self.crabroundwins = 1
            elif self.crabroundwins > 9:
                self.crabroundwins = 9
            screen.blit(self.sprites[int(self.crabroundwins)], (200 * 4, 34 * 4))

    def checkwin(self, menu):
        if self.crab == "crab1":
            if self.crabroundwins == maxrounds.crabroundwins:
                menu = "P1wins"
                clocktimer.roundtimer = 300
        elif self.crab == "crab2":
            if self.crabroundwins == maxrounds.crabroundwins:       # check if either player has the required number of round wins
                menu = "P2wins"
                clocktimer.roundtimer = 300
        if self.crab == "crab2" and (menu == "P2wins" or menu == "P1wins"):     # if self.crab == "crab2" is to ensure the code only executes the code once and after it...
            for each in range(len(P1nla.tagletters)):                           # ... has checked both crab's number of round wins
                P1nla.tagletters[each] = pygame.transform.scale(P1nla.tagletters[each], (P1nla.tagletters[each].get_width() * 4, P1nla.tagletters[each].get_height() * 4))
            for each in range(len(P2nla.tagletters)):
                P2nla.tagletters[each] = pygame.transform.scale(P2nla.tagletters[each], (P2nla.tagletters[each].get_width() * 4, P2nla.tagletters[each].get_height() * 4))
        return menu


class TemplateCrab():
    def __init__(self, crabs):
        self.currentsprite = 0
        self.sprite = []
        self.crabs = crabs
        if self.crabs == "crab1":
            self.sprite = [crab.sprites[0], crab.sprites[1]]
            self.x = 81
            self.settingsdif = -10

        elif self.crabs == "crab2":
            self.sprite = [crab2.sprites[0], crab2.sprites[1]]
            self.x = 149
            self.settingsdif = 10
        # for each in range(len(self.sprite)):
        #     self.sprite[each] = pygame.transform.scale(self.sprite[each], (self.sprite[each].get_width() * 4, self.sprite[each].get_height() * 4))

        ## Colour Block (the square next to the alphabet that shows the colour)

        if self.crabs == "crab1":
            self.imgx = 74
        if self.crabs == "crab2":
            self.imgx = 171

        blank = pygame.Surface((11, 10))
        blank.fill((1, 1, 1))
        blank.set_colorkey((1, 1, 1))
        blank.blit(image, (0, 0), (0, 79, 11, 10))
        var = pygame.PixelArray(blank)
        if self.crabs == "crab1":
            var.replace((255, 255, 255), crab.colour)
            self.colour = crab.colour
        elif self.crabs == "crab2":
            var.replace((255, 255, 255), crab2.colour)
            self.colour = crab2.colour
        blank = transform(blank)
        self.colourblock = blank

    def work(self):
        if menu == "Game":
            x = self.x
        elif menu == "Settings":
            x = self.x + self.settingsdif
            screen.blit(self.colourblock, (self.imgx * 4, 105 * 4))

        screen.blit(self.sprite[int(self.currentsprite)], (x*4, 215*4))
        if menu != "Settings":
            self.currentsprite += 0.05
            if self.currentsprite > 2:
                self.currentsprite = 0

    def colourswitch(self):
        if self.crabs == "crab1":
            self.sprite = [crab.sprites[0], crab.sprites[1]]
        elif self.crabs == "crab2":
            self.sprite = [crab2.sprites[0], crab2.sprites[1]]
        # for each in range(len(self.sprite)):
        #     self.sprite[each] = pygame.transform.scale(self.sprite[each], (
        #         self.sprite[each].get_width() * 4, self.sprite[each].get_height() * 4))

        ## Colour Block

        self.colourblock = pygame.transform.scale(self.colourblock, (self.colourblock.get_width() / 4, self.colourblock.get_height() / 4))
        var = pygame.PixelArray(self.colourblock)
        if self.crabs == "crab1":
            var.replace(self.colour, crab.colour)
            self.colour = crab.colour
        if self.crabs == "crab2":
            var.replace(self.colour, crab2.colour)
            self.colour = crab2.colour
        del var
        self.colourblock = pygame.transform.scale(self.colourblock, (self.colourblock.get_width() * 4, self.colourblock.get_height() * 4))


class PortraitCrab():
    def __init__(self, imagepath, xpos, ypos, crabs, lightcrabcolour, darkcrabcolour):
        self.xpos = xpos
        self.ypos = ypos
        self.image = pygame.image.load(imagepath)
        self.image = transform(self.image)
        self.crabs = crabs
        self.lightcrabcolour = lightcrabcolour
        self.darkcrabcolour = darkcrabcolour

    def colourswitch(self):
        var = pygame.PixelArray(self.image)
        if self.crabs == "crab1":
            crabcolours = crab.colour
        elif self.crabs == "crab2":
            crabcolours = crab2.colour
        var.replace(self.lightcrabcolour, crabcolours)  # replaces all blue in the picture to red
        self.lightcrabcolour = crabcolours
        darkcolour = getColour(crabcolours)
        var.replace(self.darkcrabcolour, darkcolour)
        self.darkcrabcolour = darkcolour
        del var

    def work(self):
        screen.blit(self.image, (self.xpos * 4, self.ypos * 4))




## Load Title objects


class Titlebuttons(pygame.sprite.Sprite):
    def __init__(self, imgposx, posx, posy, menu):
        super().__init__()
        self.counter = 0
        self.menu = menu
        image = pygame.image.load("titlescreenbuttons.png")
        self.buttons = []
        self.posx = posx*4
        self.posy = posy*4
        self.imgposx = imgposx
        imgposy = 0
        self.currentsprite = 0
        for each in range(3):
            blank = pygame.Surface((62, 21))
            blank.blit(image, (0, 0), (self.imgposx, imgposy, 62, 21))
            self.buttons.append(blank)
            imgposy += 23
        self.image = self.buttons[self.currentsprite]
        self.image = transform(self.image)
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.posx, self.posy)
    def update(self, press):
        self.currentsprite = 0
        if self.counter > 0:
            self.currentsprite = 2
            self.counter += 0.1
        if self.rect.collidepoint(pygame.mouse.get_pos()) and self.counter == 0 and self.currentsprite != 2:
            self.currentsprite = 1
            if press == 1:
                self.currentsprite = 2
                self.counter = 1
        if self.rect.collidepoint(cursor2.x, cursor2.y) and self.counter == 0 and self.currentsprite != 2:
            self.currentsprite = 1
            if joystickinputs[0] == True:
                self.currentsprite = 2
                self.counter = 1
        self.image = self.buttons[int(self.currentsprite)]
        self.image = transform(self.image)

class Clouds():
    def __init__(self):
        super().__init__()
        self.sprites = []
        for each in range(1, 3):
            blank = pygame.Surface((227, 16))
            image = pygame.image.load(f"CloudsF{each}.png")
            blank.blit(image, (0, 0))
            blank = transform(blank)
            self.sprites.append(blank)
        self.currentsprite = 0
        self.image = self.sprites[self.currentsprite]
    def update(self):
        self.currentsprite += 0.01
        if self.currentsprite >= len(self.sprites):
            self.currentsprite = 0
        self.image = self.sprites[int(self.currentsprite)]

class Titleguy():
    def __init__(self):
        super().__init__()
        self.sprites = []
        for i in range(1, 5):
            image = pygame.image.load(f"titleguyF{i}.png")
            image = transform(image)
            self.sprites.append(image)
        self.currentsprite = 0
        self.image = self.sprites[self.currentsprite]
    def update(self):
        if self.currentsprite <= 1:
            timer = 0.012
        elif 1 < self.currentsprite <= 2 or 3 < self.currentsprite <= 4:
            timer = 0.035
        elif 2 < self.currentsprite <= 3:
            timer = 0.0042
        self.currentsprite += timer
        if self.currentsprite >= len(self.sprites):
            self.currentsprite = 0
        self.image = self.sprites[int(self.currentsprite)]      #self.currentsprite gets rounded down to the nearest whole number




## Generate Objects


cursor = Cursor("P1")
cursor2 = Cursor("P2")
red = (187, 67, 67)
blue = (60, 194, 179)
purple = (168, 39, 194)
yellow = (194, 193, 39)
crab = Crab(50, 50, red, "P1")
crab2 = Crab(900, 50, blue, "P2")

tempp1col, tempp2col = crab.colour, crab2.colour

crab_group = [crab, crab2]
bullet_group = []

gun_group = []
gun_group.append(Gun("pistol", 200, 500))
gun_group.append(Gun("shotgun", 600, 100))
gun_group.append(Gun("revolver", 800, 600))
gun_group.append(Gun("ak", 400, 200))

menucounter = 0

screen = pygame.display.set_mode((1024, 960))
pygame.display.set_caption("Samurai Robo Crab Fighting")
menu = "Title"   # Game/Settings/Title
pygame.mouse.set_visible(False)

emptyUI = imgdata("emptyUI.png", 0, 0)
clocktimer = Timer()
maxrounds = RoundNos("settings", 7)
p1Score = RoundNos("crab1", 0)
p2Score = RoundNos("crab2", 0)
p1templatecrab = TemplateCrab("crab1")
p2templatecrab = TemplateCrab("crab2")
p1CrabPortrait = PortraitCrab("p1CrabPortrait.png", 0, 165, "crab1", (187, 67, 67), (128, 26, 82))
p2CrabPortrait = PortraitCrab("p2CrabPortrait.png", 201, 165, "crab2", (194, 193, 39), (8, 93, 61))
p1CrabPortrait.colourswitch()
p2CrabPortrait.colourswitch()

bluewin = pygame.image.load("bluewins.png")
bluewin = transform(bluewin)
pinkwin = pygame.image.load("pinkwins.png")     # load image when a round is won
pinkwin = transform(pinkwin)
bluewingame = pygame.image.load("bluewinsgame.png")
bluewingame = transform(bluewingame)
pinkwingame = pygame.image.load("pinkwinsgame.png")     # load image when a round is won
pinkwingame = transform(pinkwingame)
roundwindrawer = "0"

titlescreen = imgdata("EmptyTitle.png", 0, 0)
clouds = Clouds()
titleguy = Titleguy()

bluebutton = Titlebuttons(0, 25, 114, "Game")
bluebutton_group = pygame.sprite.Group()
bluebutton_group.add(bluebutton)

pinkbutton = Titlebuttons(64, 97, 114, "GameP2")
pinkbutton_group = pygame.sprite.Group()
pinkbutton_group.add(pinkbutton)

greenbutton = Titlebuttons(128, 169, 114, "Settings")
greenbutton_group = pygame.sprite.Group()
greenbutton_group.add(greenbutton)




# mainloop
while 1:
    while menu == "Title":
        xdown = False
        press = 0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                press = 1
            if event.type == pygame.JOYBUTTONDOWN:
                xdown = True
            if event.type == pygame.JOYAXISMOTION:
                analog_keys[event.axis] = event.value   # gets all controller inputs that I want each frame
        joystickinputs = [xdown, getjoystickinputs(analog_keys)]

        if bluebutton.counter != 0 or pinkbutton.counter != 0 or greenbutton.counter != 0:
            press = 2                                                                           # Disables pressing after a menu to transition to has been picked
            joystickinputs[0] = False

        # updating
        cursor.update()
        cursor2.update()
        titleguy.update()
        bluebutton_group.update(press)
        pinkbutton_group.update(press)
        greenbutton_group.update(press)
        clouds.update()
        if bluebutton.counter > 3:
            menu = bluebutton.menu
        if pinkbutton.counter > 3:
            menu = bluebutton.menu
        if greenbutton.counter > 3:
            menu = greenbutton.menu
        # drawing
        render(titlescreen)
        screen.blit(titleguy.image, (72, 632))
        bluebutton_group.draw(screen)
        pinkbutton_group.draw(screen)
        greenbutton_group.draw(screen)
        screen.blit(clouds.image, (48, 556))
        screen.blit(cursor.image, cursor.rect.topleft)
        screen.blit(cursor2.image, cursor2.rect.topleft)
        # general
        pygame.display.update()
        clock.tick(60)
    while menu == "Settings":
        pressed = False
        xdown = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    pressed = True
            if event.type == pygame.JOYBUTTONDOWN:
                xdown = True
            if event.type == pygame.JOYAXISMOTION:
                analog_keys[event.axis] = event.value  # gets all controller inputs that I want each frame
        joystickinputs = [xdown, getjoystickinputs(analog_keys)]

        cursor.update()
        cursor2.update()        # updates cursors
        screen.blit(emptysettingsUI, (0, 0))
        # colours, tags
        for each in colours_group:                      #--------------------------
            each.work(pressed, joystickinputs[0])
        counter = 0
        for each in P1alpha:
            if each.rect.collidepoint((cursor.x, cursor.y)):
                each.update(counter, pressed)
            counter += 1
        counter = 0
        for each in P2alpha:
            if each.rect.collidepoint((cursor2.x, cursor2.y)):
                each.update(counter, joystickinputs[0])
            counter += 1                                        # handles colours
        P1nla.update(pressed)
        P2nla.update(joystickinputs[0])
        if tempp1col != crab.colour:
            crab.colourswitch()
            p1CrabPortrait.colourswitch()
            p1templatecrab.colourswitch()
        if tempp2col != crab2.colour:
            crab2.colourswitch()
            p2CrabPortrait.colourswitch()
            p2templatecrab.colourswitch()
        p1templatecrab.work()
        p2templatecrab.work()
        p1CrabPortrait.work()
        p2CrabPortrait.work()
        tempp1col = crab.colour
        tempp2col = crab2.colour                         #------------------------
        # top part
        if exitbutton.rect.collidepoint((cursor.x, cursor.y)) or exitbutton.rect.collidepoint((cursor2.x, cursor2.y)) or exitbutton.menucounter != 0:   # if a cursor is hovering over the exit button
            exitbutton.display(pressed, joystickinputs[0])
        if exitbutton.menucounter > 0:
            if exitbutton.menucounter >= 3:
                menu = "Title"
                exitbutton.menucounter = 0
                exitbutton.exit = "none"
        timerupdown.work(pressed, joystickinputs[0])
        clocktimer.work()
        maxroundupdown.work(pressed, joystickinputs[0])
        maxrounds.work()
        gunonoff.work(pressed, joystickinputs[0])
        screen.blit(cursor.image, cursor.rect.topleft)
        screen.blit(cursor2.image, cursor2.rect.topleft)
        # general
        pygame.display.update()
        clock.tick(60)
    while menu == "Game":
        cursor.update()
        cursor2.update()
        clocktimer.roundtimer += 1
        if clocktimer.roundtimer > 0:
            xdown = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    crab.shoot()
                if event.type == pygame.JOYBUTTONDOWN:
                    xdown = True
                if event.type == pygame.JOYAXISMOTION:
                    analog_keys[event.axis] = event.value  # gets all controller inputs that I want each frame
                joystickinputs = [xdown, getjoystickinputs(analog_keys)]
                if joystickinputs[1][0] == 1:
                    crab2.shoot()
            for each in crab_group:
                if each.akcounter > 0:
                    each.akcounter -= 1
                    if each.akcounter % 5 == 0:
                        each.canshoot = 4
                        ran = random.randint(-20, 20)
                        offset = ran / 100
                        bullet = Bullet(offset, 20, each.crabtype)      ## Spawns 5 bullets with a few frames of time between each
                        bullet_group.append(bullet)
                        each.maxshoot = each.canshoot

            # updating
            for each in crab_group:
                each.canshoot -= 0.1
                if each.canshoot < 0:
                    each.canshoot = 0
                each.animation()                ## Update Crabs P1 and P2
                each.gunlag()
                each.rotate()
                each.roll()
                each.movement()
            for gun in gun_group:
                gun.grab()
                gun.update()
                gun.thrown()
            counter = 0                     ## Update Guns and Bullets
            roundended = False
            for bullet in bullet_group:
                if roundended == False:
                    (roundended, roundwindrawer) = bullet.collision()
                    bullet.update(counter)
                    counter += 1
            del counter
        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            if clocktimer.roundtimer == 0:
                roundwindrawer = "0"
                menu = resetround(menu)
                if menu != "Game":
                    break

        # drawing
        screen.fill((150, 150, 150))
        for gun in gun_group:
            if gun.grabbed == "0":
                screen.blit(gun.image, gun.rect.topleft)
        for bullet in bullet_group:
            screen.blit(bullet.image, bullet.rect.topleft)          ## Draw Guns and Bullets
        for each in crab_group:
            screen.blit(each.image, each.rect.topleft)
        render(emptyUI) # do it last otherwise bullets go over the UI

        # updating and drawing UI
        if clocktimer.roundtimer < 0:
            if roundwindrawer == "blue":
                screen.blit(bluewin, (0, 0))        # draw the round win screen for 60 frames
                P1nla.roundwindisplay()
            elif roundwindrawer == "pink":
                screen.blit(pinkwin, (0, 0))
                P2nla.roundwindisplay()
        p1CrabPortrait.work()
        p2CrabPortrait.work()
        clocktimer.work()
        clocktimer.gunSpawn()
        p1Score.work()              ## Update and Draw UI during game
        p2Score.work()
        p1templatecrab.work()
        p2templatecrab.work()
        screen.blit(cursor.image, cursor.rect.topleft)
        screen.blit(cursor2.image, cursor2.rect.topleft)
        # general
        pygame.display.update()
        clock.tick(60)
    while menu == "P1wins":
        menu, joystickinputs = winsfunction(bluewingame, menu)
    while menu == "P2wins":
        menu, joystickinputs = winsfunction(pinkwingame, menu)
    bluebutton.counter = 0
    pinkbutton.counter = 0
    greenbutton.counter = 0