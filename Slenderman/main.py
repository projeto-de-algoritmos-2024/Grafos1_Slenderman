import pygame
from config import *
from sprites import *
import sys

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True
        self.font = pygame.font.Font('./Slender.ttf', 32)

        self.notes_collected = 0
        self.total_notes = 7

        self.character_spritesheet = Spritesheet ('img/character.png')
        self.terrain_spritesheet = Spritesheet ('img/terrain.png')
        self.enemy_spritesheet = Spritesheet ('img/enemy.png')
        self.intro_background = pygame.image.load('./img/introbackground.png')
        self.go_background = pygame.image.load('./img/gameover.png')
        self.notes_spritesheet = Spritesheet ('./img/paper.png')

        self.lantern_radius = 200  # Raio da lanterna
        self.lantern_surface = pygame.Surface((WIN_WIDTH, WIN_HEIGHT))  # Superfície para a lanterna
        self.lantern_surface.fill((0, 0, 0))

    def draw_lantern(self, player):
        # Criar um círculo transparente onde a lanterna ilumina
        self.lantern_surface.fill((0, 0, 0))  # Limpa a superfície
        pygame.draw.circle(self.lantern_surface, (0, 0, 0), (player.rect.centerx, player.rect.centery), self.lantern_radius)
        self.lantern_surface.set_colorkey((0, 0, 0))  # Define a cor preta como transparente
        
        # Desenhar a máscara de lanterna sobre a tela
        self.screen.blit(self.lantern_surface, (0, 0))

    def createTilemap(self):
        for i, row in enumerate(tilemap):
            for j, column in enumerate(row):
                Ground(self,j,i)
                if column == 'B':
                    Block (self, j, i)
                if column == 'E':
                    Enemy(self,j,i)
                if column == 'P':
                    self.player = Player (self,j,i)
                if column == 'N':
                    Note (self,j,i)

    def new(self):
        self.playing = True

        self.notes_collected = 0  # Reinicia as páginas coletadas
        self.pages_collected = 0  # Assegure-se de que o contador de páginas está resetado
        self.total_notes = 7 

        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.blocks = pygame.sprite.LayeredUpdates()
        self.enemies = pygame.sprite.LayeredUpdates()
        self.attacks = pygame.sprite.LayeredUpdates()
        self.notes = pygame.sprite.LayeredUpdates()

        self.createTilemap()

        for enemy in self.enemies:
            enemy.speed = 0  # Ajuste inicial da velocidade do inimigo

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False

    def update(self):
        self.all_sprites.update()
        if self.player.rect.centerx or self.player.rect.centery:  # Verifica se o jogador está se movendo
            self.draw_lantern(self.player)
    
    def draw(self):
        self.screen.fill(BLACK)
        self.draw_lantern(self.player)
        self.all_sprites.draw(self.screen)

        score_text = self.font.render(f"{self.notes_collected}/{self.total_notes}", True, WHITE)
        score_rect = score_text.get_rect(topright=(WIN_WIDTH - 10, 10))
        self.screen.blit(score_text, score_rect)

        self.clock.tick(FPS)
        pygame.display.update()

    def main(self):
        while self.playing:
            self.events()
            self.update()
            self.draw()
        

    def game_over(self):
        text = self.font.render('Game Over', True, WHITE)
        text_rect = text.get_rect(center=(WIN_HEIGHT/2, WIN_HEIGHT/2))

        restart_button = Button(10, WIN_HEIGHT - 60, 120, 50, WHITE, BLACK, 'Restart', 32)

        for sprite in self.all_sprites:
            sprite.kill()

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            mouse_pos = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()

            if restart_button.is_pressed(mouse_pos, mouse_pressed):
                self.new()
                self.main()

            self.screen.blit(self.go_background, (0,0))
            self.screen.blit(text, text_rect)
            self.screen.blit(restart_button.image, restart_button.rect)
            self.clock.tick(FPS)
            pygame.display.update()

    def intro_screen(self):
        intro = True

        title = self.font.render('SLENDERMAN', True, WHITE)
        title_rect = title.get_rect(x=10, y=10)
        play_button = Button (10, 50, 100, 50, WHITE, BLACK, 'Play', 32)

        while intro:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    intro = False
                    self.running = False
            
            mouse_pos = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()

            if play_button.is_pressed(mouse_pos, mouse_pressed):
                intro = False

            self.screen.blit(self.intro_background, (0,0))
            self.screen.blit(title, title_rect)
            self.screen.blit(play_button.image, play_button.rect)
            self.clock.tick(FPS)
            pygame.display.update()

    def show_victory_screen(self):
        text = self.font.render('You Won', True, WHITE)
        text_rect = text.get_rect(center=(WIN_WIDTH / 2, WIN_HEIGHT / 2))

        continue_button = Button(10, WIN_HEIGHT - 60, 200, 50, WHITE, BLACK, 'EXIT', 32)

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    return

            mouse_pos = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()

            if continue_button.is_pressed(mouse_pos, mouse_pressed):
                self.running = False  

            self.screen.fill(BLACK)
            self.screen.blit(text, text_rect)
            self.screen.blit(continue_button.image, continue_button.rect)
            pygame.display.update()
            self.clock.tick(FPS)



g = Game()
g.intro_screen()
g.new()
while g.running:
    g.main()
    g.game_over()
pygame.quit()
sys.exit() 