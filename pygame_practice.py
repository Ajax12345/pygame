import pygame
import pygame

#need separate instance of each bullet position using sprite
class My_Bullets(pygame.sprite.Sprite):
    def __init__(self, color, width, height, x, y):
        super(My_Bullets, self).__init__()

        #pygame.sprite.Sprite.__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill((0, 0, 0))

        pygame.draw.rect(self.image, (0,0,255), (x, y, width, height))

        self.rect = self.image.get_rect()

class SomeGame(pygame.sprite.Sprite):


    def __init__(self):
        super(SomeGame, self).__init__()
        self.crashed = False
        self.tankpic = pygame.image.load("/Users/davidpetullo/Desktop/enemy_tank.png")
        self.bullet = pygame.image.load("/Users/davidpetullo/Desktop/sierra-bullets-6mm-243-107-gr-hpbt-matchking-100box.jpg")
        self.height = 800
        self.width = 600
        self.object_width = 0
        self.white = (255, 255, 255)
        self.x_change = 0
        self.tank_speed = 0
        self.gameDisplay = pygame.display.set_mode((1000, 900))
        self.y_change = 0
        self.tank_health = 0
        self.bullet_y = 100
        self.bullet_x = 50
        self.hit = 0
        self.flag = False
        #self.bullets = [(self.bullet_x+i, self.bullet_y) for i in range(1, 100, 5)]
        self.sprite_list = pygame.sprite.Group()

    def tank_bullets(self):
        self.starter = 0
        self.starter1 = 0

        for i in range(10):
            our_bullets = My_Bullets((0, 255, 0), 50, 50, self.starter, self.starter1)
            self.sprite_list.add(our_bullets)
            self.starter += 100
            self.starter1 -= 100
            self.updater()

    def updater(self):
        self.sprite_list.update()

    def init(self):
        pygame.init()
        self.gameDisplay = pygame.display.set_mode((1000, 900))
        pygame.display.set_caption('Practice Game')

    def tank(self, x, y):

        self.gameDisplay.blit(self.tankpic, (x, y))

    def update_screen(self):
        #pygame.display.update()
        pygame.display.flip()

    def draw_rect(self):
        pygame.draw.rect(self.gameDisplay, (0,0,255), (50, 100,300,600))

    def draw_generic_rect(self, color, x, y, height, width):
        self.the_colors = {"red":(255, 0, 0), "blue":(0, 0, 255), "green":(0, 255, 0), "pink":(255, 200, 200), "navy":(0, 0, 128)}
        pygame.draw.rect(self.gameDisplay, self.the_colors[color], (x, y, width, height))


    def fire_bullet(self, c, d):
        self.gameDisplay.blit(self.bullet, (c, d))

    def text_objects(self, text, font):
        surface = font.render(text, True, (0, 0, 0))
        return surface, surface.get_rect()


    def message_display(self, the_text):
        large_text = pygame.font.Font('freesansbold.ttf',115)
        self.Texts, self.textr = self.text_objects(the_text, large_text)
        self.textr.center = ((500), (450))
        self.gameDisplay.blit(self.Texts, self.textr)

    def display_counter(self, the_count):
        font = pygame.font.SysFont(None, 25)
        text = font.render("Hit: "+str(the_count), True, (0, 0, 0))
        self.gameDisplay.blit(text, (100, 25))



    def determine_hit(self):
        if self.height <= self.check and not self.flag:
            self.hit += 1
            self.flag = True
            self.message_display("Crashed!!")

        elif self.height <= self.check and self.flag:
            self.message_display("Crashed!!")

        elif self.height >= self.check and self.flag:
            self.flag = False
        print self.object_width
        print "_______________"

        print self.width
        if self.object_width == self.width and self.height <= 600 and self.height >= 400:
            self.message_display("Crashed!!")
    #self.display_counter(self.hit)
            #self.message_display("Crashed!!") #make this dependent upon a crash
        self.display_counter(self.hit)


    def write_on_screen(self, message, text_size, x, y):
        the_text = pygame.font.Font('freesansbold.ttf', text_size)
        self.textm, self.textn = self.text_objects(message, the_text)
        self.textn = ((x), (y))
        self.gameDisplay.blit(self.textm, self.textn)

    def button(self, message, x, y, w, h, col1, col2):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        if x + w > mouse[0] > x and y+h > mouse[1] > y:
            self.draw_generic_rect(col1, x, y, w, h)

            if click[0] == 1:
                self.play()

        else:
            self.draw_generic_rect(col2, x, y, w, h)

        self.write_on_screen(message, 20, x+15, y+15)

    def draw_object(self):
        self.draw_generic_rect("green", self.object_width, 500, 200, 200)


    def main_menu(self):
        self.init()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

            self.gameDisplay.fill(self.white)

            the_text = pygame.font.Font('freesansbold.ttf', 115)
            self.textm, self.textn = self.text_objects("TANK GAME", the_text)
            self.textn = ((180), (400))
            self.gameDisplay.blit(self.textm, self.textn)

            #need to make sure layering is correct. There is overlap in pygame like in kivy.
            '''
            self.draw_generic_rect("red", 100, 100, 50, 100)
            self.write_on_screen("Play", 20, 115, 115) #new function written
            self.draw_generic_rect("blue", 700, 100, 50, 100)
            '''
            self.button("Play", 100, 100, 50, 100, "red", "pink")

            self.update_screen()

        pygame.quit()

        quit()

    def play(self):

        self.init()
        self.tank_bullets()
        #self.updater()
        self.check = 400
        while not self.crashed:

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    self.crashed = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.x_change = -5


                    elif event.key == pygame.K_RIGHT:
                        self.x_change = 5


                    elif event.key == pygame.K_DOWN:
                        self.y_change = 5

                    else:
                        self.y_change = -5

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                        self.x_change = 0

                    elif event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                        self.y_change = 0



            self.height += self.x_change

            self.width += self.y_change


            self.gameDisplay.fill(self.white)

            #if (self.width >= 0 or self.width <= 600) and (self.height <= 800 or self.height >= 0):
            self.tank(self.height*0.8, self.width*0.45)
            self.object_width += 2
            self.draw_object()
            #self.tank_bullets()
            self.draw_rect()

            self.sprite_list.draw(self.gameDisplay)
            '''
            if self.height <= self.check:
                self.hit += 1
                #self.display_counter(self.hit)
                self.message_display("Crashed!!") #make this dependent upon a crash
            self.display_counter(self.hit)
            '''

            self.determine_hit()

            self.update_screen()


        pygame.quit()

        quit()

my_game = SomeGame()
my_game.main_menu()
my_game.play()
