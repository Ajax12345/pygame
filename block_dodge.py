import pygame
import random
class Block(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([w, h])
        self.image.fill((34, 139, 34))
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x
class Bug(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([20, 20])
        self.image.fill((178, 34, 34))
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x

class Sim:
    def __init__(self):
        self.loop_count = 0
        self.screen = pygame.display.set_mode((1100, 900))
        self.width = 500
        self.block_after_count = 0
        self.height = 200
        self.block_counter = 0
        self.stop = False
        self.block_flag = False
        self.image = pygame.image.load("/Users/jamespetullo/Desktop/maxresdefault.jpg")
        self.corrds = [[100, 100], [600, 600], [100, 600], [600, 100], [300, 300]]
        self.bugs = pygame.sprite.Group()
        self.prob_list = [True]*30 + [False]*70
        self.the_blocks = pygame.sprite.Group()
        self.calibration_counter = 0
        self.final_colision_count = 0
        random.shuffle(self.prob_list)


        for i, coords in enumerate(self.corrds):
            self.__dict__["sprite{}".format(i)] = Bug(*coords)

        for i in self.__dict__:
            if i.startswith("sprite"):
                self.bugs.add(self.__dict__[i])


    def update(self):
        pygame.display.flip()

    def second_moves(self):
        coords = [(self.__dict__[i].rect.x, self.__dict__[i].rect.y) for i in self.__dict__ if i.startswith("sprite")]
        if not all(abs(coords[i][0]-coords[i+1][0]) < 50 or abs(coords[i][1]-coords[i+1][1]) < 50 for i in range(len(coords)-1)):
            coord_spaces = {i:[(self.__dict__[b].rect.x - self.__dict__[i].rect.x, self.__dict__[b].rect.y - self.__dict__[i].rect.y) for b in self.__dict__ if b.startswith("sprite") and b != i] for i in self.__dict__ if i.startswith("sprite")}

            coord_spaces = {a:[map(abs, i) for i in b] for a, b in coord_spaces.items()}
            for s_name, coord in coord_spaces.items():
                [x1, y1] = sorted(coord, key=lambda x:sum(x))[-1]
                new_val = x1*0.9 + random.randint(1, 100)
                new_val1 = y1*0.9 + random.randint(1, 100)
                self.__dict__[s_name].rect.x = new_val
                self.__dict__[s_name].rect.y = new_val1

        else:

            converter = {"-":lambda x:-1*x, "+":lambda x:x}
            for s_name in [i for i in self.__dict__ if i.startswith("sprite")]:
                x_val = converter[random.choice(converter.keys())](random.randint(1, 300))
                y_val = converter[random.choice(converter.keys())](random.randint(1, 300))
                first_x = self.__dict__[s_name].rect.x
                first_y = self.__dict__[s_name].rect.y
                first_x += x_val
                first_y += y_val
                self.__dict__[s_name].rect.x = first_x
                self.__dict__[s_name].rect.y = first_y


    def move_coords(self):
        coords = [(self.__dict__[i].rect.x, self.__dict__[i].rect.y) for i in self.__dict__ if i.startswith("sprite")]

        #coord_spaces = {i:[(self.__dict__[b].rect.x - self.__dict__[i].rect.x, self.__dict__[b].rect.y - self.__dict__[i].rect.y) for b in self.__dict__ if b.startswith("sprite") and b != i] for i in self.__dict__}

        if not all(abs(coords[i][0]-coords[i+1][0]) < 50 or abs(coords[i][1]-coords[i+1][1]) < 50 for i in range(len(coords)-1)):
            coord_spaces = {i:[(self.__dict__[b].rect.x - self.__dict__[i].rect.x, self.__dict__[b].rect.y - self.__dict__[i].rect.y) for b in self.__dict__ if b.startswith("sprite") and b != i] for i in self.__dict__ if i.startswith("sprite")}

            coord_spaces = {a:[map(abs, i) for i in b] for a, b in coord_spaces.items()}
            for s_name, coord in coord_spaces.items():
                [x1, y1] = sorted(coord, key=lambda x:sum(x))[-1]
                local_count = 0
                while True:

                    new_val = x1*0.9 + random.randint(1, 100)
                    new_val1 = y1*0.9 + random.randint(1, 100)
                    self.__dict__[s_name].rect.x = new_val
                    self.__dict__[s_name].rect.y = new_val1
                    if not any(pygame.sprite.spritecollide(self.__dict__[i], self.the_blocks, False) for i in self.__dict__ if i.startswith("sprite")):
                        break
                    else:
                        self.calibration_counter += 1
                        local_count += 1
                        if local_count > 60:
                            break
        else:

            converter = {"-":lambda x:-1*x, "+":lambda x:x}
            for s_name in [i for i in self.__dict__ if i.startswith("sprite")]:
                local_count = 0
                while True:
                    x_val = converter[random.choice(converter.keys())](random.randint(1, 300))
                    y_val = converter[random.choice(converter.keys())](random.randint(1, 300))
                    first_x = self.__dict__[s_name].rect.x
                    first_y = self.__dict__[s_name].rect.y
                    first_x += x_val
                    first_y += y_val
                    self.__dict__[s_name].rect.x = first_x
                    self.__dict__[s_name].rect.y = first_y
                    if not any(pygame.sprite.spritecollide(self.__dict__[i], self.the_blocks, False) for i in self.__dict__ if i.startswith("sprite")):
                        break
                    else:
                        self.calibration_counter += 1
                        local_count += 1
                        if local_count > 60:
                            break

    def main(self):
        pygame.init()
        self.screen.fill((255, 255, 255))
        while not self.stop:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.stop = True
            if self.loop_count%7 == 0:
                self.move_coords()

            self.bugs.update()
            self.the_blocks.update()
            if self.block_after_count == 70:

                self.__dict__["block"] = Block(random.randint(100, 600), random.randint(100, 600), random.randint(100, 300), random.randint(100,300))
                self.the_blocks.add(self.__dict__["block"])
                self.block_flag = True
                self.block_after_count = 0

            if self.block_flag:
                self.block_counter += 1

            if self.block_counter == 60:


                self.block_flag = False
                self.block_counter = 0
                self.the_blocks = pygame.sprite.Group({i for i in self.the_blocks if not isinstance(i, type(self.__dict__["block"]))})

            self.screen.blit(self.image, (0, 0))
            self.bugs.draw(self.screen)
            self.the_blocks.draw(self.screen)
            if not self.block_flag:
                self.block_after_count += 1

            self.update()
            self.loop_count += 1
            self.final_colision_count += any(pygame.sprite.spritecollide(self.__dict__[i], self.the_blocks, False) for i in self.__dict__ if i.startswith("sprite"))






if __name__ == "__main__":
    game = Sim()
    game.main()
    game.move_coords()
    print game.final_colision_count
