import pygame
import sys
import random
import math

pygame.init()
pygame.mixer.init()

# Load sons
som_tiro = pygame.mixer.Sound("sons/Shoot.mp3")
som_bomba = pygame.mixer.Sound("sons/Bomb.mp3")
som_mudanca_menu = pygame.mixer.Sound("sons/Change.mp3")
som_escolha_menu = pygame.mixer.Sound("sons/Click.mp3")

som_tiro.set_volume(0.2)

# Configurações da Tela
LARGURA, ALTURA = 700, 800
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Danmaku universe")

# Controle de FPS
relogio = pygame.time.Clock()
FPS = 60

# Load imagens

IMG_JOGADOR = pygame.image.load('imagens/nave.png').convert_alpha()
IMG_TIRO_JOGADOR = pygame.image.load('imagens/laser_player.png').convert_alpha()
IMG_TIRO_INIMIGO = pygame.image.load('imagens/laser_enemy.png').convert_alpha()
IMG_INIMIGO_PADRAO1 = pygame.image.load('imagens/inimigo.png').convert_alpha()
IMG_INIMIGO_PADRAO2 = pygame.image.load('imagens/inimigo_2.png').convert_alpha()
IMG_INIMIGO_PADRAO3 = pygame.image.load('imagens/inimigo_3.png').convert_alpha()
IMG_BOSS = pygame.image.load('imagens/boss.png').convert_alpha()
IMG_BACKGROUND = pygame.image.load('imagens/fundo.png').convert()

# Dicionário de dificuldades
CONFIG_DIFICULDADE = {
    "FÁCIL": {
        "tempo_spawn": 1500, "cooldown_tiro": 2000, "quantidade_balas": 4, "padroes_disponiveis": [1],
        "boss_cooldown": 600, "boss_vel_x": 2, "boss_balas_sp1": 3, "boss_balas_sp2": 10
    },
    "MÉDIO": {
        "tempo_spawn": 1000, "cooldown_tiro": 1500, "quantidade_balas": 8, "padroes_disponiveis": [1, 2],
        "boss_cooldown": 500, "boss_vel_x": 2.5, "boss_balas_sp1": 4, "boss_balas_sp2": 12
    },
    "DIFÍCIL": {
        "tempo_spawn": 600, "cooldown_tiro": 1000, "quantidade_balas": 12, "padroes_disponiveis": [1, 2, 3],
        "boss_cooldown": 400, "boss_vel_x": 3, "boss_balas_sp1": 4, "boss_balas_sp2": 16
    },
    "INSANO": {
        "tempo_spawn": 300, "cooldown_tiro": 600, "quantidade_balas": 20, "padroes_disponiveis": [2, 3],
        "boss_cooldown": 250, "boss_vel_x": 4, "boss_balas_sp1": 6, "boss_balas_sp2": 24
    }
}

# Variaveis globais
PONTUACAO = 0
PROXIMO_BOSS = 5000 
PROXIMA_BOMBA = 5000  
APARICOES_BOSS = 0 
ESTADO = "MENU" 
DIFICULDADE_ATUAL = "MÉDIO" 
DIFICULDADES_LISTA = ["FÁCIL", "MÉDIO", "DIFÍCIL", "INSANO"]
INDICE_SELECIONADO = 1
MODO_DE_JOGO = "ENDLESS"
PONTUACAO_VITORIA = 8000
VENCEU = False
LARGURA_BG, ALTURA_BG = IMG_BACKGROUND.get_size()
fundo_y1 = 0
fundo_y2 = -ALTURA_BG
velocidade_fundo = 2

fonte_hud = pygame.font.SysFont('arial', 32, bold=True)
fonte_bombas = pygame.font.SysFont('arial', 26, bold=True)
fonte_titulo = pygame.font.SysFont('arial', 46, bold=True)
fonte_subtitulo = pygame.font.SysFont('arial', 24)
fonte_spellcard = pygame.font.SysFont('comicsansms', 22, italic=True, bold=True)

EVENTO_CRIAR_INIMIGO = pygame.USEREVENT + 1


