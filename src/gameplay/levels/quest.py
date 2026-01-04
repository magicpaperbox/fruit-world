import enum


class QuestState(enum.Enum):
    NOT_STARTED = 1
    IN_PROGRESS = 2
    COMPLETED = 3


class Quest:
    def __init__(self):
        self.quest_state = QuestState.NOT_STARTED

    def start(self):
        pass

    def get_current_dialog(self, npc_id: str) -> list[dict] | None:
        pass
