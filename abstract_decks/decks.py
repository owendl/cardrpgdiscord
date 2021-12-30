from abc import ABC, abstractmethod
import os
import discord
import glob
import random
import time
 
class Deck(ABC):
    @abstractmethod
    def draw(self, ctx, cmd_args):
        pass
    
    @abstractmethod
    def instructions(self, ctx, cmd_args):
        pass

class Juggernaut(Deck):
    def __init__(self):
        self.game = "juggernaut"
        self.deck_folder = "decks/juggernaut/deck"
        self.deck_index = 0

    async def instructions(self, ctx, cmd_args):
        instruction_text = f'''
        Need to add        
        '''
        return

    async def draw(self, ctx, cmd_args):
        self.deck_index += 1
        await ctx.send("doing a draw")
        time.sleep(15)
        matches = glob.glob(f"{self.deck_folder}/*_{self.deck_index:02}.*")
        m = random.sample(matches,1)[0]
        return [m]



implemented_decks =  {"juggernaut": Juggernaut}

def _implemented_games():
    return list(implemented_decks.keys())

def _get_deck(game):
    return implemented_decks.get(game)

