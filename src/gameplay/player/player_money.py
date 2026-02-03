class Money:
    def __init__(self):
        self.money_points = 0

    def gain(self):
        self.money_points += 1

    def buy(self, amount):
        if amount >= self.money_points:
            self.money_points -= amount
            return True
        else:
            return False
