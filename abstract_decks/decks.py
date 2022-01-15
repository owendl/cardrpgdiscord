from abc import ABC, abstractmethod
import os
import discord
import glob
import random
import time
from collections import OrderedDict
 
 
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
        self.introduction = f'''
It is July third, 1950. The Korean War is eight days old. National Security Council Report 68 is sitting on Harry Truman's desk, a grim outline of the Cold War that is to enfold the world for the next 40 years. Alan Turing's paper “Computing Ma- chinery and Intelligence” is circulating for review. “Cinderella” is a box office sensation. And you have invented a com- puter that can see the future.

Employing cutting-edge Ward-Takahashi identity derivations outside their quantum-theoretical framework, JUGGERNAUT processes enormous data sets, ostensibly in the service of code-breaking once the technology is proven and refined. The unstable geniuses behind the math have reached some curious conclusions that only experimental evidence can confirm. By the numbers, JUGGERNAUT - given enough resources - should be able to crack ciphers before they are even invented.

Each JUGGERNAUT tabulating bank is three meters long, two tall and one wide. It looks for all the world like a two-and- a-half ton bookcase. The high security tabulating room is a vast hall full of clacking machines, smelling of grease, cut paper and electricity.

JUGGERNAUT is designed to seek patterns in data encoded on Hollerith punchcards. In its current experimental configura- tion, JUGGERNAUT consists of 256 tabulat- ing banks that can process one million punchcards a day. The sorting drum within each bank rotates at 1800 revolutions per minute, using thermionic valves to detect and tabulate data stops. New cards are generated and their data is ported to summary machines, creating a cascade of further refined information. The output of a run is a single human-readable Hol- lerith card.

On that card is a simple statement about events that will happen in the future.

And JUGGERNAUT is never wrong.
        '''
        self.instruction_text = f'''
The game will last as long as it takes to reach the final summary output card. The pace of card reveals is in the player's hands.

JUGGERNAUT's summary output jobs are stacked in a sequence that is slowly revealed in play. The next summary job can be run at any time.

JUGGERNAUT is never wrong. Everything it says will happen must happen. No exceptions. It is up to you to make JUGGERNAUT's summary outputs become reality, no matter how difficult or far-fetched they may seem.

You view the available characters with "!Q characters" command. You can choose your character with "!Q choose <name>". After you choose your character, the channel you chose on will receive some info of how you feel about the others in the JUGGERNAUT room.

You can run a summary output job by typing !draw. After some delay (machinery running) you will receive a card in the channel where you sent the draw command. If the card says “you”, it refers specifically to the person drawing the card. Share its content if you wish.

The game ends when the last card in the stack has finally been revealed.       
'''

        self.characters_public = {
            "Takahashi" : '''You are Nisei - a second generation Japanese-American born in Hayward, California. Math is what you know, it is the language you speak, the air you breathe. You spent most of the Second World War in an internment camp in Idaho, working on your doc- toral dissertation in mathematics, focusing on the topology of complex manifolds. Your math is what makes this machine do the beautiful and strange things it does. Topology and the shaky field of quantum mechanics, planes of undulating data, time lurching and stuttering and perhaps breaking, you see it all in the clacking whirr of punchcards. It was your vision that provided the spark for this mad project.'''
            ,"Dorflinger" : "You have always lived at the intersection of the applied and the theoretical. While you appreciate the lonely beauty of pure mathematics, you also gain a deep satisfaction from see- ing that math harnessed to some elegant, useful purpose. Dur- ing the war that purpose was rocketry, and you helped build amazing machines that - well, you don't dwell on what they were actually used for. You aimed at the stars, but sometimes you hit London. That looks bad on a resume, but you follow the interesting work and your current hosts have been very forgiving. This computer is, by far, the most interesting thing you've ever worked on. Takahashi sweated out the math, Chandrakar built the machine - but you made it speak. What will it say?"
            ,"Chandrakar" : "Your background is one of relative privilege - your father is a well-placed politician who opposed the Indian National Congress and made sure you attended all the right schools in Britain where you became, to his dismay, a mechanical engi- neer. You spent the war building JUGGERNAUT's ancestors in Letchworth, Hertfordshire, for the British Tabulating Ma- chine Company. Miles of wiring, vacuum tubes, row after row of crisply-machined apparatus with tight tolerances. All for cracking Nazi codes. Now there are new enemies and more money and people who don't understand real power - or real oppor- tunity. If you can see the future, you can make the future."
            ,"Maj. Van Der Meer" : "You are a Major in the Army and carry yourself like the sol- dier you are. You are here because this machine has big na- tional security implications, and most of the work is being done by people you were busy killing just five years ago. It's a funny old world, and seeing a German scientist basi- cally moved from one team to the other with no ass-kicking in between makes you a little cynical. It makes you wonder how much the sacrifices you made were appreciated, and what it was all for. So here you are, babysitting a crackpot project that could change the world if, by some miracle, it actually does what the eggheads promise."
            ,"Simms" : "Simms isn't your real name. You represent a quiet agency with an interest in learning the secrets that the many enemies of your nation would prefer to keep hidden. You've seen a lot of strange stuff - during the War you worked for serious people cleaning up various unusual messes all over Europe - and hon- estly nothing surprises you any more. Thing is, a machine that can actually tell the future would raise a few jaded eyebrows, perhaps including yours. It is probably bullshit. But if it isn't, well, it represents a real Pandora's box, doesn't it? Maybe ripping the lid off the hinges isn't such a hot idea."
            ,"Brasseau" : "Word got out, after a fashion. Everything is still top secret but your boss, who is at the apex of the political food chain - felt that someone should be on hand to represent the inter- ests of the political elite. Protect the public funds. Keep an eye out for snake oil. A machine that can tell the future is the most ridiculous thing you have ever heard, but then again it is an age of wonders, isn't it? And if your boss thought it was important enough to keep tabs on, and the military, and whoever Simms works for - well, who are you to doubt it? If it actually works it'll be the biggest thing since nickel slot machines."
        }

        self.characters_secret = {
            "Takahashi" : '''Chandrakar: Hard working, patient, kind, talented. Probably knows a thing or two about racism.
Dörflinger: Ex-Nazi rocket scientist. Dredges up mixed feel-
ings.
Van Der Meer: Exactly the sort of person who put your family
in a concentration camp.
Simms: Seems nice, if slightly out of touch with what's go- ing on here.
Brasseau: A distraction.
  '''
            ,"Dorflinger" : '''Takahashi: Brilliant, and a foreigner in their own racist country of birth.
Chandrakar: Talented engineer, although without any theory as a guide for busy hands.
Van Der Meer: Military Scheißkerl of the sort this country seems full of. Horrid.
Simms: Probably eager to pack up JUGGERNAUT and ship it to some undisclosed location in Nevada.
Brasseau: You don't quite understand why this person is here
at all.'''
            ,"Chandrakar" : '''Takahashi: Someone you feel like you understand, although the work is completely beyond you.
Dörflinger: An ex-Nazi, but a repentant one. All is forgiven. The work is everything.
Van Der Meer: A little too cocksure, a little too certain, a
little too stupid.
Simms: Dangerous. Represents the intelligence apparatus and that is always trouble.
Brasseau: Infuriatingly powerful, as one well-placed word could dry up your funding.'''
            ,"Maj. Van Der Meer" : '''Takahashi: Spent the war in an internment camp in Idaho. Should probably not have been released.
Chandrakar: Seems smart. Built this thing, anyway. Someone you can work with.
Dörflinger: You killed a lot of Nazis, what would one more matter?
Simms: Probably not the actual name on this one. Soft hands,
a spy with a desk job.
Brasseau: Political asshole. A problem no matter what the outcome of the test.
  '''
            ,"Simms" : '''Takahashi: Fully vetted and solid. We did Takahashi dirty during the war but apparently all is forgiven. Valuable.
Chandrakar: Built the hardware. Cares more about the work than politics. Could be replaced.
Dörflinger: Valuable, and that's about all there is to say. Worked for the SS at Raketenflugplatz Peenemunde building V-2 rockets for Dornberger and Von Braun.
Van Der Meer: A little too loud, a little too aggressive, a little too obvious to not have some other game in play.
Brasseau: Someone to be pointed at Van Der Meer.'''
            ,"Brasseau" : '''Takahashi: “American”. Some kind of math egghead.
Chandrakar: “British”. The engineer who built this clacking monster.
Dörflinger: A reconstructed Nazi. Better on our side than their side.
Van Der Meer: Good people, the sort of stand-up officer who should be bird-dogging projects like this.
Simms: Not sure what is going on with this joker. Better find out.
  '''
        }

    async def instructions(self, ctx, cmd_args):
        return self.instruction_text

    async def draw(self, ctx, cmd_args):
        self.deck_index += 1
        await ctx.send("machine noise")
        time.sleep(15)
        # looks in the deck folder for a image file that ends in the appropriate two digits, then chooses a random one from any files that match 
        # thus you can mix the various card colors into one ever changing deck
        matches = glob.glob(f"{self.deck_folder}/*_{self.deck_index:02}.*")
        m = random.sample(matches,1)
        my_files = [discord.File(x) for x in m]
        await ctx.send(files=my_files)
    
    async def characters(self, ctx, cmd_args): 
        for key, value in self.characters_public.items():
            available_characters = f'''{key} : {value}\n\n'''
            await ctx.send(available_characters)

    async def choose(self, ctx, cmd_args): 
        self.characters_public.pop(cmd_args[1])
        await ctx.send(self.characters_secret[cmd_args[1]])

implemented_decks =  {"juggernaut": Juggernaut}

def _implemented_games():
    return list(implemented_decks.keys())

def _get_deck(game):
    return implemented_decks.get(game)

