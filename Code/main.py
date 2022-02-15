import cv2
import pygame
from src.car import Car

pygame.init()
pygame.font.init()

FPS = 120
WIDTH = 1000
HEIGHT = 700
OFFSET = 100
GREY = pygame.Color(128,128,128)
BLACK = pygame.Color(0,0,0)
L_GREEN = pygame.Color(0, 220, 0)
D_GREEN = pygame.Color(0,80,0)

SPEED_FONT = pygame.font.SysFont('comicsans', 50)
POINTS_FONT = pygame.font.SysFont('comicsans', 50)
W_FONT = pygame.font.SysFont('comicsans', 32)
A_FONT = pygame.font.SysFont('comicsans', 32)
S_FONT = pygame.font.SysFont('comicsans', 32)
D_FONT = pygame.font.SysFont('comicsans', 32)

pygame.display.set_caption("Crazy Driver")
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
SCREEN.fill((0, 0, 0))
back_image = pygame.image.load("assets/track.png").convert()
back_rect = back_image.get_rect().move(0, OFFSET)
action_space = None
observation_space = None
game_reward = 0
score = 0
terminate_run = pygame.USEREVENT + 1
key_strokes = {'w': False, 'a': False, 's': False, 'd': False}


def show_key_strokes(key_strokes):
    active = D_GREEN
    default = BLACK
    w = active if key_strokes['w'] else default
    a = active if key_strokes['a'] else default
    s = active if key_strokes['s'] else default
    d = active if key_strokes['d'] else default

    # pygame.draw.rect(SCREEN, w_bg, (905, 5, 40, 40), 2)  # W
    # pygame.draw.rect(SCREEN, a_bg, (855, 55, 40, 40), 2)  # A
    # pygame.draw.rect(SCREEN, s_bg, (905, 55, 40, 40), 2)  # S
    # pygame.draw.rect(SCREEN, d_bg, (955, 55, 40, 40), 2)  # D

    SCREEN.blit(W_FONT.render(f'W', False, w), dest=(907, 5))  # W
    SCREEN.blit(A_FONT.render(f'A', True, a), dest=(857, 55))  # A
    SCREEN.blit(S_FONT.render(f'S', True, s), dest=(907, 55))  # S
    SCREEN.blit(D_FONT.render(f'D', True, d), dest=(957, 55))  # D

def render(car, action, screen, key_strokes):
    screen.fill(tuple(BLACK))
    screen.blit(back_image, back_rect)

    # TODO: Update car pos
    car.update()
    car.draw(screen)

    if action == 1:
        pygame.draw.rect(screen, (0, 255, 0), (850, 50, 40, 40))
    if action == 2:
        pygame.draw.rect(screen, (0, 255, 0), (800, 100, 40, 40))
    if action == 3:
        pygame.draw.rect(screen, (0, 255, 0), (850, 100, 40, 40))
    if action == 4:
        pygame.draw.rect(screen, (0, 255, 0), (900, 100, 40, 40))

    # Key-strokes info
    show_key_strokes(key_strokes)

    # score
    text_surface = POINTS_FONT.render(f'Points {car.points}', True, pygame.Color('green'))
    screen.blit(text_surface, dest=(0, 0))
    # speed
    text_surface = SPEED_FONT.render(f'Speed {car.vel * -1}', True, pygame.Color('green'))
    screen.blit(text_surface, dest=(420, 0))


def main():
    track_path = 'assets/track.png'
    img = cv2.imread('assets/track1.png', cv2.IMREAD_GRAYSCALE)
    car = Car('assets/car.png', 500, 300)
    clock = pygame.time.Clock()
    data = []
    run = True

    while run:
        clock.tick(FPS)
        for event in pygame.event.get():

            # Exiting the game
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            # Checking user event
            keys_pressed = pygame.key.get_pressed()
            actions = []
            action = 0
            if keys_pressed[pygame.K_w]:
                # Increase speed
                action = 1
            if keys_pressed[pygame.K_a]:
                # Turn left
                action = 2
            if keys_pressed[pygame.K_s]:
                # Decrease Speed
                action = 3
            if keys_pressed[pygame.K_d]:
                # Turn right
                action = 4
            # TODO: do we want to implement a mechanism for constant speed without a key press
            car.action(action)
            actions.append(action)

            # Store the user data for imitation learning
            # wall_distance = car.get_wall_distance()
            # data.append([wall_distance, actions])

            # if event.type == env.terminate_run:
            #     env.return_to_home()

        key_strokes = {
            'w': keys_pressed[pygame.K_w],
            'a': keys_pressed[pygame.K_a],
            's': keys_pressed[pygame.K_s],
            'd': keys_pressed[pygame.K_d]
        }

        render(car, action, SCREEN, key_strokes)
        pygame.display.update()

if __name__ == '__main__':
    main()