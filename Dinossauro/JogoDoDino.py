# Credits to the dino bird to TSR
# All rights belong to ther owners

import pygame
from pygame.locals import *
from random import randrange, choice
import os
# Junta o diretório principal, com o diretório de imagens e sons
diretorio_principal = os.path.dirname(__file__)
diretorio_imagens = os.path.join(diretorio_principal, 'imagens')
diretorio_sons = os.path.join(diretorio_principal, 'sons')
pygame.init()
pygame.mixer.init()
LARGURA = 640
ALTURA = 480

tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption('Dino Runner')
# Carrega uma imagem, depois junta o diretório de imagens com a imagem que tem dentro dele
background_art = pygame.image.load(os.path.join(diretorio_imagens, 'pre_historia.png')).convert()
imagem_fundo = pygame.transform.scale(background_art, (LARGURA, ALTURA))
colidiu = False
escolha_obstaculo = choice([0, 1])
velocidade_jogo = 10
pontos = 0
pontuacao_maxima = 0
if os.path.exists('pontuacao.txt'):
    with open('pontuacao.txt', 'r') as file:
        pontuacao_maxima = int(file.read())
else:
    pontuacao_maxima = 0
def exibe_mensagem(msg, tamanho, cor):  # Exibe mensagens de pontos, game over e sair
    fonte = pygame.font.SysFont('choco', tamanho, True, False)
    mensagem = f'{msg}'
    texto_formatado = fonte.render(mensagem, False, cor)
    return texto_formatado

def reiniciar_jogo():
    global pontos, velocidade_jogo, colidiu, escolha_obstaculo
    dino.rect.y = ALTURA - 64 - 96 // 2
    pontos = 0
    dino.pulo = False
    velocidade_jogo = 10
    colidiu = False
    dino_voador.rect.x = LARGURA
    arvore.rect.x = LARGURA
    escolha_obstaculo = choice([0, 1])
