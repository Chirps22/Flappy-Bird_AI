import pygame
import os
import sys
import random

pygame.init()

# Game window dimensions
WIN_WIDTH = 600
WIN_HEIGHT = 600
WIN = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))

#Load and scale images
BG_IMG = pygame.transform.scale(pygame.image.load(os.path.join("GUI", "background.jpg")).convert(), (600, 600))
BIRD_IMG = pygame.transform.scale(pygame.image.load(os.path.join("GUI", "bird.png")), (40, 30))
PIPE_IMG = pygame.transform.scale(pygame.image.load(os.path.join("GUI", "pipe.png")), (100, 500))

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
        d = self.vel * self.tick_count + 1.5 * self.tick_count ** 2

        if d >= 16:
            d = 16
        if d < 0:
            d -= 2

        self.y += d

        #tilt animation
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
    GAP = 15
    VEL = 5

    def __init__(self, x):
        self.x = x
        self.height = 0
        self.top = 0
        self.bottom = 0
        self.PIPE_BOTTOM = PIPE_IMG 
        self.PIPE_TOP = pygame.transform.flip(PIPE_IMG, False, True) 
        self.passed = False
        self.set_height()

    def set_height(self):
        self.height = random.randrange(50, WIN_HEIGHT - 50 - self.GAP)
        self.top = self.height - self.PIPE_TOP.get_height()
        self.bottom = self.height + self.GAP

    def move(self):
        self.x -= self.VEL

    def draw(self, win):
        win.blit(self.PIPE_TOP, (self.x, self.top))
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

def draw_window(win, bird, pipes, score, high_score):
    # Draw background
    win.blit(BG_IMG, (0, 0))

    # Draw pipes
    for pipe in pipes:
        pipe.draw(win)

    # Draw bird
    bird.draw(win)

    #Draw score
    font = pygame.font.SysFont("Arial", 40, bold=True)
    score_text = font.render(f"{score}", True, (255, 255, 255))
    win.blit(score_text, (WIN_WIDTH // 2 - score_text.get_width() // 2, 20))

    small_font = pygame.font.SysFont("Arial", 24)
    high_score_text = small_font.render(f"High Score: {high_score}", True, (255, 255, 255))
    win.blit(high_score_text, (10, 10))

    pygame.display.update()


def main():
    bird = Bird(230, 300)
    pipes = [Pipe(700)]
    clock = pygame.time.Clock()
    run = True
    score = 0

    try:
        with open("highscore.txt", "r") as f:
            high_score = int(f.read().strip())
    except:
        high_score = 0

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
            
            if bird.y + bird.img.get_height() >= WIN_HEIGHT or bird.y < 0:
                run = False

            if pipe.x + pipe.PIPE_TOP.get_width() < 0:
                rem.append(pipe)

            if not pipe.passed and pipe.x < bird.x:
                pipe.passed = True
                add_pipe = True
                score += 1
                # Update high score
                if score > high_score:
                    high_score = score

        if add_pipe:
            pipes.append(Pipe(550))
        for r in rem:
            pipes.remove(r)

        draw_window(WIN, bird, pipes, score, high_score)
    
    with open("highscore.txt", "w") as f:
        f.write(str(high_score))


if __name__ == "__main__":
    main()