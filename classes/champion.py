from typing import List
from utils.stats import Stats
from classes.skill import Skill


class Champion:
    def __init__(
        self, 
        name:str='', 
        stat:List[int]=[0,0,0,0,0], 
        minions:tuple[str, int]=('',0),
        skill:List[Skill]=[]
    ):
        self.name: str = name
        self.stat: List[int] = stat
        self.minionType, self.minionCount = minions
        self.skills = skill

    # returns the name of champion
    def getName(self) -> str:
        return self.name

    # returns the tuple of minion type(str) and minion count(int) of current champinon
    def getMinion(self) -> tuple:
        return (self.minionType, self.minionCount) 
    
    # returns the stat value based on string input of which stat is needed
    def getStat(self, lfstat:str) -> int:
        stat_enum = Stats[lfstat.upper()]
        return self.stat[stat_enum.value]