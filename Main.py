#Initialisations
import pygame, time

from pygame.constants import K_ESCAPE
pygame.init()
pygame.font.init()

#Settings
FPS = 60
VOLUME = 0.5
SIZE = HEIGHT, WIDTH = (1920, 1080)
CENTER = CENTERX, CENTERY = HEIGHT/2, WIDTH/2
BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255,0,0)
FONT = 'PIXELBOY.TTF'
mainClock = pygame.time.Clock()
BG = pygame.image.load(r'assets\BG\bg.jpg')
ICON = pygame.image.load(r'assets\ICON.png')
MUSIC = pygame.mixer.music.load(r'assets\audio\mainmenu.mp3')
pygame.display.set_caption('Project Vulcan')
pygame.display.set_icon(ICON)
pygame.mixer.music.set_volume(VOLUME)
pygame.mixer.music.play(-1)

#Flags
RUNNING = True
TITLE = True
OPTIONS = False
START = False
GAME = False

#Sounds
HoverSound = pygame.mixer.Sound(r'assets\audio\hover.mp3')

sounds = [HoverSound]

def SetVolume(sounds, VOLUME):
    for sound in sounds:
        sound.set_volume(VOLUME)
        pygame.mixer.music.set_volume(VOLUME)

#Display

screen = pygame.display.set_mode(SIZE)
screenRect = screen.get_rect()

#Functions
def hightlight(textobject):
    if textobject.isOver():
        textobject.updateColour(RED)
    else:
        textobject.updateColour(WHITE)

def collide(obj1, obj2):
    offset_x = obj1.x - obj2.x
    offset_y = obj1.y - obj2.y
    return obj1.mask.overlap(obj2, (offset_x, offset_y)) != None

#Classes
class Text():
    def __init__(self, string, colour, fontsize, x, y, font=FONT):
        self.string = string
        self.colour = colour
        self.fontsize = fontsize
        self.x = x
        self.y = y
        self.font = font
        

    def render(self):
        self.object = pygame.font.Font(self.font, self.fontsize).render(self.string, True, self.colour)
        self.rect = self.object.get_rect(center = (self.x, self.y))
        return self.object, self.rect

    def isOver(self):
        if pygame.mouse.get_pos()[0] > self.rect.left and pygame.mouse.get_pos()[0] < self.rect.right and pygame.mouse.get_pos()[1] > self.rect.top and pygame.mouse.get_pos()[1] < self.rect.bottom:
            return True
        else:
            return False

    def updateColour(self, newcolour):
        self.colour = newcolour

class Object():
    def __init__(self, img, x, y):
        self.img = pygame.image.load(img)
        self.x = x
        self.y = y
        self.rect = self.img.get_rect(center = (self.x, self.y))
        self.mask = pygame.mask.from_surface(self.img)


    def blit(self):
        screen.blit(self.img, self.rect)

class Player(Object):
    def __init__(self, img, x, y):
        super().__init__(img, x, y)
        self.health = 100
        self.max_health = 100
        self.speed = 8
        
    def shoot(self):
        self.laser = Laser(self.rect.midright[0], self.rect.midright[1])
        print('Laser created.')

class Laser:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.img = pygame.image.load(r'assets\flame_02.png')
        self.mask = pygame.mask.from_surface(self.img)
        self.rect = self.img.get_rect(center = (self.x, self.y))
        self.vel = 20

    def move(self):
        self.rect = self.rect.move(self.vel, 0)

    def off_screen(self, width):
        return self.rect.centerx <= width and self.rect.centerx >= 0 

    def collision(self, obj):
        return collide(self, obj)
    
    def blit(self):
        screen.blit(self.img, self.rect)
    
#Text
Title = Text('Vulcan', WHITE, 250, CENTERX, CENTERY - 150)
StartButton = Text('Start Game', WHITE, 40, CENTERX, CENTERY + 150)
OptionsButton = Text('Options', WHITE, 40, CENTERX, CENTERY + 185)
QuitButton = Text('Quit', WHITE, 40, CENTERX, CENTERY + 220)
VerNumber = Text('v 0 . 3', WHITE, 20, 1890, 20)
Vol = Text('Volume', WHITE, 40, CENTERX, CENTERY + 185)
Plus = Text('+', WHITE, 50, CENTERX + 70, CENTERY + 230)
Minus = Text('-', WHITE, 50, CENTERX - 70, CENTERY + 230)
Back = Text('Back', WHITE, 40, CENTERX, CENTERY + 300)

