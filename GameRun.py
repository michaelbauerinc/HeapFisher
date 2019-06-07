import pygame
from Heap import MaxHeap
from Queue import Node
from Queue import Queue
import random
import time
from time import sleep

#Initialize
pygame.init()
pygame.font.init()
display_width = 1200
display_height = 600
gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('HeapFisher')
clock = pygame.time.Clock()


#Bools
run = True
left = False
right = False
hasControl = True
hookDropped = False
goingUp = False
goingDown = False
fishSpawned = False

#Colors
black = (0, 0, 0, 255)
white = (255, 255, 255, 255)
red = (255, 0, 0, 255)
green = (0, 255, 0, 255)
gold = (255,215,0)

#fishHitbox = (0, 0, 0, 0)

#PlayerMoveVars
x = 300
y = 60
vel = 10


screenContent = {}
toBeDrawn = {}
fish = []
fishHitboxes = {}
numbers = []
timerTick = 0
scoreQueue = Queue(10)

#scoreQueue.enqueue
#scoreQueue.dequeue()


Heap = MaxHeap()
#while len(Heap.heap_list) != 16:
   #Heap.add(random.randint(1, 10))

#Heap.print_heap()


class Image(pygame.sprite.Sprite):
    def __init__(self, image_file, location):
        pygame.sprite.Sprite.__init__(self)  #call Sprite initializer
        self.image = pygame.image.load(image_file)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location

class Rectangle:
    def __init__(self, x, y, w, h, id):
        self.x1 = x
        self.y1 = y
        self.x2 = x + w
        self.y2 = y + h

        self.w = w
        self.h = h

        self.fillColor = red

        self.stained = False
        self.id = id

    def setXY(self, xy):
        self.x1, self.y1 = xy
        self.x2 = xy[0] + self.w
        self.y2 = xy[1] + self.h

    def getXY(self):
        return (self.x1, self.y1)

    def rect(self):
        return self.getXY() + (self.w, self.h)


    def coords(self):
        return self.getXY() + (self.x2, self.y2)

    def setCoords(self, location):
        self.x1 = location[0]
        self.y1 = location[1]
        self.x2 = location[2]
        self.y2 = location[3]

    def hasCollided(self, target):
        tx1, ty1, tx2, ty2 = target.coords()
        if tx1 > self.x2 or tx2 < self.x1 or ty1 > self.y2 or ty2 < self.y1:
            return False
        else:
            return True

    def draw(self, surface = gameDisplay):
        pygame.draw.rect(surface, self.fillColor, self.rect(), 2)


class Number:

    def __init__(self, value, x, y, idx):

        self.value = value
        self.x = x
        self.y = y
        self.idx = idx

    def text_to_screen(self, screen=gameDisplay, size=40, color=(0, 0, 0, 255), font_type='freesansbold.ttf'):

        text = str(self.value)
        font = pygame.font.Font(font_type, size)
        text = font.render(text, True, color)
        screen.blit(text, (self.x, self.y))

def screenRefresh():
    screenContent.clear()
    #global hookDropped
    #global hasControl
    global left
    global right
    #goingUp = False
    #global Player
    #global Background
    #global Hook
    global hookHitbox
    global fishHitbox
    global score
    global timerTick



    if left:
        Player.image = player_flipped
        Player.rect = [x, y]
        Hook.rect.left = x + 100

    elif right:
        Player.image = player
        Player.rect = [x, y]
        Hook.rect.left = x + 100


    queueDrawings()



    for key, value in screenContent.items():
        gameDisplay.blit(key, value)



    score.text_to_screen()

    hookHitbox = Rectangle(Hook.rect.left+10, Hook.rect.top+10, 40, 30, "Hook")
    hookHitbox.draw()

    for key, value in fishHitboxes.items():
       key.draw()

    #text_to_screen(gameDisplay, 3, 45, 298, size=50, color=(0, 0, 0, 255))#, font_type='data/fonts/orecrusherexpand.ttf')

    Heap.heapify_up()

    for i in Heap.heap_list:
        try:
            if i.value >= 10:
                i.text_to_screen(screen = gameDisplay, size = 40, color = (255,215,0))
            else:
                i.text_to_screen()
        except AttributeError:
            "Skipping None"

    scoreQueue.drawNumbers()

    timerTick += 1
    timer.text_to_screen()
    if timerTick == 30:
        timer.value -= 1
        timerTick = 0

    Heap.heapify_up()

    pygame.display.update()



def queueDrawings():

    screenContent[Background.image] = (Background.rect)
    screenContent[Player.image] = (Player.rect)
    screenContent[Hook.image] = (Hook.rect)

    for i in fish:
        screenContent[i.image] = (i.rect)



def raiseHook():
    global goingUp
    global goingDown
    global hasControl

    goingUp = True
    if Hook.rect.top == y + 130:
        hasControl = True
        goingDown = False

    else:
        Hook.rect.top -= 15

def dropHook():
    global hasControl
    global goingDown
    global goingUp

    goingDown = True
    if Hook.rect.top > 550:
        hasControl = False
        return

    else:
        Hook.rect.top += 15


def collision(hitbox, image):
    global hasControl

    idx = hitbox.id
    number = Heap.heap_list[idx]

    if hitbox.y1 <= y + 130:
        resetHitboxPos(hitbox)
        #resetNumbers(hitbox)
        captureNumber(number)
    else:
        hasControl = False
        number.y -= 15
        hitbox.y1 -= 15

