# Danmaku Universe 🚀🌌

Um jogo de nave no estilo **Danmaku (Bullet Hell)** desenvolvido em Python utilizando a biblioteca **Pygame**. Este projeto foi criado como um trabalho acadêmico durante o **1º período de Engenharia de Software**, com o objetivo de aprofundar o domínio da linguagem Python, lógica de programação e arquitetura básica de jogos.

---

## 🎮 Sobre o Jogo

Em *Danmaku Universe*, o jogador controla uma nave espacial que deve sobreviver a ondas intensas de inimigos e desviar de padrões complexos de projéteis. O jogo testa os reflexos do jogador com mecânicas clássicas de jogos arcade e progressão de dificuldade.

### Principais Funcionalidades Implementadas:
* **Máquina de Estados:** Gerenciamento estruturado de telas (Menu Principal, Seleção de Dificuldade, Gameplay, Modo Boss e Game Over).
* **Sistema de Dificuldades Dinâmico:** Ajuste fino de *cooldowns*, velocidade, quantidade de balas e padrões de ataque para 4 modos: *Fácil, Médio, Difícil e Insano*.
* **Padrões de Tiro Matemáticos:** Inimigos utilizam funções trigonométricas (`math.atan2`, `math.cos`, `math.sin`) para calcular ângulos de tiro na direção do jogador ou em espirais geométricas.
* **Mecânica de Hitbox Precisa:** O jogador possui uma hitbox reduzida (ponto verde) centralizada na nave, fiel ao estilo *Bullet Hell*.
* **Habilidades Especiais:** Sistema de Bombas (*Screen Clear*) para limpar projéteis da tela e causar dano a chefes, além de períodos de invulnerabilidade temporária (*iframes*) após sofrer dano.
* **Modo Chefe (Boss Battle):** Lutas contra chefes com barras de vida dinâmicas e transição de padrões de ataque baseados na vida restante (*Spellcards*).

---

## 🛠️ Tecnologias Utilizadas

* **Python 3.12**
* **Pygame:** Biblioteca para desenvolvimento de jogos 2D (gráficos, eventos e áudio).
* **Math (Biblioteca Nativa):** Para os cálculos vetoriais e circulares dos projéteis.

---

## 📦 Estrutura do Projeto

Para que o código funcione corretamente, certifique-se de que a estrutura de pastas do repositório siga o padrão esperado pelo script:

```text
├── imagens/
│   ├── nave.png
│   ├── laser_player.png
│   ├── laser_enemy.png
│   ├── inimigo.png
│   ├── inimigo_2.png
│   ├── inimigo_3.png
│   └── boss.png
├── musica/
│   ├── Stage.mp3
│   └── Boss.mp3
├── sons/
│   ├── Shoot.mp3
│   ├── Bomb.mp3
│   ├── Change.mp3
│   └── Click.mp3
└── main.py
```

---

## 🕹️ Controles
* Setas / WASD: Movimentam a nave.
* SHIFT (Esquerdo/Direito): Modo Foco (reduz a velocidade da nave para desvios precisos).
* BARRA DE ESPAÇO: Atirar.
* X: Soltar Bomba (Limpa a tela e causa dano ao Boss).

---

## 🧠 Aprendizado Acadêmico
Este projeto foi fundamental para consolidar conceitos de:
* Programação Orientada a Objetos (POO): Utilização de classes e herança através do pygame.sprite.Sprite.
* Gerenciamento de Recursos: Carregamento de texturas e buffers de áudio.
* Game Loop e FPS: Controle do tempo e atualização de física na tela de forma assíncrona.

---

Feito com 💜 por Haislan Halabura