class Dino(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.som_pulo = pygame.mixer.Sound(os.path.join(diretorio_sons, 'jump_sound.wav'))
        self.som_pulo.set_volume(1)
        self.som_da_colisao = pygame.mixer.Sound(os.path.join(diretorio_sons, 'death_sound.wav'))
        self.som_da_colisao.set_volume(1)
        self.som_pontuacao = pygame.mixer.Sound(os.path.join(diretorio_sons, 'score_sound.wav'))
        self.som_pontuacao.set_volume(1)
        self.musica_fundo = pygame.mixer.Sound(os.path.join(diretorio_sons, 'musica_dino.wav'))
        self.musica_fundo.set_volume(1)
        self.som_do_dino = pygame.mixer.Sound(os.path.join(diretorio_sons,'som_do_dino.wav'))
        self.som_do_dino.set_volume(1)
       # Foi criada uma lista de imagens
        self.imagens_dinossauro = []
        self.imagens_dinossauro.append(pygame.image.load('imagens/dino_correndo0.png'))
        self.imagens_dinossauro.append(pygame.image.load('imagens/dino_correndo1.png'))
        self.imagens_dinossauro.append(pygame.image.load('imagens/dino_correndo2.png'))
        self.imagens_dinossauro.append(pygame.image.load('imagens/dino_correndo3.png'))
        self.imagens_dinossauro.append(pygame.image.load('imagens/dino_correndo4.png'))
        self.imagens_dinossauro.append(pygame.image.load('imagens/dino_correndo5.png'))
        self.imagens_dinossauro.append(pygame.image.load('imagens/dino_correndo6.png'))
        self.imagens_dinossauro.append(pygame.image.load('imagens/dino_correndo7.png'))
        self.imagens_dinossauro.append(pygame.image.load('imagens/dino_correndo8.png'))
        self.imagens_dinossauro.append(pygame.image.load('imagens/dino_correndo9.png'))
        self.index_lista = 0
        self.image = self.imagens_dinossauro[self.index_lista]
        self.image = pygame.transform.scale(self.image, (48*2, 41*2))
        self.rect = self.image.get_rect()
        # Posicione o centro desse retângulo na posição 100x e 100y
        self.rect.center = (100, ALTURA-64)
        self.pulo = False
        self.pos_y_inicial = ALTURA-68 - 96//2
        self.mask = pygame.mask.from_surface(self.image)
        # Foi criado uma máscara para a imagem do dino para poder trabalhar a colisão

    def pular(self):
        self.pulo = True
        self.som_pulo.play()

    def rugir(self):
        self.som_do_dino.play()

    def colidir(self):
        self.som_da_colisao.play()

    def update(self):
        if self.pulo == True:
            self.rect.y = self.rect.y - 60
            if self.rect.y <= 70:
                self.pulo = False
        else:
            if self.rect.y < self.pos_y_inicial:
                self.rect.y += 20
            else:
                self.rect.y = self.pos_y_inicial
        if self.index_lista > 2:
            self.index_lista = 0
        self.index_lista = self.index_lista + 0.25
        self.image = self.imagens_dinossauro[int(self.index_lista)]
        self.image = pygame.transform.scale(self.image, (48 * 2, 41 * 2))

class Nuvens(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.lista_nuvens = []
        self.lista_nuvens.append(pygame.image.load('imagens/cloud-sprite0.png'))
        self.lista_nuvens.append(pygame.image.load('imagens/cloud-sprite1.png'))
        self.index_lista = 0
        self.image = self.lista_nuvens[self.index_lista]
        self.image = pygame.transform.scale(self.image,(32*2, 32*2))
        self.rect = self.image.get_rect()
        self.rect.y = randrange(50, 200, 50)
        self.rect.x = randrange(LARGURA, 0, -50)

    def update(self):
        if self.rect.topright[0] < 0:
            self.rect.x = LARGURA
            self.rect.y = randrange(50, 200, 50)
        self.rect.x = self.rect.x - velocidade_jogo
        if self.index_lista > 1:
            self.index_lista = 0
        self.index_lista += 0.20
        self.image = self.lista_nuvens[int(self.index_lista)]
        self.image = pygame.transform.scale(self.image, (32*2, 32*2))
class Chao(pygame.sprite.Sprite):
    def __init__(self, pos_x):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('imagens/chao_pre_historico.png')
        self.rect = self.image.get_rect()
        self.rect.center = (100, 400)
        self.image = pygame.transform.scale(self.image, (32*2, 32*2))
        self.rect.y = ALTURA - 50
        self.rect.x = pos_x * 64

    def update(self):
        if self.rect.topright[0] < 0:
            self.rect.x = LARGURA
        self.rect.x = self.rect.x - 10


class Arvore(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.imagem_arvore = []
        self.imagem_arvore.append(pygame.image.load('imagens/arvore_pre_historia0.png'))
        self.imagem_arvore.append(pygame.image.load('imagens/arvore_pre_historia1.png'))
        self.index_lista = 0
        self.image = self.imagem_arvore[self.index_lista]
        self.image = pygame.transform.scale(self.image, (32*2, 32*2))
        self.rect = self.image.get_rect()
        self.rect.center = (LARGURA, ALTURA - 87)
        self.mask = pygame.mask.from_surface(self.image)
        self.escolha = escolha_obstaculo
        self.rect.x = LARGURA

    def update(self):
        if self.escolha == 0:
            if self.rect.topright[0] < 0:
                self.rect.x = LARGURA
            else:
                self.rect.x = self.rect.x - velocidade_jogo
            if self.index_lista > 1:
                self.index_lista = 0
            self.index_lista += 0.20
            self.image = self.imagem_arvore[int(self.index_lista)]
        self.image = pygame.transform.scale(self.image, (28 * 2, 43 * 2))

class DinoVoador(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.imagens_dino_voador = []
        self.imagens_dino_voador.append(pygame.image.load('imagens/dino_voador0.png'))
        self.imagens_dino_voador.append(pygame.image.load('imagens/dino_voador1.png'))
        self.imagens_dino_voador.append(pygame.image.load('imagens/dino_voador2.png'))
        self.imagens_dino_voador.append(pygame.image.load('imagens/dino_voador3.png'))
        self.index_lista = 0
        self.image = self.imagens_dino_voador[self.index_lista]
        self.image = pygame.transform.scale(self.image, (28*2, 43*2))
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.center = (LARGURA, 200)
        self.escolha = escolha_obstaculo
        self.rect.x = LARGURA

    def update(self):
        if self.escolha == 1:
            if self.rect.topright[0] < 0:
                self.rect.x = LARGURA
            else:
                self.rect.x = self.rect.x - velocidade_jogo
            if self.index_lista > 1:
                self.index_lista = 0
            self.index_lista += 0.20
            self.image = self.imagens_dino_voador[int(self.index_lista)]
        self.image = pygame.transform.scale(self.image, (28 * 2, 43 * 2))


AMARELO = (204, 138, 0)
def mostrar_texto():
    fonte = pygame.font.SysFont('choco', 50)
    titulo = fonte.render('HÁ 65 MILHÕES DE ANOS ATRÁS...', False, AMARELO, None)
    tela.blit(titulo,[30, 150])
    pygame.display.flip()

def mostrar_titulo_jogo():
    fonte = pygame.font.SysFont('choco', 50)
    texto = fonte.render('DINO RUNNER', False, AMARELO, None)
    tela.blit(texto, [200, 150])
    pygame.display.flip()

def mostrar_pontuacao_no_final(pontuacao): # Mostra a pontuação no final do jogo
    fonte = pygame.font.SysFont("choco", 50)
    texto = fonte.render(f'Sua pontuação é {pontuacao}', False, (238, 104, 0), None)
    tela.blit(texto, [200, 150])
    pygame.display.flip()

def mostrar_pontuacao_maxima(maxima_pontuacao):  # Mostra a pontuação máxima
    fonte = pygame.font.SysFont('choco', 50)
    texto = fonte.render(f'Pontuação máxima: {maxima_pontuacao}', False, (0, 0, 0), None)
    tela.blit(texto, [200, 100])

todas_as_sprites = pygame.sprite.Group()
dino = Dino()
arvore = Arvore()
dino_voador = DinoVoador()
todas_as_sprites.add(dino)
todas_as_sprites.add(arvore)
grupo_obstaculos = pygame.sprite.Group()
grupo_obstaculos.add(arvore)
todas_as_sprites.add(dino_voador)
grupo_obstaculos.add(dino_voador)
desvanecimento = 0

for c in range(LARGURA*3//64): # Aqui vai ser criado a repetição das sprites do chão
    chao = Chao(c)
    todas_as_sprites.add(chao)

for i in range(3):  # Criado a repetição das sprites da nuvem
    nuvens = Nuvens()
    todas_as_sprites.add(nuvens)
relogio = pygame.time.Clock()
deve_continuar = True
mostrar_texto()
dino.rugir()
dino.musica_fundo.play()
pygame.time.delay(6000)
tela.fill((0, 0, 0))
pygame.time.delay(2000)
mostrar_titulo_jogo()
pygame.time.delay(2000)
while deve_continuar:
    relogio.tick(25)
    tela.blit(imagem_fundo, (0, 0))
    for event in pygame.event.get():
        if event.type == QUIT:
            deve_continuar = False
        if event.type == KEYDOWN:
            if event.key == K_SPACE and colidiu == False:
                if dino.rect.y != dino.pos_y_inicial:
                    pass
                else:
                    dino.pular()
            if event.key == K_r and colidiu == True:
                reiniciar_jogo()
            if event.key == K_ESCAPE and colidiu == True:
                deve_continuar = False
    colisoes = pygame.sprite.spritecollide(dino, grupo_obstaculos, False, pygame.sprite.collide_mask)
    todas_as_sprites.draw(tela)  # a variável ao lado contém todas as sprites, o método draw() desenha na tela essas imagens
    if arvore.rect.topright[0] <= 0 or dino_voador.rect.topright[0] <= 0:  # Impede que os obstáculos apareçam ao mesmo tempo
        escolha_obstaculo = choice([0, 1])
        arvore.rect.x = LARGURA
        dino_voador.rect.x = LARGURA
        arvore.escolha = escolha_obstaculo
        dino_voador.escolha = escolha_obstaculo
    if colisoes and colidiu == False:  # Verifica as colisões
        dino.colidir()
        colidiu = True
    if colidiu == True:  # Escreve a pontuação máxima em um arquivo
        if pontos > pontuacao_maxima:
            pontuacao_maxima = pontos
            with open('pontuacao.txt', 'w') as file:
                file.write(str(pontuacao_maxima))
        if desvanecimento < LARGURA:  # Efeito da tela preta no final do jogo
            desvanecimento += 20
            pygame.draw.rect(tela,(0,0,0),(0, 0, LARGURA, ALTURA))
        game_over = exibe_mensagem("FIM DE JOGO", 40, (204,138,0))
        tela.blit(game_over, (LARGURA//2, ALTURA//2))
        texto_reiniciar = exibe_mensagem('Pressione r para reiniciar', 26, (204,138,0))
        texto_sair = exibe_mensagem('ou ESC para sair', 26, (204,138,0))
        tela.blit(texto_reiniciar, (LARGURA//2, (ALTURA//2)+60))
        tela.blit(texto_sair, (LARGURA//2, (ALTURA//2)+75))
        mostrar_pontuacao_no_final(pontos)
    else:
        pontos += 1   # Aqui ele vai incrementar a pontuação
        mostrar_pontuacao_maxima(pontuacao_maxima)
        todas_as_sprites.update()  # o método update() atualiza na tela o movimento das sprites
        texto_pontos = exibe_mensagem(pontos, 50, (0, 0, 0))
    if pontos % 100 == 0 and colidiu == False:  # A cada 100 pontos ele exibe o som da pontuação.
        dino.som_pontuacao.play()
        if velocidade_jogo >= 23:
            velocidade_jogo += 0
        else:
            velocidade_jogo += 1
    desvanecimento = 0
    tela.blit(texto_pontos, (520, 30))
    pygame.display.update()
