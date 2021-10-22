from abc import ABC, abstractmethod
import os

 
class Deck(ABC):
    @abstractmethod
    def draw(self, kwargs):
        pass

class Juggernaut(Deck):
    def __init__(self):
        self.game = "juggernaut"
        self.deck_folder = "decks/juggernaut/deck"
        self.deck_index = -1 

    def draw(self):
        self.deck_index += 1
        return [os.path.join(self.deck_folder, os.listdir(self.deck_folder)[self.deck_index])]



implemented_decks =  {"juggernaut": Juggernaut}

def _implemented_games():
    return list(implemented_decks.keys())

def _get_deck(game):
    return implemented_decks.get(game)

