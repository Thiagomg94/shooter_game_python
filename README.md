# Mountain Shooter 🚀

Este projeto consiste em um jogo de tiro/nave horizontal (*side-scrolling shoot 'em up*) desenvolvido em **Python** utilizando a biblioteca **Pygame**. O projeto foi estruturado com foco em boas práticas de programação orientada a objetos (POO) e aplicação de padrões de projeto (*design patterns*), caracterizando-se como um excelente recurso prático de cunho acadêmico.

---

## 🎓 Contexto Acadêmico

*   **Instituição:** Uninter - Centro Universitário Internacional
*   **Curso:** Análise e Desenvolvimento de Sistemas
*   **Disciplina:** Linguagem de Programação Aplicada
*   **Semestre/Ano:** 2026/3

---

## 🎮 O Jogo: Mountain Shooter

O objetivo principal do jogo é sobreviver e acumular pontos ao derrotar inimigos em um ambiente montanhoso que se move dinamicamente com efeitos de paralaxe.

### Modos de Jogo:
1.  **NEW GAME 1P (Single Player):** O jogador controla a nave do Jogador 1 (verde) e tenta sobreviver às duas fases.
2.  **NEW GAME 2P - COOPERATIVE (Coop):** Dois jogadores jogam juntos na mesma tela compartilhando a sobrevivência. No final, a pontuação gravada é a **média aritmética** dos pontos obtidos por ambos.
3.  **NEW GAME 2P - COMPETITIVE (Competitivo):** Dois jogadores se enfrentam indiretamente para ver quem consegue a maior pontuação na fase. No final, a pontuação gravada é a do **jogador vencedor (maior score)**.

### Estrutura das Fases:
*   **Level 1:** O nível inicial do jogo. Possui 7 camadas de background em parallax, inimigos básicos e velocidade balanceada. O tempo limite da fase é de 20 segundos (`TIMEOUT_LEVEL = 20000ms`).
*   **Level 2:** O nível final. Possui 5 camadas de background em parallax, velocidade de movimentação modificada e spawns dinâmicos. A conclusão bem-sucedida do Level 2 leva os jogadores vitoriosos à gravação de sua pontuação.

---

## 🛠️ Padrões de Projeto (Design Patterns) Aplicados

A arquitetura do projeto foi pensada para demonstrar a aplicação de padrões de projeto clássicos da engenharia de software, garantindo baixo acoplamento e alta coesão:

### 1. **Mediator (Padrão de Mediação)**
*   **Implementação:** [EntityMediator](file:///c:/Users/Thiago/PycharmProjects/PythonProject/game/EntityMediator.py)
*   **Objetivo:** Centraliza a detecção de colisões (AABB - *Axis-Aligned Bounding Box*), verificação de vida e limites da janela. Sem o mediator, cada entidade teria que monitorar as coordenadas de todas as outras entidades ativas, gerando uma complexidade de acoplamento de $O(n^2)$. Com o mediator, as entidades apenas gerenciam sua própria locomoção e disparo, enquanto o `EntityMediator` atua como o ponto de decisão e distribuição de pontos.

### 2. **Factory Method / Simple Factory (Fábrica Simples)**
*   **Implementação:** [EntityFactory](file:///c:/Users/Thiago/PycharmProjects/PythonProject/game/EntityFactory.py)
*   **Objetivo:** Encapsula a lógica de criação de entidades de jogo a partir de strings de identificação (como `"Level1Bg"`, `"Player1"`, `"Enemy2"`). A fábrica instancia a classe correta com sua respectiva posição inicial, desacoplando o carregamento de fases e a inicialização de entidades da lógica de execução do loop principal (`Level`).

### 3. **Proxy (ou Data Access Object - DAO)**
*   **Implementação:** [DBProxy](file:///c:/Users/Thiago/PycharmProjects/PythonProject/game/DBProxy.py)
*   **Objetivo:** Intermedeia toda a comunicação entre a interface gráfica do ranking ([Score](file:///c:/Users/Thiago/PycharmProjects/PythonProject/game/Score.py)) e o banco de dados relacional **SQLite** (`DBScore`). Desta forma, a lógica de persistência de dados fica completamente separada da lógica de renderização gráfica.

### 4. **Herança e Poliomorfismo**
*   **Implementação:** [Entity](file:///c:/Users/Thiago/PycharmProjects/PythonProject/game/Entity.py) (Classe Base Abstrata)
*   **Objetivo:** Define o contrato padrão para todas as entidades de jogo através do método abstrato `move()`. As classes derivadas:
    *   [Background](file:///c:/Users/Thiago/PycharmProjects/PythonProject/game/Background.py)
    *   [Player](file:///c:/Users/Thiago/PycharmProjects/PythonProject/game/Player.py)
    *   [Enemy](file:///c:/Users/Thiago/PycharmProjects/PythonProject/game/Enemy.py)
    *   [PlayerShot](file:///c:/Users/Thiago/PycharmProjects/PythonProject/game/PlayerShot.py)
    *   [EnemyShot](file:///c:/Users/Thiago/PycharmProjects/PythonProject/game/EnemyShot.py)
    
    Implementam comportamentos específicos para o movimento (por exemplo, leitura de teclado para o jogador, deslocamento automático para a esquerda com paralaxe para o background e trajetórias programadas para os inimigos).

---

## 🕹️ Controles do Jogo

Os comandos de controle foram mapeados de forma a viabilizar a experiência multiplayer em um mesmo teclado de forma confortável.

| Comando / Ação | Jogador 1 (Nave Verde 🟢) | Jogador 2 (Nave Azul 🔵) |
| :--- | :--- | :--- |
| **Mover para Cima** | Tecla Direcional `CIMA` ⬆️ | Tecla `W` |
| **Mover para Baixo** | Tecla Direcional `BAIXO` ⬇️ | Tecla `S` |
| **Mover para Esquerda** | Tecla Direcional `ESQUERDA` ⬅️ | Tecla `A` |
| **Mover para Direita** | Tecla Direcional `DIREITA` ➡️ | Tecla `D` |
| **Atirar / Disparar** | Tecla `Right Ctrl` (Control Direito) | Tecla `Left Ctrl` (Control Esquerdo) |

> [!NOTE]
> *   Na tela de inserção de recorde (**You Win**), digite exatamente **4 caracteres** usando seu teclado e pressione **ENTER** para salvar.
> *   Na tela de **Ranking (Score)**, pressione **ESC** para retornar ao menu principal.

---

## 📁 Estrutura do Projeto

Abaixo está descrita a organização modular do repositório:

```text
├── assets/                  # Assets visuais (imagens PNG) e sonoros (músicas MP3)
├── game/                    # Diretório contendo a lógica centralizada do jogo
│   ├── __init__.py          # Inicializador de pacote Python
│   ├── Background.py        # Camada de paralaxe (scroll de fundo infinito)
│   ├── Const.py             # Configurações globais (velocidades, vida, cores, danos, teclas)
│   ├── DBProxy.py           # Comunicação e persistência de dados no SQLite
│   ├── Enemy.py             # Lógica e movimentação das naves inimigas
│   ├── EnemyShot.py         # Projétil disparado pelos inimigos
│   ├── Entity.py            # Classe Abstrata base para todas as entidades
│   ├── EntityFactory.py     # Fábrica simples para instanciação de entidades
│   ├── EntityMediator.py    # Gerenciador centralizado de colisões e ciclo de vida
│   ├── Game.py              # Fluxo principal do jogo e alternância de telas
│   ├── Level.py             # Gerenciamento do ciclo da fase (game loop, spawn, timeout)
│   ├── Menu.py              # Renderização e navegação do menu principal
│   ├── Player.py            # Lógica e comandos do jogador humano
│   ├── PlayerShot.py        # Projétil disparado pelo jogador
│   ├── Score.py             # Telas de visualização do ranking e cadastro de novo score
├── DBScore                  # Arquivo de banco de dados SQLite criado automaticamente
├── identifier.sqlite        # Arquivo local com a estrutura de dados (metadados do banco)
├── main.py                  # Ponto de entrada do sistema
├── requirements.txt         # Lista de dependências Python necessárias
└── README.md                # Documentação do projeto (este arquivo)
```

---

## 🚀 Instalação e Execução

### Pré-requisitos
Certifique-se de possuir o Python 3.10 ou superior instalado em sua máquina.

1.  **Clonar o Repositório:**
    ```bash
    git clone https://github.com/Thiagomg94/shooter_game_python.git
    cd shooter_game_python
    ```

2.  **Instalar dependências:**
    Recomenda-se utilizar um ambiente virtual (`venv`):
    ```bash
    # Criar e ativar o ambiente virtual (Windows)
    python -m venv .venv
    .venv\Scripts\activate

    # Instalar as dependências do arquivo requirements.txt
    pip install -r requirements.txt
    ```

3.  **Iniciar o jogo:**
    ```bash
    python main.py
    ```

---

## 🗄️ Detalhes da Persistência de Dados (SQLite)

O jogo utiliza um banco de dados SQLite para manter o Top 10 histórico de pontuações de forma local. A tabela gerada possui a seguinte estrutura de schema:

```sql
CREATE TABLE IF NOT EXISTS game_data(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    score INTEGER NOT NULL,
    date TEXT NOT NULL
);
```

*   **Identificação:** Os jogadores informam seu nome identificador de 4 caracteres.
*   **Formato de Data:** A data é salva em tempo real com formatação local `HH:MM - DD/MM/AAAA`.
