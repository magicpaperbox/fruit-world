import enum

from gameplay.levels.dialog import DialogStep


class QuestState(enum.Enum):
    NOT_STARTED = 1
    IN_PROGRESS = 2
    COMPLETED = 3


class Quest:
    def __init__(self):
        self.quest_state = QuestState.NOT_STARTED

    def start(self):
        self.quest_state = QuestState.IN_PROGRESS

    def get_current_dialog(self, npc_id: str) -> list[DialogStep] | None:
        pass
