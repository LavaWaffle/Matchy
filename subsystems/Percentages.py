ROUNDING_PRECISION = 4

class Percentages:
    def __init__(self, wins, losses, ties):
        total = wins + losses + ties
        self.win_percentage = round(wins / total, ROUNDING_PRECISION) * 100
        self.loss_percentage = round(losses / total, ROUNDING_PRECISION) * 100
        self.tie_percentage = round(ties / total, ROUNDING_PRECISION) * 100