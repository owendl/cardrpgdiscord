from abc import ABC, abstractmethod
import os

 
class Deck(ABC):
    @abstractmethod
    def draw(self, kwargs):
        pass

class Juggernaut(Deck):
    def __init__(self):
        self.game = "juggernaut"
        self.deck_folder = "decks/juggernaut"
        self.deck_index = 0 

    def draw(self):
        print(os.listdir(self.deck_folder)[0])



implemented_decks =  {"juggernaut": Juggernaut}

def _implemented_games():
    return list(implemented_decks.keys())

def _get_deck(game):
    return implemented_decks.get(game)

