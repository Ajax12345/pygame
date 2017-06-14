import pygame
import time
import random

#------------------------------------------------------------------------
#TODO: Add health bar, game menu, background choices, and sound effects.

#------------------------------------------------------------------------
class Ken(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([10, 10]) #perhaps want to change this
        self.image.fill((0, 255, 0))
        #self.image = pygame.image.load("/Users/davidpetullo/Desktop/kenmasters.png")
        self.image = pygame.image.load("/Users/davidpetullo/Desktop/kenmasters.png")
        self.rect = self.image.get_rect()

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([10, 10]) #perhaps want to change this
        self.image.fill((0, 255, 0))
        #self.image = pygame.image.load("/Users/davidpetullo/Desktop/kenmasters.png")
        self.image = pygame.image.load("/Users/davidpetullo/Desktop/enemy.png") #/Users/davidpetullo/Desktop/enemy.png
        self.rect = self.image.get_rect()


class Ball(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.Surface([10, 10])
        self.image.fill((0, 255, 0))
        self.image = pygame.image.load("/Users/davidpetullo/Desktop/energyball.png")

        self.rect = self.image.get_rect()

    def throw(self):
        self.rect.x += 17


class StreetFighter:
    def __init__(self):
        self.width = 500
        self.height = 200

        self.screen = pygame.display.set_mode((1000, 900))

        self.alive = True
        self.fighter = pygame.sprite.Group()
        self.balls = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.bad_guy = Enemy()
        self.x1 = 700
        self.y1 = 500
        self.bad_guy.rect.x = 700
        self.bad_guy.rect.y = 500
        self.enemies.add(self.bad_guy)

        #self.player_x = self.width
        #self.player_y = self.height
        self.player = Ken()
        self.player.rect.x = self.width
        self.player.rect.y = self.height
        self.fighter.add(self.player)

        self.x = 0
        self.y = 0
        self.time = 0
        self.punch = False
        self.kick = False
        self.uppercut = False
        self.flyingkick = False
        self.speed_const = 15
        self.backkick = False
        self.time1 = 0
        self.enemy_side_kick = False
        self.enemyfrontkick = False
        self.sidekickcount = 0
        self.frontkickcount = 0
        self.axekickcount = 0
        self.energy_ball_count = 2

        self.img3 = pygame.image.load("/Users/davidpetullo/Desktop/thumb-1920-573779.png")

        self.enemyaxekick = False

        self.clock_object = pygame.time.Clock()

        self.ken_healt = 500
        self.bad_guy_health = 500

        self.energy_ball_time = 0
        self.energy_ball_time_flag = False


    def update_screen(self):
        pygame.display.flip()

    def enemy_freeze(self):
        if self.time1 > 10 and self.enemy_side_kick:
            self.bad_guy.image = pygame.image.load("/Users/davidpetullo/Desktop/enemy.png")
            self.time1 = 0
            self.bad_guy.rect.y = self.y1 - 50
            self.bad_guy.rect.x = self.x1 - 40
            self.enemy_side_kick = False

        if self.time1 > 20 and self.enemyfrontkick:
            self.bad_guy.image = pygame.image.load("/Users/davidpetullo/Desktop/enemy.png")
            self.time1 = 0
            self.bad_guy.rect.y = self.y1 - 50
            self.bad_guy.rect.x = self.x1 - 40
            self.enemyfrontkick = False

        if self.time1 > 20 and self.enemyaxekick:

            self.bad_guy.image = pygame.image.load("/Users/davidpetullo/Desktop/enemy.png")
            self.time1 = 0
            self.bad_guy.rect.y = self.y1 - 50
            self.bad_guy.rect.x = self.x1 - 40
            self.enemyaxekick = False



    def enemy_counter(self):

        if abs(self.player.rect.x - self.bad_guy.rect.x) < 50 and abs(self.player.rect.y - self.bad_guy.rect.y) < 200:
            if self.sidekickcount > 40:
                self.bad_guy.image = pygame.image.load("/Users/davidpetullo/Desktop/enemyfrontkick.png")
                self.bad_guy.rect.y = self.y1 - 100
                self.bad_guy.rect.x = self.x1 - 100
                self.enemyfrontkick = True
                self.time1 += 1
                self.frontkickcount += 1

                self.sidekickcount = 0

            else:
                self.bad_guy.image = pygame.image.load("/Users/davidpetullo/Desktop/enemysidekick.png")
                self.bad_guy.rect.y = self.y1 - 100
                self.bad_guy.rect.x = self.x1 - 100

                self.enemy_side_kick = True
                self.sidekickcount += 1


                self.time1 += 1

        elif abs(self.player.rect.x - self.bad_guy.rect.x) < 200 and abs(self.player.rect.y - self.bad_guy.rect.y) < 200:
            if self.frontkickcount > 50:
                self.bad_guy.image = pygame.image.load("/Users/davidpetullo/Desktop/enemysidekick.png")
                self.bad_guy.rect.y = self.y1 - 100
                self.bad_guy.rect.x = self.x1 - 100

                self.enemy_side_kick = True
                self.sidekickcount += 1

                self.time1 += 1

                self.frontkickcount = 0

                self.energy_ball_time_flag = True

            else:
                self.bad_guy.image = pygame.image.load("/Users/davidpetullo/Desktop/enemyfrontkick.png")
                self.bad_guy.rect.y = self.y1 - 100
                self.bad_guy.rect.x = self.x1 - 100
                self.enemyfrontkick = True
                self.time1 += 1
                self.frontkickcount += 1

                self.sidekickcount = 0

    def draw_heath_bar(self):
        raise NotImplementedError("We are working on it")

    def check_collision(self):
        if any(len(pygame.sprite.spritecollide(i, self.enemies, False)) > 0 for i in self.balls):
            self.bad_guy_health -= 400

            print "hit"

    def energy_ball_time_incremement(self):

        if self.energy_ball_time_flag:
            self.energy_ball_time += 1

            if self.energy_ball_time > 60:
                self.energy_ball_time_flag = False
                self.energy_ball_count = 2

                self.energy_ball_time = 0




    def board(self):
        pygame.init()

        #self.screen = pygame.display.set_mode((self.width, self.height))
        self.screen.fill((255, 255, 255))

        pygame.display.set_caption("Street Fighter 5")

        while self.alive:

            self.clock_object.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.should_continue = False

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

                    elif event.key == pygame.K_SPACE:
                        if self.energy_ball_count > 0:
                            self.energy = Ball()
                            self.energy.rect.x = self.height + 40
                            self.energy.rect.y = self.width + 20

                            self.fighter.add(self.energy)
                            self.balls.add(self.energy)

                            self.player.image = pygame.image.load("/Users/davidpetullo/Desktop/kenpower.png")
                            self.punch = True
                            self.energy_ball_count -= 1

                        else:
                            

                            self.energy_ball_time_flag = True




                    elif event.key == pygame.K_a:
                        self.player.image = pygame.image.load("/Users/davidpetullo/Desktop/kenkicking.png")

                        self.kick = True

                    elif event.key == pygame.K_w:
                        self.player.image = pygame.image.load("/Users/davidpetullo/Desktop/kenuppercut.png")
                        self.uppercut = True

                    elif event.key == pygame.K_s:
                        self.player.image = pygame.image.load("/Users/davidpetullo/Desktop/kenflyingkick1.png") #/Users/davidpetullo/Desktop/kenflyingkick.png
                        self.flyingkick = True
                        self.player.x = self.width + 100
                        self.player.y = self.height + 50

                    elif event.key == pygame.K_d:
                        self.player.image = pygame.image.load("/Users/davidpetullo/Desktop/kenbackkick.png")
                        self.backkick = True

                        self.player.x = self.height + 100
                        self.player.y = self.width + 100









                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                        self.x = 0

                    elif event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                        self.y = 0


            self.width += self.y

            self.height += self.x



            self.screen.fill((255, 255, 255))
            self.screen.blit(self.img3, (0, 0))
            self.player.rect.x = self.height
            self.player.rect.y = self.width


            #self.fighter.update()


            self.fighter.update()
            for i in self.balls:
                i.throw()

            self.enemies.update()
            self.enemies.draw(self.screen)

            self.balls.draw(self.screen)

            self.fighter.draw(self.screen)

            #keep time object that once within a few frames, will not revert the photo back to the original until the time is up.

            if self.punch:
                self.time += 1

            if self.kick:
                self.time += 1

            if self.uppercut:
                self.time += 1

            if self.flyingkick:
                self.time += 1

            if self.backkick:
                self.time += 1

            if self.time > 35 and self.punch:


                self.player.image = pygame.image.load("/Users/davidpetullo/Desktop/kenmasters.png")
                self.punch = False
                self.time = 0

            if self.time > 14 and self.kick:
                self.player.image = pygame.image.load("/Users/davidpetullo/Desktop/kenmasters.png")
                self.kick = False
                self.time = 0

            if self.time > 15 and self.uppercut:
                self.player.image = pygame.image.load("/Users/davidpetullo/Desktop/kenmasters.png")

                self.uppercut = False
                self.time = 0

            if self.time > 20 and self.flyingkick:
                self.player.image = pygame.image.load("/Users/davidpetullo/Desktop/kenmasters.png")

                self.flyingkick = False
                self.time = 0

            if self.time > 30 and self.backkick:
                self.player.image = pygame.image.load("/Users/davidpetullo/Desktop/kenmasters.png")
                self.backkick = False
                self.time = 0


            self.enemy_counter()
            self.enemy_freeze()

            self.check_collision()

            self.energy_ball_time_incremement()



            self.update_screen()





        pygame.quit()
        quit()


the_fighter = StreetFighter()
the_fighter.board()
