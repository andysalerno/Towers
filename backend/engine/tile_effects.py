#this class keeps an array of tile effects that are currently affecting a tile.
class tile_effects():


    def __init__(self):
        self.effects = []
        #self.effects.append(fire(25)) #Please note that this is for testing purposes. It sets everything on fire.

    #adds the effect to the effects on the tile
    def append(self, effect):
        self.effects.append(effect)

        #iterates through the effects and calls their update methods
    def update(self):
        for i in range(0,len(self.effects)): 
            self.effects[i].update()