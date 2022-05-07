#imports
import pygame
import sys
import random
from pygame.math import Vector2
import neat
import os

#classes
class SNAKE:
    def __init__(self):
        self.body = [Vector2(5,10),Vector2(4,10),Vector2(3,10)]
        self.direction = Vector2(0,0)

        self.head_up = pygame.transform.scale(pygame.image.load("graphics/head_up.png").convert_alpha(), (cell_size, cell_size))
        self.head_down = pygame.transform.scale(pygame.image.load("graphics/head_down.png").convert_alpha(), (cell_size, cell_size))
        self.head_right = pygame.transform.scale(pygame.image.load("graphics/head_right.png").convert_alpha(), (cell_size, cell_size))
        self.head_left = pygame.transform.scale(pygame.image.load("graphics/head_left.png").convert_alpha(), (cell_size, cell_size))
        
        self.tail_up = pygame.transform.scale(pygame.image.load("graphics/tail_up.png").convert_alpha(), (cell_size, cell_size))
        self.tail_down = pygame.transform.scale(pygame.image.load("graphics/tail_down.png").convert_alpha(), (cell_size, cell_size))
        self.tail_right = pygame.transform.scale(pygame.image.load("graphics/tail_right.png").convert_alpha(), (cell_size, cell_size))
        self.tail_left = pygame.transform.scale(pygame.image.load("graphics/tail_left.png").convert_alpha(), (cell_size, cell_size))
        
        self.body_tr = pygame.transform.scale(pygame.image.load("graphics/body_tr.png").convert_alpha(), (cell_size, cell_size))
        self.body_tl = pygame.transform.scale(pygame.image.load("graphics/body_tl.png").convert_alpha(), (cell_size, cell_size))
        self.body_br = pygame.transform.scale(pygame.image.load("graphics/body_br.png").convert_alpha(), (cell_size, cell_size))
        self.body_bl = pygame.transform.scale(pygame.image.load("graphics/body_bl.png").convert_alpha(), (cell_size, cell_size))
        
        self.body_vertical = pygame.transform.scale(pygame.image.load("graphics/body_vertical.png").convert_alpha(), (cell_size, cell_size))
        self.body_horizontal = pygame.transform.scale(pygame.image.load("graphics/body_horizontal.png").convert_alpha(), (cell_size, cell_size))

        self.head = self.head_right
        self.tail = self.tail_right
        self.grow = False

    def update_head_graphic(self):
        head_direction =  self.body[0] - self.body[1]
        if(head_direction == Vector2(1,0)): self.head = self.head_right
        elif(head_direction == Vector2(-1,0)): self.head = self.head_left
        elif(head_direction == Vector2(0,-1)): self.head = self.head_up
        elif(head_direction == Vector2(0,1)): self.head = self.head_down
            
    def update_tail_graphic(self):
        tail_direction =  self.body[-2] - self.body[-1]
        if(tail_direction == Vector2(1,0)): self.tail = self.tail_right
        elif(tail_direction == Vector2(-1,0)): self.tail = self.tail_left
        elif(tail_direction == Vector2(0,-1)): self.tail = self.tail_up
        elif(tail_direction == Vector2(0,1)): self.tail = self.tail_down
            
    def draw_snake(self):
        # drawing snake as a set of colored squares
        # pygame.draw.rect(screen, (222, 200, 20),pygame.Rect(int(self.body[0].x * cell_size), int(self.body[0].y * cell_size), cell_size, cell_size))
        # for block in self.body[1:]:
        #     #create a rect
        #     #draw the rectangle
        #     block_rect = pygame.Rect(int(block.x * cell_size), int(block.y * cell_size), cell_size, cell_size)
        #     pygame.draw.rect(screen,(222, 222, 22),block_rect)
        self.update_head_graphic()
        self.update_tail_graphic()

        for index, block in enumerate(self.body):
            x_pos = int(block.x * cell_size)
            y_pos = int(block.y * cell_size)
            block_rect = pygame.Rect(x_pos, y_pos, cell_size, cell_size)

            if (index == 0):
                screen.blit(self.head,block_rect)
            elif (index == len(self.body)-1):
                screen.blit(self.tail, block_rect)
            else:
                #pygame.draw.rect(screen,(222, 222, 22),block_rect)
                previous_block =  self.body[index + 1] - block
                next_block = self.body[index - 1] - block
                
                #horizontal / vertical
                if(previous_block.x == next_block.x):#vertical movement
                    screen.blit(self.body_vertical, block_rect)
                elif(previous_block.y == next_block.y):
                    screen.blit(self.body_horizontal, block_rect)
                #turning
                else:
                    if(previous_block.x == -1 and next_block.y == -1) or (previous_block.y == -1 and next_block.x == -1):
                        screen.blit(self.body_tl, block_rect)
                    elif(previous_block.x == 1 and next_block.y == -1) or (previous_block.y == -1 and next_block.x == 1):
                        screen.blit(self.body_tr, block_rect)
                    elif(previous_block.x == -1 and next_block.y == 1) or (previous_block.y == 1 and next_block.x == -1):
                        screen.blit(self.body_bl, block_rect)
                    elif(previous_block.x == 1 and next_block.y == 1) or (previous_block.y == 1 and next_block.x == 1):
                        screen.blit(self.body_br, block_rect)

    def change_snake_direction(self, dir):
        if self.direction.y == 0:
            if (dir == "u" or dir == "up"):
                self.direction = Vector2(0,-1)
            if dir == "d" or dir == "down":
                self.direction = Vector2(0,1)
        if self.direction.x == 0:        
            if dir == "r" or dir == "right":
                self.direction = Vector2(1,0)
            if dir == "l" or dir == "left":
                self.direction = Vector2(-1,0)

    #grow = False

    def move_snake(self):
        if self.direction != Vector2 (0,0):
            if self.grow:
                body_copy = self.body
                self.grow = False
            else:
                body_copy = self.body[:-1]

            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy

    def add_block(self):
        self.grow = True

    def reset(self):
        self.body = [Vector2(5,10),Vector2(4,10),Vector2(3,10)]
        self.direction = Vector2(0,0)

