
class BestBet:

    def __init__(self, game, date, book_home, odd_home, book_draw, odd_draw, book_away, odd_away):
        self.game = game
        self.date = date
        self.book_home = book_home
        self.odd_home = odd_home
        self.book_draw = book_draw
        self.odd_draw = odd_draw
        self.book_away = book_away
        self.odd_away = odd_away

        BestBet.margin = (1/float(self.odd_home)) + (1/float(self.odd_draw)) + (1/float(self.odd_away))

    def get_best_bet(self):
        return self.game, self.date, self.book_home, self.odd_home, self.book_draw, self.odd_draw, self.book_away, self.odd_away, BestBet.margin


class SingleGame:

    def __init__(self, game, date, book, home, draw, away):
        self.game = game
        self.date = date
        self.book = book
        self.home = home
        self.draw = draw
        self.away = away

    def get_single_game(self):
        return self.game, self.date, self.book, self.home, self.draw, self.away



