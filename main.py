from classes.champion import Champion
from simulation.battle import Battle
from instance.champion_factory import create_champion

def printChamp(champ: Champion):
    print(f"\nWe have champion \"{champ.getName()}\":")
    print(f"\tHP:{champ.getCurrHealth()}, ATK:{champ.getStat('ATK')}, DEF:{champ.getStat('DEF')},")
    print(f"\tSPATK:{champ.getStat('SPATK')}, SPDEF:{champ.getStat('SPDEF')}, SPD:{champ.getStat('SPD')}")
    mtype,mcount = champ.getMinion()
    print(f"\n\tMinion-Type: {mtype}, \n\tMinion-Count:{mcount}\n")

if __name__ == "__main__":
    Garen = create_champion("Garen")
    Darius = create_champion("Darius")
    printChamp(Garen)
    printChamp(Darius)

    battle = Battle(Garen, Darius)
    battle.start()
    
    