import enum

from gameplay.player.inventory import Inventory

from gameplay.levels.npcs import Npc
from gameplay.levels.quest import Quest, QuestState


_WELCOME_DIALOG = [
    {"text": "Mouse: Hello my friend!", "frame": "hello", "ms": 800, "mode": "next", "quest": 0, "react": False},
    {
        "text": "Mouse: I need your help. I'm starving, but I can't leave my house.",
        "frame": "thinking",
        "ms": 800,
        "mode": "next",
        "quest": 1,
        "react": False,
    },
    {
        "text": "Mouse:  Please, bring me 3 strawberries.",
        "frame": "thinking",
        "ms": 800,
        "mode": "next",
        "quest": 1,
        "react": True,
    },
    {
        "text": "Sara: Oki",
        "frame": "happy",
        "ms": 800,
        "mode": "end",
        "quest": 1,
        "react": True,
    },
]

def search_in_progress_dialog(amount: int):
    return [
        {
            "text": "Mouse: I can't believe that you agreed to help me! I need {amount} more of this.".format(amount=amount),
            "frame": "happy",
            "ms": 800,
            "mode": "end",
            "quest": 1,
            "react": True,
        },
    ]

_SEARCH_DONE_DIALOG = [
    {
        "text": "Mouse: Thank you I never forget your help",
        "frame": "happy",
        "ms": 800,
        "mode": "end",
        "quest": 1,
        "react": True,
    },
]

_COLLECTED_ALL_STRAWBERRIES_DIALOG = [
    {
        "text": "Mouse: Oh great! Now I have all strawberries I needed",
        "frame": "happy",
        "ms": 800,
        "mode": "end",
        "quest": 1,
        "react": True,
    },
]


def received_items_dialog(received_count: int, remaining_count: int):
    strawberry_word = "strawberies" if received_count > 1 else "strawberry"
    return [
        {
            "text": f"Mouse: Thanks you for these {received_count} {strawberry_word}! I need {remaining_count} more!",
            "frame": "happy",
            "ms": 800,
            "mode": "end",
            "quest": 1,
            "react": True,
        },
    ]


class StrawberryQuest(Quest):
    def __init__(self, mouse: Npc, inventory: Inventory):
        super().__init__()
        self._mouse = mouse
        self._inventory = inventory

        self._welcome_dialog_completed = False
        self._remaining_strawberries = 3
        self._strawberry_id = "strawberry"

    def start(self):
        super().start()
        self._mouse.set_quest(self)

    def get_current_dialog(self, npc_id: str) -> list[dict] | None:
        if npc_id != self._mouse.npc_id:
            return None

        if not self._welcome_dialog_completed:
            self._welcome_dialog_completed = True
            return _WELCOME_DIALOG
        elif self._remaining_strawberries > 0:
            player_count = self._inventory.count(self._strawberry_id)
            if player_count >= self._remaining_strawberries:
                self._inventory.remove(self._strawberry_id, self._remaining_strawberries)
                self._remaining_strawberries = 0
                self.quest_state = QuestState.COMPLETED
                return _COLLECTED_ALL_STRAWBERRIES_DIALOG
            elif player_count == 0:
                return search_in_progress_dialog(self._remaining_strawberries)
            else:
                self._inventory.remove(self._strawberry_id, player_count)
                self._remaining_strawberries -= player_count
                return received_items_dialog(player_count, self._remaining_strawberries)
        else:
            return _SEARCH_DONE_DIALOG