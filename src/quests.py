import pygame
import enum

class QuestState(enum.Enum):
    NOT_STARTED = 1
    IN_PROGRESS = 2
    COMPLETED = 3

class Quest:
    def __init__(self, npc_id: int, quest_id: int, steps: list[dict], reward: list[Reward], required_npcs: list[int]):
        self.quest_id = quest_id
        self.required_npcs = required_npcs
        self.npc_id = npc_id
        self.steps = steps
        self.step_index = 0
        self.reward = reward
        self.quest_state = QuestState.NOT_STARTED


    def start():
        pass
        # ustawiamy npcom ich pierwsze dialogi lub jego brak

    def set_dialog(self, npc_id, quest_id):
        for step in self.steps:
            if step["npc_id"] == npc_id and step["quest_id"] == quest_id:
                self.dialog = step["dialog"]
                return


        # quest 1 npc 1
        dialogs = ([
            {"text": "Hello my friend!", "frame": "hello", "ms": 800, "mode": "next", "quest": 0, "react": False},
            {"text": "I need your help. I'm starving, but I can't leave my house.", "frame": "thinking", "ms": 800,
             "mode": "next", "quest": 1, "react": False},
            {"text": "Please, bring me 3 strawberries.", "frame": "happy", "ms": 800, "mode": "stay", "quest": 1,
             "react": True},
            {"text": "Thank you!", "frame": "happy", "ms": 800, "mode": "stay", "quest": 1, "react": False},
            {"text": f"I can\'t believe that you agreed to help me! I need {amount} more of this.", "frame": "happy",
             "ms": 800, "mode": "stay", "quest": 1, "react": True},
        ])  # zrobic moze nowa klase na questy

    # po dialogu trzeba powiadomić quest, że został zaktualizowany (zmiana statusu na started oraz trzeba podmienić dialogi)
    class Reward: