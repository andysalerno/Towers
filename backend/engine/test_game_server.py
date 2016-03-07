"""This file acts as the main entrance point to the server."""
import time
from game_pieces.creep import Creep
from engine.clock import Clock
# from game_states.main_menu import MainMenu
# from game_states.gameplay_state import GameplayState
from engine.network import Network
from game_pieces.levels import Levels
from gameplay_state import GameplayState
import game_pieces.levels
from game_pieces.tower import Tower

# Define our globals
TPS = 2  # ticks per second
TICK_LEN = 1.0 / TPS  # never update more fequently than this interval
WORLD_WIDTH = 10
WORLD_HEIGHT = 10


class GameRunner:
    """This class runs the ENTIRE game backend, from the websocket server
    to the game engine loop to the websocket client that connects the
    game engine loop to the server."""

    def __init__(self, print_gametick=False, print_on_receive=False):

        self.level_creeps_spawn_timers = {1,2,3,4,5,6,7,8,9,10}
        self.spawnCreeps = {}

        for i in range(0, 10):
            self.spawnCreeps.append(Creep.factory("Default",i))

        levels = Levels(self.level_creeps_spawn_timers, self.spawnCreeps);
        self.game_state = GameplayState(levels.level_one, WORLD_WIDTH, WORLD_HEIGHT)
        # game_state = MainMenu()

        self.game_state.build_tower(Tower((9,9),10000000,1,1,0))

        self.network = Network()
        self.print_gametick = print_gametick
        self.print_on_receive = print_on_receive

    def run(self):
        """Run this game, along with all its network requirements, like the websocket server.
        Runs in a blocking infinite loop."""
        clock = Clock(TICK_LEN)
        clock.tick()  # tick once to initialize counter

        try:
            for i in range(0,40):
                dt = clock.tick()
                self.game_loop(dt)

        except KeyboardInterrupt:
            pass
        finally:
            # do any cleanup you want to do here
            pass

    def game_loop(self, dt):


        tupleReturned = self.game_state.update(dt,[])

        text_file = open("Output.txt", "w")
        text_file.write(tupleReturned[0]+"\n")
        text_file.write(tupleReturned[1]+"\n")
        text_file.write(tupleReturned[2]+"\n")
        text_file.write(tupleReturned[3]+"\n")
        text_file.write("\n")
        text_file.close()

        #if self.print_gametick:
            #print("it's been " + str(dt * 1000) + " ms since last frame")

        #message = self.network.receive()
        #if message is not False and self.print_on_receive:
            #print("gameloop got message: {}".format(message))