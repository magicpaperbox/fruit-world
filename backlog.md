Wydzielić osobny komponent(y?) do rysowania stanu gracza (hp, mana)


Przenieść logikę przemieszczania się między mapami/kolizji ze ścianą do levelu (player jako parametr)


zmienne lokalne nie powinny się zaczynać od _

--------------

if obj.kind == "heart":
  heart_logic()
elif obj.kind == "mana":
  mana_logic()

obj.try_collect(player)

class Collectible:
  def try_collect(self, player: Player) -> bool:
    if not player.position.collides(self.rect):
        return False
    return self._try_collect(player)

  @abc.abstractmethod
  def _try_collect(self, player: Player) -> bool:
     pass

class HealthCollectible(Collectible):
  def _try_collect(self, player: Player) -> bool:
    player.health.gain()
    return True

