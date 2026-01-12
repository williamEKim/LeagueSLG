from typing import List


class Champion:
    def __init__(self, name:str, stat:List[int], minions:tuple[str, int]):
        self.name: str = name
        self.atk: int = stat[0]
        self.defs: int = stat[1]
        self.spatk: int = stat[2]
        self.spdefs: int = stat[3]
        self.spd: int = stat[4]
        self.minionType, self.minionCount = minions

    # returns the tuple of minion type(str) and minion count(int) of current champinon
    def getMinion(self):
        return (self.minionType, self.minionCount) 