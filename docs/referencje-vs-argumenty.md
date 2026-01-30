# Notatki: Referencje vs Argumenty

## Problem
Gdy klasa potrzebuje listy, która może się zmieniać (np. lista obiektów na aktualnej mapie), mamy dwa podejścia.

---

## Wersja A: Trzyma referencję (w `__init__`)

```python
class CollectResources:
    def __init__(self, collectibles):
        self.collectibles = collectibles  # <- zapamiętuje listę na stałe
    
    def check_collisions(self, player_rect, health):
        for c in self.collectibles:  # <- używa tej zapamiętanej listy
            ...
```

**Jak to działa:**
- `CollectResources` **pamięta** listę przekazaną w konstruktorze
- Używa tej samej listy przy każdym wywołaniu `check_collisions()`

**Problem:**
- Jeśli mapa się zmieni, musisz też zaktualizować `self.collectibles`
- Ryzyko że lista jest nieaktualna

---

## Wersja B: Dostaje jako argument (za każdym razem)

```python
class CollectResources:
    def __init__(self):
        pass  # <- nic nie zapamiętuje!
    
    def check_collisions(self, player_rect, collectibles, health):
        for c in collectibles:  # <- używa listy przekazanej w tym momencie
            ...
```

**Jak to działa:**
- `CollectResources` **nie pamięta** żadnej listy
- Za każdym wywołaniem `check_collisions()` dostaje aktualną listę

**Zalety:**
- Zawsze masz aktualną listę z aktualnej mapy
- Nie musisz się martwić o synchronizację

---

## Analogia

| Wersja | Analogia |
|--------|----------|
| A (referencja) | Masz kartkę z numerem telefonu. Jak przyjaciel zmieni numer, Twoja kartka jest nieaktualna. |
| B (argument) | Za każdym razem pytasz "jaki jest aktualny numer?" - zawsze masz najnowszy. |

---

## Kiedy co używać?

| Sytuacja | Lepsze podejście |
|----------|------------------|
| Lista **nigdy** się nie zmienia | Wersja A (referencja) |
| Lista **może** się zmienić (np. zmiana mapy) | Wersja B (argument) |
| Chcesz prostszy kod bez synchronizacji | Wersja B (argument) |

---

## Przykład w kontekście gry

```python
# W main.py - wersja B (bezpieczniejsza):
self.collect_resources.check_collisions(
    self.sara.player_rect,
    self.level.current_map.collectible_objects,  # <- zawsze aktualna lista!
    self.health
)
```

Nie musisz aktualizować `CollectResources` gdy zmienia się mapa - po prostu przekazujesz aktualną listę.
