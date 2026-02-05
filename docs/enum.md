# Notatki: Enum w Pythonie

## Kontekst
Chciałam stworzyć system czcionek z różnymi typami (DIALOG, INVENTORY, RESOURCES) zamiast "magicznych" liczb rozsypanych po kodzie.

---

## Co to jest Enum?

**Enum** (enumeration = wyliczenie) to sposób na definiowanie zestawu **nazwanych stałych**.

```python
from enum import Enum

class FontType(Enum):
    DIALOG = 8
    INVENTORY = 9
    RESOURCES = 14
    OTHER = 10
```

Zamiast pisać `8` czy `"dialog"` w kodzie, piszesz `FontType.DIALOG` — czytelniej i IDE podpowiada!

---

## Podstawowe użycie

```python
# Przypisanie
my_font_type = FontType.SMALL

# Porównanie
if my_font_type == FontType.SMALL:
    print("To jest font do dialogów!")

# Dostęp do wartości liczbowej
print(FontType.SMALL.value)  # wypisze: 8

# Dostęp do nazwy
print(FontType.SMALL.name)  # wypisze: DIALOG
```

---

## ⚠️ WAŻNE: Enum jest IMMUTABLE (niezmienny)!

**NIE DZIAŁA:**

```python
font_type = FontType.SMALL
font_type.value += 2  # ❌ AttributeError! Nie można zmienić .value
```

**ROZWIĄZANIE:** Wyciągnij wartość do zmiennej i ją modyfikuj:

```python
font_type = FontType.SMALL
size = font_type.value + enlarge  # ✅ Działa! Tworzysz nową zmienną
```

---

## Przykład z systemu czcionek

### Problem: Chciałam powiększać rozmiar czcionki w zależności od rozdzielczości

```python
class SetFont:
    def get_font(self, font_type: FontType):
        enlarge = self.calculate_enlarge()
        
        # ❌ ŹLE - nie można modyfikować enum!
        # font_type.value += enlarge
        
        # ✅ DOBRZE - wyciągamy wartość i tworzymy nową zmienną
        size = font_type.value + enlarge
        
        return pygame.font.SysFont("comicsansms", size)
```

---

## Metoda klasy vs metoda instancji

### Problem: Wywołanie metody na klasie zamiast na instancji

```python
# ❌ ŹLE - wywołujesz na KLASIE (brak self!)
font = SetFont.get_font(FontType.LARGE)

# ✅ DOBRZE - tworzysz INSTANCJĘ i wywołujesz metodę
font_manager = SetFont()
font = font_manager.get_font(FontType.LARGE)

# ✅ Lub w jednej linii:
font = SetFont().get_font(FontType.LARGE)
```

**Dlaczego?** Metoda `get_font(self, font_type)` potrzebuje `self` — czyli instancji obiektu. 
Gdy wywołujesz ją na klasie bez tworzenia obiektu, Python nie ma skąd wziąć `self`.

---

## Podsumowanie

| Składnia | Co robi | Przykład |
|----------|---------|----------|
| `FontType.DIALOG` | Dostęp do elementu enum | — |
| `FontType.DIALOG.value` | Dostęp do wartości (int) | `8` |
| `FontType.DIALOG.name` | Dostęp do nazwy (str) | `"DIALOG"` |

### Kluczowe zasady:
1. **Enum jest immutable** — nie możesz zmienić `.value`, musisz wyciągnąć do nowej zmiennej
2. **Metody instancji wymagają instancji** — `SetFont().get_font(...)` nie `SetFont.get_font(...)`
