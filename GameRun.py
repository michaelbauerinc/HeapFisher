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
gameStart = False
gameOver = False
firstEndLoop = True

#Colors
black = (0, 0, 0, 255)
white = (255, 255, 255, 255)
red = (255, 0, 0, 255)
green = (0, 255, 0, 255)
gold = (255,215,0)

#fishHitbox = (0, 0, 0, 0)
cheatCounter = 0

#PlayerMoveVars
x = 300
y = 60
vel = 10


screenContent = []
toBeDrawn = {}
fish = []
enemies = []
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

class Enemy:

    def __init__(self, x, y, idx):
        self.x = x
        self.y = y
        self.idx = idx
        self.hitbox = Rectangle(self.x+13, self.y+20, 60, 40, idx)
        self.picture = Image('piranha.png', [self.x, self.y])

    def draw(self):
        #screenContent[self.picture.image] = (self.picture.rect)
        self.hitbox.draw()


def screenRefresh():
    global left
    global right
    global hookHitbox
    global fishHitbox
    global score
    global timerTick
    global gameOver
    global firstEndLoop


    screenContent.clear()

    if left:
        Player.image = player_flipped
        Player.rect = [x, y]
        Hook.rect.left = x + 100

    elif right:
        Player.image = player
        Player.rect = [x, y]
        Hook.rect.left = x + 100


    queueDrawings()


    #Enemy.draw()

    for i in screenContent:
        gameDisplay.blit(i.image, i.rect)



    score.text_to_screen()
    hookHitbox = Rectangle(Hook.rect.left+10, Hook.rect.top+10, 40, 30, "Hook")

    for key, value in fishHitboxes.items():
       if key.id == "Enemy1":
           if key.x1 < 0:
               value.rect.left = 1200
               key.x1 = value.rect.left
               key.x2 = key.x1 + key.w
               key.y2 = key.y1 + key.h
           value.rect.left -= 15
           key.x1 -= 15
           key.x2 = key.x1 + key.w
           key.y2 = key.y1 + key.h
       if key.id == "Enemy":
           if key.x1 < 0:
               value.rect.left = 1200
               key.x1 = value.rect.left
               key.x2 = key.x1 + key.w
               key.y2 = key.y1 + key.h
           value.rect.left -= 10
           key.x1 -= 10
           key.x2 = key.x1 + key.w
           key.y2 = key.y1 + key.h


    #Heap.heapify_up()

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
    if timer.value == 0:
        gameOver = True
    elif timerTick == 30:
        timer.value -= 1
        timerTick = 0

    if gameOver:
        gameDisplay.blit(gameEnd.image, gameEnd.rect)
        score.x = 560
        score.y = 400
        score.text_to_screen()
        pygame.display.update()
        if firstEndLoop:
            time.sleep(2)
            firstEndLoop = False

    Heap.heapify_up()

    pygame.display.update()



def queueDrawings():

    screenContent.append(Background)
    screenContent.append(Player)
    screenContent.append(Hook)


    for i in fish:
        screenContent.append(i)

    for i in enemies:
        screenContent.append(i)



def raiseHook():
    global goingUp
    global goingDown
    global hasControl

    goingUp = True
    if Hook.rect.top == y + 130:
        hasControl = True
        goingDown = False
        goingUp = False

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
    global y
    global cheatCounter
    global scoreQueue

    idx = hitbox.id


    if idx == None or type(idx) == str and goingUp:
        return

    elif type(idx) == str and not goingUp:
        hasControl = False
        if scoreQueue.size > 0:
            scoreQueue.dequeue()
            placeQueueNums()
            return

    elif hitbox.y1 <= y + 130:
        number = Heap.heap_list[idx]
        resetHitboxPos(hitbox)
        captureNumber(number)
    else:
        number = Heap.heap_list[idx]
        hasControl = False
        number.y -= 15
        hitbox.y1 -= 15





