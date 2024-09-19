import pygame, os

# --- game settings ---------------------
SCREEN_WIDTH, SCREEN_HEIGHT = 1500, 760
FPS = 60
# ---------------------------------------

class Engine:

    def __init__(self, SCREEN_WIDTH, SCREEN_HEIGHT, FPS) -> None:
        pygame.init()
        pygame.mixer.init() # add this line
        pygame.display.set_caption("Steller Duel")

        self.SCREEN_WIDTH = SCREEN_WIDTH
        self.SCREEN_HEIGHT = SCREEN_HEIGHT
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))

        self.clock = pygame.time.Clock()
        self.FPS = FPS

        self.gameStateManager = gameStateManager('start')
        self.actions = {
            "left1":False, "right1":False, "up1": False, "down1": False,
            "left2":False, "right2":False, "up2": False, "down2": False,
            "shoot1":False, "shoot2": False, "startGame": False, "reset": False,
            "gameStopped": False, "mousePos": pygame.mouse.get_pos(), "muteSound": False,
            "mouseDown": False
            }
        self.start = Start(self.screen, self.gameStateManager)
        self.level = Level(self.screen, self.gameStateManager, self.actions)
        self.settings = Settings(self.screen, self.gameStateManager, self.actions)
        self.pause = Pause(self.screen, self.gameStateManager)

        self.state = {"level": self.level, "start":self.start, "settings":self.settings, "pause":self.pause}   

    def run(self):
        run = True

        bulletCooldown = 20 # the time the player have to wait between each shot to fire another one
        coolDown1, coolDown2  = bulletCooldown, bulletCooldown
        while run:

            self.actions["shoot1"] = False
            self.actions["shoot2"] = False
            self.actions["mousePos"] = pygame.mouse.get_pos()

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    run = False

                self.actions["mouseDown"] = event.type == pygame.MOUSEBUTTONDOWN

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE and self.gameStateManager.getState() == "level":
                        self.gameStateManager.setState("pause")

                    if event.key == pygame.K_a: self.actions["left1"] = True
                    if event.key == pygame.K_d: self.actions["right1"] = True
                    if event.key == pygame.K_w: self.actions["up1"] = True
                    if event.key == pygame.K_s: self.actions["down1"] = True

                    if event.key == pygame.K_LEFT: self.actions["left2"] = True
                    if event.key == pygame.K_RIGHT: self.actions["right2"] = True
                    if event.key == pygame.K_UP: self.actions["up2"] = True
                    if event.key == pygame.K_DOWN: self.actions["down2"] = True

                    if event.key == pygame.K_r: self.actions["reset"] = True

                    if event.key == pygame.K_SPACE:

                        self.actions["startGame"] = True

                        if coolDown1 <= 0:
                            self.actions["shoot1"] = True
                            coolDown1 = bulletCooldown

                    if event.key == pygame.K_KP0:
                        if coolDown2 <= 0:
                            self.actions["shoot2"] = True
                            coolDown2 = bulletCooldown


                    

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_a: self.actions["left1"] = False
                    if event.key == pygame.K_d: self.actions["right1"] = False
                    if event.key == pygame.K_w: self.actions["up1"] = False
                    if event.key == pygame.K_s: self.actions["down1"] = False

                    if event.key == pygame.K_LEFT: self.actions["left2"] = False
                    if event.key == pygame.K_RIGHT: self.actions["right2"] = False
                    if event.key == pygame.K_UP: self.actions["up2"] = False
                    if event.key == pygame.K_DOWN: self.actions["down2"] = False

                    if event.key == pygame.K_r: self.actions["reset"] = False

            if coolDown1 > 0: coolDown1 -= 1
            if coolDown2 > 0: coolDown2 -= 1

                    
            self.state[self.gameStateManager.getState()].run(self.actions)
            self.displayFps()

            pygame.display.update()
            self.clock.tick(self.FPS)

        pygame.quit()

    def displayFps(self):
        font = pygame.font.SysFont('roboto', 40)
        text = font.render(f"FPS: {round(self.clock.get_fps())}", True , "white")
        textRect = text.get_rect()
        textRect.center = (SCREEN_WIDTH - 60, SCREEN_HEIGHT - 20)
        self.screen.blit(text, textRect)

