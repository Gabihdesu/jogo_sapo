import pygame
from pygame.locals import *
from sys import exit
import random

pygame.init()

largura = 640
altura = 400
pontos = 0
max_pontos = 10

tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption('Sprites')

# Carregar a imagem de fundo
fundo = pygame.image.load('sprites/grama.jpg')
fundo = pygame.transform.scale(fundo, (largura, altura))


def tocar_musica(musica):
    pygame.mixer.music.load(musica)
    pygame.mixer.music.play(-1)  # O argumento -1 faz a música tocar continuamente

def parar_musica():
    pygame.mixer.music.stop()

class Apple(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.sprite = pygame.image.load('sprites/maca.png')
        self.image = pygame.transform.scale(self.sprite, (100,100))
        self.rect = self.image.get_rect()
        self.rect.topleft = 400, 180

    def trocar_posicao(self):
        self.rect.x = random.randint(0, largura - self.rect.width)
        self.rect.y = random.randint(0, altura - self.rect.height)

class Sapo(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.sprites = [pygame.image.load(f'sprites/attack_{i}.png') for i in range(1, 11)]
        self.atual = 0
        self.image = self.sprites[self.atual]
        self.image = pygame.transform.scale(self.image, (128 * 3, 64 * 3))
        self.rect = self.image.get_rect()
        self.rect.topleft = 100, 100
        self.animar = False
        self.colisao_registrada = False

    def update(self):
        global pontos
        if self.animar:
            self.atual += 0.5
            if self.atual >= len(self.sprites):
                self.atual = 0
                self.animar = False
                self.colisao_registrada = False
            self.image = self.sprites[int(self.atual)]
            self.image = pygame.transform.scale(self.image, (128 * 3, 64 * 3))
            if int(self.atual) == 5 or int(self.atual) == 6:
                if self.rect.colliderect(maca.rect) and not self.colisao_registrada:
                    maca.trocar_posicao()
                    pontos += 1
                    self.colisao_registrada = True
    def atacar(self):
        self.animar = True

def reiniciar_jogo():
    global pontos, sapo, maca, todas_sprites
    pontos = 0
    sapo = Sapo()
    maca = Apple()
    todas_sprites = pygame.sprite.Group()
    todas_sprites.add(sapo)
    todas_sprites.add(maca)


# Inicializar as sprites
reiniciar_jogo()

pygame.font.init()
fonte_pontos = pygame.font.SysFont('arial', 50)
fonte_fim = pygame.font.SysFont('arial', 40)
fonte_opcoes = pygame.font.SysFont('arial', 30)

relogio = pygame.time.Clock()
velocidade = 5
jogo_ativo = True
tocar_musica('musica-fundo.mp3')
while True:
    while jogo_ativo:
        relogio.tick(30)
        tela.blit(fundo, (0, 0))
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()
            if event.type == KEYDOWN:
                if event.key == K_SPACE:
                    sapo.atacar()
                if event.key == K_ESCAPE:
                    pygame.quit()
                    exit()

        keys = pygame.key.get_pressed()
        if keys[K_LEFT]:
            sapo.rect.x -= velocidade
        if keys[K_RIGHT]:
            sapo.rect.x += velocidade
        if keys[K_UP]:
            sapo.rect.y -= velocidade
        if keys[K_DOWN]:
            sapo.rect.y += velocidade

        todas_sprites.update()
        todas_sprites.draw(tela)

        texto = fonte_pontos.render(f"Maçãs: {pontos}", True, (255, 255, 255))
        tela.blit(texto, (largura - 10 - texto.get_width(), 10))

        pygame.display.flip()

        if pontos >= max_pontos:
            jogo_ativo = False
            # Parar a música atual e iniciar outra
            parar_musica()
            tocar_musica('victory.mp3')


    tela.fill((0, 0, 0))
    texto_fim = fonte_fim.render(f"PARABÉNS! VOCÊ FEZ {pontos} PONTOS!!!", True, (255, 255, 255))
    tela.blit(texto_fim, (largura // 2 - texto_fim.get_width() // 2, altura // 3 - texto_fim.get_height() // 2))

    texto_reiniciar = fonte_opcoes.render("Pressione R para Reiniciar", True, (255, 255, 255))
    texto_sair = fonte_opcoes.render("Pressione ESC para Sair", True, (255, 255, 255))
    tela.blit(texto_reiniciar, (largura // 2 - texto_reiniciar.get_width() // 2, altura // 2))
    tela.blit(texto_sair, (largura // 2 - texto_sair.get_width() // 2, altura // 2 + 50))

    pygame.display.flip()

    while not jogo_ativo:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()
            if event.type == KEYDOWN:
                if event.key == K_r:
                    reiniciar_jogo()
                    jogo_ativo = True
                if event.key == K_ESCAPE:
                    pygame.quit()
                    exit()
