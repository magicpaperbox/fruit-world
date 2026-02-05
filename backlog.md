fonts:
😄move fonts from sprites/ to toplevel fonts/
😭można się zastanowić nad cache jak w sprite factory
😄resolution size vs enlarge vs get font size🤔
😄podawać wielkość czcionki w game units
self.font -> self.fonts/font_factory
self.font_size - do wywalenia, przejść na GameUnit

refactor debug draw rects, etc into a class with font as state


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

inventory draw picked item - poprawic sposob rysowania zebyranych rzeczy i ich licczb