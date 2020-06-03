import pygame, random
from pygame.locals import* 
import sys


SCREEN_WIDTH = 400
SCREEN_HEIGHT = 650

SPEED = 10
GRAVITY = 1

ANGLE_INIT = 10
ANGLE_FINALY = -1

GAME_SPEED = 5 
GROUND_WIDTH = 2 * SCREEN_WIDTH
GROUND_HEIGHT = 80
PIPE_WIDTH = 88
PIPE_HEIGHT = 500
PIPE_GAP = 100 

def main():
    class Bird(pygame.sprite.Sprite):
        def __init__(self):
            pygame.sprite.Sprite.__init__(self)

            self.images = [pygame.image.load('assets/sprites/bluebird-upflap.png').convert_alpha(),
                        pygame.image.load('assets/sprites/bluebird-midflap.png').convert_alpha(),
                        pygame.image.load('assets/sprites/bluebird-downflap.png').convert_alpha() ]

            self.speed = SPEED
            self.rotate = ANGLE_INIT

            self.current_image = 0

            self.image = pygame.image.load('assets/sprites/bluebird-midflap.png').convert_alpha()
            self.mask = pygame.mask.from_surface(self.image)

            
            self.rect = self.image.get_rect()
            self.rect[0] = SCREEN_WIDTH / 4     
            self.rect[1] = SCREEN_HEIGHT / 2

    

        def update(self):
            self.current_image = (self.current_image + 1) % 3
            self.image = self.images[self.current_image] 

            self.image = pygame.transform.rotate(self.images[self.current_image], self.rotate)

            self.speed += GRAVITY

            self.rotate += ANGLE_FINALY

            self.rect[1] += self.speed 

            
        def bump(self):
            self.speed = -SPEED
            self.rotate = ANGLE_INIT
            


    class Pipe(pygame.sprite.Sprite):
        def __init__(self, inverted, xpos, ysize):
            pygame.sprite.Sprite.__init__(self)

            self.image = pygame.image.load('assets/sprites/pipe-green.png').convert_alpha()
            self.image = pygame.transform.scale(self.image, (PIPE_WIDTH,PIPE_HEIGHT))

            self.rect = self.image.get_rect()
            self.rect[0] = xpos

            if inverted:
                self.image = pygame.transform.flip(self.image, False, True)
                self.rect[1] = - (self.rect[3] - ysize)
            else:
                self.rect[1] = SCREEN_HEIGHT - ysize

            self.mask = pygame.mask.from_surface(self.image)


        def update(self):
            self.rect[0] -= GAME_SPEED

    class Ground(pygame.sprite.Sprite):
        
        def __init__(self, xpos):
            pygame.sprite.Sprite.__init__(self)

            self.image = pygame.image.load('assets/sprites/base.png').convert_alpha() 
            self.image = pygame.transform.scale(self.image, (GROUND_WIDTH, GROUND_HEIGHT))

            self.mask = pygame.mask.from_surface(self.image)


            self.rect = self.image.get_rect()
            self.rect[0] = xpos
            self.rect[1] = SCREEN_HEIGHT - GROUND_HEIGHT

        def update(self):
            self.rect[0] -= GAME_SPEED


    def is_off_screen(sprite):
        return sprite.rect[0] < -(sprite.rect[2])

    def point(sprite, sprite1):
        return sprite.rect[0] == 100 

        
    def pipe_get_radom(xpos):
        size = random.randint(100, 350)
        pipe = Pipe(False, xpos, size)
        pipe_inverted = Pipe(True, xpos, SCREEN_HEIGHT - size - PIPE_GAP)
        return pipe, pipe_inverted


    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT ))

    BACKGROUND = pygame.image.load('assets/sprites/background-day.png')
    BACKGROUND = pygame.transform.scale(BACKGROUND, (SCREEN_WIDTH, SCREEN_HEIGHT))

    WING = pygame.mixer.Sound('assets/audio/wing.wav')
    DIE = pygame.mixer.Sound('assets/audio/die.wav')
    HIT = pygame.mixer.Sound('assets/audio/hit.wav')
    POINT = pygame.mixer.Sound('assets/audio/point.wav')
    MUSIC = pygame.mixer.music.load('assets/audio/init.mp3')
    MUSIC = pygame.mixer.music.play(1, 0.0)


    bird_group = pygame.sprite.Group()
    bird = Bird()
    bird_group.add(bird)


    pipe_group = pygame.sprite.Group()
    for g in range(2):     
        pipes = pipe_get_radom(SCREEN_WIDTH * g + 800)
        pipe_group.add(pipes[0])
        pipe_group.add(pipes[1])

    ground_group = pygame.sprite.Group()
    for i in range(2):
        ground = Ground(GROUND_WIDTH * i)                        
        ground_group.add(ground)

    clock = pygame.time.Clock()

    score = 0

    font_init = pygame.font.Font('assets/fonts/bing_bam_boum/Bing Bam Boum.ttf', 45)
    text = font_init.render(str(score), True, (255,255,225), False)
    textRect = text.get_rect()
    textRect.center = (200, 60)

    while True:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == KEYDOWN:
                if event.key == K_SPACE:
                    bird.bump()
                    WING.play()
                    
        
        screen.blit(BACKGROUND,(0,0))


        if is_off_screen(ground_group.sprites()[0]):
            ground_group.remove(ground_group.sprites()[0])

            new_ground = Ground(GROUND_WIDTH - 20) 
            ground_group.add(new_ground)

        
        if is_off_screen(pipe_group.sprites()[0]):
            pipe_group.remove(pipe_group.sprites()[0])
            pipe_group.remove(pipe_group.sprites()[0])

            new_pipes = pipe_get_radom(SCREEN_WIDTH * 2) 
            pipe_group.add(new_pipes[0])
            pipe_group.add(new_pipes[1])

        if point(pipe_group.sprites()[0], False  ):
            score += 1
            text = font_init.render(str(score), True, (255,255,225), False)
            POINT.play()
            
        pipe_group.update()
        ground_group.update()
        bird_group.update()
        
        
        pipe_group.draw(screen )      
        ground_group.draw(screen)
        bird_group.draw(screen)   
        
        
        screen.blit(text, textRect)
        pygame.display.update()

        if pygame.sprite.groupcollide(bird_group, ground_group, False,False, pygame.sprite.collide_mask):
            HIT.play()
            break  
            game_over()           
            
        elif pygame.sprite.groupcollide(bird_group, pipe_group, False,False, pygame.sprite.collide_mask):
            HIT.play()
            DIE.play()
            break
            game_over()
            
    