class Button():
    def __init__(self, image, imageHover, pos, toggle = None):
        self.toggle = toggle
        self.image = image
        self.imageHover = imageHover
        self.displayImg = image
        self.x_pos = pos[0]
        self.y_pos = pos[1]
        self.type = type
        if self.toggle == None:
            self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
        else: self.rect = self.image[0].get_rect(center=(self.x_pos, self.y_pos))
        self.clicked = True

    def updateToggle(self, toggle): self.toggle = toggle
    
    def update(self, screen, actions):

        if actions["mousePos"][0] in range(self.rect.left, self.rect.right) and actions["mousePos"][1] in range(self.rect.top, self.rect.bottom):
            self.displayImg = self.imageHover
        else:
            self.displayImg = self.image

        if self.toggle == None: screen.blit(self.displayImg, self.rect)
        else: screen.blit(self.displayImg[{True: 1, False: 0}[self.toggle]], self.rect)


    def checkForInput(self, actions):
        action = False
        #check mouseover and clicked conditions
        if self.rect.collidepoint(actions["mousePos"]):
            if actions["mouseDown"] and self.clicked == False:
                self.clicked = True
                action = True

        if not actions["mouseDown"]:
            self.clicked = False

        return action




class Start:
    
    def __init__(self, display, gameStateManager) -> None:
        self.display = display
        self.gameStateManager = gameStateManager
        spaceBetweenButtons = 160 # the space between the start menu buttons
        spaceFromScreenTop = 250 # the space between the buttons and the top of the screen
        self.playBtn = Button(image = pygame.image.load(os.path.join("assets", "startBtn.png")),
            imageHover = pygame.image.load(os.path.join("assets", "startBtnHover.png")), pos=(SCREEN_WIDTH // 2, spaceFromScreenTop))
        self.settingsBtn = Button(image = pygame.image.load(os.path.join("assets", "settingsBtn.png")),
            imageHover = pygame.image.load(os.path.join("assets", "settingsBtnHover.png")), pos=(SCREEN_WIDTH // 2, spaceFromScreenTop + spaceBetweenButtons))
        self.buttons = (self.playBtn, self.settingsBtn)

    def run(self, actions):
        # settings
        if actions["startGame"] or self.playBtn.checkForInput(actions):
            self.gameStateManager.setState('level')
            actions["reset"] = True

        if self.settingsBtn.checkForInput(actions):
            self.gameStateManager.setState('settings')

        self.draw(actions)


    def draw(self, actions):

        START_BG_IMAGE = pygame.image.load(os.path.join("assets", "startbg.png"))
        self.display.blit(pygame.transform.scale(START_BG_IMAGE, (SCREEN_WIDTH, SCREEN_HEIGHT)), (0,0))
        for btn in self.buttons:
            btn.update(self.display, actions)




class Level:
    
    def __init__(self, display, gameStateManager, actions) -> None:
        self.display = display
        self.gameStateManager = gameStateManager

        self.xOffset = 150 # ship's distance from screen sides
        self.yOffset = SCREEN_HEIGHT // 2 # ship's distance from screen top
        self.shipSetup(self.xOffset, self.yOffset, actions)

    def run(self, actions):

        if actions["reset"]: self.shipSetup(self.xOffset, self.yOffset, actions)
        actions["reset"] = False
        
        self.draw()

        if self.countDown <= 0:
            actions["gameStopped"] = False
            self.countDown -= 1
        else: self.countDown -= 1

        for ship in self.spaceShips:
            ship.run(actions, self.spaceShips)

    def shipSetup(self, xOffset, yOffset, actions):

        self.shipWidth, self.shipHeight = 80, 80 # the spaceship's width and height
        
        self.ship1 = spaceShip(self.gameStateManager, xOffset, yOffset,  self.shipWidth, self.shipHeight, self.display, 1)
        self.ship2 = spaceShip(self.gameStateManager, SCREEN_WIDTH - xOffset - self.shipWidth, yOffset, self.shipWidth, self.shipHeight, self.display, 2)
        self.spaceShips = (self.ship1, self.ship2)

        self.countDown = 119
        actions["gameStopped"] = True
        

    def draw(self):

        outlineThickness = 4 # change outline thickness
        barScalar = 2 # change healthbar size
        xDistance = 20 # bar's distance from screen sides
        yDistance = 10 # bar's distance from screen top
        

        def healthBar(x, y, ship):
            pygame.draw.rect(self.display, (130, 130, 130), (x-outlineThickness, y-outlineThickness, 100 * barScalar + outlineThickness * 2, 10 * barScalar + outlineThickness * 2))
            pygame.draw.rect(self.display, (235, 62, 49), (x, y, 100 * barScalar, 10 * barScalar))
            pygame.draw.rect(self.display, (0, 255, 89), (x, y, ship.health * barScalar, 10 * barScalar))

        SPACE_BG_IMAGE = pygame.image.load(os.path.join("assets", "spaceBackground.png"))
        self.display.blit(pygame.transform.scale(SPACE_BG_IMAGE, (SCREEN_WIDTH, SCREEN_HEIGHT)), (0,0))

        healthBar(xDistance, yDistance, self.ship1)
        healthBar(SCREEN_WIDTH - xDistance - 100 * barScalar - outlineThickness * 2, yDistance, self.ship2)

        if self.countDown > 0:
            font = pygame.font.SysFont('roboto', 500)
            text = font.render(str(self.countDown // 40 + 1), True , "white")
            textRect = text.get_rect()
            textRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
            self.display.blit(text, textRect)


class Settings:
    
    def __init__(self, display, gameStateManager, actions) -> None:
        self.display = display
        self.gameStateManager = gameStateManager

        self.spaceBetweenButtons = 450 # the space between the settings menu buttons
        self.spaceFromScreenTop = 350 # the space between the settings and the top of the screen

        self.muteBtn = Button(image = (pygame.image.load(os.path.join("assets", "muteBtn.png")), pygame.image.load(os.path.join("assets", "unmuteBtn.png"))),
            imageHover = (pygame.image.load(os.path.join("assets", "muteBtnHover.png")), pygame.image.load(os.path.join("assets", "unmuteBtnHover.png"))),
            pos=((SCREEN_WIDTH - self.spaceBetweenButtons) // 2, self.spaceFromScreenTop), toggle =  actions["muteSound"])
        self.backBtn = Button(image = pygame.image.load(os.path.join("assets", "backBtn.png")),
            imageHover = pygame.image.load(os.path.join("assets", "backBtnHover.png")), pos=((SCREEN_WIDTH + self.spaceBetweenButtons) // 2, self.spaceFromScreenTop))
        self.buttons = (self.muteBtn, self.backBtn)

    def run(self, actions):

        if self.muteBtn.checkForInput(actions):
            actions["muteSound"] = not actions["muteSound"]

        if self.backBtn.checkForInput(actions):
            self.gameStateManager.returnToPrevState()

        self.draw(actions)

    def draw(self, actions):
        
        START_BG_IMAGE = pygame.image.load(os.path.join("assets", "startbg.png"))
        self.display.blit(pygame.transform.scale(START_BG_IMAGE, (SCREEN_WIDTH, SCREEN_HEIGHT)), (0,0))

        self.muteBtn.updateToggle(actions["muteSound"])
        for btn in self.buttons:
            btn.update(self.display, actions)

class Pause:
    
    def __init__(self, display, gameStateManager) -> None:
        self.display = display
        self.gameStateManager = gameStateManager
        spaceBetweenButtons = 250 # the space between the start menu buttons
        spaceFromScreenTop = 300 #the space between the buttons and the screen top
        self.settingsBtn = Button(image = pygame.image.load(os.path.join("assets", "settingsBtn.png")),
            imageHover = pygame.image.load(os.path.join("assets", "settingsBtnHover.png")), pos=(SCREEN_WIDTH// 2, spaceFromScreenTop))
        self.backBtn = Button(image = pygame.image.load(os.path.join("assets", "backBtn.png")),
            imageHover = pygame.image.load(os.path.join("assets", "backBtnHover.png")), pos=((SCREEN_WIDTH // 2, spaceFromScreenTop + spaceBetweenButtons)))
        self.buttons = (self.settingsBtn, self.backBtn)

    def run(self, actions):

        if self.settingsBtn.checkForInput(actions):
            self.gameStateManager.setState('settings')

        if self.backBtn.checkForInput(actions):
            self.gameStateManager.returnToPrevState()

        self.draw(actions)


    def draw(self, actions):

        START_BG_IMAGE = pygame.image.load(os.path.join("assets", "startbg.png"))
        self.display.blit(pygame.transform.scale(START_BG_IMAGE, (SCREEN_WIDTH, SCREEN_HEIGHT)), (0,0))
        for btn in self.buttons:
            btn.update(self.display, actions)



class gameStateManager:

    def __init__(self, currentState) -> None:
        self.currentState = currentState
        self.previousStates = [currentState]

    def getState(self):
        return self.currentState
    
    def returnToPrevState(self):
        if len(self.previousStates) >= 2:
            self.previousStates.pop()
            self.currentState = self.previousStates[-1]
        else: self.currentState = 'start'
    
    def setState(self, state):
        self.currentState = state
        self.previousStates.append(self.currentState)
    

class spaceShip:

    def __init__(self, gameStateManager , x, y, width, height, display, id):
        self.gameStateManager = gameStateManager
        self.id = id
        self.x = x
        self.y = y
        self.vel = 6 # the speed of each ship
        self.rotation = {1: 270, 2: 90}[self.id]
        self.display = display
        self.SPACESHIP_WIDTH, self.SPACESHIP_HEIGHT = width, height
        SPACESHIP_IMG  = pygame.image.load(os.path.join('assets', f'spaceship{self.id}.png'))
        self.SPACESHIP_SPRITE = pygame.transform.rotate(pygame.transform.scale(SPACESHIP_IMG, (self.SPACESHIP_WIDTH, self.SPACESHIP_HEIGHT)), self.rotation)
        self.rect = self.SPACESHIP_SPRITE.get_rect()
        self.bullets = []
        self.maxAmountOfBullets = 5 # the maximun amount of bullets shot at once
        self.health = 100
        self.explosionFrames = [
            pygame.image.load(os.path.join("assets", f"exp1{self.id}.png")),
            pygame.image.load(os.path.join("assets", f"exp2{self.id}.png")),
            pygame.image.load(os.path.join("assets", f"exp3{self.id}.png")),
            pygame.image.load(os.path.join("assets", f"exp4{self.id}.png")),
            pygame.image.load(os.path.join("assets", f"exp5{self.id}.png")),
            pygame.image.load(os.path.join("assets", f"exp6{self.id}.png"))
            ]
        self.deathAnimation = 0
        self.timePerFrame = 6 # the time each explosion frame displays
        self.sounds = {"shoot": pygame.mixer.Sound(os.path.join('assets', 'shootSoundEffect.mp3'))}

    def run(self, actions, spaceShips):

        if 0 < self.deathAnimation < 100:
            self.deathAnimation += 1
        elif self.deathAnimation >= 100:
            self.deathAnimation = -1
            actions["startGame"] = False
            self.gameStateManager.setState("start")
        elif self.health <= 0 and self.deathAnimation == 0:
            self.deathAnimation = 1
        for spaceShip in spaceShips:
            if spaceShip.deathAnimation != 0: actions["gameStopped"] = True

        if actions[f"left{self.id}"] and self.x > self.vel and not actions["gameStopped"]: self.x -= self.vel
        if actions[f"right{self.id}"] and self.x + self.SPACESHIP_WIDTH < SCREEN_WIDTH - self.vel and not actions["gameStopped"]: self.x += self.vel
        if actions[f"up{self.id}"] and self.y > 0 and not actions["gameStopped"]: self.y -= self.vel
        if actions[f"down{self.id}"] and self.y + self.SPACESHIP_HEIGHT < SCREEN_HEIGHT - self.vel and not actions["gameStopped"]: self.y += self.vel
        self.rect.x, self.rect.y = self.x, self.y
        
        if actions[f"shoot{self.id}"] and len(self.bullets) < self.maxAmountOfBullets and not actions["gameStopped"]:
            self.bullets.append(bullet(self.id, self.x, self.y + self.SPACESHIP_HEIGHT // 2, self.display))
            if not actions["muteSound"]: pygame.mixer.Sound.play(self.sounds["shoot"])
        if actions["gameStopped"]: self.bullets.clear()
        for bul in self.bullets:
            bul.run(self.bullets, spaceShips)


        self.draw()

    def draw(self):
       if 0 < self.deathAnimation < 6 * self.timePerFrame -1: 
        explosionImg = pygame.transform.rotate(pygame.transform.scale(self.explosionFrames[self.deathAnimation // self.timePerFrame], (self.SPACESHIP_WIDTH, self.SPACESHIP_HEIGHT)), self.rotation)
        self.display.blit(explosionImg, (self.x, self.y))
       elif self.deathAnimation == 0:
        self.display.blit(self.SPACESHIP_SPRITE, (self.x, self.y))


class bullet:

    def __init__(self, shipId, x, y, display) -> None:

        self.display = display
        self.shipId = shipId
        dir = {1: 1, 2: -1}[self.shipId]
        speed = 20 # the speed of each bullet
        self.vel = speed * dir
        self.color = {1: 'blue', 2: 'red'}[shipId]
        self.duration = 0
        self.maxDuration = 60 # the distance of each bullet
        self.rect = pygame.Rect(x, y, 20, 6)
        self.damage = 10 # the damage each bullet deals

    def run(self, bullets, spaceShips):

        enemyShip = spaceShips[{1:1, 2:0}[self.shipId]]
        colide = self.rect.colliderect(enemyShip.rect)
        if colide:
            enemyShip.health -= self.damage
            bullets.pop(bullets.index(self)) 
        elif self.duration > self.maxDuration:
            bullets.pop(bullets.index(self)) 
        else:
            self.draw()
            self.rect.x += self.vel
            self.duration += 1

    def draw(self):
        pygame.draw.rect(self.display, self.color, self.rect)


def main():
    game = Engine(SCREEN_WIDTH, SCREEN_HEIGHT, FPS)
    game.run()


if __name__ == "__main__":
    main()


