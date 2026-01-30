# Notatki: *args, **kwargs i dziedziczenie

## Kontekst
Chciałam stworzyć klasę `CollectibleSpec` dziedziczącą po `SpriteObjectSpec`, dodając tylko jedno pole `kind`.

---

## Opcje projektowe dla Collectibles

### Opcja A: Jeden Spec z typem
```python
class CollectibleSpec:
    def __init__(self, x, y, sprite_path, kind: str):  # "heart", "coin"
        ...
```
✅ Proste, szybkie do zrobienia  
⚠️ Wszystkie collectibles mają te same pola

### Opcja B: Osobne klasy Spec dla każdego typu
```python
class HeartSpec(SpriteObjectSpec):
    pass  # dziedziczy x, y, sprite_path

class CoinSpec(SpriteObjectSpec):
    def __init__(self, x, y, sprite_path, value: int):  # dodatkowe pole!
        ...
```
✅ Każdy typ może mieć inne pola  
✅ Typ sprawdzany automatycznie (`isinstance(spec, HeartSpec)`)  
⚠️ Więcej klas

### Opcja C: Bazowy Spec + osobne klasy obiektów

```python
# Spec - tylko dane
CollectibleSpec(x=100, y=200, sprite="heart.png", kind="heart")


# Obiekty gry - zachowanie
class Heart:
    def on_collect(self, player):
        player.health.gain()


class Coin:
    def on_collect(self, player):
        player.coins += 1
```
✅ Spec jest prosty, zachowanie jest w osobnych klasach  
✅ Łatwo testować logikę osobno

---

## Dziedziczenie z dodatkowym polem

Jak dziedziczyć i dodać tylko jedno pole (`kind`)?

```python
# Klasa bazowa
class SpriteObjectSpec:
    def __init__(self, x: int, y: int, height_units: int, sprite_path: str):
        self.x = ss.game_units_to_px(x)
        self.y = ss.game_units_to_px(y)
        self.height = ss.game_units_to_px(height_units)
        self.sprite_path = sprite_path

# Klasa dziedzicząca - dodaje TYLKO nowe pole
class CollectibleSpec(SpriteObjectSpec):
    def __init__(self, x: int, y: int, height_units: int, sprite_path: str, kind: str):
        super().__init__(x, y, height_units, sprite_path)  # <- wywołuje __init__ rodzica!
        self.kind = kind  # <- tylko nowe pole
```

---

## Problem z *args i **kwargs

### Wersja z `*args` (NIE DZIAŁA z nazwanymi argumentami!)
```python
class CollectibleSpec(SpriteObjectSpec):
    def __init__(self, *args, kind: str):
        super().__init__(*args)
        self.kind = kind
```

**Problem:** `*args` łapie tylko argumenty **pozycyjne** (bez nazwy).

Wywołanie:
```python
CollectibleSpec(x=1350, y=190, height_units=50, sprite_path="...", kind="heart")
```
Daje błąd: `TypeError: got an unexpected keyword argument 'x'`

Bo `x=1350` to argument **nazwany**, a `*args` go nie łapie!

---

### Rozwiązanie: Dodaj `**kwargs`
```python
class CollectibleSpec(SpriteObjectSpec):
    def __init__(self, *args, kind: str, **kwargs):
        super().__init__(*args, **kwargs)  # <- przekaż oba!
        self.kind = kind
```

Teraz działa:
```python
CollectibleSpec(x=1350, y=190, height_units=50, sprite_path="...", kind="heart")
```

---

## Podsumowanie

| Składnia | Co łapie | Przykład |
|----------|----------|----------|
| `*args` | Argumenty **pozycyjne** (bez nazwy) | `foo(1, 2, 3)` |
| `**kwargs` | Argumenty **nazwane** | `foo(x=1, y=2)` |

Jeśli chcesz przekazywać argumenty **przez nazwę** do klasy bazowej, potrzebujesz `**kwargs`!
