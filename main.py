import pygame, sys

SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
FPS = 60

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
gravity = 0.001

# class Player:
#     def __init__(self, dx: float, dy: float, image: str):
#         self.dx = dx
#         self.dy = dy
#         self.on_ground = on_ground
#         self.current_img = image


class Map:
    def __init__(self, sprite: pygame.surface.Surface):
        self.sprite = sprite
        self.rect = sprite.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))

    @staticmethod
    def scale(direction_image: pygame.surface.Surface) -> pygame.surface.Surface:
        return pygame.transform.smoothscale(direction_image, (800, 600))

    @classmethod
    def load(cls, sprite_name: str) -> "Map":
        sprite = pygame.image.load(f"sprites/map/{sprite_name}.png")
        sprite = cls.scale(sprite)
        return Map(sprite)

    def draw(self, screen: pygame.surface.Surface):
        screen.blit(self.sprite, self.rect)


map_1 = Map.load("background_1")


# todo: skala postaci zgodna z proporcjami zdjecia
def scale_player(direction_image: pygame.surface.Surface) -> pygame.surface.Surface:
    return pygame.transform.smoothscale(direction_image, (40, 80))

def load_player_sprite(sprite_name: str) -> pygame.surface.Surface:
    sprite = pygame.image.load(f"sprites/player/{sprite_name}.png")
    return scale_player(sprite)

player_static = load_player_sprite("static")
player_left1 = load_player_sprite("left_1")
player_left2 = load_player_sprite("left_2")
player_left3 = load_player_sprite("left_3")
player_left4 = load_player_sprite("left_4")
player_left5 = load_player_sprite("left_5")


player_right1 = load_player_sprite("right_1")
player_right2 = load_player_sprite("right_2")
player_right3 = load_player_sprite("right_3")
player_right4 = load_player_sprite("right_4")
player_right5 = load_player_sprite("right_5")

player_img = player_static
player_rect = player_img.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
player_velocity_y = 0
count = 0
jumps_left = 2

running = True
while running:
    dt = clock.tick(FPS)  # sekundy od poprzedniej klatki

    space_down_this_frame = False

    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False
        elif e.type == pygame.KEYDOWN and e.key == pygame.K_SPACE:
            space_down_this_frame = True

    keys = pygame.key.get_pressed()
    is_right_pressed = keys[pygame.K_RIGHT]
    is_left_pressed = keys[pygame.K_LEFT]
    is_space_pressed = keys[pygame.K_SPACE]

    if count == 30:
        count = 0

    ground = 480

    # player_pos_y = player_rect.y
    # player_pos_x = player_rect.x
    on_ground = False

    if player_rect.y == ground:
        on_ground = True

    if space_down_this_frame and jumps_left > 0:
        jumps_left -= 1
        player_velocity_y = -0.35
        on_ground = False

    player_rect.y += player_velocity_y * dt #y
    player_velocity_y += gravity * dt #dy

    if player_rect.y >= ground:
        player_rect.y = ground
        player_velocity_y = 0
        on_ground = True
        jumps_left = 2


    if is_right_pressed:
        count += 1
        player_rect.x += 2
        if player_velocity_y != 0:
            player_img = player_right2
        elif count < 5:
            player_img = player_right3
        elif 5 <= count < 10:
            player_img = player_right4
        elif 10 <= count < 15:
            player_img = player_right3
        else:
            player_img = player_right2


    elif is_left_pressed:
        count += 1
        player_rect.x -= 2
        if player_velocity_y != 0:
            player_img = player_left2
        elif count < 5:
            player_img = player_left3
        elif 5 <= count < 10:
            player_img = player_left4
        elif 10 <= count < 15:
            player_img = player_left3
        else:
            player_img = player_left2
    else:
        player_img = player_static

    map_1.draw(screen)
    # screen.fill((0, 255, 0))
    screen.blit(player_img, player_rect)
    pygame.display.flip()

pygame.quit()
sys.exit()