def animacao():
    class Bird(pygame.sprite.Sprite):
        def __init__(self):
            pygame.sprite.Sprite.__init__(self)

            self.images = [pygame.image.load('assets/sprites/bluebird-upflap.png').convert_alpha(),
                        pygame.image.load('assets/sprites/bluebird-midflap.png').convert_alpha(),
                        pygame.image.load('assets/sprites/bluebird-downflap.png').convert_alpha() ]

            self.speed = SPEED
            self.current_image = 0

            self.image = pygame.image.load('assets/sprites/bluebird-midflap.png').convert_alpha()
            self.mask = pygame.mask.from_surface(self.image)

            
            self.rect = self.image.get_rect()
            self.rect[0] = SCREEN_WIDTH / 4     
            self.rect[1] = SCREEN_HEIGHT / 2

    

        def update(self):
            self.current_image = (self.current_image + 1) % 3
            self.image = self.images[self.current_image] 


    class Ground(pygame.sprite.Sprite):
        
        def __init__(self, xpos):
            pygame.sprite.Sprite.__init__(self)

            self.image = pygame.image.load('assets/sprites/base.png').convert_alpha() 
            self.image = pygame.transform.scale(self.image, (GROUND_WIDTH, GROUND_HEIGHT))

            self.mask = pygame.mask.from_surface(self.image)


            self.rect = self.image.get_rect()
            self.rect[0] = xpos
            self.rect[1] = SCREEN_HEIGHT - GROUND_HEIGHT

        def update(self):
            self.rect[0] -= GAME_SPEED


    def is_off_screen(sprite):
        return sprite.rect[0] < -(sprite.rect[2])


    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT ))

    BACKGROUND = pygame.image.load('assets/sprites/background-day.png')
    BACKGROUND = pygame.transform.scale(BACKGROUND, (SCREEN_WIDTH, SCREEN_HEIGHT))

    MUSIC = pygame.mixer.music.load('assets/audio/init.mp3')
    MUSIC = pygame.mixer.music.play(1, 0.0)
    
    bird_group = pygame.sprite.Group()
    bird = Bird()
    bird_group.add(bird)

    

    ground_group = pygame.sprite.Group()
    for i in range(2):
        ground = Ground(GROUND_WIDTH * i)                        
        ground_group.add(ground)

    clock = pygame.time.Clock()

    while True:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == KEYDOWN:
                if event.key == K_SPACE:
                    main()
        
        screen.blit(BACKGROUND,(0,0))

        if is_off_screen(ground_group.sprites()[0]):
            ground_group.remove(ground_group.sprites()[0])

            new_ground = Ground(GROUND_WIDTH - 20) 
            ground_group.add(new_ground)

        bird_group.update()
        ground_group.update()
        
     
        ground_group.draw(screen)
        bird_group.draw(screen)   
        
        pygame.display.update()




def game_over(game_main):


    while True:

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == KEYDOWN:
                if event.key == K_SPACE:
                    main()
            
                    
animacao()
game_main = main()



if __name__ == '__main__':
    main()