#Objects
#Player = Object(r'assets\Spaceships\ship.png', CENTERX - 760, CENTERY)
player = Player(r'assets\Spaceships\ship.png', CENTERX - 760, CENTERY)
Chris = Object(r'assets\enemy\chris.png', CENTERX + 400, CENTERY + 100)
Amogus = Object(r'assets\enemy\redamogus.png', CENTERX + 200, CENTERY - 200)
 
#Main Game Loop    
while RUNNING:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if TITLE:
                    if QuitButton.isOver():
                        HoverSound.play()
                        time.sleep(0.5)
                        pygame.quit()
                        RUNNING = False
                    if StartButton.isOver():
                        HoverSound.play()
                        print("Game started.")
                        TITLE, GAME = False, True
                    if OptionsButton.isOver():
                        HoverSound.play()
                        TITLE, OPTIONS = False, True

                if OPTIONS:
                    if Plus.isOver():
                        if VOLUME < 1:
                            VOLUME += 0.1
                            VOLUME = round(VOLUME, 2)
                        HoverSound.play()
                    if Minus.isOver():
                        if VOLUME > 0:
                            VOLUME -= 0.1
                            VOLUME = round(VOLUME, 2)
                        HoverSound.play()
                    if Back.isOver():
                        HoverSound.play()
                        TITLE, OPTIONS = True, False

    #Button States
    keys = pygame.key.get_pressed()

    if GAME:
        if keys[K_ESCAPE]:
            TITLE, GAME = True, False
        if keys[pygame.K_RIGHT] and player.rect.right < 1920 - 100 or keys[pygame.K_d] and player.rect.right < 1920 - 100:
            player.rect = player.rect.move(player.speed,0)
        if keys[pygame.K_LEFT] and player.rect.left > 100 or keys[pygame.K_a] and player.rect.left > 100:
            player.rect = player.rect.move(-player.speed,0)
        if keys[pygame.K_UP] and player.rect.top > 100 or keys[pygame.K_w] and player.rect.top > 100:
            player.rect = player.rect.move(0,-player.speed)
        if keys[pygame.K_DOWN] and player.rect.bottom < 1080 - 100 or keys[pygame.K_s] and player.rect.bottom < 1080 - 100:
            player.rect = player.rect.move(0,player.speed)

        if keys[pygame.K_SPACE]:
            player.shoot()
            print('Laser fired.')
                    
    TitleObj, TitleRect = Title.render()
    StartButtonObj, StartButtonRect = StartButton.render()
    OptionsButtonObj, OptionsButtonRect = OptionsButton.render()
    QuitButtonObj, QuitButtonRect = QuitButton.render()
    VerNumberObj, VerNumberRect = VerNumber.render()
    VolObj, VolRect = Vol.render()
    PlusObj, PlusRect = Plus.render()
    MinusObj, MinusRect = Minus.render()
    BackObj, BackRect = Back.render()

    #Always
    SetVolume(sounds, VOLUME)

    #Title Screen
    if TITLE:
        
        screen.blit(BG, (0,0))
        screen.blit(StartButtonObj, StartButtonRect)
        screen.blit(TitleObj, TitleRect)
        screen.blit(OptionsButtonObj, OptionsButtonRect)
        screen.blit(QuitButtonObj, QuitButtonRect)
        screen.blit(VerNumberObj, VerNumberRect)

    #Options Screen
    if OPTIONS:

        screen.blit(BG, (0,0))
        screen.blit(TitleObj, TitleRect)
        screen.blit(VolObj, VolRect)
        screen.blit(PlusObj, PlusRect)
        screen.blit(MinusObj, MinusRect)
        screen.blit(BackObj, BackRect)

    #In-Game
    if GAME:
        screen.blit(BG, (0,0))
        player.blit()
        Chris.blit()
        Amogus.blit()
        try:
            player.laser.blit()
            player.laser.move()
        except AttributeError:
            pass

    #Check Events
    hightlight(StartButton)
    hightlight(OptionsButton)
    hightlight(QuitButton)
    hightlight(Plus)
    hightlight(Minus)
    hightlight(Back)

    pygame.display.flip()
    mainClock.tick(FPS)