# Classe de tiro inimigo
class TiroInimigo(pygame.sprite.Sprite):
    def __init__(self, x, y, angulo, velocidade_bala):
        super().__init__()
        self.image = pygame.transform.scale(IMG_TIRO_INIMIGO, (12, 12))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.vel_x = math.cos(angulo) * velocidade_bala
        self.vel_y = math.sin(angulo) * velocidade_bala

    def update(self):
        self.rect.x += self.vel_x
        self.rect.y += self.vel_y
        if (self.rect.top > ALTURA or self.rect.bottom < 0 or 
            self.rect.left > LARGURA or self.rect.right < 0):
            self.kill()


# Classe inimigo
class Inimigo(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        
        self.rect = pygame.Rect(0, 0, 40, 40) # Cria um retângulo base para o posicionamento
        self.rect.x = random.randint(50, LARGURA - 50)
        self.rect.y = random.randint(-100, -40)
        self.velocidade_y = random.randint(2, 4)
        self.tempo_ultimo_tiro = pygame.time.get_ticks()
        
        config = CONFIG_DIFICULDADE[DIFICULDADE_ATUAL]
        self.tipo_padrao = random.choice(config["padroes_disponiveis"])
        self.qtd_balas = config["quantidade_balas"]
        
        # Define o sprite/imagem de acordo com o padrão sorteado
        if self.tipo_padrao == 1:
            self.image = pygame.transform.scale(IMG_INIMIGO_PADRAO1, (40, 40))
        elif self.tipo_padrao == 2:
            self.image = pygame.transform.scale(IMG_INIMIGO_PADRAO2, (40, 40))
        elif self.tipo_padrao == 3:
            self.image = pygame.transform.scale(IMG_INIMIGO_PADRAO3, (40, 40))
            
        # Ajusta o rect definitivo para o tamanho da imagem escolhida
        self.rect = self.image.get_rect(center=(self.rect.x, self.rect.y))
        
        # Mantém a logica alterada para o tipo 2
        if self.tipo_padrao == 2:
            self.cooldown_tiro = config["cooldown_tiro"] * 2.5
        else:
            self.cooldown_tiro = random.randint(config["cooldown_tiro"] - 100, config["cooldown_tiro"] + 100)

    def update(self):
        self.rect.y += self.velocidade_y
        if self.rect.top > ALTURA:
            self.kill()
            
        agora = pygame.time.get_ticks()
        if agora - self.tempo_ultimo_tiro > self.cooldown_tiro:
            self.tempo_ultimo_tiro = agora
            self.atirar()

    def atirar(self):
        dx = jogador.rect.centerx - self.rect.centerx
        dy = jogador.rect.centery - self.rect.bottom
        angulo_mirado = math.atan2(dy, dx)

        if self.tipo_padrao == 1:
            angulos = [angulo_mirado - math.radians(20), angulo_mirado, angulo_mirado + math.radians(20)]
            for ang in angulos:
                bala = TiroInimigo(self.rect.centerx, self.rect.bottom, ang, 4.5)
                todos_os_sprites.add(bala)
                grupo_tiros_inimigos.add(bala)
                
        elif self.tipo_padrao == 2:
            for i in range(self.qtd_balas):
                ang = (2 * math.pi / self.qtd_balas) * i
                bala = TiroInimigo(self.rect.centerx, self.rect.bottom, ang, 3)
                todos_os_sprites.add(bala)
                grupo_tiros_inimigos.add(bala)
                
        elif self.tipo_padrao == 3:
            for i in range(4):
                ang = (2 * math.pi / 4) * i + angulo_mirado
                bala = TiroInimigo(self.rect.centerx, self.rect.bottom, ang, 5)
                todos_os_sprites.add(bala)
                grupo_tiros_inimigos.add(bala)


# Classe boss
class Boss(pygame.sprite.Sprite):
    def __init__(self, numero_aparicoes):
        super().__init__()
        self.image = pygame.transform.scale(IMG_BOSS, (100, 100))
        self.rect = self.image.get_rect()
        self.rect.centerx = LARGURA // 2
        self.rect.y = -100 
        
        self.vida_max = 1500 + (numero_aparicoes * 1000)
        self.vida = self.vida_max
        
        config_boss = CONFIG_DIFICULDADE[DIFICULDADE_ATUAL]
        self.velocidade_x = config_boss["boss_vel_x"]
        self.cooldown_tiro = config_boss["boss_cooldown"]
        self.balas_sp1 = config_boss["boss_balas_sp1"]
        self.balas_sp2 = config_boss["boss_balas_sp2"]
        
        self.tempo_ultimo_tiro = pygame.time.get_ticks()
        self.angulo_rotacao = 0

    def update(self):
        if self.rect.y < 180:
            self.rect.y += 2
        else:
            self.rect.x += self.velocidade_x
            if self.rect.right >= LARGURA - 20 or self.rect.left <= 20:
                self.velocidade_x *= -1 

        agora = pygame.time.get_ticks()
        if agora - self.tempo_ultimo_tiro > self.cooldown_tiro and self.rect.y >= 180:
            self.tempo_ultimo_tiro = agora
            self.atirar()

    def atirar(self):
        dx = jogador.rect.centerx - self.rect.centerx
        dy = jogador.rect.centery - self.rect.bottom
        angulo_mirado = math.atan2(dy, dx)

        if self.vida > (self.vida_max / 2):
            self.angulo_rotacao += 0.25 
            for i in range(self.balas_sp1):
                ang = (2 * math.pi / self.balas_sp1) * i + self.angulo_rotacao + (angulo_mirado * 0.1)
                bala = TiroInimigo(self.rect.centerx, self.rect.bottom, ang, 4.5)
                todos_os_sprites.add(bala)
                grupo_tiros_inimigos.add(bala)
        else:
            for i in range(self.balas_sp2):
                ang = (2 * math.pi / self.balas_sp2) * i + angulo_mirado
                bala = TiroInimigo(self.rect.centerx, self.rect.bottom, ang, 3.8)
                todos_os_sprites.add(bala)
                grupo_tiros_inimigos.add(bala)


# Classe tiro jogador
class Tiro(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.transform.scale(IMG_TIRO_JOGADOR, (8, 20))
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.velocidade_y = -14

    def update(self):
        self.rect.y += self.velocidade_y
        if self.rect.bottom < 0:
            self.kill()


# Classe jogador
class Jogador(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.imagem_original = pygame.transform.scale(IMG_JOGADOR, (50, 50))
        self.image = self.imagem_original
        self.rect = self.image.get_rect()
        self.rect.centerx = LARGURA // 2
        self.rect.bottom = ALTURA - 50
        
        self.hitbox = pygame.Rect(0, 0, 10, 10)
        self.hitbox.center = self.rect.center
        self.velocidade = 6
        self.tempo_ultimo_tiro = 0
        self.cooldown_tiro = 150 
        self.vidas = 3
        self.bombas = 2  

        # Iframes
        self.invulneravel = False
        self.tempo_dano = 0
        self.duracao_iframe = 500

    def update(self):
        teclas = pygame.key.get_pressed()
        agora = pygame.time.get_ticks()

        # Gerenciamento de Iframes e efeito de piscar
        if self.invulneravel:
            if agora - self.tempo_dano > self.duracao_iframe:
                self.invulneravel = False
                self.image = self.imagem_original
            else:
                # Efeito visual de piscar
                if (agora // 50) % 2 == 0:
                    self.image = pygame.Surface((0, 0))
                else:
                    self.image = self.imagem_original

        if teclas[pygame.K_LSHIFT] or teclas[pygame.K_RSHIFT]:
            v_atual = self.velocidade / 2  
        else:
            v_atual = self.velocidade      
        
        dx, dy = 0, 0
        if teclas[pygame.K_LEFT] or teclas[pygame.K_a]:  dx = -1
        if teclas[pygame.K_RIGHT] or teclas[pygame.K_d]: dx = 1
        if teclas[pygame.K_UP] or teclas[pygame.K_w]:    dy = -1
        if teclas[pygame.K_DOWN] or teclas[pygame.K_s]:  dy = 1

        if dx != 0 and dy != 0:
            self.rect.x += dx * v_atual * 0.7071
            self.rect.y += dy * v_atual * 0.7071
        else:
            self.rect.x += dx * v_atual
            self.rect.y += dy * v_atual

        if teclas[pygame.K_SPACE]:
            self.atirar()
            som_tiro.play()

        if self.rect.left < 0: self.rect.left = 0
        if self.rect.right > LARGURA: self.rect.right = LARGURA
        if self.rect.top < 0: self.rect.top = 0
        if self.rect.bottom > ALTURA: self.rect.bottom = ALTURA
        
        self.hitbox.center = self.rect.center

    def atirar(self):
        agora = pygame.time.get_ticks()
        if agora - self.tempo_ultimo_tiro > self.cooldown_tiro:
            self.tempo_ultimo_tiro = agora
            tiro = Tiro(self.rect.centerx, self.rect.top)
            todos_os_sprites.add(tiro)
            grupo_tiros.add(tiro)

    def soltar_bomba(self, boss_atual):
        global PONTUACAO
        if self.bombas > 0:
            self.bombas -= 1
            for bala in grupo_tiros_inimigos:
                bala.kill()
            for inimigo in grupo_inimigos:
                inimigo.kill()
                PONTUACAO += 100
            if boss_atual:
                boss_atual.vida -= 300

    def receber_dano(self):
        if not self.invulneravel:
            self.vidas -= 1
            self.invulneravel = True
            self.tempo_dano = pygame.time.get_ticks()


# Renderização de HUD e telas
def desenhar_hud():
    txt_p = fonte_hud.render(f"SCORE: {PONTUACAO}", True, (255, 255, 255))
    tela.blit(txt_p, (10, 10))
    txt_d = fonte_subtitulo.render(f"{MODO_DE_JOGO} - {DIFICULDADE_ATUAL}", True, (180, 180, 180))
    tela.blit(txt_d, (10, 45))
    
    txt_v = fonte_hud.render(f"LIVES: {jogador.vidas}", True, (0, 255, 100))
    tela.blit(txt_v, (LARGURA - 150, 10))
    
    txt_b = fonte_bombas.render(f"BOMBS: {jogador.bombas}", True, (255, 150, 0))
    tela.blit(txt_b, (LARGURA - 150, 45))

def atualizar_e_desenhar_fundo():
    global fundo_y1, fundo_y2
    
    fundo_y1 += velocidade_fundo
    fundo_y2 += velocidade_fundo
    
    if fundo_y1 >= ALTURA:
        fundo_y1 = -ALTURA_BG + (fundo_y1 - ALTURA)
        
    if fundo_y2 >= ALTURA:
        fundo_y2 = -ALTURA_BG + (fundo_y2 - ALTURA)
        
    tela.blit(IMG_BACKGROUND, (0, fundo_y1))
    tela.blit(IMG_BACKGROUND, (0, fundo_y2))

def desenhar_barra_boss():
    if boss and ESTADO == "BOSS":
        nome_spell = "Spellcard 1: Signo do Caos" if boss.vida > (boss.vida_max/2) else "Final Spell: Juízo Final"
        txt_spell = fonte_spellcard.render(nome_spell, True, (255, 100, 150))
        
        tela.blit(txt_spell, (LARGURA // 2 - txt_spell.get_width() // 2, 80))
        
        pygame.draw.rect(tela, (100, 0, 30), (50, 115, LARGURA - 100, 12))
        largura_vida = (LARGURA - 100) * (boss.vida / boss.vida_max)
        if largura_vida > 0:
            pygame.draw.rect(tela, (255, 0, 50), (50, 115, largura_vida, 12))

def mostrar_tela_menu():
    tela.fill((10, 10, 20))
    txt_titulo = fonte_titulo.render("DANMAKU UNIVERSE", True, (255, 220, 0))
    txt_sub = fonte_subtitulo.render("Pressione ENTER para campanha", True, (255, 255, 255))
    txt_endless = fonte_subtitulo.render("Pressione E para modo endless", True, (200, 200, 200))
    tela.blit(txt_titulo, (LARGURA // 2 - txt_titulo.get_width() // 2, ALTURA // 3))
    tela.blit(txt_sub, (LARGURA // 2 - txt_sub.get_width() // 2, ALTURA // 2))
    tela.blit(txt_endless, (LARGURA // 2 - txt_endless.get_width() // 2, ALTURA // 1.5))

def mostrar_tela_dificuldade():
    tela.fill((15, 20, 35))
    txt_tit = fonte_titulo.render("SELECIONE A DIFICULDADE", True, (255, 255, 255))
    tela.blit(txt_tit, (LARGURA // 2 - txt_tit.get_width() // 2, ALTURA // 5))
    
    for i, diff in enumerate(DIFICULDADES_LISTA):
        if i == INDICE_SELECIONADO:
            texto = fonte_hud.render(f">  {diff}  <", True, (255, 220, 0))
        else:
            texto = fonte_hud.render(diff, True, (140, 140, 140))
        tela.blit(texto, (LARGURA // 2 - texto.get_width() // 2, ALTURA // 2.5 + (i * 60)))
        
    txt_ajuda = fonte_subtitulo.render("Use as SETAS (Cima/Baixo) e ENTER para confirmar", True, (180, 180, 180))
    tela.blit(txt_ajuda, (LARGURA // 2 - txt_ajuda.get_width() // 2, ALTURA - 100))

def mostrar_tela_gameover():
    tela.fill((30, 10, 10)) 
    txt_go = fonte_titulo.render("GAME OVER", True, (255, 50, 50))
    txt_pts = fonte_hud.render(f"Pontuação Final: {PONTUACAO}", True, (255, 255, 255))
    txt_RE = fonte_subtitulo.render("Pressione ENTER para Voltar ao Menu", True, (200, 200, 200))
    tela.blit(txt_go, (LARGURA // 2 - txt_go.get_width() // 2, ALTURA // 4))
    tela.blit(txt_pts, (LARGURA // 2 - txt_pts.get_width() // 2, ALTURA // 2))
    tela.blit(txt_RE, (LARGURA // 2 - txt_RE.get_width() // 2, ALTURA // 1.5))

def mostrar_tela_vitoria():
    tela.fill((10, 40, 20))
    txt_vit = fonte_titulo.render("VOCÊ SALVOU O UNIVERSO", True, (0, 255, 150))
    txt_RE = fonte_subtitulo.render("Pressione ENTER para Voltar ao Menu", True, (200, 200, 200))
    
    tela.blit(txt_vit, (LARGURA // 2 - txt_vit.get_width() // 2, ALTURA // 4))
    tela.blit(txt_RE, (LARGURA // 2 - txt_RE.get_width() // 2, ALTURA // 1.5))

def iniciar_gameplay():
    global PONTUACAO, PROXIMO_BOSS, PROXIMA_BOMBA, APARICOES_BOSS, jogador, boss, VENCEU
    PONTUACAO = 0
    PROXIMA_BOMBA = 5000
    boss = None
    VENCEU = False

    if MODO_DE_JOGO == "CAMPANHA":
        PROXIMO_BOSS = 8000
    else:
        PROXIMO_BOSS = 5000

    todos_os_sprites.empty()
    grupo_tiros.empty()
    grupo_inimigos.empty()
    grupo_tiros_inimigos.empty()
    
    jogador = Jogador()
    todos_os_sprites.add(jogador)
    
    tempo_spawn = CONFIG_DIFICULDADE[DIFICULDADE_ATUAL]["tempo_spawn"]
    pygame.time.set_timer(EVENTO_CRIAR_INIMIGO, tempo_spawn)


# Configuações iniciais dos grupos de sprites e do jogador
todos_os_sprites = pygame.sprite.Group()
grupo_tiros = pygame.sprite.Group()
grupo_inimigos = pygame.sprite.Group()
grupo_tiros_inimigos = pygame.sprite.Group()

jogador = Jogador()
todos_os_sprites.add(jogador)
boss = None 

# Loop principal
duracao_flash_bomba = 0

rodando = True
while rodando:
    
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False
            
        if evento.type == EVENTO_CRIAR_INIMIGO and ESTADO == "JOGANDO":
            inimigo = Inimigo()
            todos_os_sprites.add(inimigo)
            grupo_inimigos.add(inimigo)
            
        if evento.type == pygame.KEYDOWN:
            if ESTADO == "MENU":
                if evento.key == pygame.K_RETURN:
                    som_escolha_menu.play()
                    MODO_DE_JOGO = "CAMPANHA"
                    ESTADO = "SELECAO_DIFICULDADE"
                elif evento.key == pygame.K_e:
                    som_escolha_menu.play()
                    MODO_DE_JOGO = "ENDLESS"    
                    ESTADO = "SELECAO_DIFICULDADE"
                    
            elif ESTADO == "SELECAO_DIFICULDADE":
                if evento.key == pygame.K_UP or evento.key == pygame.K_w:
                    INDICE_SELECIONADO = (INDICE_SELECIONADO - 1) % 4
                    som_mudanca_menu.play()
                elif evento.key == pygame.K_DOWN or evento.key == pygame.K_s:
                    INDICE_SELECIONADO = (INDICE_SELECIONADO + 1) % 4
                    som_mudanca_menu.play()
                elif evento.key == pygame.K_RETURN:
                    som_escolha_menu.play()
                    DIFICULDADE_ATUAL = DIFICULDADES_LISTA[INDICE_SELECIONADO]
                    iniciar_gameplay()
                    ESTADO = "JOGANDO"
                    pygame.mixer.music.load('musica/Stage.mp3')
                    pygame.mixer.music.play(-1)
                    
            elif ESTADO in ["JOGANDO", "BOSS"]:
                if evento.key == pygame.K_x:
                    jogador.soltar_bomba(boss)
                    som_bomba.play()
                    duracao_flash_bomba = 10
                    
            elif ESTADO in ["GAMEOVER", "VITORIA"]:
                if evento.key == pygame.K_RETURN:
                    ESTADO = "MENU"

    # Maquina de estados
    if ESTADO == "MENU":
        mostrar_tela_menu()

    elif ESTADO == "SELECAO_DIFICULDADE":
        mostrar_tela_dificuldade()

    elif ESTADO in ["JOGANDO", "BOSS"]:
        todos_os_sprites.update()

        if PONTUACAO >= PROXIMA_BOMBA:
            jogador.bombas += 1
            PROXIMA_BOMBA += 5000

        if ESTADO == "JOGANDO" and PONTUACAO >= PROXIMO_BOSS:
            ESTADO = "BOSS"
            pygame.mixer.music.stop()
            pygame.mixer.music.load('musica/Boss.mp3')
            pygame.mixer.music.play(-1)
            pygame.mixer.music.set_volume(0.7)
            for inimigo in grupo_inimigos: inimigo.kill()
            boss = Boss(APARICOES_BOSS)
            todos_os_sprites.add(boss)

        # Colisões dos tiros do jogador com inimigos e boss
        for tiro in grupo_tiros:
            inimigos_atingidos = pygame.sprite.spritecollide(tiro, grupo_inimigos, True)
            if inimigos_atingidos:
                tiro.kill()
                PONTUACAO += 100
            
            if ESTADO == "BOSS" and boss and tiro.rect.colliderect(boss.rect):
                tiro.kill()
                boss.vida -= 10

        if ESTADO == "BOSS" and boss and boss.vida <= 0:
            boss.kill()
            boss = None
            PONTUACAO += 1500
            if MODO_DE_JOGO == "CAMPANHA":
                ESTADO = "VITORIA"
                pygame.mixer.music.stop()
            else:
                APARICOES_BOSS += 1 
                PROXIMO_BOSS += 5000 
                ESTADO = "JOGANDO"
                pygame.mixer.music.stop()
                pygame.mixer.music.load('musica/Stage.mp3')
                pygame.mixer.music.play(-1)

        for inimigo in grupo_inimigos:
            if jogador.hitbox.colliderect(inimigo.rect):
                inimigo.kill()
                jogador.receber_dano()
        
        if ESTADO == "BOSS" and boss and jogador.hitbox.colliderect(boss.rect):
            jogador.receber_dano()
                
        for bala in grupo_tiros_inimigos:
            if jogador.hitbox.colliderect(bala.rect):
                bala.kill()
                jogador.receber_dano()
        
        if jogador.vidas <= 0:
            ESTADO = "GAMEOVER"
            pygame.mixer.music.stop()

        # Renderização
        atualizar_e_desenhar_fundo()
        todos_os_sprites.draw(tela)

        if duracao_flash_bomba > 0:
            flash = pygame.Surface((LARGURA,ALTURA))
            flash.fill((255,255,255))
            flash.set_alpha(50)
            tela.blit(flash,(0,0))
            duracao_flash_bomba -=1

        # Só renderiza a Hitbox se o jogador NÃO estiver piscando/invisível
        if jogador.image.get_width() > 0:
            pygame.draw.rect(tela, (0, 255, 0), jogador.hitbox) 
            
        desenhar_hud() 
        desenhar_barra_boss() 

    elif ESTADO == "GAMEOVER":
        mostrar_tela_gameover()

    elif ESTADO == "VITORIA":
        mostrar_tela_vitoria()

    pygame.display.flip()
    relogio.tick(FPS)

pygame.quit()
sys.exit()