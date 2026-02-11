from gameplay.levels.dialog import DialogStep
from gameplay.levels.npcs import Npc
from gameplay.levels.quest import Quest, QuestState
from gameplay.player.inventory import Inventory

_WELCOME_DIALOG = [
    DialogStep("Hello my friend!", frame="hello", speaker="Mouse"),
    DialogStep(
        "I need your help. I need some food for my poor sick baby. "
        + "There should be some strawberries growing somewhere nearby, but I can't leave my house. ",
        frame="thinking",
        speaker="Mouse",
    ),
    DialogStep("Can you bring me 14 strawberries?", frame="thinking", speaker="Mouse"),
    DialogStep("Ok", frame="happy", speaker="Sara"),
]


def search_in_progress_dialog(amount: int):
    return [
        DialogStep(
            "I can't believe that you agreed to help me! I need {amount} more.".format(amount=amount),
            frame="happy",
            speaker="Mouse",
        ),
    ]


_SEARCH_DONE_DIALOG = [
    DialogStep("Thank you! We will never forget your help!", frame="happy", speaker="Mouse"),
]

_COLLECTED_ALL_STRAWBERRIES_DIALOG = [
    DialogStep(
        "How wonderful! Now I have all strawberries I needed!",
        frame="happy",
        speaker="Mouse",
    ),
]


def received_items_dialog(received_count: int, remaining_count: int) -> list[DialogStep]:
    strawberry_word = "strawberies" if received_count > 1 else "strawberry"
    return [
        DialogStep(
            f"Thanks you for these {received_count} {strawberry_word}! I need {remaining_count} more!",
            frame="happy",
            speaker="Mouse",
        ),
    ]


class StrawberryQuest(Quest):
    def __init__(self, mouse: Npc, inventory: Inventory):
        super().__init__()
        self._mouse = mouse
        self._inventory = inventory

        self._welcome_dialog_completed = False
        self._remaining_strawberries = 14
        self._strawberry_id = "strawberry"

    def start(self):
        super().start()
        self._mouse.set_quest(self)

    def get_current_dialog(self, npc_id: str) -> list[DialogStep] | None:
        if npc_id != self._mouse.npc_id:
            return None

        if not self._welcome_dialog_completed:
            self._welcome_dialog_completed = True
            return _WELCOME_DIALOG + search_in_progress_dialog(self._remaining_strawberries)
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
