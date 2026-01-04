import enum

from inventory import Inventory

from npcs import Npc
from quest import Quest


# dialogs = ([
#     {"text": "Thank you!", "frame": "happy", "ms": 800, "mode": "stay", "quest": 1, "react": False},
#     {"text": f"I can\'t believe that you agreed to help me! I need {amount} more of this.", "frame": "happy",
#      "ms": 800, "mode": "stay", "quest": 1, "react": True},
# ])  # zrobic moze nowa klase na questy


class QuestState(enum.Enum):
    NOT_STARTED = 1
    IN_PROGRESS = 2
    COMPLETED = 3

class StrawberryQuest(Quest):
    def __init__(self, mouse: Npc, inventory: Inventory):
        super().__init__()
        self._mouse = mouse
        self._inventory = inventory
        self.quest_state = QuestState.NOT_STARTED
        self._current_dialog = None
        self._current_dialog_completed = False

    # trzeba następny krok questa triggerować po dialogu  

    def start(self):
        self._current_dialog = [
            {"text": "Hello my friend!", "frame": "hello", "ms": 800, "mode": "next", "quest": 0, "react": False},
            {"text": "I need your help. I'm starving, but I can't leave my house.", "frame": "thinking", "ms": 800,
             "mode": "next", "quest": 1, "react": False},
            {"text": "Please, bring me 3 strawberries.", "frame": "happy", "ms": 800, "mode": "stay", "quest": 1,
             "react": True},
        ]

    def get_current_dialog(self, npc_id: str) -> list[dict] | None:
        if npc_id == self._mouse.npc_id:
            self._current_dialog_completed = True
            return self._current_dialog
        else:
            return None
