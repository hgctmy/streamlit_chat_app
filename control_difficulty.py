class Question:
    def __init__(self, text, score):
        self.text = text
        self.score = score


class User:
    def __init__(self):
        self.scores = []

    def add_scores(self, score):
        self.scores.append(score)

    def calc_average(self):
        return sum(self.scores) / len(self.scores)