def captureNumber(number):
    global score
    global cheatCounter

    if int(number.idx) <= 7:
        cheatCounter = 0
    elif int(number.idx) > 7:
        cheatCounter += 1
    if cheatCounter > 2:
        return


    queueVar = Heap.prepDelete(number.idx)
    if scoreQueue.size == 4:
       for i in range(4):
           itemToAdd = scoreQueue.dequeue()
           score.value += itemToAdd.value



    scoreQueue.enqueue(queueVar)

    placeQueueNums()

    if Heap.heap_list[1].value < 10:
        randomNum = 15
    else:
        randomNum = 9


    toAdd = Number(random.randint(1, randomNum), 1085, y + 18, 15)


    Heap.add(toAdd)

def placeQueueNums():

    if scoreQueue.size == 0:
        return

    current = scoreQueue.head
    currentNum = current.number
    x = 830

    if not current:
        return
    else:
        for i in range(scoreQueue.size):
            currentNum.x = x
            currentNum.y = 10
            x += 60
            if current.get_next_node() and scoreQueue.size > 1:
                current = current.get_next_node()
                currentNum = current.number





def resetHitboxPos(hitbox):


    if type(hitbox.id) == str:
        return
    elif  hitbox.id == 1:
        hitbox.y1 = 565
        Heap.heap_list[hitbox.id].y = 565

    elif hitbox.id >= 2 and hitbox.id <= 3:
       hitbox.y1 = 510
       Heap.heap_list[hitbox.id].y = 510

    elif hitbox.id >= 4 and hitbox.id <= 7:
        hitbox.y1 = 390
        Heap.heap_list[hitbox.id].y = 390

    elif hitbox.id > 7:
       hitbox.y1 = 270
       Heap.heap_list[hitbox.id].y = 270


def spawnChests():
    x = 520
    y = 545
    global gameStart
    global display_width
    global fishHitboxes
    gameStart = True
    idx = 1

    for i in range(15, 16):

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

        fishName = Image("chest.png", [x, y])
        HB = Rectangle(x+13, 270, 50, 30, idx)
        pointsNum = Number(random.randint(1,4), x+26, y+18, idx)
        Heap.add(pointsNum)
        fishHitboxes[HB] = (fishName)
        fish.append(fishName)
        x += (display_width/8)
        idx += 1



def spawnEnemies():

    x = 100

    for i in range(4):
        i = Enemy(x, 298, "Enemy")
        fishHitboxes[i.hitbox] = (i.picture)
        enemies.append(i.picture)
        x += 300
    x = 200
    for i in range(4):
        i = Enemy(x, 420, "Enemy1")
        fishHitboxes[i.hitbox] = (i.picture)
        enemies.append(i.picture)
        x += 300


def gameRestart():
    global gameOver
    global score
    global timer
    global timerTick
    global cheatCounter
    global x
    global y
    global firstEndLoop

    gameOver = False
    firstEndLoop = False

    x = 300
    y = 60
    score.value = 0
    score.x = 30
    score.y = 30
    timer.value = 60
    timerTick = 0
    cheatCounter = 0

    for i in range(scoreQueue.size):
        scoreQueue.dequeue()


#Images
Background = Image('background.png', [0,0])
Player = Image('player.png', [x, y])
gameEnd = Image('gameoverscreen.png', [50, 50])

Hook = Image('hook.png', [x+100, y+130])
hookHitbox = Rectangle(Hook.rect.left - 3, Hook.rect.top, 40, 50, "Hook")

Fish = Image('chest.png', [500, 500])
player = pygame.image.load('player.png')
player_flipped = pygame.transform.flip(Player.image, True, False)







score = Number(0, 30, 30, None)
timer = Number(60, 1120, 10, None)

while run:
    clock.tick(30)
    if not gameStart:
        spawnChests()
        spawnEnemies()

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
    if gameOver and keys[pygame.K_SPACE]:
        gameRestart()
    if not gameOver:
        if not hasControl:
            raiseHook()
        elif not keys[pygame.K_SPACE] and goingDown:
            raiseHook()
        if hasControl == True:
            if keys[pygame.K_LEFT] and x > -35:
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