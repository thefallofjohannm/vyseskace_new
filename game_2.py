import pygame
from platforms import Platform
from config import *
from Block import Block
from jumper import Jumper
from coin import Coin
from io import BytesIO

class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("You jump and have fun")
        self.clock = pygame.time.Clock()

        # Load sounds
        self.load_sounds()

        # Initialize game objects
        self.player = Jumper(self.screen, 200, 10)
        self.blocks = []
        self.number_of_blocks = 5
        self.platforms = self.create_platforms()
        self.coin_group = pygame.sprite.Group()
        self.coin = Coin(self.screen)
        self.coin_group.add(self.coin)

        self.score = 0
        self.done = False

    def load_sounds(self):
        with open('OfGodsAndPhilosophers(loop)(120).mp3', 'rb') as wav_file:
            wav_data = wav_file.read()
        wav_file = BytesIO(wav_data)
        self.soundtrack = pygame.mixer.Sound(wav_file)
        self.soundtrack.play(-1)

        with open('Stinger_Fail4.wav', 'rb') as wav_file_2:
            wav_data_2 = wav_file_2.read()
        wav_file_2 = BytesIO(wav_data_2)
        self.fail_sound = pygame.mixer.Sound(wav_file_2)

        with open('Stinger_Success6.wav', 'rb') as wav_file_3:
            wav_data_3 = wav_file_3.read()
        wav_file_3 = BytesIO(wav_data_3)
        self.collect_sound = pygame.mixer.Sound(wav_file_3)

    def create_platforms(self):
        platforms = pygame.sprite.Group()
        # x,y,width,height,velocity
        platform_data = [
            (100, 400, 50, 10, 2),
            (200, 100, 30, 10, 3),
            (300, 600, 50, 10, 1),
            (400, 550, 25, 10, 4),
            (500, 52, 30, 10, 1),
            (600, 420, 50, 10, 3),
            (700, 69, 50, 10, 2),
            (800, 51, 25, 10, 8),
            (900, 320, 25, 10, 1),
            (1000, 500, 50, 10, 2)
        ]

        for data in platform_data:
            platforms.add(Platform(*data))

        return platforms

    def draw_background(self):
        self.screen.fill(LBLUE)
        self.draw_tree(20, 450)
        self.draw_sun(300, 100)

    def draw_tree(self, x, y):
        pygame.draw.rect(self.screen, BROWN, [60 + x, 170 + y, 30, 45])
        pygame.draw.polygon(self.screen, GREEN2, [[150 + x, 170 + y], [75 + x, 20 + y], [x, 170 + y]])
        pygame.draw.polygon(self.screen, GREEN2, [[140 + x, 120 + y], [75 + x, y], [10 + x, 120 + y]])

    def draw_sun(self, x, y):
        pygame.draw.ellipse(self.screen, YELLOW, [900, 100, 50, 50])
        pygame.draw.line(self.screen, YELLOW, [885, 85], [965, 165], 2)
        pygame.draw.line(self.screen, YELLOW, [925, 75], [925, 175], 2)
        pygame.draw.line(self.screen, YELLOW, [965, 85], [885, 165], 2)
        pygame.draw.line(self.screen, YELLOW, [975, 125], [875, 125], 2)

    def draw_ground(self):
        pygame.draw.rect(self.screen, WHITE, [0, self.screen.get_height() - 43, self.screen.get_width(), 43], 30)

    def update_blocks(self):
        # fake blocks for confusion
        for i in range(self.number_of_blocks - len(self.blocks)):
            self.blocks.append(Block(self.screen, self.get_height_of_highest_block() - 50))

        new_blocks = []
        for b in self.blocks:
            if b.position_y < self.screen.get_height():
                b.shift()
                b.draw()
                new_blocks.append(b)
        self.blocks = new_blocks

    def get_height_of_highest_block(self):
        min_height = self.screen.get_height() - 500
        for b in self.blocks:
            min_height = min(min_height, b.position_y)
        return min_height

    def draw_score(self):
        font = pygame.font.Font(None, 36)
        text = font.render(f"Score: {self.score}", True, BLACK)
        self.screen.blit(text, (900, 10))

    def check_coin_collision(self):
        for coin in self.coin_group:
            if self.player.rect.colliderect(coin.rect):
                coin.spawn()
                self.score += 936
                self.collect_sound.play()

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.done = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.player.go_left()
                elif event.key == pygame.K_RIGHT:
                    self.player.go_right()
                elif event.key == pygame.K_UP:
                    self.player.jump()

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    self.player.stop_movement()

    def limit_player_movement(self):
        if self.player.position[0] >= 1085:
            self.player.position[0] = 1085
        if self.player.position[0] <= 0:
            self.player.position[0] = 0
        if self.player.position[1] <= -5:
            self.player.position[1] = -5

    def check_respawn(self):
        if 6000 >= self.player.position[1] >= 700:
            self.player.stop_movement()
            self.player.position[0] = 200
            self.player.position[1] = 10
            self.score = 0
            self.fail_sound.play()

    def game_loop(self):
        while not self.done:
            self.handle_input()

            self.player.update(self.platforms)
            self.draw_background()

            self.update_blocks()

            self.player.draw()
            self.platforms.update()
            self.platforms.draw(self.screen)

            self.draw_ground()
            self.coin_group.draw(self.screen)

            self.check_coin_collision()
            self.limit_player_movement()
            self.check_respawn()

            self.draw_score()

            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()
