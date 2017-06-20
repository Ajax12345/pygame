import pygame

class Lander(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([10, 10])
        self.image.fill((0, 255, 0))
        self.image = pygame.image.load("/Users/davidpetullo/Desktop/lander.png")
        self.rect = self.image.get_rect()

    def downwards(self):
        self.rect.y += 6


class LandScape(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([10, 10])
        self.image.fill((0, 255, 0))
        self.image = pygame.image.load("/Users/davidpetullo/Desktop/rock.png")
        self.rect = self.image.get_rect()

class LunarLander:
    def __init__(self):
        self.screen = pygame.display.set_mode((1000, 900))
        self.width = 500
        self.height = 200
        self.not_crashed = True
        self.x = 0
        self.y = 0
        self.speed_const = 5
        self.background = pygame.sprite.Group()
        self.rocks = LandScape()
        self.background.add(self.rocks)
        self.rocks.rect.x = 0
        self.rocks.rect.y = 400
        self.ship = pygame.sprite.Group()
        self.craft = Lander()
        self.speed_const = 5
        self.ship.add(self.craft)
        self.craft.rect.x = 300
        self.craft.rect.y = 0
        self.height = 300
        self.width = 0
        self.game_timer = 0
        self.right_or_left = False
        self.side_timer = 0
        self.previous_velocity = 0
        self.velocity = 0
        self.landed_safly = False
        self.did_crash = False

        self.background_image = pygame.image.load("/Users/davidpetullo/Desktop/FZP4NQ.jpg")

    def crashed(self):


        if len(pygame.sprite.groupcollide(self.background, self.ship, False, False)) > 0 and self.velocity == 0:
            self.did_crash = True
            self.not_crashed = False

        elif len(pygame.sprite.groupcollide(self.background, self.ship, False, False)) > 0 and self.velocity == 5:
            self.landed_safly = True
            self.not_crashed = False








    def update(self):
        pygame.display.flip()

    def results(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1000, 900))
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

            self.screen.fill((255, 255, 255))
            font = pygame.font.SysFont(None, 50)
            if self.landed_safly:

                self.text = font.render("You landed safely", True, (255, 0, 0))

            if self.did_crash:
                self.text = font.render("Captain, you crashed", True, (255, 0, 0))
            self.screen.blit(self.text, (300, 300))
            self.update()

    def main_game(self):
        pygame.init()
        self.screen.fill((255, 255, 255))
        pygame.display.set_caption("Lunar Lander")
        while self.not_crashed:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.not_crashed = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        #self.x = -10
                        self.x += -1*self.speed_const

                    elif event.key == pygame.K_RIGHT:
                        #self.x = 10
                        self.x += self.speed_const


                    elif event.key == pygame.K_DOWN:
                        #self.y = 10
                        self.y += self.speed_const

                    elif event.key == pygame.K_UP:
                        #self.y  = -10
                        self.y += -1*self.speed_const

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                        self.x = 0


                    elif event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                        self.y = 0






            self.screen.blit(self.background_image, (0, 0))
            self.craft.downwards()
            self.width += self.y

            self.crashed()
            self.height += self.x
            self.previous_velocity = self.craft.rect.y
            self.craft.rect.x = self.height
            self.craft.rect.y += self.y #this works
            self.velocity = abs(self.craft.rect.y - self.previous_velocity)


            #print self.velocity







            self.ship.update()
            self.ship.draw(self.screen)



            self.background.update()
            self.background.draw(self.screen)
            self.update()





game = LunarLander()
game.main_game()
game.results()