class FRUIT:
    def __init__(self):
        self.randomize()

    def draw_fruit(self):
        fruit_rect = pygame.Rect(int(self.pos.x * cell_size),int(self.pos.y * cell_size),cell_size,cell_size)
        #drawin fruit as a red square:
        #pygame.draw.rect(screen,(255,20,20),fruit_rect)
        #drawing fruit as a png:
        screen.blit(apple, fruit_rect)

    def randomize(self):
        self.x = random.randint(0,cell_number-1)
        self.y = random.randint(0,cell_number-1)
        self.pos = pygame.math.Vector2(self.x, self.y)

class MAIN:
    def __init__ (self):
        self.snake = SNAKE()
        self.fruit = FRUIT()

    def update(self):
        self.snake.move_snake()
        self.check_collision()
        self.check_fail()

    def draw_elements(self):
        self.draw_grass()
        self.fruit.draw_fruit()
        self.snake.draw_snake()
        self.draw_score()
    
    def check_collision (self):
        if self.fruit.pos == self.snake.body[0]:
            self.fruit.randomize()
            self.snake.add_block()

        for block in self.snake.body[1:]:
            if block == self.fruit.pos:
                self.fruit.randomize()

    def check_fail(self):
        if (not 0 <= self.snake.body[0].x < cell_number) or (not 0 <= self.snake.body[0].y < cell_number):
            self.game_over()
        
        if(self.snake.body[0] in self.snake.body[1:]):
            self.game_over()

    def game_over(self):
        # pygame.quit() 
        # sys.exit()
        self.snake.reset()

    def draw_grass(self):
        grass_color = (136, 202, 53)

        modifier = 0
        for row in range(cell_number):
            if row % 2 == 0: modifier = 0
            else: modifier = 1

            for col in range(cell_number):
                if (col + modifier) % 2 == 0:
                    grass_rect = pygame.Rect(col * cell_size, row * cell_size,cell_size, cell_size)
                    pygame.draw.rect(screen, grass_color, grass_rect)

    def draw_score(self):
        score_text = str(len(self.snake.body) - 3)
        score_surface = game_font.render(score_text,True, (0,0,0))
        score_x = int(cell_size*cell_number - 60)
        score_y = int(cell_size*cell_number - 40)
        score_rect = score_surface.get_rect(center = (score_x, score_y))
        apple_rect = apple.get_rect(midright = (score_rect.left, score_rect.centery))

        screen.blit(score_surface, score_rect)
        screen.blit(apple,apple_rect)
#setup & game variables
pygame.init()