def captureNumber(number):
    global score
    x = number.x
    y = number.y
    queueVar = Heap.prepDelete(number.idx)
    if scoreQueue.size == 4:
       for i in range(scoreQueue.size):
           itemToAdd = scoreQueue.dequeue()
           score.value += itemToAdd
    if scoreQueue.size == 0:
        queueVar.x = 830
        queueVar.y = 10
    if scoreQueue.size == 1:
        queueVar.x = 890
        queueVar.y = 10
    if scoreQueue.size == 2:
        queueVar.x = 950
        queueVar.y = 10
    if scoreQueue.size == 3:
        queueVar.x = 1004
        queueVar.y = 10

    #Heap.heap_list[1] = Number(0, x + 26, y + 18, 1)
    #QueueAddition = Number(number.value, number.x, number.y, number.idx)
    scoreQueue.enqueue(queueVar)
    #chance = random.randint(1, 3)
    randomNum = 9
    if Heap.heap_list[1].value < 10:
        randomNum = 15
    else:
        randomNum = 9


    toAdd = Number(random.randint(1, randomNum), 1085, y + 18, 15)
    #randomNum = 9

    Heap.add(toAdd)



   # if scoreQueue.size == 1:
        #queueVar.x = 830
        #queueVar = 500
    #if scoreQueue.size == 2:
        #number.x = 880
        #number.y = 10
    #if scoreQueue.size == 3:
        #number.x = 920
       # number.y = 10
   # if scoreQueue.size == 4:
        #number.x = 970
      #  number.y = 10
    #if scoreQueue.size == 5:
        #number.x = 1020
        #number.y = 10

    scoreQueue.print()

    #Heap.heap_list[1] = Number(0, x + 26, y + 18, 1)

def resetHitboxPos(hitbox):

    if  hitbox.id == 1:
        hitbox.y1 = 565
        Heap.heap_list[hitbox.id].y = 565
        hasControl = True
    if hitbox.id >= 2 and hitbox.id <= 3:
       hitbox.y1 = 510
       Heap.heap_list[hitbox.id].y = 510
       hasControl = True
    if hitbox.id >= 4 and hitbox.id <= 7:
        hitbox.y1 = 390
        Heap.heap_list[hitbox.id].y = 390
        hasControl = True
    elif hitbox.id > 7:
       hitbox.y1 = 270
       Heap.heap_list[hitbox.id].y = 270
       hasControl = True


       # hitbox.y1 = 270
        #hasControl = True
    #elif hitbox.id > 8 and hitbox.id <= 12:
        #hitbox.y1 = 390
        #hasControl = True
   # elif hitbox.id > 12 and hitbox.id <= 14:
       # hitbox.y1 = 510
        #hasControl = True
    #else:
        #hitbox.y1 = 565
        #hasControl = True



def spawnFish():
    x = 520
    y = 545
    global fishSpawned
    global display_width
    global fishHitboxes
    fishSpawned = True
    idx = 1
    #proc =
    for i in range(15, 16):
        #fishNum = i
        hitboxName = ("fish" + str(i))
        HB = Rectangle(x + 13, 565, 50, 30, idx)
        pointsNum = Number(random.randint(10,20), x+14, y+18, idx)
        Heap.add(pointsNum)
        fishName = Image("chest.png", [x, y])
        fishHitboxes[HB] = (fishName)
        fish.append(fishName)
        idx += 1

    x = 220
    y = 490
    for i in range(13, 15):
        # fishNum = i
        fishName = Image("chest.png", [x, y])
        HB = Rectangle(x + 13, 510, 50, 30, idx)
        pointsNum = Number(random.randint(6, 9), x + 20, y + 18, idx)
        Heap.add(pointsNum)
        fishHitboxes[HB] = (fishName)
        fish.append(fishName)
        x += (display_width / 2)
        idx += 1

    x = 80
    y = 370
    for i in range(9, 13):
        #fishNum = i
        fishName = Image("chest.png", [x, y])
        HB = Rectangle(x + 13, 390, 50, 30, idx)
        pointsNum = Number(random.randint(5,9), x+26, y+18, idx)
        Heap.add(pointsNum)
        fishHitboxes[HB] = (fishName)
        fish.append(fishName)
        x += (display_width/4)
        idx += 1

    x = 10
    y = 250
    for i in range(1,9):
        #fishNum = i
        fishName = Image("chest.png", [x, y])
        HB = Rectangle(x+13, 270, 50, 30, idx)
        pointsNum = Number(random.randint(1,4), x+26, y+18, idx)
        Heap.add(pointsNum)
        fishHitboxes[HB] = (fishName)
        fish.append(fishName)
        x += (display_width/8)
        idx += 1

    #Heap.print_heap()

#Images
Background = Image('background.png', [0,0])
Player = Image('player.png', [x, y])

Hook = Image('hook.png', [x+100, y+130])
hookHitbox = Rectangle(Hook.rect.left - 3, Hook.rect.top, 40, 50, "Hook")

Fish = Image('chest.png', [500, 500])
player = pygame.image.load('player.png')
player_flipped = pygame.transform.flip(Player.image, True, False)

score = Number(0, 30, 30, None)
timer = Number(60, 1120, 10, None)

while run:
    clock.tick(30)
    if not fishSpawned:
        spawnFish()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    for key, value in fishHitboxes.items():
        if key.hasCollided(hookHitbox):
            key.fillColor = green
            collision(key, value)
            pass

        if not key.hasCollided(hookHitbox):
            key.fillColor = red
            resetHitboxPos(key)

    keys = pygame.key.get_pressed()

    if not hasControl:
        raiseHook()
    elif not keys[pygame.K_SPACE] and goingDown:
        raiseHook()
        hasControl = False
    if hasControl == True:
        if keys[pygame.K_LEFT] and x > -15:
            x -= vel
            left = True
            right = False
        elif keys[pygame.K_RIGHT] and x < 940:
            x += vel
            left = False
            right = True
        if keys[pygame.K_SPACE]:
            dropHook()
    screenRefresh()