import json
from classes.champion import Champion
#from instance.skill_factory import create_skill

_CHAMPION_DATA = None


def _load_champion_data():
    global _CHAMPION_DATA
    if _CHAMPION_DATA is None:
        with open("instance/champions.json", "r", encoding="utf-8") as f:
            _CHAMPION_DATA = json.load(f)
    return _CHAMPION_DATA


def create_champion(champion_id: str) -> Champion:
    data = _load_champion_data()

    if champion_id not in data:
        raise ValueError(f"Champion '{champion_id}' not found")

    c = data[champion_id]

    #skills = [create_skill(sid) for sid in c["skills"]]

    return Champion(
        name=c["name"],
        base_stat=c["base_stat"],
        stat_growth=c["stat_growth"],
        #skills=skills,
        minions=tuple(c["minions"]) if c["minions"] else None
    )
