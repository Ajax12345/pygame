import pygame
import random
import time
import sqlite3

class Bullets(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([10, 10]) #perhaps want to change this
        self.image.fill((0, 255, 0))

        #self.image.set_colorkey((255, 255, 255))
        #self.image = pygame.image.load("/Users/davidpetullo/Desktop/laser.png")

        self.rect = self.image.get_rect()


    def update(self):
        self.rect.y -= 3



class Ship(pygame.sprite.Sprite):
    def __init__(self, img):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([60, 60])
        self.image.fill((0, 255, 0))

        self.image = img
        self.rect = self.image.get_rect()





class Asteroid(pygame.sprite.Sprite):
    def __init__(self):
        #super(pygame.sprite.Sprite, self).__init__()
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([800, 600])
        self.image.fill((255, 255, 255))
        self.image.set_colorkey((255, 255, 255))

        self.image = pygame.image.load("/Users/davidpetullo/Desktop/Asteroididadactyl.png")

        self.rect = self.image.get_rect()

        self.reverse = 1

        self.health = 80



    def forward(self, distance):
        if self.rect.y + distance >= 600:
            self.reverse = -1

        elif self.rect.y + distance*self.reverse < 0:
            self.reverse = 1
        self.rect.y += self.reverse*distance

    def backward(self, distance):
        if self.rect.y - distance <= 0:
            self.reverse = -1

        elif self.rect.y + distance*self.reverse >= 800:
            self.reverse = 1
        self.rect.y -= self.reverse*distance

    def left(self, distance):
        if self.rect.x - distance <= 0:
            self.reverse = -1
        elif self.rect.x + self.reverse*distance >= 800:
            self.reverse = 1

        self.rect.x -= self.reverse*distance

    def right(self, distance):
        if self.rect.x + distance >= 800:
            self.reverse = -1

        elif self.rect.x + self.reverse*distance <= 0:
            self.reverse = 1
        self.rect.x += self.reverse*distance


    #now, add a method that will switch the direction of the asteroid if it hits the wall

class Games1:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.hit_counter = 0
        self.possible_directions = ["up", "down", "right", "left"]
        self.height = 800
        self.width = 600
        self.move1 = 0
        pygame.mixer.init(44100, -16, 2, 2048)
        self.impact = pygame.mixer.Sound("/Users/davidpetullo/Downloads/Explosion+3.wav")
        self.blaster = pygame.mixer.Sound("/Users/davidpetullo/Downloads/soundsblaster/probedroidgun01.wav")
        self.img1 = pygame.image.load("/Users/davidpetullo/Desktop/shuttle.png")
        self.asteroid = pygame.image.load("/Users/davidpetullo/Desktop/Asteroididadactyl.png")

        self.img2 = pygame.image.load("/Users/davidpetullo/Desktop/space-1.jpg")
        self.should_continue = True

        self.gameDisplay = pygame.display.set_mode((1000, 900))
        self.speed_up = 0
        self.speed_down = self.height
        self.speed_across1 = 0
        self.speed_across2 = self.width
        self.generic_astroids = pygame.sprite.Group()
        self.asteroids = pygame.sprite.Group()


        for i in range(30):
            self.the_asteroid = Asteroid()
            self.the_asteroid.rect.x = random.randint(1, 600)
            self.the_asteroid.rect.y = random.randint(1, 800)
            self.asteroids.add(self.the_asteroid)
            self.generic_astroids.add(self.the_asteroid)

        #The Asteroids: -----------------------------
        #--------------The Asteroids-------------------------

        #-----------------------------------------
        self.bullet_list = pygame.sprite.Group() #this is important

        self.starship_list = pygame.sprite.Group()

        #self.ship = Ship(self.img1)

        #self.starship_list.add(self.ship)
        #self.asteroids.add(self.ship)


        self.clock = pygame.time.Clock()

        self.minutes = 0
        self.seconds = 0
        self.milliseconds = 0

        self.speed_const = 0

        self.generic_health = 0

    def DrawBackground(self):
        self.gameDisplay.blit(self.img2, (0, 0))

    def draw_shuttle(self, x, y):
        self.gameDisplay.blit(self.img1, (x, y))

    def health_bar(self):
        if 800-self.hit_counter < 400:

            pygame.draw.rect(self.gameDisplay, (255, 0, 0), (0, 0, 800-self.hit_counter-100, 15))

        else:
            pygame.draw.rect(self.gameDisplay, (0, 255, 0), (0, 0, 800-self.hit_counter-100, 15))

    def update_screen(self):
        #pygame.display.update()
        pygame.display.flip()


    def counterdisplay(self):
        font = pygame.font.SysFont(None, 50)
        text = font.render("Hits:"+str(self.hit_counter), True, (255, 255, 255))
        self.gameDisplay.blit(text, (100, 25))

    def button1(self, message, x, y, w, h):
        #this button sets the stats for the hunter fighter
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        if x + w > mouse[0] > x and y+h > mouse[1] > y:
            pygame.draw.rect(self.gameDisplay, (0, 255, 0), (100, 100, 70, 30))

            if click[0] == 1:

                self.speed_const = 7
                self.generic_health = 100

                self.player()

        else:
            pygame.draw.rect(self.gameDisplay, (0, 255, 0), (100, 100, 70, 30))

    def button2(self, message, x, y, w, h):
        #this button sets the stats for the falchion
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        if x + w > mouse[0] > x and y+h > mouse[1] > y:
            pygame.draw.rect(self.gameDisplay, (0, 255, 0), (100, 300, 90, 30))

            if click[0] == 1:
                self.img1 = pygame.image.load("/Users/davidpetullo/Desktop/falchion.png")
                #self.ship = Ship(self.img1)
                self.speed_const = 20
                self.generic_health = 250
                self.player()

        else:
            pygame.draw.rect(self.gameDisplay, (0, 255, 0), (100, 300, 90, 30))

    def button3(self, message, x, y, w, h):
        #this sets the stats for the eagle
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        if x + w > mouse[0] > x and y+h > mouse[1] > y:
            pygame.draw.rect(self.gameDisplay, (0, 255, 0), (100, 600, 70, 30))

            if click[0] == 1:
                self.img1 = pygame.image.load("/Users/davidpetullo/Desktop/eagle.png")
                self.speed_const = 3
                #self.ship = Ship(self.img1)
                self.generic_health = 50
                self.player()

        else:
            pygame.draw.rect(self.gameDisplay, (0, 255, 0), (100, 600, 70, 30))

    def display_results(self):
        pygame.init()
        self.gameDisplay = pygame.display.set_mode((1000, 900))
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

            self.gameDisplay.fill((255, 255, 255))
            font = pygame.font.SysFont(None, 50)

            text = font.render("Surival Time:"+str(self.minutes)+"-"+str(self.seconds)+"-"+str(self.milliseconds), True, (255, 0, 0))
            self.gameDisplay.blit(text, (300, 300))
            self.update_screen()

    def shoot(self):
        bullet = Bullets(self.height, self.width)
        self.asteroids.add(bullet)
        self.bullets.add(bullet)


    def menu(self):
        pygame.init()
        self.gameDisplay = pygame.display.set_mode((1000, 900))
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

            self.gameDisplay.fill((65, 105, 225))
            font = pygame.font.SysFont(None, 30)
            text = font.render("Welcome to Pilot Survival", True, (0, 0, 0))
            self.gameDisplay.blit(text, (300, 300))
            self.button1("hunter", 100, 100, 70, 30)
            new_font = pygame.font.SysFont(None, 1)
            text = font.render("hunter", True, (0, 0, 0))
            self.gameDisplay.blit(text, (100, 100))


            self.button2("falchion", 100, 300, 70, 30)
            new_font = pygame.font.SysFont(None, 1)
            text = font.render("falchion", True, (0, 0, 0))
            self.gameDisplay.blit(text, (100, 300))

            self.button3("eagle", 100, 600, 70, 30)
            new_font = pygame.font.SysFont(None, 1)
            text = font.render("eagle", True, (0, 0, 0))
            self.gameDisplay.blit(text, (100, 600))



            self.update_screen()








    def player(self):
        pygame.init()
        self.gameDisplay = pygame.display.set_mode((1000, 900))

        pygame.display.set_caption("Asteroid belt")


        self.ship = Ship(self.img1)

        self.starship_list.add(self.ship)
        self.asteroids.add(self.ship)

        #while self.should_continue:
        while 800-self.hit_counter-100 > 0:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.should_continue = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        #self.x = -10
                        self.x = -1*self.speed_const

                    elif event.key == pygame.K_RIGHT:
                        #self.x = 10
                        self.x = self.speed_const


                    elif event.key == pygame.K_DOWN:
                        #self.y = 10
                        self.y = self.speed_const

                    elif event.key == pygame.K_UP:
                        #self.y  = -10
                        self.y = -1*self.speed_const

                    elif event.key == pygame.K_SPACE:
                        pygame.mixer.Sound.play(self.blaster)
                        self.bullet = Bullets()
                        self.bullet.rect.x = self.height+100
                        self.bullet.rect.y = self.width + 100

                        self.asteroids.add(self.bullet)
                        self.bullet_list.add(self.bullet)


                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                        self.x = 0

                    elif event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                        self.y = 0


            self.height += self.x

            self.width += self.y

            self.ship.rect.x = self.height
            self.ship.rect.y = self.width
            #self.random_direction = random.choice(self.possible_directions)
            #print self.random_direction

            for i, a in enumerate(self.generic_astroids):
                if i%2 == 0:
                    a.backward(4)

                elif i%3 == 0:
                    a.forward(4)

                elif i%5 == 0:
                    a.right(4)

                else:
                    a.left(4)
            self.asteroids.update()
            #self.bullets.update()
            '''
            for i in self.bullet_list:
                self.certain_hits = pygame.sprite.spritecollide(i, self.generic_astroids, True)
                #print self.certain_hits
                '''
            #for i in self.asteroids:
                #self.new_hits = pygame.sprite.spritecollide(i, self.starship_list, False)

            if any(len(pygame.sprite.spritecollide(i, self.starship_list, False)) > 0 for i in self.generic_astroids):
                #pygame.mixer.Sound.play(self.impact)
                self.hit_counter += 1

            for i in self.generic_astroids:
                if len(pygame.sprite.spritecollide(i, self.bullet_list, False)) > 0:
                    if i.health <= 0:
                        i.kill()

                    else:
                        i.health -= 1

            self.DrawBackground()
            #self.draw_shuttle(self.height*0.8, self.width*0.45)
            self.asteroids.draw(self.gameDisplay)
            #self.bullets.draw(self.gameDisplay)
            #self.checkcollision()
            self.health_bar()
            self.counterdisplay()
            if self.milliseconds > 1000:
                self.seconds += 1
                self.milliseconds -= 1000

            if self.seconds > 60:
                self.minutes += 1
                self.seconds -= 60


            self.milliseconds += self.clock.tick_busy_loop(60)

            self.update_screen()




        self.display_results() #replace with overall time of game
        pygame.quit()
        quit()



my_game = Games1()
my_game.menu()

