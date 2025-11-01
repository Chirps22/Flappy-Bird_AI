import pygame
import os
import sys
import random

pygame.init()

# Game window dimensions
WIN_WIDTH = 600
WIN_HEIGHT = 600
WIN = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))

# Load images
# Load and scale images
BIRD_IMG = pygame.transform.scale(pygame.image.load(os.path.join("GUI", "bird.png")), (40, 30))
BG_IMG = pygame.transform.scale(pygame.image.load(os.path.join("GUI", "background.jpg")).convert(), (600, 600))
PIPE_IMG = pygame.transform.scale(pygame.image.load(os.path.join("GUI", "pipe.png")), (200, 500))

class Bird:
    MAX_ROTATION = 25
    ROT_VEL = 20
    ANIMATION_TIME = 5

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.tilt = 0
        self.tick_count = 0
        self.vel = 0
        self.height = self.y
        self.img = BIRD_IMG

    def jump(self):
        self.vel = -10.5
        self.tick_count = 0
        self.height = self.y

    def move(self):
        self.tick_count += 1
        # basic physics for gravity
        d = self.vel * self.tick_count + 1.5 * self.tick_count ** 2

        if d >= 16:
            d = 16
        if d < 0:
            d -= 2

        self.y += d

        # simple tilt animation
        if d < 0 or self.y < self.height + 50:
            if self.tilt < self.MAX_ROTATION:
                self.tilt = self.MAX_ROTATION
        else:
            if self.tilt > -90:
                self.tilt -= self.ROT_VEL

    def draw(self, win):
        rotated_image = pygame.transform.rotate(self.img, self.tilt)
        new_rect = rotated_image.get_rect(center=self.img.get_rect(topleft=(self.x, self.y)).center)
        win.blit(rotated_image, new_rect.topleft)

class Pipe:
    GAP = 200
    VEL = 5

    def __init__(self, x):
        self.x = x
        self.height = 0
        self.top = 0
        self.bottom = 0
        self.PIPE_BOTTOM = PIPE_IMG  # normal pipe (opening at top)
        self.PIPE_TOP = pygame.transform.flip(PIPE_IMG, False, True)  # flipped (opening at bottom)
        self.passed = False
        self.set_height()

    def set_height(self):
        # Random vertical position for the gap
        self.height = random.randrange(100, 400)
        self.top = self.height - self.PIPE_TOP.get_height()
        self.bottom = self.height + self.GAP

    def move(self):
        self.x -= self.VEL

    def draw(self, win):
        # Draw top pipe (upside down)
        win.blit(self.PIPE_TOP, (self.x, self.top))
        # Draw bottom pipe (normal)
        win.blit(self.PIPE_BOTTOM, (self.x, self.bottom))

    def collide(self, bird):
        bird_mask = pygame.mask.from_surface(bird.img)
        top_mask = pygame.mask.from_surface(self.PIPE_TOP)
        bottom_mask = pygame.mask.from_surface(self.PIPE_BOTTOM)

        top_offset = (self.x - bird.x, self.top - round(bird.y))
        bottom_offset = (self.x - bird.x, self.bottom - round(bird.y))

        b_point = bird_mask.overlap(bottom_mask, bottom_offset)
        t_point = bird_mask.overlap(top_mask, top_offset)

        return b_point or t_point

def draw_window(win, bird, pipes):
    # Draw background
    win.blit(BG_IMG, (0, 0))

    # Draw pipes
    for pipe in pipes:
        pipe.draw(win)

    # Draw bird
    bird.draw(win)

    # Update display ONCE here
    pygame.display.update()


def main():
    bird = Bird(230, 300)
    pipes = [Pipe(700)]
    clock = pygame.time.Clock()
    run = True

    while run:
        clock.tick(30)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                bird.jump()

        # Move bird and pipes
        bird.move()
        add_pipe = False
        rem = []

        for pipe in pipes:
            pipe.move()
            if pipe.collide(bird):
                 run = False
            
            if bird.y + bird.img.get_height() >= WIN_HEIGHT:
                run = False  # hit the ground
            elif bird.y < 0:
                run = False  # flew too high

            if pipe.x + pipe.PIPE_TOP.get_width() < 0:
                rem.append(pipe)

            if not pipe.passed and pipe.x < bird.x:
                pipe.passed = True
                add_pipe = True

        if add_pipe:
            pipes.append(Pipe(600))
        for r in rem:
            pipes.remove(r)

        draw_window(WIN, bird, pipes)


if __name__ == "__main__":
    main()