def eval_genomes(genomes, config):
    global cell_size, cell_number, screen, apple, game_font, snakes, fruits, ge, nets
    cell_size = 40
    cell_number = 20

    screen = pygame.display.set_mode((cell_number * cell_size,cell_number*cell_size))

    apple = pygame.transform.scale(pygame.image.load("graphics/Apple0002.png").convert_alpha(), (cell_size, cell_size))

    game_font = pygame.font.Font("VT323.ttf", 40)

    SCREEN_UPDATE = pygame.USEREVENT
    pygame.time.set_timer(SCREEN_UPDATE, 170)
    clock = pygame.time.Clock()
    
    #init
    snakes = []
    fruits = []
    #fitness = [0 for snake in range(len(snakes))]
    ge = []
    nets = []

    for genome_id, genome in genomes:
        snakes.append(SNAKE())
        fruits.append(FRUIT())
        ge.append(genome)
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        nets.append(net)
        genome.fitness = 0

    #functions
    def update():
        for snake in snakes:
            snake.move_snake()
        check_collision()
        check_fail()
        #count_fitness()
        kill_nonactive()

    def kill_nonactive():
        for index, snake in enumerate(snakes):
            if snake.direction == Vector2(0,0):
                game_over(index)
                print ("Nonactive - ", end="")
    def draw_elements():
        draw_grass()
        for index, snake in enumerate(snakes):
            fruits[index].draw_fruit()
            snake.draw_snake()

    def check_collision ():
        for index, snake in enumerate(snakes):
            fruit = fruits[index]
            if fruit.pos == snake.body[0]:
                #this snake just got better!
                ge[index].fitness += 1
                fruit.randomize()
                snake.add_block()
                while fruit.pos in snake.body:
                    fruit.randomize()

    def check_fail():
        for index, snake in enumerate(snakes):
            if (not 0 <= snake.body[0].x < cell_number) or (not 0 <= snake.body[0].y < cell_number):
                game_over(index)
            
            if(snake.body[0] in snake.body[1:]):
                game_over(index)

    def game_over(index):
        #loose fitness on death - we don't want that
        ge[index].fitness -= 5
        snakes.pop(index)
        fruits.pop(index)
        ge.pop(index)
        nets.pop(index)
        print (f'{str(index)} has died. Snakes left: {len(snakes)}')

    def draw_grass():
        grass_color = (136, 202, 53)

        modifier = 0
        for row in range(cell_number):
            if row % 2 == 0: modifier = 0
            else: modifier = 1

            for col in range(cell_number):
                if (col + modifier) % 2 == 0:
                    grass_rect = pygame.Rect(col * cell_size, row * cell_size,cell_size, cell_size)
                    pygame.draw.rect(screen, grass_color, grass_rect)

    def stats():
        text_1 = game_font.render(f'Generation: {population.generation}', True, (0,0,0))
        screen.blit(text_1, ((cell_number-6)*cell_size, (cell_number-2)*cell_size))

    # def count_fitness():
    #     for index, snake in enumerate (snakes):
    #        fitness[index] = len(snake.body) - 3

    run = True
    #game loop
    while run:
        if not (len(snakes) > 0):
            run = False
            break
        for event in pygame.event.get():
            if (event.type == pygame.QUIT):
                run = False
                pygame.quit() 
                sys.exit()
            if (event.type == SCREEN_UPDATE):
                update()
            
            #user_input = pygame.key.get_pressed()

            for index, snake in enumerate(snakes):
                ge[index].fitness += 0.1 #Snakes get points for staing alive
                output = nets[index].activate((snake.body[0].x, snake.body[0].y, fruits[index].pos.x, fruits[index].pos.y))
                if output[0] > 0.5:
                    snake.change_snake_direction("up")
                elif output[1] > 0.5:
                    snake.change_snake_direction("d")
                if output[2] > 0.5:
                    snake.change_snake_direction("r")
                elif output[3] > 0.5:
                    snake.change_snake_direction("left")


        screen.fill((136, 222, 53))
        draw_elements()
        stats()
        pygame.display.update()
        clock.tick(30)

def run(config_path):
    print("RUN!")
    config = neat.config.Config(neat.DefaultGenome, 
                                neat.DefaultReproduction, 
                                neat.DefaultSpeciesSet, 
                                neat.DefaultStagnation,
                                config_path)
    global population
    population = neat.Population(config)
    population.run(eval_genomes, 50) #evolution (fitness) fuction, how many generations

if __name__ == '__main__':
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config.txt")
    run(config_path)
