import pygame
import random
import collections
import time
import sys
converter = {"tercoise":(0,238,238), 'yellow':(255,215,0), 'purple':(191,62,255), 'green':(127,255,0), 'red':(255,0,0), 'blue':(0, 0, 255), 'brown':(255,127,36)}

class Block(pygame.sprite.Sprite):
    def __init__(self, x, y, color):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([40, 40])
        self.image.fill(converter[color])
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x
class Rectangle(pygame.sprite.Sprite):
    def __init__(self, x, y, color):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([100, 40])
        self.image.fill(converter[color])
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x =x

class LittleRectangle(pygame.sprite.Sprite):
    def __init__(self, x, y, color):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([80, 40])
        self.image.fill(converter[color])
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x =x
class I:
    def __init__(self):
        self.group = pygame.sprite.Group()
        self.main_block = Rectangle(400, 30, 'tercoise')
        self.group.add(self.main_block)
    def __iter__(self):
        for sprite in self.group:
            yield sprite

class O:
    def __init__(self):
        self.group = pygame.sprite.Group()
        self.top = LittleRectangle(400, 30, 'yellow')
        self.bottom = LittleRectangle(400, 70, 'yellow')
        for a, b in self.__dict__.items():
            if a in ['top', 'bottom']:
                self.group.add(b)
    def __iter__(self):
        for sprite in self.group:
            yield sprite
class T:
    def __init__(self):
        self.group = pygame.sprite.Group()
        self.top = Block(430, 30, 'purple')
        self.bottom = Rectangle(400, 70, 'purple')
        self.group.add(self.top)
        self.group.add(self.bottom)
    def __iter__(self):
        for sprite in self.group:
            yield sprite

class S:
    def __init__(self):
        self.group = pygame.sprite.Group()
        self.top = LittleRectangle(440, 30, 'green')
        self.bottom = LittleRectangle(400, 70, 'green')
        self.group.add(self.top)
        self.group.add(self.bottom)
    def __iter__(self):
        for sprite in self.group:
            yield sprite

class Z:
    def __init__(self):
        self.group = pygame.sprite.Group()
        self.top = LittleRectangle(400, 30, 'red')
        self.bottom = LittleRectangle(440, 70, 'red')
        self.group.add(self.top)
        self.group.add(self.bottom)

    def __iter__(self):
        for sprite in self.group:
            yield sprite

class J:
    def __init__(self):
        self.group = pygame.sprite.Group()
        self.top = Block(400, 30, 'blue')
        self.bottom = Rectangle(400, 70, 'blue')
        self.group.add(self.top)
        self.group.add(self.bottom)
    def __iter__(self):
        for sprite in self.group:
            yield sprite

class L:
    def __init__(self):
        self.group = pygame.sprite.Group()
        self.top = Block(460, 30, 'brown')
        self.bottom = Rectangle(400, 70, 'brown')
        self.group.add(self.top)
        self.group.add(self.bottom)
    def __iter__(self):
        for sprite in self.group:
            yield sprite
class MainGame:
    def __init__(self):
        self.image = pygame.image.load('/Users/jamespetullo/Desktop/maxresdefault.jpg')
        self.screen = pygame.display.set_mode((1100, 900))
        self.quit = False
        self.first_group = pygame.sprite.Group()
        self.block_types = {'I':I, 'O':O, 'T':T, 'S':S, 'Z':Z, 'J':J, 'L':L}
        self.game_clock = 1
        self.navigation_y = 0
        self.navigation_x = 0
        self.current_block = pygame.sprite.Group()
        self.current_block = L().group
        self.future_block = pygame.sprite.Group()
        self.final_blocks = pygame.sprite.Group()
        self.flag = False
        self.prioraty = collections.deque()
        self.current_time = time.time()
    def play(self):
        pygame.init()
        self.screen.fill((255, 255, 255))
        while not self.quit:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit = True
                if event.type == pygame.KEYDOWN:
                    print 'here111'
                    if event.key == pygame.K_RIGHT:
                        print "here"
                        self.navigation_x = 1
                    if event.key == pygame.K_LEFT:
                        print "here"
                        self.navigation_x = -1

            for sprite in self.current_block:
                sprite.rect.y += 3
                sprite.rect.x += 10*self.navigation_x

            for sprite in self.future_block:
                sprite.rect.y += 3

            for group in self.prioraty:
                for sprite in group:
                    sprite.rect.y += 3

            self.navigation_x = 0

            if self.game_clock%70 == 0:
                new_group = self.block_types[random.choice(self.block_types.keys())]()
                self.prioraty.append(new_group.group)

            '''
            for sprite in self.future_block:
                if any(pygame.sprite.collide_rect(i, sprite2) for sprite2 in self.final_blocks for i in self.future_block):
                    for s
            '''
            for group in self.prioraty:

                if any(pygame.sprite.collide_rect(i, sprite2) for sprite2 in self.final_blocks for i in group):
                    for sprite in group:
                        self.final_blocks.add(sprite)


            for sprite in self.current_block:
                if sprite.rect.y >= 700 or any(pygame.sprite.collide_rect(i, sprite2) for sprite2 in self.final_blocks for i in self.current_block):
                    for sprite in self.current_block:
                        self.final_blocks.add(sprite)
                    try:
                        self.current_block = self.prioraty.popleft()
                    except IndexError:
                        print "Congrats! Game time was {} minutes".format(round(abs(self.current_time-time.time())/60))
                        sys.exit()

                    break

            self.screen.blit(self.image, (0, 0))
            self.current_block.update()
            self.current_block.draw(self.screen)
            '''
            self.future_block.update()
            self.future_block.draw(self.screen)
            '''
            for group in self.prioraty:
                group.update()
                group.draw(self.screen)
            self.final_blocks.update()
            self.final_blocks.draw(self.screen)
            self.game_clock += 1
            pygame.display.flip()


if __name__ == '__main__':
    tetris = MainGame()
    tetris.play()
