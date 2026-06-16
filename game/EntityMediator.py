"""
Módulo que implementa o Mediator de colisões e gerenciamento de vida das entidades.
"""

from game.Const import WIN_WIDTH
from game.Enemy import Enemy
from game.EnemyShot import EnemyShot
from game.Entity import Entity
from game.Player import Player
from game.PlayerShot import PlayerShot
from game.HealthItem import HealthItem, HEALTH_RESTORE


class EntityMediator:
    """Mediator que gerencia interações entre entidades: colisões, limites de tela e remoção.

    Centraliza toda a lógica de colisão, evitando que as entidades precisem conhecer
    umas às outras diretamente (baixo acoplamento). Implementa o padrão Mediator.

    Todas as colisões verificadas:
        • Enemy vs PlayerShot → inimigo toma dano do tiro; tiro toma dano do inimigo
        • Player vs EnemyShot → jogador toma dano do tiro; tiro toma dano do jogador
        • Player vs Enemy (corpo a corpo) → NÃO verificado na implementação atual
    """

    @staticmethod
    def __verify_collision_window(ent: Entity):
        """Elimina entidades que saíram dos limites da tela.

            Regras por tipo:
                • Enemy: destruído ao sair pela esquerda (sem dar pontos ao jogador).
                • PlayerShot: destruído ao sair pela direita (não atingiu nenhum inimigo).
                • EnemyShot: destruído ao sair pela esquerda (passou pelos jogadores).

            Args:
                ent: Entidade a verificar.
        """
        if isinstance(ent, Enemy):
            if ent.rect.right <= 0:
                ent.health = 0 # saiu da tela sem ser abatido

        if isinstance(ent, PlayerShot):
            if ent.rect.left >= WIN_WIDTH:
                ent.health = 0 # saiu da tela sem atingir nenhum inimigo

        if isinstance(ent, EnemyShot):
            if ent.rect.right <= 0:
                ent.health = 0 # saiu da tela sem atingir nenhum jogador

        if isinstance(ent, HealthItem):
            if ent.rect.right <= 0:
                ent.health = 0 # saiu sem ser coletado

    @staticmethod
    def __verify_collision_entity(ent_one: Entity, ent_two: Entity):
        """Verifica colisão entre duas entidades e aplica o dano mútuo se válido.

            Somente pares específicos interagem entre si para evitar colisões indevidas
            (ex: jogador não toma dano do próprio tiro).

            A detecção usa AABB (Axis-Aligned Bounding Box): compara as bordas dos
            retângulos de ambas as entidades para determinar sobreposição.

            Args:
                ent_one: Primeira entidade.
                ent_two: Segunda entidade.
        """

        valid_interaction = False

        # Define os pares de entidades que podem colidir entre si
        if isinstance(ent_one, Enemy) and isinstance(ent_two, PlayerShot):
            valid_interaction = True
        elif isinstance(ent_one, PlayerShot) and isinstance(ent_two, Enemy):
            valid_interaction = True
        elif isinstance(ent_one, Player) and isinstance(ent_two, EnemyShot):
            valid_interaction = True
        elif isinstance(ent_one, EnemyShot) and isinstance(ent_two, Player):
            valid_interaction = True
        elif isinstance(ent_one, Player) and isinstance(ent_two, HealthItem):
            valid_interaction = True
        elif isinstance(ent_one, HealthItem) and isinstance(ent_two, Player):
            valid_interaction = True

        if valid_interaction:
            # Detecção AABB: os retângulos sobrepõem-se quando todas as condições
            # abaixo forem verdadeiras simultaneamente.
            if (ent_one.rect.right >= ent_two.rect.left and
                ent_one.rect.left <= ent_two.rect.right and
                ent_one.rect.bottom >= ent_two.rect.top and
                ent_one.rect.top <= ent_two.rect.bottom):

                # tratamento: HealthItem cura em vez de causar dano
                if isinstance(ent_one, HealthItem):
                    ent_two.health += HEALTH_RESTORE
                    ent_one.health = 0
                elif isinstance(ent_two, HealthItem):
                    ent_one.health += HEALTH_RESTORE
                    ent_two.health = 0
                else:
                    # Aplica dano mútuo: cada entidade recebe o dano da outra
                    ent_one.health -= ent_two.damage
                    ent_two.health -= ent_one.damage

                    # Registra quem causou o dano (usado para atribuir pontuação)
                    ent_one.last_dmg = ent_two.name
                    ent_two.last_dmg = ent_one.name

    @staticmethod
    def __give_score(enemy: Enemy, entity_list: list[Entity]):
        """Atribui a pontuação do inimigo eliminado ao jogador que deu o tiro final.

        Verifica o atributo `last_dmg` do inimigo para identificar qual projétil
        (e, portanto, qual jogador) causou o dano letal.

            Args:
                enemy: Inimigo que acabou de ser eliminado (health <= 0).
                entity_list: Lista completa de entidades para localizar o jogador.
        """
        if enemy.last_dmg == "Player1Shot":
            for ent in entity_list:
                if ent.name == "Player1":
                    ent.score += enemy.score
        elif enemy.last_dmg == "Player2Shot":
            for ent in entity_list:
                if ent.name == "Player2":
                    ent.score += enemy.score

    @staticmethod
    def verify_collision(entity_list: list[Entity]):
        """Verifica colisões de todas as entidades entre si e com os limites da tela.

        Usa índices para evitar verificar o mesmo par duas vezes (i < j),
        reduzindo o número de comparações de O(n²) para O(n²/2).

            Args:
                entity_list: Lista de todas as entidades ativas no nível.
        """
        for i in range(len(entity_list)):
            entity_one = entity_list[i]
            EntityMediator.__verify_collision_window(entity_one)
            for j in range(i + 1, len(entity_list)):
                entity_two = entity_list[j]
                EntityMediator.__verify_collision_entity(entity_one, entity_two)

    @staticmethod
    def verify_health(entity_list: list[Entity]):
        """Remove entidades com vida esgotada e distribui pontuação quando necessário.

            Args:
                entity_list: Lista de entidades ativas (modificada in-place).
        """
        # 1ª passagem: distribui pontos de todos os inimigos eliminados neste frame
        for ent in entity_list:
            if ent.health <= 0 and isinstance(ent, Enemy):
                EntityMediator.__give_score(ent, entity_list)

        # 2ª passagem: remove todas as entidades sem vida de uma só vez.
        # Usa variável `e` para não confundir com `ent` do loop acima.
        entity_list[:] = [e for e in entity_list if e.health > 0]